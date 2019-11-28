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

def label(file):
    filename = file.name.split('.')[0]
    file = open('./Images/output/%s.txt'%(filename), 'r')
    lines = file.read().split('\n')
    outpath = './Images/output/g_%s.txt'%(filename)
    output = open(outpath, 'a')

    for line in lines:
        output.write(line + '\n')

def gaussian(file):
    image = io.imread('./Images/output/%s'%file.name)

    image = filters.gaussian(image, sigma=0.8, preserve_range=True)

    io.imsave(fname='./Images/output/g_%s'%(file.name), arr=image)

def data_prep(file):
    gaussian(file)
    label(file)

DIR = './Images/output/'
current = 1

with os.scandir('./Images/output/') as entries:
    total = str(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) / 2)
    for entry in entries:
        if (len(entry.name.split('.')) == 2 and entry.name.split('.')[1] != "txt"):
            data_prep(entry)
            print('Modified %s, %s/%s'%(entry.name, str(current), total))
            current += 1