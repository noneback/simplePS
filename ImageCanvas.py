import tkinter as tk
from PIL import ImageTk, ImageDraw
from PIL import Image


class ImageCanvas(tk.Canvas):
    """
    ImageCanvas 用来放置图像
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.pack(side='left')
        self.last_x = 0
        self.last_y = 0

    def resize(self,x,y,e):
        # print(x,y,e)
        if self.last_x==x and self.last_y==y:
            return
        else:
            self.last_x = x
            self.last_y = y
        self.config(width=x)
        self.config(height=y)
        if hasattr(self, 'img_handler_') :
            self.update(self.img_handler_,x,y)

    def update(self, img_handler,x=-1,y=-1):
        '''更新图像'''
        self.img_handler_ = img_handler
        if x==-1 : x=self.winfo_width()
        if y == -1 : y = self.winfo_height()
        rate = max((img_handler.img.width /x), (img_handler.img.height / y))
        if rate < 1: rate = 1
        try:
            tempImg = img_handler.img.resize((int(img_handler.img.width / rate), int(img_handler.img.height / rate)),
                                         Image.BILINEAR)
        except:
            tempImg = img_handler.img
        img_handler.img_tk = ImageTk.PhotoImage(tempImg)

        # x,y=img_handler.img.size
        # 调整canva大小
        # self.config(width=x)
        # self.config(height=y)

        self.create_image(x / 2, y / 2, image=img_handler.img_tk)
        self.pack(side='left')
