import random

from PIL import Image, ImageEnhance, ImageTk, ImageFilter,ImageOps
from ImageCanvas import ImageCanvas
import numpy as np
from matplotlib import pyplot as plt

class ImageHandler:
    """
    图像处理类,需要卷积核的地方均为3x3
    Attributes:
        img:每一步图像处理的输入图像
        src_img:原始图像
        ret_img:图像处理之后的输出图像
        img_tk:用于ImageCanvas画图的图像格式
        canvas:用来放图的容器
        self.undoStack:

    """
    def __init__(self, path):
        super().__init__()
        self.img = Image.open(path)
        self.src_img = Image.open(path)
        self.ret_img=Image.open(path)
        self.img_tk = ImageTk.PhotoImage(self.img)
        self.path = path
        self.undoStack = []

    def __init__(self):
        super().__init__()
        self.img = None
        self.img_tk = None
        self.src_img = None
        self.undoStack = []

    def show_hist(self):
        image_array = np.array(self.img)
        plt.hist(image_array.flatten(), 256)  # flatten可以将矩阵转化成一维序列
        plt.show()

    def set_img(self, path):
        self.img = Image.open(path)
        self.src_img=Image.open(path)
        self.ret_img = Image.open(path)
        self.img_tk = ImageTk.PhotoImage(self.img)

    def set_imgObj(self, img):
        self.img = img
        self.src_img=img
        self.ret_img = img
        self.img_tk = ImageTk.PhotoImage(self.img)

    def set_canvas(self, canvas: ImageCanvas):
        self.canvas = canvas


    def recover(self):
        '''
        恢复到原始图像
        '''
        if self.img:
            self.img = self.src_img
            self.ret_img=self.src_img
            self.update_image()

    def undo(self, event=None):
        '''
        撤销一步
        '''
        if len(self.undoStack)!=0 :
            self.img = self.undoStack.pop()
            self.ret_img = self.img
            self.update_image()

    def resume(self):
        '''
        将img设置为ret_img,用与每次图像操作之前
        '''
        if self.img:
            self.img=self.ret_img
            self.undoStack.append(self.img)
            self.update_image()

    def convert_L(self):
        '''转为灰度图'''
        if self.img:
            self.resume()
            self.img=self.img.convert('L')
            self.update_image()
            self.ret_img = self.img

    # def convert_RGB(self):
    #     if self.img:
    #         self.recover()
    #         # self.img = self.img.convert('rgb')
    #         # self.update_image()


    def convert_B(self,threshold=127):
        '''
        转为二值图
        Args:
            threshold:二值转换的阈值
        '''
        if self.img:
            self.resume()
            self.img= self.img.convert('L').point(lambda x: 255 * (x > threshold))
            self.update_image()

    def convert_B2(self,threshold=2):
        '''
        转为二值图 随机抖动
        Args:
            threshold:随机量
        '''
        if self.img:
            self.resume()
            self.img= self.img.convert('L').point(lambda x: 255 * (x > random.randint(-32,32)*threshold + 127))
            self.update_image()

    def convert_Floyd_dithering(self):
        '''
        转为二值图 Floyd_dithering
        '''
        if self.img:
            self.resume()
            self.img= self.img.convert('1')
            self.update_image()

    '''
       factor should be an int >0
    '''
    def brightness_enhance(self, factor):
        if self.img:
            self.resume()
            self.img = ImageEnhance.Brightness(self.img).enhance(factor)
            self.update_image()

    def color_enhance(self, factor):
        if self.img:
            self.resume()
            self.img = ImageEnhance.Color(self.img).enhance(factor)
            self.update_image()

    def contrast_enhance(self, factor):
        if self.img:
            self.resume()
            self.img = ImageEnhance.Contrast(self.img).enhance(factor)
            self.update_image()

    def sharpness_enhance(self, factor):
        if self.img:
            self.img = ImageEnhance.Sharpness(self.img).enhance(factor)
            self.update_image()

    def rotate(self,angle):
        self.resume()
        self.img=self.img.rotate(angle,expand=True)
        self.update_image()


    def apply_filter(self,filter:ImageFilter):
        '''
        应用一些图像滤波操作
        Args：
            filter:ImageFilter中的滤波器
        '''
        if self.img:
            self.resume()
            self.img=self.img.filter(filter)
            self.update_image()
            self.ret_img=self.img

    def equalize(self):
        '''图像均衡化'''
        if self.img:
            self.resume()
            self.img=ImageOps.equalize(self.img.convert('RGB'))
            self.update_image()
            self.ret_img=self.img

    def apply_ops(self,ops_func):
        '''
        应用一些图像操作
        Args：
            ops_func:应当是ImageOps中的函数，接受一个必要图像操作
        '''
        if self.img:
            self.resume()
            self.img=ops_func(self.img.convert('RGB'))
            self.update_image()
            self.ret_img=self.img

    def rank_filter(self,rank):
        '''
        用于rankfilter操作
        Args:

            rank:像素的次序

        '''
        self.resume()
        self.img = self.img.filter(ImageFilter.RankFilter(3,rank))
        self.update_image()




    def update_image(self):
            self.canvas.update(self)




