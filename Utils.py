import tkinter as tk
from tkinter import filedialog



'''choose a file to open'''
def open_file(image_handler):
        file_path = filedialog.askopenfilename(
            title='Please choose a file',
            #initialdir='./',
            filetypes=[('All file', '*.*'),
                       ('PNG file', '*.png'),
                       ('JPG file', '*.jpg'),
                       ('GIF file', '*.gif'),
                       ('BMP file', '*.bmp')]
            #spectify filetype
        )
        image_handler.set_img(file_path)
        # image_handler.set_img('./1.png') #for test
        image_handler.update_image()


'''save file'''
def save_file(image_handler):
    if image_handler.img:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG",".png"),("JPG",".jpg")])
        image_handler.img.save(save_path)


'''create scale widget on a toplevel with a button'''
def create_scale(image_handler,from_,to,command=None,**kw):

    top=tk.Toplevel()
    scale=tk.Scale(top,from_=from_,to=to,**kw)
    scale.set(from_+(to-from_)/2)

    def exit(top):
        image_handler.undoStack.append(image_handler.img)
        image_handler.ret_img=image_handler.img # save the final image
        top.destroy()

    btn = tk.Button(top, text='yes', command=lambda :exit(top))
    btn.pack()

    def scale_event(scale,command):
        if command:
            command(scale.get())

    scale['command']=lambda x:scale_event(scale,command)
    scale.pack()






    
        