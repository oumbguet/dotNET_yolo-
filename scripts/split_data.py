import random
import os
import subprocess
import sys

def split_data_set(image_dir):

    f_test = open("test.txt", 'w')
    f_train = open("train.txt", 'w')
    f_val = open("valid.txt", 'w')
    
    path, dirs, files = next(os.walk(image_dir))
    data_size = len(files)

    ind = 0
    count = 0
    data_test_size = int(0.2 * data_size)
    test_array = random.sample(range(data_size), k=data_test_size)
    
    for f in os.listdir(image_dir):
        if(len(f.split(".")) > 1 and f.split(".")[1] == "png"):
            ind += 1
            
            if ind in test_array:
                if count < data_test_size / 2.0:
                    f_test.write(image_dir+'/'+f+'\n')
                    count += 1
                else:
                    f_val.write(image_dir+'/'+f+'\n')
            else:
                f_train.write(image_dir+'/'+f+'\n')


split_data_set('./Images')