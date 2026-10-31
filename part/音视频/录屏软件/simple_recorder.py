#!/usr/bin/env python3
"""
简易Python屏幕录制工具 - 命令行版本
使用方法: python3 simple_recorder.py [选项]
"""

import cv2
import numpy as np
import pyautogui
import time
import argparse
import os
from datetime import datetime

def record_screen(output_file=None, duration=10, fps=30, region=None, quality=85):
    """
    录制屏幕
    
    Args:
        output_file: 输出文件名
        duration: 录制时长(秒)
        fps: 帧率
        region: 录制区域 (x, y, width, height)
        quality: 质量 (1-100)
    """
    
    # 禁用pyautogui的安全特性
    pyautogui.FAILSAFE = False
    
    # 获取屏幕尺寸
    if region is None:
        screen_width, screen_height = pyautogui.size()
        region = (0, 0, screen_width, screen_height)
    
    x, y, width, height = region
    
    # 生成输出文件名
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"screen_record_{timestamp}.mp4"
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
    
    # 创建视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    if not video_writer.isOpened():
        print(f"❌ 无法创建视频文件: {output_file}")
        return False
    
    print(f"🎬 开始录制...")
    print(f"📁 输出文件: {output_file}")
    print(f"📏 录制区域: {x},{y} 尺寸: {width}×{height}")
    print(f"⏱️  录制时长: {duration}秒")
    print(f"🎞️  帧率: {fps}fps")
    print("按 Ctrl+C 提前停止录制")
    
    frame_count = 0
    start_time = time.time()
    frame_interval = 1.0 / fps
    
    try:
        while True:
            frame_start = time.time()
            elapsed = time.time() - start_time
            
            # 检查是否超时
            if duration > 0 and elapsed >= duration:
                break
            
            # 截取屏幕
            screenshot = pyautogui.screenshot(region=region)
            frame = np.array(screenshot)
            
            # 转换颜色格式
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # 写入帧
            video_writer.write(frame)
            frame_count += 1
            
            # 显示进度
            if frame_count % (fps * 2) == 0:  # 每2秒显示一次
                progress = (elapsed / duration * 100) if duration > 0 else elapsed
                if duration > 0:
                    print(f"🔴 录制中... {progress:.1f}% ({elapsed:.1f}s/{duration}s)")
                else:
                    print(f"🔴 录制中... {elapsed:.1f}s (无限时长)")
            
            # 控制帧率
            frame_time = time.time() - frame_start
            sleep_time = max(0, frame_interval - frame_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    except KeyboardInterrupt:
        print("\n⏹️  录制被用户中断")
    
    finally:
        # 关闭视频写入器
        video_writer.release()
        
        # 显示结果
        final_time = time.time() - start_time
        actual_fps = frame_count / final_time if final_time > 0 else 0
        
        print(f"\n✅ 录制完成!")
        print(f"📁 文件: {output_file}")
        print(f"📊 统计: {frame_count}帧, {final_time:.1f}秒, 平均{actual_fps:.1f}fps")
        
        # 检查文件大小
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
            print(f"💾 文件大小: {file_size:.1f}MB")
    
    return True

def interactive_select_region():
    """交互式选择录制区域"""
    print("\n🎯 区域选择模式:")
    print("1. 全屏录制")
    print("2. 自定义区域")
    
    choice = input("请选择 (1-2): ").strip()
    
    if choice == "1":
        screen_width, screen_height = pyautogui.size()
        return (0, 0, screen_width, screen_height)
    
    elif choice == "2":
        print("\n请输入录制区域坐标:")
        try:
            x = int(input("X坐标: "))
            y = int(input("Y坐标: "))
            width = int(input("宽度: "))
            height = int(input("高度: "))
            
            # 验证坐标
            screen_width, screen_height = pyautogui.size()
            if x < 0 or y < 0 or x + width > screen_width or y + height > screen_height:
                print("⚠️  警告: 录制区域超出屏幕范围")
            
            return (x, y, width, height)
        except ValueError:
            print("❌ 输入格式错误")
            return None
    
    else:
        print("❌ 无效选择")
        return None

def main():
    parser = argparse.ArgumentParser(description="简易Python屏幕录制工具")
    parser.add_argument("-o", "--output", help="输出文件名")
    parser.add_argument("-t", "--time", type=int, default=10, help="录制时长(秒), 0为无限时长")
    parser.add_argument("-f", "--fps", type=int, default=30, help="帧率")
    parser.add_argument("-q", "--quality", type=int, default=85, help="质量(1-100)")
    parser.add_argument("-r", "--region", help="录制区域 'x,y,width,height'")
    parser.add_argument("-i", "--interactive", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    # 解析录制区域
    region = None
    if args.region:
        try:
            x, y, w, h = map(int, args.region.split(','))
            region = (x, y, w, h)
        except ValueError:
            print("❌ 区域格式错误，应为: x,y,width,height")
            return
    
    # 交互模式
    if args.interactive:
        print("🎬 简易Python屏幕录制工具")
        print("=" * 40)
        
        # 选择录制区域
        if region is None:
            region = interactive_select_region()
            if region is None:
                return
        
        # 输入录制时长
        if args.time == 10:  # 默认值
            try:
                duration = int(input(f"\n录制时长(秒) [默认{args.time}]: ") or args.time)
                args.time = duration
            except ValueError:
                pass
        
        # 输入输出文件名
        if not args.output:
            filename = input("\n输出文件名 [默认自动生成]: ").strip()
            if filename:
                args.output = filename
    
    # 开始录制
    print(f"\n{'='*50}")
    success = record_screen(
        output_file=args.output,
        duration=args.time,
        fps=args.fps,
        region=region,
        quality=args.quality
    )
    
    if success:
        print(f"{'='*50}")
        print("🎉 录制任务完成!")
    else:
        print("❌ 录制失败!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 程序被用户中断")
    except Exception as e:
        print(f"❌ 程序错误: {e}")
