import tkinter as tk
from threading import Timer
import sys
from PIL import Image, ImageDraw, ImageFont
from ImageCanvas import ImageCanvas
from TopMenu import TopMenu
from ImageHandler import ImageHandler


class AppFrame(tk.Frame):
    """
    程序主界面
    Attributes:
        master:父窗口
        img_canvas:画板，用来放置图像
        top_menu:顶部菜单
        image_handler:图像处理类
    """

    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.master = master
        self.create_widgets()
        Timer(0.5, self.show_init_img).start()
        self.layout()


    '''
    create widgets that on thar frame
    '''

    def show_init_img(self):

        if sys.platform == 'win32':
            newImg = Image.new('RGBA', (400, 100), color=(255, 255, 255,0))
            d = ImageDraw.Draw(newImg)
            font1 = ImageFont.truetype('arial.ttf', 30)
            font2 = ImageFont.truetype('arial.ttf', 20)
        else:
            newImg = Image.new('RGB', (400, 100), color=(255, 255, 255))
            d = ImageDraw.Draw(newImg)
            font1 = ImageFont.truetype('Arial.ttf', 30)
            font2 = ImageFont.truetype('Arial.ttf', 20)
        d.text((0, 0), "Welcome to use photo editor~", font=font1,fill=(0,0,0))
        d.text((70, 50), "Please open a image to start", font=font2,fill=(150,150,150))
        self.image_handler.set_imgObj(newImg)
        self.image_handler.update_image()

    def create_widgets(self):
        self.image_handler = ImageHandler()
        self.img_canvas = ImageCanvas(self)
        self.top_menu = TopMenu(self.image_handler,self.master)
        #建立部件之间的联系
        self.image_handler.set_canvas(self.img_canvas)
        self.top_menu.image_handler=self.image_handler
        #bind events
        self.bind_events()


    '''
    initialize all events
    '''

    def bind_events(self):
        pass

    '''initialize layout'''

    def layout(self):
        self.pack()







