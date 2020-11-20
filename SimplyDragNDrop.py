# -*- coding: utf-8 -*-
# @Time    : 2020/10/29 11:20 上午
# @Author  : Yushuo Wang
# @FileName: simply-drag-n-drop.py
# @Software: PyCharm
# @Blog    ：https://lesliewongcv.github.io/

"""
Useful tool for image registration.
It can read the coordinate and plot the images.
You can simply drag and drop with mouse, move image pixel by pixel with keyboard.
It also has multiple transparency options, different display modes such as contrast mode, sharpness mode.
You can save the coordinate by simply press <S> on the keyboard, it would be saved as txt and csv.

"""
from tkinter import *
from PIL import Image, ImageTk, ImageEnhance
import pandas as pd
import argparse


W = 900  # the width and height of the canvas
H = 900
TRAN = 0.7  # the factor of transparency
CONTRAST_FACTOR = 2  # the factor of contrast
SHARPNESS_FACTOR = 3  # the factor of sharpness
C = 1  # index of image list, index[0] is the number of the images

MODE = 'Sharpness'  # Sharpness as the default mode
PRED = True  # is the toolkit take the coordinates to plot the images
parser = argparse.ArgumentParser(description='manual to this script')  # use -path to indicate the PATH of the data
parser.add_argument('-path', type=str, default=None)
args = parser.parse_args()
PATH = args.path  # PATH = "/Users/leslie/Desktop/大象分形/科目三初赛第一阶段/test1/"

save_list = []  # loading the data
cor_dir = open(PATH + 'img_list_path.txt')
img_list = cor_dir.readlines()
if len(img_list[C].split(' ')) == 3:
    PRED = False

cor_dir.close()
file = open(PATH + "cor_save.txt", 'a')
file.write(img_list[0][:-1] + '\n')
file.close()

def main():
    root = Tk()
    root.title('Simply Drag n Drop')
    root.geometry("2000x1000")  # the width and height of the window

    img_canvas = Canvas(root, width=W, height=H, bg="white", bd=5, confine=False, cursor="plus")
    img_canvas.pack(pady=0)

    def plot_img():
        global img, img2, X, Y
        tmp = img_list[C].split(' ')
        if PRED:
            pil_image = Image.open(PATH + 'optical/' + tmp[1])  # format of list: 2 2_1.tif 2_sar_1.tif 193 190
            pil_image2 = addTransparency(Image.open(PATH + 'sar/' + tmp[2]))
        else:
            pil_image = Image.open(PATH + 'optical/' + tmp[2][:-1])  # format of list: 2 2_sar_1.tif 2_1.tif
            pil_image2 = addTransparency(Image.open(PATH + 'sar/' + tmp[1]))

        if MODE == 'Sharpness':  # sharpness mode which is default mode
            en = ImageEnhance.Sharpness(pil_image)
            pil_image = en.enhance(SHARPNESS_FACTOR)
            img = ImageTk.PhotoImage(image=pil_image)
            my_image = img_canvas.create_image(str(50), str(50), anchor='nw', image=img)  # the location of the optical

            en = ImageEnhance.Sharpness(pil_image2)
            pil_image2 = en.enhance(SHARPNESS_FACTOR)
            img2 = ImageTk.PhotoImage(image=pil_image2)
            my_image2 = img_canvas.create_image(X, Y, anchor='center', image=img2)  # the location of the sar

        elif MODE == 'Contrast':  # contrast mode
            en = ImageEnhance.Contrast(pil_image)
            pil_image = en.enhance(CONTRAST_FACTOR)
            img = ImageTk.PhotoImage(image=pil_image)
            my_image = img_canvas.create_image(str(50), str(50), anchor='nw', image=img)

            en = ImageEnhance.Contrast(pil_image2)
            pil_image2 = en.enhance(CONTRAST_FACTOR)
            img2 = ImageTk.PhotoImage(image=pil_image2)
            my_image2 = img_canvas.create_image(X, Y, anchor='center', image=img2)

        else:  # MODE == 'Original'  # original mode
            img = ImageTk.PhotoImage(image=pil_image)
            my_image = img_canvas.create_image(str(50), str(50), anchor='nw', image=img)

            img2 = ImageTk.PhotoImage(image=pil_image2)
            my_image2 = img_canvas.create_image(X, Y, anchor='center', image=img2)

        img_label.config(text="Coordinates X: " + str(int(X) - 256 - 50) + " Y: " + str(int(Y) - 256 - 50) + "\n" +
                             "Img: " + tmp[1] + " | " + tmp[2])  # print the coordinates

    def next_img(e):
        global X, Y, C
        C = C + 1
        tmp = img_list[C].split(' ')
        if PRED:
            X = int(tmp[3]) + 306  # 256 + 50
            Y = int(tmp[4][:-1]) + 306  # 256 + 50
        plot_img()

    def last_img(e):
        global X, Y, C
        C = C - 1
        tmp = img_list[C].split(' ')
        if PRED:
            X = int(tmp[3]) + 306  # 256 + 50
            Y = int(tmp[4][:-1]) + 306  # 256 + 50
        plot_img()

    def addTransparency(img):
        img = img.convert('RGBA')
        img_blender = Image.new('RGBA', img.size, (0, 0, 0, 0))
        img = Image.blend(img_blender, img, TRAN)
        return img

    def move(e):
        global X, Y
        X = e.x
        Y = e.y
        plot_img()

    def left(e):
        global X, Y
        X = X - 1
        plot_img()

    def right(e):
        global X, Y
        X = X + 1
        plot_img()

    def up(e):
        global X, Y
        Y = Y - 1
        plot_img()

    def down(e):
        global X, Y
        Y = Y + 1
        plot_img()

    def note(e):  # save the coordinates as txt and csv
        file = open(PATH + "cor_save.txt", 'a')
        tmp = img_list[C].split(' ')
        if PRED:
            file.write(tmp[0] + ' ' + tmp[1] + ' ' + tmp[2] + ' ' + str(X - 256 - 50) + ' ' + str(Y - 256 - 50) + '\n')
            save_list.append([tmp[0], tmp[1], X - 256 - 50, Y - 256 - 50])
        else:
            file.write(
                tmp[0] + ' ' + tmp[2][:-1] + ' ' + tmp[1] + ' ' + str(X - 256 - 50) + ' ' + str(Y - 256 - 50) + '\n')
            save_list.append([tmp[0], tmp[2][:-1], X - 256 - 50, Y - 256 - 50])

        name = ['class', 'Img', 'Column', 'Row']
        test = pd.DataFrame(columns=name, data=save_list)
        print(test)
        test.to_csv((PATH + 'cor_save.csv'), encoding='gbk')
        file.close()

    def transp_3(e):
        global TRAN
        TRAN = 0.3
        plot_img()

    def transp_5(e):
        global TRAN
        TRAN = 0.5
        plot_img()

    def transp_7(e):
        global TRAN
        TRAN = 0.7
        plot_img()

    def transp_1(e):
        global TRAN
        TRAN = 1
        plot_img()

    def transp_0(e):
        global TRAN
        TRAN = 0
        plot_img()

    def contrast_mode(e):
        global MODE
        MODE = 'Contrast'
        plot_img()

    def original_mode(e):
        global MODE
        MODE = 'Original'
        plot_img()

    def sharpness_mode(e):
        global MODE
        MODE = 'Sharpness'
        plot_img()

    def egg(e):
        global img, img2
        img2 = []
        pil_image = Image.open("Imgs/egg.jpg")
        img = ImageTk.PhotoImage(image=pil_image)
        my_image123 = img_canvas.create_image('450', '450', anchor='center', image=img)

    root.bind("<Left>", left)
    root.bind("<Right>", right)
    root.bind("<Up>", up)
    root.bind("<Down>", down)
    root.bind("<space>", next_img)
    root.bind("<Key-s>", note)
    root.bind("<Key-q>", transp_3)
    root.bind("<Key-w>", transp_5)
    root.bind("<Key-e>", transp_7)
    root.bind("<Key-r>", transp_1)
    root.bind("<Key-v>", transp_0)
    root.bind("<Key-c>", contrast_mode)
    root.bind("<Key-x>", original_mode)
    root.bind("<Key-z>", sharpness_mode)
    root.bind("<BackSpace>", last_img)
    root.bind("<Control-A>", egg)

    img_label = Label(root, text="")
    img_label.pack(pady=0)
    root.bind('<B1-Motion>', move)
    root.mainloop()


if __name__ == '__main__':
    main()
