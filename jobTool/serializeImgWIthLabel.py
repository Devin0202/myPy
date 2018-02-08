# -*- coding: utf-8 -*-
"""
Given a start No. to serialize the names of image and reedit the dataLabel.
Assuring the images can be read, and saving them in a mirroring path.
Meanwhile, making the sort of image uniform by using png.
"""
import os
import sys
import time
import random
import cv2
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

cvImgSaver = [int(cv2.IMWRITE_PNG_COMPRESSION), 3]
startNo = 0
saveNo = startNo
srcRoot = "/home/devin/Desktop/tmp/"
dstRoot = "/home/devin/Desktop/tmpEx/"
nodeSuffix = "dataLabel.txt"
imageUniformSuffix = ".png"
suffixLength = len(nodeSuffix)
lastFolders = set()
renameDictionary = {}
lineBuffer = []
dstBuffer = []
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if len(name) - suffixLength == name.find(nodeSuffix):
                absoluteRoute = os.path.join(rt, name)
                lastFolders.add(rt)
else:
    print("No Source!!!")
    sys.exit(0)
print "Folders numbers:"
print len(lastFolders)

for folder in lastFolders:
    print os.linesep
    print "ORIGINAL FOLDER:"
    print folder
    renameDictionary.clear()
    lineBuffer = []
    dstBuffer = []
    for rt, dirs, files in os.walk(folder):
        index = 0
        for name in files:
            sys.stdout.write("\r" + str(index) + '/' + str(len(files)))
            sys.stdout.flush()
            if name.split('.')[-1] in ["png", "PNG", "jpg", "JPG"]:
                img = cv2.imread(os.path.join(rt, name), cv2.IMREAD_UNCHANGED)
                if img is None:
                    continue
                else:
                    renameDictionary[name] = str(saveNo) + imageUniformSuffix
                    dstRoute = os.path.join(dstRoot, renameDictionary[name])
                    dstFolder = os.path.split(dstRoute)[0]
                    if not os.path.exists(dstFolder):
                        os.makedirs(dstFolder)
                    cv2.imwrite(dstRoute, img, cvImgSaver)
                    index += 1
                    saveNo += 1
            elif len(name) - suffixLength == name.find(nodeSuffix):
                    with open(os.path.join(rt, name), 'r') as fr:
                        lineBuffer = fr.readlines()
                    index += 1
            else:
                continue
        for line in lineBuffer:
            if 1 < len(line.split()):
                stringChip = line.split()[0]
                line = line.replace(stringChip, renameDictionary[stringChip])
                dstBuffer.append(line)
            else:
                continue

        folderEle = folder.split('/')
        if 2 < len(folderEle):
            dstFile = folderEle[-2] + '_' + folderEle[-1] + ".txt"
        elif 1 < len(folderEle):
            dstFile = folderEle[-1] + ".txt"
        else:
            continue
        with open(os.path.join(dstRoot, dstFile), 'w') as fw:
            fw.writelines(dstBuffer)

print os.linesep
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())