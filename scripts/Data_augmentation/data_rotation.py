from skimage import data
from skimage import io
from skimage.transform import rotate
from random import *
import numpy as np
import math
import os

def get_box(width, height, angle):
    ang = 90 / 100 * (angle % 90)
    dif = abs(width - height)
    a = 0
    b = 0
    if (ang < 50.0):
        a = width - (dif / 100 * ang)
        b = height + (dif / 100 * ang)
    else:
        a = width - dif + (dif / 100 * ang)
        b = height + dif - (dif / 100 * ang)
    return a, b

def pts_rotate(filename, image, ang, i):
    file = open('./Labels/%s.txt'%(filename), 'r')
    y1, x1, z1 = image.shape
    lines = file.read().split('\n')
    outpath = './Labels/r%s_%s.txt'%(str(i), filename)
    output = open(outpath, 'a')

    for line in lines:
        elems = line.split()
        if (len(elems) < 2):
            continue
        point = (float(elems[1]) * x1, float(elems[2]) * y1)
        origin = (x1 / 2, y1 / 2)
        angle = -1 * math.radians(ang)
        # print("Point : ", point)
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

        bx, by = get_box(float(elems[3]) * x1, float(elems[4]) * y1, ang)

        output.write(elems[0] + " " + str(qx / (x1 / 100) / 100) + " " + str(qy / (y1 / 100) / 100) + " " + str(bx / (x1 / 100) / 100) + " " + str(by / (y1 / 100) / 100) + '\n')
        # print(qx, qy)

def img_rotate(file, angle, i):
    image = io.imread('./Images/%s'%file.name)
    
    pts_rotate(file.name.split('.')[0], image, angle, i)

    image = rotate(image, angle, resize=False)
    io.imsave(fname='./Images/r%s_%s'%(str(i),file.name), arr=image)

def data_prep(file, total, current):
    for i in range(-2, 2):
        img_rotate(file, randint(i * 45, (i + 1) * 45), i + 3)
        print('Rotated %s, %s/%s'%(entry.name, str(current), total))
        current += 1
    return current

DIR = './Images/'
current = 1

with os.scandir('./Images/') as entries:
    total = str(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) * 2)
    for entry in entries:
        if (len(entry.name.split('.')) == 2 and entry.name.split('.')[1] != "txt"):
            current = data_prep(entry, total, current)