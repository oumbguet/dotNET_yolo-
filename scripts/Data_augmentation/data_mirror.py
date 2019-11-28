from skimage import data
from skimage import io
from skimage.transform import rescale
from random import *
from enum import Enum
import numpy as np
import math
import os
import sys

class Flip(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    BOTH = 2

def img_flip(file, side, i):
    image = io.imread('./Images/%s'%file.name)
    if (side == Flip.HORIZONTAL.value or side == Flip.BOTH.value):
        image = np.fliplr(image)
    if (side == Flip.VERTICAL.value or side == Flip.BOTH.value):
        image = np.flipud(image)
    io.imsave(fname='./Images/m%s_%s'%(str(i - 1), file.name), arr=image)

def label_flip(file, side, i):
    filename = file.name.split('.')[0]
    image = io.imread('./Images/%s'%file.name)
    y1, x1, z1 = image.shape
    file = open('./Labels/%s.txt'%(filename), 'r')
    lines = file.read().split('\n')
    outpath = './Labels/m%s_%s.txt'%(str(i - 1), filename)
    output = open(outpath, 'a')

    for line in lines:
        elems = line.split()
        if (len(elems) < 2):
            continue
        point = (float(elems[1]) * x1, float(elems[2]) * y1)
        nx = x1 - point[0] if (side == Flip.HORIZONTAL.value or side == Flip.BOTH.value) else point[0]
        ny = y1 - point[1] if (side == Flip.VERTICAL.value or side == Flip.BOTH.value) else point[1]
    
        output.write(elems[0] + " " + str(nx / (x1 / 100) / 100) + " " + str(ny / (y1 / 100) / 100) + " " + elems[3] + " " + elems[4] + '\n')

def data_prep(file, side, i):
    img_flip(file, side, i)
    label_flip(file, side, i)

if (int(sys.argv[1][0]) < 0 or int(sys.argv[1][0]) > 2):
    print("\n>> python %s (int:side)\n\t0 to flip horizontally\n\t1 to flip vertically\n\t2 to flip on both sides\n\n"%(sys.argv[0]))
    exit()

# ERROR HANDLING SYS ARGV

DIR = './Images/'
current = 1

with os.scandir('./Images/') as entries:
    total = str(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) * (len(sys.argv) - 1))
    for entry in entries:
        for i in range(1, len(sys.argv)):
            data_prep(entry, int(sys.argv[i]), i)
            print('Flipped %s, %s/%s'%(entry.name, str(current), total))
            current += 1