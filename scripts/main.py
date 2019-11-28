from __future__ import division
from tkinter import *
from PIL import Image, ImageTk
import os
import glob
import random
import itertools

COLORS = ['red', 'blue', 'yellow', 'pink', 'cyan', 'green', 'black']

def convert(size, box):
    dw = size[0] / 100
    dh = size[1] / 100
    print("size : ", size)
    x = (box[0] + box[2])/2.0
    y = (box[1] + box[3])/2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x / dw / 100
    w = w / dw / 100
    y = y / dh / 100
    h = h / dh / 100
    return (x,y,w,h)

class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("LabelTool")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width = FALSE, height = FALSE)

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None
        self.label = 0

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0

        # reference to bbox
        self.bboxIdList = []
        self.bboxId = None
        self.bboxList = []
        self.hl = None
        self.vl = None

        # ----------------- GUI stuff ---------------------
        # dir entry & load
        self.entry = Entry(self.frame)
        self.loadDir

        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.parent.bind("<Escape>", self.cancelBBox)  # press <Espace> to cancel current bbox
        self.parent.bind("s", self.cancelBBox)
        self.parent.bind("a", self.prevImage) # press 'a' to go backforward
        self.parent.bind("d", self.nextImage) # press 'd' to go forward
        self.parent.bind('<Key>', self.setLabel)
        self.mainPanel.grid(row = 1, column = 1, rowspan = 4, sticky = W+N)

        # showing bbox info & delete bbox
        self.lb1 = Label(self.frame, text = 'Bounding boxes:')
        self.lb1.grid(row = 1, column = 2,  sticky = W+N)
        self.listbox = Listbox(self.frame, width = 22, height = 12)
        self.listbox.grid(row = 2, column = 2, sticky = N)
        self.btnDel = Button(self.frame, text = 'Delete', command = self.delBBox)
        self.btnDel.grid(row = 3, column = 2, sticky = W+E+N)
        self.btnClear = Button(self.frame, text = 'ClearAll', command = self.clearBBox)
        self.btnClear.grid(row = 4, column = 2, sticky = W+E+N)

        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 5, column = 1, columnspan = 2, sticky = W+E)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)

        # display label
        self.lab = Label(self.ctrPanel, text = "Current label = " + str(self.label))
        self.lab.pack(side = BOTTOM)

        # display mouse position
        self.disp = Label(self.ctrPanel, text='')
        self.disp.pack(side = RIGHT)

        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(4, weight = 1)

        self.loadDir()

    def loadDir(self, dbg = False):
        if not dbg:
            s = self.entry.get()
            self.parent.focus()
        else:
            s = r'D:\workspace\python\labelGUI'
        # get image list
        self.imageDir = './Images'
        self.imageList = glob.glob(os.path.join(self.imageDir, '*.png'))
        if len(self.imageList) == 0:
            print ('No .PNG images found in the specified dir!')
            return

        # default to the 1st image in the collection
        self.cur = 1
        self.total = len(self.imageList)

         # set up output dir
        self.outDir = './Labels'
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)

     
        self.loadImage()
        print ('%d images loaded' %(self.total))

    def loadImage(self):
        # load image
        imagepath = self.imageList[self.cur - 1]
        self.img = Image.open(imagepath)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width = max(self.tkimg.width(), 400), height = max(self.tkimg.height(), 400))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)
        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))

        # load labels
        self.clearBBox()
        self.imagename = os.path.split(imagepath)[-1].split('.')[0]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        bbox_cnt = 0
        w = int(self.img.size[0])
        h = int(self.img.size[1])
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                for (i, line) in enumerate(f):
                    # if i == 0:
                    #     bbox_cnt = int(line.strip())
                    #     continue
                    tmp = [float(t.strip()) for t in line.split()]
##                    print tmp
                    cl = int(tmp[0])
                    tmp.pop(0)
                    tmp.append(cl)
                    self.bboxList.append(tuple(tmp))
                    print(self.bboxList)
                    print ("tmp : " + str(tmp))
                    tmpId = self.mainPanel.create_rectangle(w / 100.0 * (tmp[0] * 100) - ((w / 100.0 * (tmp[2] * 100)) / 2.0), h / 100.0 * (tmp[1] * 100) - ((h / 100.0 * (tmp[3] * 100)) / 2.0), \
                                                            w / 100.0 * (tmp[0] * 100) + ((w / 100.0 * (tmp[2] * 100)) / 2.0), h / 100.0 * (tmp[1] * 100) + ((h / 100.0 * (tmp[3] * 100)) / 2.0), \
                                                            width = 2, \
                                                            outline = COLORS[(len(self.bboxList)-1) % len(COLORS)])
                    self.bboxIdList.append(tmpId)
                    self.listbox.insert(END, '(%d, %d) -> (%d, %d)' %(int(w / 100.0 * (tmp[0] * 100) - ((w / 100.0 * (tmp[2] * 100)) / 2.0)), int(h / 100.0 * (tmp[1] * 100) - ((h / 100.0 * (tmp[3] * 100)) / 2.0)), int(w / 100.0 * (tmp[0] * 100) + ((w / 100.0 * (tmp[2] * 100)) / 2.0)), int(h / 100.0 * (tmp[1] * 100) + ((h / 100.0 * (tmp[3] * 100)) / 2.0))))
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])


    def setLabel(self, event):
        self.label = 1 if (event.char == '&' or event.char == '1') else 2 if (event.char == 'é' or event.char == '2') else 3 if (event.char == '"' or event.char == '3') else 4 if (event.char == '\'' or event.char == '4') else 5 if (event.char == '(' or event.char == '5') else 6 if (event.char == '-' or event.char == '6') else 7 if (event.char == 'è' or event.char == '7') else 8 if (event.char == '_' or event.char == '8') else 9 if (event.char == 'ç' or event.char == '9') else 0 if (event.char == 'à' or event.char == '0') else self.label
        self.lab.config(text = "Current label : " + str(self.label))

    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            # f.write('%d\n' %len(self.bboxList))
            w = int(self.img.size[0])
            h = int(self.img.size[1])
            for bbox in self.bboxList:
                print ("bbox : ", bbox)
                if (bbox[0] < 1.0 and bbox[1] < 1.0 and bbox[2] < 1.0 and bbox[3] < 1.0):
                    arr = list(bbox)
                    arr.pop(4)
                else:
                    arr = convert((w, h), bbox)
                    
                print ("arr : ", arr)
                # arr.insert(0, bbox[4])
                f.write(str(bbox[4]) + ' ' + ' '.join(map(str, arr)) + '\n')
        print ('Image No. %d saved' %(self.cur))


    def mouseClick(self, event):
        if self.STATE['click'] == 0:
            self.STATE['x'], self.STATE['y'] = event.x, event.y
        else:
            x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
            y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
            self.bboxList.append((x1, y1, x2, y2, self.label))
            self.bboxIdList.append(self.bboxId)
            self.bboxId = None
            self.listbox.insert(END, '(%d, %d) -> (%d, %d)' %(x1, y1, x2, y2))
            self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
        self.STATE['click'] = 1 - self.STATE['click']

    def mouseMove(self, event):
        self.disp.config(text = 'x: %d, y: %d' %(event.x, event.y))
        if self.tkimg:
            if self.hl:
                self.mainPanel.delete(self.hl)
            self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width = 2)
            if self.vl:
                self.mainPanel.delete(self.vl)
            self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width = 2)
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
            self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], \
                                                            event.x, event.y, \
                                                            width = 2, \
                                                            outline = COLORS[len(self.bboxList) % len(COLORS)])

    def cancelBBox(self, event):
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
                self.bboxId = None
                self.STATE['click'] = 0

    def delBBox(self):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            return
        idx = int(sel[0])
        self.mainPanel.delete(self.bboxIdList[idx])
        self.bboxIdList.pop(idx)
        self.bboxList.pop(idx)
        self.listbox.delete(idx)

    def clearBBox(self):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []

    def prevImage(self, event = None):
        self.saveImage()
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()

    def nextImage(self, event = None):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()
            
if __name__ == '__main__':
    root = Tk()
    root.state('zoomed')
    tool = LabelTool(root)
    root.resizable(width =  True, height = True)
    root.mainloop()
