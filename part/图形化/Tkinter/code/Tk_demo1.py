from tkinter import *
 
root = Tk()
root.title('窗口标题')      # 设置窗口标题
root.geometry('300x300')   # 设置窗口尺寸
root.iconbitmap('favicon.ico') # 设置窗口图标
root.resizable(width=False, height=True) # 设置窗口的宽度和高度是否可以改变
# root.destroy() # 销毁窗口
lab1 = Label(text='Hello World!', bg='red', fg='white', font=('Arial', 12), width=10, height=2, relief='solid')
lab1.pack() # 将lab控件添加到窗口
lab2 = Label(text='Hello World!', bg='green', fg='white', font=('Arial', 12), width=10, height=2, relief='flat')
lab2.pack() # 将lab控件添加到窗口
lab3 = Label(text='Hello World!', bg='violet', fg='white', font=('Arial', 12), width=10, height=2, relief='raised')
lab3.pack() # 将lab控件添加到窗口
lab4 = Label(text='Hello World!', bg='brown', fg='white', font=('Arial', 12), width=10, height=2, relief='sunken')
lab4.pack() # 将lab控件添加到窗口

mainloop()