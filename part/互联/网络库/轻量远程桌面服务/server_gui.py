import sys
import socket
import threading
import time
import struct
from io import BytesIO

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal, Qt

from PIL import Image
import mss
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
from pynput.keyboard import Controller as KeyboardController, Key

# 默认端口
CTRL_TCP_PORT = 50021

class AgentCore(QtCore.QObject):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.clients_lock = threading.Lock()
        self.video_clients = set()  # (ip, udp_port)
        self.stop_event = threading.Event()
        self.threads = []
        # 配置
        self.password = "123456"
        self.target_fps = 20
        self.jpeg_quality = 60
        self.downscale = 1.0

    def log(self, msg: str):
        self.log_signal.emit(msg)

    def start(self):
        if any(t.is_alive() for t in self.threads):
            self.log("[Agent] 已在运行。")
            return
        self.stop_event.clear()
        t_ctrl = threading.Thread(target=self._start_control_server, daemon=True)
        t_vid = threading.Thread(target=self._capture_and_stream, daemon=True)
        self.threads = [t_ctrl, t_vid]
        for t in self.threads:
            t.start()
        self.log(f"[Agent] 已启动。控制TCP: {CTRL_TCP_PORT}，视频UDP端口由控制端提供。")

    def stop(self):
        self.stop_event.set()
        self.log("[Agent] 停止中...")
        # 等待短暂时间让线程退出
        for _ in range(30):
            if not any(t.is_alive() for t in self.threads):
                break
            time.sleep(0.1)
        with self.clients_lock:
            self.video_clients.clear()
        self.threads.clear()
        self.log("[Agent] 已停止。")

    def _capture_and_stream(self):
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                frame_interval = 1.0 / max(1, self.target_fps)
                prev_time = 0.0
                while not self.stop_event.is_set():
                    now = time.time()
                    wait = frame_interval - (now - prev_time)
                    if wait > 0:
                        time.sleep(wait)
                    prev_time = time.time()

                    img = sct.grab(monitor)
                    im = Image.frombytes("RGB", img.size, img.rgb)

                    if self.downscale != 1.0:
                        new_size = (int(im.width * self.downscale), int(im.height * self.downscale))
                        im = im.resize(new_size, Image.LANCZOS)

                    buf = BytesIO()
                    im.save(buf, format="JPEG", quality=int(self.jpeg_quality))
                    frame = buf.getvalue()

                    max_chunk = 1400
                    total = len(frame)
                    header = b"FRAM"
                    with self.clients_lock:
                        targets = list(self.video_clients)
                    for addr in targets:
                        try:
                            udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            udp_sock.sendto(header + struct.pack("!I", total), addr)
                            for offset in range(0, total, max_chunk):
                                chunk = frame[offset:offset+max_chunk]
                                pkt = b"CHNK" + struct.pack("!I", offset) + chunk
                                udp_sock.sendto(pkt, addr)
                            udp_sock.close()
                        except Exception as e:
                            self.log(f"[Video] 向 {addr} 发送失败：{e}")
                            with self.clients_lock:
                                if addr in self.video_clients:
                                    self.video_clients.remove(addr)
        except Exception as e:
            self.log(f"[Video] 线程异常：{e}")

    def _handle_control(self, conn, addr):
        try:
            conn.settimeout(10)
            line = conn.recv(256).decode("utf-8", errors="ignore").strip()
            if line != self.password:
                conn.sendall(b"ERR\n")
                self.log(f"[Auth] {addr} 密码错误，已拒绝。")
                return
            conn.sendall(b"OK\n")
            self.log(f"[Auth] {addr} 通过。")

            while not self.stop_event.is_set():
                data = conn.recv(1024)
                if not data:
                    break
                cmd = data.decode("utf-8", errors="ignore").strip()
                if not cmd:
                    continue
                if cmd.startswith("VIDEOPORT"):
                    try:
                        _, p = cmd.split()
                        video_port = int(p)
                        with self.clients_lock:
                            self.video_clients.add((addr[0], video_port))
                        conn.sendall(b"VIDEOPORT OK\n")
                        self.log(f"[Ctrl] {addr} 视频端口 {video_port} 已登记。")
                    except Exception:
                        conn.sendall(b"VIDEOPORT ERR\n")
                elif cmd.startswith("MOUSE_MOVE"):
                    try:
                        _, xs, ys = cmd.split()
                        x, y = int(xs), int(ys)
                        self.mouse.position = (x, y)
                    except Exception:
                        pass
                elif cmd.startswith("MOUSE_DOWN"):
                    try:
                        _, b = cmd.split()
                        btn = Button.left if b == "left" else Button.right if b == "right" else Button.middle
                        self.mouse.press(btn)
                    except Exception:
                        pass
                elif cmd.startswith("MOUSE_UP"):
                    try:
                        _, b = cmd.split()
                        btn = Button.left if b == "left" else Button.right if b == "right" else Button.middle
                        self.mouse.release(btn)
                    except Exception:
                        pass
                elif cmd.startswith("KEY_DOWN"):
                    try:
                        _, k = cmd.split(maxsplit=1)
                        key_obj = getattr(Key, k, None)
                        self.keyboard.press(key_obj if key_obj else k)
                    except Exception:
                        pass
                elif cmd.startswith("KEY_UP"):
                    try:
                        _, k = cmd.split(maxsplit=1)
                        key_obj = getattr(Key, k, None)
                        self.keyboard.release(key_obj if key_obj else k)
                    except Exception:
                        pass
                elif cmd == "PING":
                    conn.sendall(b"PONG\n")
        except Exception as e:
            self.log(f"[Ctrl] {addr} 连接异常：{e}")
        finally:
            with self.clients_lock:
                for item in list(self.video_clients):
                    if item[0] == addr[0]:
                        self.video_clients.remove(item)
            try:
                conn.close()
            except:
                pass
            self.log(f"[Ctrl] {addr} 已断开。")

    def _start_control_server(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", CTRL_TCP_PORT))
            s.listen(5)
            self.log(f"[Agent] 控制端口 TCP {CTRL_TCP_PORT} 监听中...")
            s.settimeout(1.0)
            while not self.stop_event.is_set():
                try:
                    conn, caddr = s.accept()
                except socket.timeout:
                    continue
                threading.Thread(target=self._handle_control, args=(conn, caddr), daemon=True).start()
        except Exception as e:
            self.log(f"[Agent] 控制服务器异常：{e}")

class ServerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("远控 被控端 (Server)")
        self.core = AgentCore()
        self.core.log_signal.connect(self.append_log)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # 配置行
        cfg_layout = QHBoxLayout()
        cfg_layout.addWidget(QLabel("密码:"))
        self.ed_pwd = QLineEdit("123456")
        self.ed_pwd.setEchoMode(QLineEdit.Password)
        cfg_layout.addWidget(self.ed_pwd)

        cfg_layout.addWidget(QLabel("FPS:"))
        self.spin_fps = QSpinBox()
        self.spin_fps.setRange(1, 60)
        self.spin_fps.setValue(20)
        cfg_layout.addWidget(self.spin_fps)

        cfg_layout.addWidget(QLabel("JPEG质量:"))
        self.spin_q = QSpinBox()
        self.spin_q.setRange(10, 95)
        self.spin_q.setValue(60)
        cfg_layout.addWidget(self.spin_q)

        cfg_layout.addWidget(QLabel("缩放:"))
        self.spin_scale = QDoubleSpinBox()
        self.spin_scale.setRange(0.3, 1.0)
        self.spin_scale.setSingleStep(0.1)
        self.spin_scale.setValue(1.0)
        cfg_layout.addWidget(self.spin_scale)

        layout.addLayout(cfg_layout)

        # 按钮
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("启动服务")
        self.btn_stop = QPushButton("停止服务")
        self.btn_stop.setEnabled(False)
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        layout.addLayout(btn_layout)

        # 日志
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        layout.addWidget(self.log_edit)

        self.setLayout(layout)

        # 信号
        self.btn_start.clicked.connect(self.on_start)
        self.btn_stop.clicked.connect(self.on_stop)

    def append_log(self, text: str):
        self.log_edit.append(text)

    def on_start(self):
        self.core.password = self.ed_pwd.text().strip()
        self.core.target_fps = self.spin_fps.value()
        self.core.jpeg_quality = self.spin_q.value()
        self.core.downscale = float(self.spin_scale.value())
        self.core.start()
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)

    def on_stop(self):
        self.core.stop()
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    w = ServerGUI()
    w.resize(720, 480)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()