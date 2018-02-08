import os
import time
import random
import cv2
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

srcRoot = "/home/devin/Desktop/mnt/20171112/"
dstRoot = "/home/devin/Desktop/mnt/20171112_256144/"
dstRootLabels = "/home/devin/Desktop/mnt/20171112_256144Labels/"
rowSize = 144
colSize = 256
index = 0
downSample = 1
allLines = []

if not os.path.exists(dstRoot):
    os.makedirs(dstRoot)
if not os.path.exists(dstRootLabels):
    os.makedirs(dstRootLabels)
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if 0 == name.find("dataLabel.txt"):
                elements = os.path.join(rt, name).split('/')
                tmp = "".join(elements[5 : -1])
                dstFolder = os.path.join(dstRoot, tmp)
                if not os.path.exists(dstFolder):
                    os.makedirs(dstFolder)
                    print "MAKEDIR: " + dstFolder

                print "ORI: " + os.path.join(rt, name)
                with open(os.path.join(rt, name), 'r') as f:
                    oriList = f.readlines()

                newFile = dstRootLabels + tmp + ".txt"
                print "WRITE: " + newFile
                with open(newFile, 'w') as f:
                    for line in oriList:
                        elementsF = line.split()
                        if len(elementsF) > 1 and os.path.exists(os.path.join(rt, elementsF[0])):
                            img = cv2.imread(os.path.join(rt, elementsF[0]), cv2.IMREAD_COLOR)
                            if img is None:
                                continue

                            newImg = dstFolder + '/' + elementsF[0]
                            # print "NEWIMG: " + newImg
                            dstImg = cv2.resize(img, (colSize, rowSize))
                            cv2.imwrite(newImg, dstImg)

                            col = img.shape[1]
                            row = img.shape[0]
                            colR = colSize / float(col)
                            rowR = rowSize / float(row)
                            newEle = [elementsF[0], str(int(elementsF[6]) + 1), str(int(float(elementsF[2]) * colR)), \
                                        str(int(float(elementsF[3]) * rowR)), str(int(float(elementsF[4]) * colR)) ,str(int(float(elementsF[5]) * rowR))]
                            singleLine = ""
                            for tmpElement in newEle:
                                singleLine += str(tmpElement) + ' '
                            # print singleLine
                            f.write(singleLine + "\r\n")
else:
    print("No Source!!!")

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())