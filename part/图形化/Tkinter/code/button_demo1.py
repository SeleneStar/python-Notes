from tkinter import *
 
root = Tk()
root.title('窗口标题')      # 设置窗口标题
#root.geometry('300x300')   # 设置窗口尺寸
root.geometry("300x100+20+50") # 设置窗口尺寸为300x100，位于与屏幕最左边相隔20像素，与屏幕最上方相隔50像素
root.iconbitmap('favicon.ico') # 设置窗口图标
root.resizable(width=False, height=True) # 设置窗口的宽度和高度是否可以改变

def callback():
    print("你点了一下按钮")
 
button = Button(root, text="按钮", command=callback, activeforeground="red", activebackground="yellow")
button.pack()
 
mainloop()