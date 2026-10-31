import sys
import socket
import threading
import struct
from io import BytesIO

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSpinBox
from PyQt5.QtCore import pyqtSignal, Qt

from PIL import Image
import numpy as np

CTRL_TCP_PORT = 50021

class VideoLabel(QLabel):
    mouse_event_signal = pyqtSignal(str, int, int)  # type, x, y

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: black;")

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent):
        x, y = ev.x(), ev.y()
        self.mouse_event_signal.emit("move", x, y)

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        btn = "left" if ev.button() == Qt.LeftButton else "right" if ev.button() == Qt.RightButton else "middle"
        self.mouse_event_signal.emit(f"down:{btn}", ev.x(), ev.y())

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        btn = "left" if ev.button() == Qt.LeftButton else "right" if ev.button() == Qt.RightButton else "middle"
        self.mouse_event_signal.emit(f"up:{btn}", ev.x(), ev.y())

class ClientCore(QtCore.QObject):
    frame_signal = pyqtSignal(QtGui.QImage)
    log_signal = pyqtSignal(str)
    connected_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.ctrl_sock = None
        self.host = ""
        self.local_udp_port = 55000
        self.password = "123456"
        self.stop_event = threading.Event()
        self.recv_thread = None

    def log(self, s: str):
        self.log_signal.emit(s)

    def connect(self, host: str, local_udp_port: int, password: str):
        self.host = host
        self.local_udp_port = local_udp_port
        self.password = password
        self.stop_event.clear()
        try:
            self.ctrl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ctrl_sock.connect((self.host, CTRL_TCP_PORT))
            self.ctrl_sock.sendall((self.password + "\n").encode("utf-8"))
            auth = self.ctrl_sock.recv(16)
            if not auth.startswith(b"OK"):
                self.log("[Ctrl] 密码错误或被拒绝。")
                self.ctrl_sock.close()
                self.ctrl_sock = None
                self.connected_signal.emit(False)
                return
            self.ctrl_sock.sendall(f"VIDEOPORT {self.local_udp_port}\n".encode("utf-8"))
            _ = self.ctrl_sock.recv(64)
            self.log("[Ctrl] 已连接，开始接收视频。")
            self.connected_signal.emit(True)
            self.recv_thread = threading.Thread(target=self._video_receiver, daemon=True)
            self.recv_thread.start()
        except Exception as e:
            self.log(f"[Ctrl] 连接失败：{e}")
            self.connected_signal.emit(False)

    def disconnect(self):
        self.stop_event.set()
        try:
            if self.ctrl_sock:
                self.ctrl_sock.close()
        except:
            pass
        self.ctrl_sock = None
        self.connected_signal.emit(False)
        self.log("[Ctrl] 已断开。")

    def _video_receiver(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind(("0.0.0.0", self.local_udp_port))
        except Exception as e:
            self.log(f"[Video] 绑定端口失败：{e}")
            return
        expected = None
        chunks = {}
        while not self.stop_event.is_set():
            try:
                data, _ = s.recvfrom(65535)
            except Exception:
                break
            if data.startswith(b"FRAM"):
                expected = struct.unpack("!I", data[4:8])[0]
                chunks.clear()
            elif data.startswith(b"CHNK") and expected is not None:
                offset = struct.unpack("!I", data[4:8])[0]
                chunks[offset] = data[8:]
                total = sum(len(v) for v in chunks.values())
                if total >= expected:
                    frame = b"".join(chunks[k] for k in sorted(chunks.keys()))
                    try:
                        im = Image.open(BytesIO(frame)).convert("RGB")
                        arr = np.array(im)  # HxWx3 RGB
                        h, w, _ = arr.shape
                        qimg = QtGui.QImage(arr.data, w, h, w*3, QtGui.QImage.Format_RGB888)
                        self.frame_signal.emit(qimg.copy())
                    except Exception:
                        pass
                    expected = None
                    chunks.clear()
        try:
            s.close()
        except:
            pass

    def send_mouse(self, typ: str, x: int, y: int):
        if not self.ctrl_sock:
            return
        try:
            if typ == "move":
                self.ctrl_sock.sendall(f"MOUSE_MOVE {x} {y}\n".encode("utf-8"))
            elif typ.startswith("down:"):
                btn = typ.split(":",1)[1]
                self.ctrl_sock.sendall(f"MOUSE_DOWN {btn}\n".encode("utf-8"))
            elif typ.startswith("up:"):
                btn = typ.split(":",1)[1]
                self.ctrl_sock.sendall(f"MOUSE_UP {btn}\n".encode("utf-8"))
        except:
            pass

    def send_key(self, keyname: str, down: bool):
        if not self.ctrl_sock:
            return
        try:
            cmd = "KEY_DOWN" if down else "KEY_UP"
            self.ctrl_sock.sendall(f"{cmd} {keyname}\n".encode("utf-8"))
        except:
            pass

class ClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("远控 控制端 (Client)")
        self.core = ClientCore()
        self.core.frame_signal.connect(self.update_frame)
        self.core.log_signal.connect(self.append_log)
        self.core.connected_signal.connect(self.on_connected)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        row = QHBoxLayout()
        row.addWidget(QLabel("对方IP:"))
        self.ed_ip = QLineEdit()
        row.addWidget(self.ed_ip)

        row.addWidget(QLabel("本机UDP端口:"))
        self.spin_port = QSpinBox()
        self.spin_port.setRange(1024, 65534)
        self.spin_port.setValue(55000)
        row.addWidget(self.spin_port)

        row.addWidget(QLabel("密码:"))
        self.ed_pwd = QLineEdit("123456")
        self.ed_pwd.setEchoMode(QLineEdit.Password)
        row.addWidget(self.ed_pwd)

        self.btn_connect = QPushButton("连接")
        self.btn_disconnect = QPushButton("断开")
        self.btn_disconnect.setEnabled(False)
        row.addWidget(self.btn_connect)
        row.addWidget(self.btn_disconnect)

        layout.addLayout(row)

        self.video = VideoLabel()
        self.video.setMinimumSize(800, 450)
        layout.addWidget(self.video)

        self.log_edit = QtWidgets.QTextEdit()
        self.log_edit.setReadOnly(True)
        layout.addWidget(self.log_edit)

        self.setLayout(layout)

        # 事件
        self.btn_connect.clicked.connect(self.on_connect)
        self.btn_disconnect.clicked.connect(self.on_disconnect)
        self.video.mouse_event_signal.connect(self.on_mouse_event)

    def append_log(self, s: str):
        self.log_edit.append(s)

    def on_connect(self):
        host = self.ed_ip.text().strip()
        if not host:
            QMessageBox.warning(self, "提示", "请输入对方IP")
            return
        port = int(self.spin_port.value())
        pwd = self.ed_pwd.text().strip() or "123456"
        self.core.connect(host, port, pwd)
        self.btn_connect.setEnabled(False)

    def on_disconnect(self):
        self.core.disconnect()

    def on_connected(self, ok: bool):
        self.btn_disconnect.setEnabled(ok)
        self.btn_connect.setEnabled(not ok)

    def update_frame(self, qimg: QtGui.QImage):
        # 自适应居中显示
        pm = QtGui.QPixmap.fromImage(qimg)
        self.video.setPixmap(pm.scaled(self.video.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def on_mouse_event(self, typ: str, x: int, y: int):
        # 直接发送控件坐标（MVP 简化，未做分辨率比例换算）
        self.core.send_mouse(typ, x, y)

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        key_map = {
            Qt.Key_Return: "enter",
            Qt.Key_Enter: "enter",
            Qt.Key_Escape: "esc",
            Qt.Key_Tab: "tab",
            Qt.Key_Backspace: "backspace",
            Qt.Key_Delete: "delete",
            Qt.Key_Left: "left",
            Qt.Key_Right: "right",
            Qt.Key_Up: "up",
            Qt.Key_Down: "down",
        }
        if e.key() in key_map:
            self.core.send_key(key_map[e.key()], True)
        else:
            ch = e.text()
            if ch:
                self.core.send_key(ch, True)

    def keyReleaseEvent(self, e: QtGui.QKeyEvent):
        key_map = {
            Qt.Key_Return: "enter",
            Qt.Key_Enter: "enter",
            Qt.Key_Escape: "esc",
            Qt.Key_Tab: "tab",
            Qt.Key_Backspace: "backspace",
            Qt.Key_Delete: "delete",
            Qt.Key_Left: "left",
            Qt.Key_Right: "right",
            Qt.Key_Up: "up",
            Qt.Key_Down: "down",
        }
        if e.key() in key_map:
            self.core.send_key(key_map[e.key()], False)
        else:
            ch = e.text()
            if ch:
                self.core.send_key(ch, False)

def main():
    app = QApplication(sys.argv)
    w = ClientGUI()
    w.resize(1024, 720)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()