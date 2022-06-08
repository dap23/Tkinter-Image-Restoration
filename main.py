import tkinter as tk
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
import random

x = 1500
y = 1000


class imageRestore(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
        self.init_ui()

    def init_ui(self):
        self.pack()
        self.judul = tk.Label(
            self, text="Image Restoration", font=('Helvetica', 20))
        self.judul.pack()
        # self.nama = tk.Label(self, text="Kelompok 8", font=('Helvetica', 18))
        # self.nama.pack(pady=(10, 0))

        # Upload Image
        self.frame1 = tk.Frame(self)
        self.frame1.pack(side=LEFT, padx=(0, 50))
        self.imageFrame = tk.LabelFrame(
            self.frame1, text='Image View', font=(20))
        self.imageFrame.pack()
        self.labelImage = tk.Label(
            self.imageFrame, width=40, height=20)
        self.labelImage.pack()
        self.btn = tk.Button(self.frame1, text='Upload Image',
                             font=(20), command=self.openImage)
        self.btn.pack(side=LEFT)
        self.btn2 = tk.Button(self.frame1, text='Repair', font=20,
                              command=self.repairImage)
        self.btn2.pack(side=LEFT, padx=(10, 0))
        # End Upload Image

        # Container 1
        self.container = tk.Frame(self)
        self.container.pack(side=TOP)

        # Marked Image
        self.frame2 = tk.Frame(self.container)
        self.frame2.pack(side=RIGHT)
        self.imageFrame2 = tk.LabelFrame(
            self.frame2, text='Marked Image', font=20)
        self.imageFrame2.pack()
        self.labelImage2 = tk.Label(
            self.imageFrame2, width=40, height=20)
        self.labelImage2.pack()

        # Thresh Image
        self.frame3 = tk.Frame(self.container)
        self.frame3.pack(side=RIGHT)
        self.imageFrame3 = tk.LabelFrame(
            self.frame3, text="Thresh Image", font=20)
        self.imageFrame3.pack()
        self.labelImage3 = tk.Label(self.imageFrame3, width=40, height=20)
        self.labelImage3.pack()
        # End Container 1

        # Container 2
        self.container2 = tk.Frame(self)
        self.container2.pack(side=BOTTOM)

        # Mask
        self.frame4 = tk.Frame(self.container2)
        self.frame4.pack(side=LEFT)
        self.imageFrame4 = tk.LabelFrame(
            self.frame4, text="Mask Image", font=20)
        self.imageFrame4.pack()
        self.labelImage4 = tk.Label(self.imageFrame4, width=40, height=20)
        self.labelImage4.pack()

        # Repair
        self.frame5 = tk.Frame(self.container2)
        self.frame5.pack(side=RIGHT)
        self.imageFrame5 = tk.LabelFrame(
            self.frame5, text="Restored Image", font=20)
        self.imageFrame5.pack()
        self.labelImage5 = tk.Label(self.imageFrame5, width=40, height=20)
        self.labelImage5.pack()

        # End Container 2

    def openImage(self):
        self.filename = filedialog.askopenfilename()
        self.img = Image.open(self.filename)
        self.x = int(self.img.size[0]*0+x*.50)
        self.y = int(self.img.size[1]*0+x*.60)
        self.img2 = self.img.resize((self.x, self.y))
        self.imgtk = ImageTk.PhotoImage(self.img)
        self.labelImage.config(image=self.imgtk, width=300, height=400)

    def repairImage(self):
        self.damageImage = cv2.imread(self.filename)
        self.markedImage = cv2.imread(self.filename, 0)

        self.ret, self.thresh1 = cv2.threshold(
            self.markedImage, 250, 255, cv2.THRESH_BINARY)

        self.kernel = np.ones((7, 7), np.uint8)
        self.mask = cv2.dilate(self.thresh1, self.kernel, iterations=1)

        self.restored = cv2.inpaint(
            self.damageImage, self.mask, 3, cv2.INPAINT_NS)

        self.randomName = random.randint(1, 1000)

        cv2.imwrite('image/repair_image' +
                    str(self.randomName)+'.png', self.restored)
        self.bacamark = ImageTk.PhotoImage(Image.fromarray(self.markedImage))
        self.bacathresh = ImageTk.PhotoImage(Image.fromarray(self.thresh1))
        self.bacamask = ImageTk.PhotoImage(Image.fromarray(self.mask))
        self.bacarepair = ImageTk.PhotoImage(
            Image.open(r"image/repair_image" +
                       str(self.randomName)+".png"))
        self.labelImage2.config(image=self.bacamark, width=300, height=400)
        self.labelImage3.config(image=self.bacathresh, width=300, height=400)
        self.labelImage4.config(image=self.bacamask, width=300, height=400)
        self.labelImage5.config(image=self.bacarepair, width=300, height=400)


window = tk.Tk()
gui = imageRestore(window)
window.geometry(f'{x}x{y}')
window.title("Kelompok 8")
window.mainloop()
