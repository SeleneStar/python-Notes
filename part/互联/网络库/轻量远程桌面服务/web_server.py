import asyncio
import json
import socket
import threading
import time
from io import BytesIO
from typing import Optional

from aiohttp import web, WSMsgType
from PIL import Image
import mss
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

# 配置
HTTP_PORT = 50080
PASSWORD = "123456"         # 访问令牌（浏览器URL ?token=123456）
TARGET_FPS = 15             # MJPEG 帧率
JPEG_QUALITY = 60           # 10-95
DOWNSCALE = 0.8             # 0.3~1.0，降低带宽

# 支持通过环境变量覆盖端口和密码
import os
HTTP_PORT = int(os.getenv("REMOTE_HTTP_PORT", HTTP_PORT))
PASSWORD = os.getenv("REMOTE_PASSWORD", PASSWORD)

mouse = MouseController()
keyboard = KeyboardController()

latest_jpeg_lock = threading.Lock()
latest_jpeg: Optional[bytes] = None
screen_size = (1920, 1080)

stop_event = threading.Event()

def capture_loop():
    global latest_jpeg, screen_size
    try:
        with mss.mss() as sct:
            mon = sct.monitors[1]
            screen_size = (mon["width"], mon["height"])
            interval = 1.0 / max(1, TARGET_FPS)
            prev = 0.0
            while not stop_event.is_set():
                now = time.time()
                sleep = interval - (now - prev)
                if sleep > 0:
                    time.sleep(sleep)
                prev = time.time()
                shot = sct.grab(mon)
                im = Image.frombytes("RGB", (shot.size.width, shot.size.height), shot.rgb)
                if DOWNSCALE != 1.0:
                    im = im.resize((int(im.width * DOWNSCALE), int(im.height * DOWNSCALE)), Image.LANCZOS)
                buf = BytesIO()
                im.save(buf, format="JPEG", quality=JPEG_QUALITY)
                data = buf.getvalue()
                with latest_jpeg_lock:
                    latest_jpeg = data
    except Exception as e:
        print(f"[Capture] 异常: {e}")

def check_token(req: web.Request) -> bool:
    token = req.query.get("token", "")
    return token == PASSWORD

async def handle_index(req: web.Request):
    if not check_token(req):
        return web.Response(status=403, text="Forbidden")
    # 尝试读取磁盘文件，若不存在则返回内置简易页面
    try:
        with open("web_client.html", "rb") as f:
            html = f.read()
        return web.Response(body=html, content_type="text/html")
    except FileNotFoundError:
        inline = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>远程桌面</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body {{ margin: 0; background: #111; color: #eee; font-family: system-ui; }}
.header {{ padding: 10px; background: #222; position: sticky; top:0; }}
.wrap {{ display:flex; justify-content:center; align-items:center; }}
img {{ max-width: 100%; height: auto; display:block; }}
small {{ color:#aaa; }}
.wrap {{ position: relative; }}
#overlay {{ position: absolute; inset: 0; touch-action: none; }}
</style>
</head>
<body>
<div class="header">
  <strong>内置页面</strong>（web_client.html 未找到）<br>
  <small>若需自定义前端，在同目录放置 web_client.html 即可。</small>
</div>
<div class="wrap">
  <img id="screen" src="stream?token={PASSWORD}" alt="screen stream">
  <div id="overlay"></div>
</div>
<script>
(() => {{
  const img = document.getElementById('screen');
  const overlay = document.getElementById('overlay');
  const wsProto = location.protocol === 'https:' ? 'wss' : 'ws';
  const ws = new WebSocket(`${{wsProto}}://${{location.host}}/ws?token={PASSWORD}`);

  // 禁用图片的长按弹窗与选中
  img.draggable = false;
  img.style.webkitTouchCallout = 'none';
  img.style.userSelect = 'none';
  img.style.webkitUserSelect = 'none';

  function rect() {{
    return img.getBoundingClientRect();
  }}

  function normXYFromClientXY(cx, cy) {{
    const r = rect();
    const x = (cx - r.left) / r.width;
    const y = (cy - r.top) / r.height;
    return {{
      nx: Math.min(1, Math.max(0, x)),
      ny: Math.min(1, Math.max(0, y)),
    }};
  }}

  function normXY(e) {{
    return normXYFromClientXY(e.clientX, e.clientY);
  }}

  function btnName(button) {{
    // 0:左，1:中，2:右
    return button === 2 ? 'right' : (button === 1 ? 'middle' : 'left');
  }}

  function sendPayload(payload) {{
    try {{ if (ws.readyState === 1) ws.send(JSON.stringify(payload)); }} catch (err) {{}}
  }}

  function send(act, e) {{
    const {{ nx, ny }} = normXY(e);
    sendPayload({{ type: 'mouse', act, btn: btnName(e.button), nx, ny }});
  }}

  // 在 overlay 上绑定所有交互，避免触发图片的系统菜单
  overlay.addEventListener('contextmenu', (e) => {{
    e.preventDefault();
    send('down', e);
    send('up', e);
  }});

  overlay.addEventListener('mousemove', (e) => {{
    const {{ nx, ny }} = normXY(e);
    sendPayload({{ type: 'mouse', act: 'move', nx, ny }});
  }});

  overlay.addEventListener('mousedown', (e) => {{
    e.preventDefault();
    send('down', e);
  }});

  overlay.addEventListener('mouseup', (e) => {{
    e.preventDefault();
    send('up', e);
  }});

  overlay.addEventListener('dblclick', (e) => {{
    e.preventDefault();
    const {{ nx, ny }} = normXY(e);
    sendPayload({{ type: 'mouse', act: 'double', btn: btnName(e.button), nx, ny }});
  }});

  // 触控：短按左键、长按右键、拖动移动、双击为双击
  let touchTimer = null;
  let lastTapTime = 0;
  let longPressed = false;

  function firstTouch(ev) {{
    return (ev.touches && ev.touches[0]) || (ev.changedTouches && ev.changedTouches[0]) || null;
  }}

  overlay.addEventListener('touchstart', (ev) => {{
    ev.preventDefault();
    const t = firstTouch(ev);
    if (!t) return;
    longPressed = false;

    const {{ nx, ny }} = normXYFromClientXY(t.clientX, t.clientY);
    // 移动开始时发送一次 move
    sendPayload({{ type: 'mouse', act: 'move', nx, ny }});

    // 500ms 长按判定：触发右键单击
    touchTimer = setTimeout(() => {{
      longPressed = true;
      sendPayload({{ type: 'mouse', act: 'down', btn: 'right', nx, ny }});
      sendPayload({{ type: 'mouse', act: 'up', btn: 'right', nx, ny }});
    }}, 500);
  }}, {{ passive: false }});

  overlay.addEventListener('touchmove', (ev) => {{
    ev.preventDefault();
    const t = firstTouch(ev);
    if (!t) return;
    const {{ nx, ny }} = normXYFromClientXY(t.clientX, t.clientY);
    sendPayload({{ type: 'mouse', act: 'move', nx, ny }});
  }}, {{ passive: false }});

  overlay.addEventListener('touchend', (ev) => {{
    ev.preventDefault();
    if (touchTimer) {{ clearTimeout(touchTimer); touchTimer = null; }}
    const t = firstTouch(ev);
    if (!t) return;
    const {{ nx, ny }} = normXYFromClientXY(t.clientX, t.clientY);

    if (!longPressed) {{
      const now = Date.now();
      if (now - lastTapTime < 300) {{
        sendPayload({{ type: 'mouse', act: 'double', btn: 'left', nx, ny }});
        lastTapTime = 0;
      }} else {{
        sendPayload({{ type: 'mouse', act: 'down', btn: 'left', nx, ny }});
        sendPayload({{ type: 'mouse', act: 'up', btn: 'left', nx, ny }});
        lastTapTime = now;
      }}
    }}
  }}, {{ passive: false }});

  ws.onmessage = (ev) => {{
    // 保持连接即可
  }};
}})();
</script>
</body>
</html>""".encode("utf-8")
        return web.Response(body=inline, content_type="text/html")
    except Exception as e:
        return web.Response(status=500, text=f"Index error: {e}")

async def handle_screen(req: web.Request):
    if not check_token(req):
        return web.json_response({"ok": False}, status=403)
    w, h = screen_size
    return web.json_response({"ok": True, "width": w, "height": h, "fps": TARGET_FPS})

async def handle_stream(req: web.Request):
    if not check_token(req):
        return web.Response(status=403, text="Forbidden")
    boundary = "frame"
    resp = web.StreamResponse(
        status=200,
        reason="OK",
        headers={
            "Content-Type": f"multipart/x-mixed-replace; boundary=--{boundary}",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )
    await resp.prepare(req)
    try:
        while True:
            await asyncio.sleep(1.0 / max(1, TARGET_FPS))
            with latest_jpeg_lock:
                data = latest_jpeg
            if not data:
                continue
            await resp.write(f"--{boundary}\r\n".encode("ascii"))
            await resp.write(b"Content-Type: image/jpeg\r\n")
            await resp.write(f"Content-Length: {len(data)}\r\n\r\n".encode("ascii"))
            await resp.write(data)
            await resp.write(b"\r\n")
    except asyncio.CancelledError:
        pass
    except ConnectionResetError:
        pass
    finally:
        try:
            await resp.write_eof()
        except Exception:
            pass
    return resp

def key_from_name(name: str):
    # 映射部分常用键，其它字符按字面发送
    special = {
        "enter": Key.enter, "esc": Key.esc, "tab": Key.tab, "backspace": Key.backspace,
        "delete": Key.delete, "left": Key.left, "right": Key.right, "up": Key.up, "down": Key.down,
        "shift": Key.shift, "ctrl": Key.ctrl, "alt": Key.alt, "meta": Key.cmd
    }
    return special.get(name.lower(), None)

async def handle_ws(req: web.Request):
    if not check_token(req):
        return web.Response(status=403, text="Forbidden")
    ws = web.WebSocketResponse()
    await ws.prepare(req)
    # 首次发送屏幕尺寸
    w, h = screen_size
    await ws.send_json({"type": "hello", "width": w, "height": h})

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                try:
                    obj = json.loads(msg.data)
                except Exception:
                    continue
                t = obj.get("type")
                if t == "mouse":
                    # {type:"mouse", act:"move|down|up", btn:"left|right|middle", nx:0..1, ny:0..1}
                    nx = float(obj.get("nx", 0))
                    ny = float(obj.get("ny", 0))
                    sx = max(0, min(1, nx)) * screen_size[0]
                    sy = max(0, min(1, ny)) * screen_size[1]
                    act = obj.get("act", "move")
                    if act == "move":
                        mouse.position = (int(sx), int(sy))
                    elif act in ("down", "up"):
                        btn = obj.get("btn", "left")
                        bmap = Button.left if btn == "left" else Button.right if btn == "right" else Button.middle
                        if act == "down":
                            mouse.press(bmap)
                        else:
                            mouse.release(bmap)
                    elif act == "double":
                        # 双击：移动到目标位置后按压/释放两次
                        btn = obj.get("btn", "left")
                        bmap = Button.left if btn == "left" else Button.right if btn == "right" else Button.middle
                        mouse.position = (int(sx), int(sy))
                        try:
                            for _ in range(2):
                                mouse.press(bmap)
                                time.sleep(0.05)
                                mouse.release(bmap)
                                time.sleep(0.05)
                        except Exception:
                            pass
                elif t == "key":
                    # {type:"key", act:"down|up", key:"enter"|"a"|...}
                    act = obj.get("act", "down")
                    name = str(obj.get("key", ""))
                    key_obj = key_from_name(name)
                    try:
                        if act == "down":
                            keyboard.press(key_obj if key_obj else name)
                        else:
                            keyboard.release(key_obj if key_obj else name)
                    except Exception:
                        pass
                elif t == "ping":
                    await ws.send_json({"type": "pong"})
            elif msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED, WSMsgType.ERROR):
                break
    finally:
        await ws.close()
    return ws

def main():
    # 启动采集线程
    t = threading.Thread(target=capture_loop, daemon=True)
    t.start()

    app = web.Application()
    app.add_routes([
        web.get("/", handle_index),
        web.get("/stream", handle_stream),
        web.get("/screen", handle_screen),
        web.get("/ws", handle_ws),
    ])
    print(f"[Web] 打开浏览器访问: http://<被控端IP>:{HTTP_PORT}/?token={PASSWORD}")
    web.run_app(app, host="0.0.0.0", port=HTTP_PORT)

if __name__ == "__main__":
    main()