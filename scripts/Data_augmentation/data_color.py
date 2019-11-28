from skimage import data
from skimage import io
from skimage import filters
from skimage.transform import rescale
from random import *
from enum import Enum
import numpy as np
import math
import os
import sys

def label(file, c):
    filename = file.name.split('.')[0]
    file = open('./Labels/%s.txt'%(filename), 'r')
    lines = file.read().split('\n')
    outpath = './Labels/c%s_%s.txt'%(c, filename)
    output = open(outpath, 'a')

    for line in lines:
        output.write(line + '\n')

# 0 1 2 => R G B
# 3 4 => Brightness up / down

def rgb(file, channel):
    image = io.imread('./Images/%s'%file.name)

    h, w, c = image.shape

    if (channel == 0):
        copy = image
        for i in range(0, h):
            for j in range(0, w):
                image[i, j] = image[i, j] + [20 if image[i, j][0] + 20 <= 255 else 255, 0, 0, 0]
        io.imsave(fname='./Images/cr_%s'%(file.name), arr=image)
        label(file, 'r')
        image = copy
    if (channel == 1):
        copy = image
        for i in range(0, h):
            for j in range(0, w):
                image[i, j] = image[i, j] + [0, 20 if image[i, j][1] + 20 <= 255 else 255, 0, 0]
        io.imsave(fname='./Images/cg_%s'%(file.name), arr=image)
        label(file, 'g')
        image = copy
    if (channel == 2):
        copy = image
        for i in range(0, h):
            for j in range(0, w):
                image[i, j] = image[i, j] + [0, 0, 20 if image[i, j][2] + 20 <= 255 else 255, 0]
        io.imsave(fname='./Images/cb_%s'%(file.name), arr=image)
        label(file, 'b')
        image = copy
    if (channel == 3):
        copy = image
        for i in range(0, h):
            for j in range(0, w):
                image[i, j] = image[i, j] - [40 if image[i, j][0] - 40 >=0 else 0, 40 if image[i, j][1] - 40 >=0 else 0, 40 if image[i, j][2] - 40 >=0 else 0, 0]
        io.imsave(fname='./Images/cu_%s'%(file.name), arr=image)
        print(">>>> ", image[0, 0])
        label(file, 'u')
        image = copy
    if (channel == 4):
        copy = image
        for i in range(0, h):
            for j in range(0, w):
                image[i, j] = image[i, j] + [40 if image[i, j][0] + 40 <= 255 else 255, 40 if image[i, j][1] + 40 <= 255 else 255, 40 if image[i, j][2] + 40 <= 255 else 255, 0]
        io.imsave(fname='./Images/cd_%s'%(file.name), arr=image)
        print(">>>> ", image[0, 0])
        label(file, 'd')
        image = copy

def data_prep(file, channel):
    rgb(file, channel)

# ERROR HANDLING SYS ARGV

DIR = './Images/'
current = 1

with os.scandir('./Images/') as entries:
    total = str(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) * (len(sys.argv) - 1))
    for entry in entries:
        if (len(entry.name.split('.')) == 2 and entry.name.split('.')[1] != "txt"):
            for i in range(1, len(sys.argv)):
                data_prep(entry, int(sys.argv[i]))
                print('Modified %s, %s/%s'%(entry.name, str(current), total))
                current += 1