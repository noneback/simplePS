import tkinter as tk
import tkinter.messagebox
from PIL import ImageFilter, ImageOps
from Utils import open_file, save_file, create_scale
import sys



class TopMenu(tk.Menu):
    """
    顶部菜单
      Attributes:
          master:父窗口
          image_handler:图像处理类
          file_menu:File 一级菜单
          enhance_menu:Image Enhance 一级菜单，图像增强
          other_menu:Other Tool 一级菜单，其他处理图像工具
          about_menu:About 一级菜单，有关信息
          font:字体配置（配置可独立成类）

    """

    def __init__(self, image_handler, master=None, **kw):
        super().__init__(master=master, **kw)
        self.master = master
        self.image_handler = image_handler
        self.font = ('SimHei', 10)

        self.create_widgets()
        self.layout()
        self.bind_events()

    def create_widgets(self):
        """
        创建菜单组建
        """

        self.file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label='File', menu=self.file_menu, font=self.font)

        self.bin_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label='Binarization', menu=self.bin_menu, font=self.font)

        self.enhance_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label='Image Enhance', menu=self.enhance_menu, font=self.font)

        self.blur_filter_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label='Blur and Filter', menu=self.blur_filter_menu, font=self.font)

        self.other_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label='Other Tools', menu=self.other_menu, font=self.font)

        self.about_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label='About', menu=self.about_menu, font=self.font)


    def bind_events(self):
        """
        初始化菜单的组建，并绑定事件函数

        :return:
        """
        # File_Menu
        if sys.platform == "darwin":  # in macos
            self.file_menu.add_command(label='Open',
                                       command=lambda: open_file(self.image_handler), accelerator="Command+O")
            self.bind_all("<Command-o>", lambda e: open_file(self.image_handler))
            self.file_menu.add_command(label='Save',
                                       command=lambda: save_file(self.image_handler), accelerator="Command+S")
            self.bind_all("<Command-s>", lambda e: save_file(self.image_handler))
        else:  # windows or linux
            self.file_menu.add_command(label='Open',
                                       command=lambda: open_file(self.image_handler), accelerator="Ctrl+O")
            self.bind_all("<Control-o>", lambda e: open_file(self.image_handler))
            self.file_menu.add_command(label='Save',
                                       command=lambda: save_file(self.image_handler), accelerator="Ctrl+S")
            self.bind_all("<Control-s>", lambda e: save_file(self.image_handler))



        self.bin_menu.add_command(label='Simple Binarization',
                                   command=lambda: create_scale(self.image_handler, from_=0, to=255,
                                                                command=self.image_handler.convert_B,
                                                                orient=tk.HORIZONTAL, resolution=1))

        self.bin_menu.add_command(label='Random dithering',
                                  command=lambda: create_scale(self.image_handler, from_=0, to=6,
                                                               command=self.image_handler.convert_B2,
                                                               orient=tk.HORIZONTAL, resolution=0.1))

        self.bin_menu.add_command(label='Floyd-Steinberg dithering',
                                   command=self.image_handler.convert_Floyd_dithering)

        self.file_menu.add_command(label='Grayscale',
                                   command=self.image_handler.convert_L)

        self.file_menu.add_command(label='Equalize',
                                   command=self.image_handler.equalize)

        self.file_menu.add_command(label='Histogram',
                                   command=self.image_handler.show_hist)

        self.file_menu.add_command(label='Recover',
                                   command=self.image_handler.recover)

        if sys.platform == "darwin":  # in macos
            self.file_menu.add_command(label='Undo',
                                       command=self.image_handler.undo, accelerator="Command+Z")
            self.bind_all("<Command-z>", self.image_handler.undo)
        else:  # windows or linux
            self.file_menu.add_command(label='Undo',
                                       command=self.image_handler.undo, accelerator="Ctrl+Z")
            self.bind_all("<Control-z>", self.image_handler.undo)

        # Image enhance
        self.enhance_menu.add_command(label='Brightness',
                                      command=lambda: create_scale(self.image_handler, from_=0, to=2,
                                                                   command=self.image_handler.brightness_enhance,
                                                                   orient=tk.HORIZONTAL, resolution=0.01))
        self.enhance_menu.add_command(label='Color',
                                      command=lambda: create_scale(self.image_handler, from_=0, to=3,
                                                                   command=self.image_handler.color_enhance,
                                                                   orient=tk.HORIZONTAL, resolution=0.01))
        self.enhance_menu.add_command(label='Constrast',
                                      command=lambda: create_scale(self.image_handler, from_=0, to=3,
                                                                   command=self.image_handler.contrast_enhance,
                                                                   orient=tk.HORIZONTAL, resolution=0.01))

        self.enhance_menu.add_command(label='Sharpness',
                                      command=lambda: create_scale(self.image_handler, from_=0, to=3,
                                                                   command=self.image_handler.sharpness_enhance,
                                                                   orient=tk.HORIZONTAL, resolution=0.01))
        # Blur and Filter
        self.blur_filter_menu.add_command(label='BoxBlur',
                                          command=lambda: self.image_handler.apply_filter(ImageFilter.BoxBlur(3)))
        self.blur_filter_menu.add_command(label='GaussianBlur',
                                          command=lambda: self.image_handler.apply_filter(ImageFilter.GaussianBlur(3)))
        self.blur_filter_menu.add_command(label='MedianFilter',
                                          command=lambda: self.image_handler.apply_filter(ImageFilter.MedianFilter(3)))

        self.blur_filter_menu.add_command(label='MinFilter',
                                          command=lambda: self.image_handler.apply_filter(ImageFilter.MinFilter(3)))

        self.blur_filter_menu.add_command(label='ModeFilter',
                                          command=lambda: self.image_handler.apply_filter(ImageFilter.ModeFilter(3)))

        self.blur_filter_menu.add_command(label='UnsharpMask',
                                          command=lambda: self.image_handler.apply_filter(ImageFilter.UnsharpMask()))

        self.blur_filter_menu.add_command(label='MaxFilter',
                                          command=lambda: self.image_handler.apply_filter(ImageFilter.MaxFilter(3)))

        self.blur_filter_menu.add_command(label='RankFilter',
                                          command=lambda: create_scale(self.image_handler, from_=0, to=8,
                                                                       command=self.image_handler.rank_filter,
                                                                       orient=tk.HORIZONTAL, resolution=1))

        # other tool
        self.other_menu.add_command(label='Invert',
                                    command=lambda: self.image_handler.apply_ops(ImageOps.invert))
        self.other_menu.add_command(label='Mirror',
                                    command=lambda: self.image_handler.apply_ops(ImageOps.mirror))
        self.other_menu.add_command(label='Flip',
                                    command=lambda: self.image_handler.apply_ops(ImageOps.flip))
        self.other_menu.add_command(label='Rotate',
                                    command=lambda: create_scale(self.image_handler, from_=0, to=360,
                                                                 command=self.image_handler.rotate,
                                                                 orient=tk.HORIZONTAL, resolution=1))

        self.about_menu.add_command(label='About',
                                    command=lambda: tk.messagebox.showinfo('关于','软件学院多媒体大作业\n版本：1.0'))

    def layout(self):
        """放置于父窗口"""
        self.master.config(menu=self)
