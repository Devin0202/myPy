# -*- coding: utf-8 -*-
"""
1. Serialize the images'name from a starting No.
2. If there are label files, also converting it with the new images'name
3. Save images by jpg
"""
import os
import sys
import time
import random
import shutil
import cv2
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

cvImgSaver = [int(cv2.IMWRITE_JPEG_QUALITY), 95]
# cvImgSaver = [int(cv2.IMWRITE_PNG_COMPRESSION), 3]
pfsn = 'a'      # pfsn is "prefix for startNo"
startNo = 286616
srcRoot = "/media/devin/Elements/20180124"
dstRoot = srcRoot + "Serials"

if not os.path.exists(dstRoot):
    os.makedirs(dstRoot)
else:
    print "Destination folder: " + dstRoot + " is already existed!"
    print "Please check it!"
    sys.exit(0)

labelList = []
nfwlfList = []      # nfwlf is "node folder with label file"
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in dirs:
            newFolder = os.path.join(rt, name)
            newFolder = newFolder.replace(srcRoot, dstRoot)
            print newFolder
            if not os.path.exists(newFolder):
                os.makedirs(newFolder)
        for name in files:
            if "txt" == name.split('.')[-1]:
                if "dataLabel.txt" == name \
                    or rt.split(os.path.sep)[-1] == name.split('.')[-2]:
                    labelList.append(os.path.join(rt, name))
                    nfwlfList.append(rt)
                else:
                    continue
            else:
                continue
    print labelList
    print nfwlfList
else:
    print "No resource!!!"
    sys.exit(0)

index = startNo
# work with labels
for item in labelList:
    imageList = []
    writeList = []
    serialDict = {}
    with open(item, 'r') as fr:
        oriContent = fr.readlines()
    for line in oriContent:
        imageList.append(line.split()[0])
    imageSet = set(imageList)
    tmp = -1 * len(item.split(os.path.sep)[-1])
    currentFolder = item[: tmp]
    for rt, dirs, files in os.walk(currentFolder):
        for name in files:
            if name in imageSet:
                sys.stdout.write("\r" + str(index))
                sys.stdout.flush()

                src = os.path.join(rt, name)
                img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
                if img is None:
                    continue
                else:
                    dst = rt.replace(srcRoot, dstRoot)
                    newName = pfsn + '_' + str(index) + ".jpg"
                    dst = os.path.join(dst, newName)
                    index += 1
                    cv2.imwrite(dst, img, cvImgSaver)
                    serialDict[name] = newName
            else:
                continue
    for line in oriContent:
        key = line.split()[0]
        value = serialDict[key]
        writeList.append(line.replace(key, value))

    with open(item.replace(srcRoot, dstRoot), 'w') as fw:
        fw.writelines(writeList)
# work without labels
for rt, dirs, files in os.walk(srcRoot):
    for name in files:
        sys.stdout.write("\r" + str(index))
        sys.stdout.flush()

        tmp = name.split('.')[-1]
        if "jpg" == tmp or "JPG" == tmp or "PNG" == tmp or "png" == tmp:
            if rt not in nfwlfList:
                src = os.path.join(rt, name)
                img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
                if img is None:
                    continue
                else:
                    dst = rt.replace(srcRoot, dstRoot)
                    newName = pfsn + '_' + str(index) + ".jpg"
                    dst = os.path.join(dst, newName)
                    index += 1
                    cv2.imwrite(dst, img, cvImgSaver)
            else:
                continue
        else:
            continue

with open("/home/devin/Desktop/nextStartNo.txt", 'a') as fw:
    fw.write(time.strftime('%Y-%m-%d %H:%M', time.localtime()) + os.linesep)
    fw.write("Next serializing startNo: " + str(index) + os.linesep)

print os.linesep
print "Next serializing startNo: " + str(index)
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
