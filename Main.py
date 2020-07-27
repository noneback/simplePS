import sys

from AppFrame import *
import tkinter as tk

if __name__ == '__main__':
    #  adapt for hidpi on Windows
    if sys.platform == 'win32':
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    window = tk.Tk()
    window.title('Multi-media big homework')
    window.geometry('800x500')
    mf = AppFrame(window)
    #  支持放大缩小窗口改变图片大小
    window.bind('<Configure>', lambda e: mf.img_canvas.resize(window.winfo_width(),window.winfo_height(),e))
    mf.mainloop()
