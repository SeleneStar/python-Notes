#!/usr/bin/env python3
"""
Python屏幕录制工具 - 支持区域选择
使用opencv-python, numpy, tkinter等库实现

pip3 install opencv-python pillow numpy pyautogui imageio[ffmpeg] --user
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import os
import sys
from PIL import Image, ImageTk
import subprocess
import platform

class ScreenRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Python屏幕录制工具")
        self.root.geometry("600x400")
        
        # 录制参数
        self.is_recording = False
        self.output_path = "recordings"
        self.fps = 20
        self.quality = 80
        
        # 录制区域 (x, y, width, height)
        self.record_area = None
        
        # 创建输出目录
        os.makedirs(self.output_path, exist_ok=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="Python屏幕录制工具", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 录制区域设置
        area_frame = ttk.LabelFrame(main_frame, text="录制区域设置", padding="10")
        area_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(area_frame, text="选择录制区域", 
                  command=self.select_area).grid(row=0, column=0, padx=(0, 10))
        
        self.area_label = ttk.Label(area_frame, text="未选择区域")
        self.area_label.grid(row=0, column=1)
        
        ttk.Button(area_frame, text="全屏录制", 
                  command=self.select_fullscreen).grid(row=1, column=0, pady=(10, 0))
        
        # 录制设置
        settings_frame = ttk.LabelFrame(main_frame, text="录制设置", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # FPS设置
        ttk.Label(settings_frame, text="帧率(FPS):").grid(row=0, column=0, sticky=tk.W)
        self.fps_var = tk.StringVar(value="20")
        fps_spinbox = ttk.Spinbox(settings_frame, from_=5, to=60, 
                                 textvariable=self.fps_var, width=10)
        fps_spinbox.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # 质量设置
        ttk.Label(settings_frame, text="质量(1-100):").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.quality_var = tk.StringVar(value="80")
        quality_spinbox = ttk.Spinbox(settings_frame, from_=1, to=100, 
                                     textvariable=self.quality_var, width=10)
        quality_spinbox.grid(row=1, column=1, padx=(10, 0), sticky=tk.W, pady=(10, 0))
        
        # 输出设置
        output_frame = ttk.LabelFrame(main_frame, text="输出设置", padding="10")
        output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(output_frame, text="保存目录:").grid(row=0, column=0, sticky=tk.W)
        ttk.Button(output_frame, text="选择目录", 
                  command=self.select_output_dir).grid(row=0, column=1, padx=(10, 0))
        
        self.output_label = ttk.Label(output_frame, text=f"当前: {self.output_path}")
        self.output_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # 控制按钮
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        self.record_button = ttk.Button(control_frame, text="开始录制", 
                                       command=self.toggle_recording)
        self.record_button.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(control_frame, text="打开录制目录", 
                  command=self.open_output_dir).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(control_frame, text="退出", 
                  command=self.root.quit).grid(row=0, column=2)
        
        # 状态显示
        self.status_label = ttk.Label(main_frame, text="就绪", 
                                     font=("Arial", 10))
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        # 配置网格权重
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def select_area(self):
        """选择录制区域"""
        self.root.withdraw()  # 隐藏主窗口
        time.sleep(0.1)  # 等待窗口隐藏
        
        # 创建区域选择窗口
        selector = AreaSelector()
        area = selector.select_area()
        
        self.root.deiconify()  # 显示主窗口
        
        if area:
            self.record_area = area
            x, y, w, h = area
            self.area_label.config(text=f"区域: {x},{y} 尺寸: {w}x{h}")
            self.status_label.config(text="已选择录制区域")
        else:
            self.status_label.config(text="未选择区域")

    def select_fullscreen(self):
        """选择全屏录制"""
        try:
            import pyautogui
            screen_width, screen_height = pyautogui.size()
            self.record_area = (0, 0, screen_width, screen_height)
            self.area_label.config(text=f"全屏: {screen_width}x{screen_height}")
            self.status_label.config(text="已选择全屏录制")
        except ImportError:
            messagebox.showerror("错误", "需要安装pyautogui库:\npip install pyautogui")

    def select_output_dir(self):
        """选择输出目录"""
        directory = filedialog.askdirectory(initialdir=self.output_path)
        if directory:
            self.output_path = directory
            self.output_label.config(text=f"当前: {self.output_path}")

    def open_output_dir(self):
        """打开输出目录"""
        if platform.system() == "Windows":
            os.startfile(self.output_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", self.output_path])
        else:  # Linux
            subprocess.run(["xdg-open", self.output_path])

    def toggle_recording(self):
        """开始/停止录制"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """开始录制"""
        if not self.record_area:
            messagebox.showerror("错误", "请先选择录制区域!")
            return
        
        try:
            self.fps = int(self.fps_var.get())
            self.quality = int(self.quality_var.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值!")
            return
        
        self.is_recording = True
        self.record_button.config(text="停止录制", state="disabled")
        self.status_label.config(text="正在录制...")
        
        # 在新线程中开始录制
        self.record_thread = threading.Thread(target=self.record_screen)
        self.record_thread.daemon = True
        self.record_thread.start()
        
        # 启用停止按钮
        self.root.after(1000, lambda: self.record_button.config(state="normal"))

    def stop_recording(self):
        """停止录制"""
        self.is_recording = False
        self.record_button.config(text="开始录制")
        self.status_label.config(text="录制已停止")

    def record_screen(self):
        """录制屏幕的主要逻辑"""
        try:
            import pyautogui
            import imageio
            
            # 禁用pyautogui的安全特性
            pyautogui.FAILSAFE = False
            
            x, y, width, height = self.record_area
            
            # 生成输出文件名
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.output_path, f"screen_record_{timestamp}.mp4")
            
            # 创建视频写入器
            writer = imageio.get_writer(output_file, fps=self.fps, 
                                      quality=self.quality, macro_block_size=1)
            
            frame_count = 0
            start_time = time.time()
            
            while self.is_recording:
                # 截取屏幕
                screenshot = pyautogui.screenshot(region=(x, y, width, height))
                frame = np.array(screenshot)
                
                # 转换颜色格式 (PIL使用RGB，我们需要RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # 写入帧
                writer.append_data(frame)
                
                frame_count += 1
                
                # 更新状态
                elapsed = time.time() - start_time
                self.root.after(0, lambda: self.status_label.config(
                    text=f"录制中... 帧数: {frame_count} 时间: {elapsed:.1f}s"))
                
                # 控制帧率
                time.sleep(1.0 / self.fps)
            
            writer.close()
            
            # 更新UI
            self.root.after(0, lambda: self.status_label.config(
                text=f"录制完成! 保存为: {os.path.basename(output_file)}"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("录制错误", str(e)))
            self.root.after(0, lambda: self.status_label.config(text="录制失败"))
        finally:
            self.is_recording = False
            self.root.after(0, lambda: self.record_button.config(text="开始录制"))

class AreaSelector:
    """区域选择器"""
    
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.selected_area = None
        
    def select_area(self):
        """选择屏幕区域"""
        try:
            import pyautogui
            
            # 创建全屏透明窗口
            self.overlay = tk.Toplevel()
            self.overlay.attributes('-fullscreen', True)
            self.overlay.attributes('-alpha', 0.3)
            self.overlay.configure(bg='black')
            self.overlay.attributes('-topmost', True)
            
            # 创建画布
            screen_width = self.overlay.winfo_screenwidth()
            screen_height = self.overlay.winfo_screenheight()
            
            self.canvas = tk.Canvas(self.overlay, width=screen_width, height=screen_height,
                                   bg='black', highlightthickness=0)
            self.canvas.pack()
            
            # 添加说明文字
            self.canvas.create_text(screen_width//2, 50, 
                                   text="按住鼠标左键拖拽选择录制区域，按ESC取消",
                                   fill="white", font=("Arial", 16))
            
            # 绑定事件
            self.canvas.bind("<Button-1>", self.on_click)
            self.canvas.bind("<B1-Motion>", self.on_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_release)
            self.overlay.bind("<Escape>", self.cancel_selection)
            
            self.overlay.focus_set()
            
            # 等待选择完成
            self.overlay.wait_window()
            
            return self.selected_area
            
        except ImportError:
            messagebox.showerror("错误", "需要安装pyautogui库:\npip install pyautogui")
            return None
    
    def on_click(self, event):
        """鼠标按下"""
        self.start_x = event.x
        self.start_y = event.y
    
    def on_drag(self, event):
        """鼠标拖拽"""
        if self.start_x is not None:
            # 清除之前的矩形
            self.canvas.delete("selection")
            
            # 绘制新矩形
            self.canvas.create_rectangle(self.start_x, self.start_y, 
                                       event.x, event.y,
                                       outline="red", width=2, tags="selection")
    
    def on_release(self, event):
        """鼠标释放"""
        if self.start_x is not None:
            self.end_x = event.x
            self.end_y = event.y
            
            # 计算选择区域
            x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
            x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
            
            width = x2 - x1
            height = y2 - y1
            
            if width > 10 and height > 10:  # 最小尺寸检查
                self.selected_area = (x1, y1, width, height)
                self.overlay.destroy()
            else:
                self.canvas.delete("selection")
                self.start_x = None
                self.start_y = None
    
    def cancel_selection(self, event):
        """取消选择"""
        self.selected_area = None
        self.overlay.destroy()

def check_dependencies():
    """检查依赖库"""
    required_packages = [
        ("cv2", "opencv-python"),
        ("PIL", "Pillow"),
        ("numpy", "numpy"),
        ("pyautogui", "pyautogui"),
        ("imageio", "imageio[ffmpeg]")
    ]
    
    missing_packages = []
    
    for package, install_name in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(install_name)
    
    if missing_packages:
        message = "缺少以下依赖库，请安装:\n\n"
        message += "pip install " + " ".join(missing_packages)
        messagebox.showerror("依赖检查", message)
        return False
    
    return True

def main():
    """主函数"""
    if not check_dependencies():
        return
    
    app = ScreenRecorder()
    
    try:
        app.root.mainloop()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        messagebox.showerror("错误", f"程序运行出错: {str(e)}")

if __name__ == "__main__":
    main()
