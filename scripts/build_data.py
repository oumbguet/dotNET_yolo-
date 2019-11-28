import os
import sys

# OBJ.DATA
output = open('./cfg/obj.data', 'w')

output.write("classes = " + str(sys.argv[7]) + "\ntrain = train.txt\ntest = test.txt\nvalid = valid.txt\nnames = cfg/obj.names\nbackup = output/")

output.close()

# OBJ.CFG
model = open('./models/yolo_model.cfg', 'r')
output = open('./cfg/obj.cfg', 'a')
DIR = './Images'
file_nb = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

for line in model.read().split("\n"):
    print (line)
    if "batch=" in line:
        output.write("batch=" + sys.argv[1] + "\n")
    elif "max_batches=" in line:
        output.write("max_batches=" + sys.argv[6] + "\n")
    elif "subdivisions=" in line:
        output.write("subdivisions=" + sys.argv[2] + "\n")
    elif "width=" in line:
        output.write("width=" + sys.argv[3] + "\n")
    elif "height=" in line:
        output.write("height=" + sys.argv[4] + "\n")
    elif "learning_rate=" in line:
        output.write("learning_rate=" + sys.argv[5] + "\n")
    elif "yolo_filters=" in line:
        output.write("filters=" + str(3 * (int(sys.argv[7]) + 5)) + "\n")
    elif "classes=" in line:
        output.write("classes=" + str(sys.argv[7]) + "\n")
    else:
        output.write(line + "\n")