# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Make 50%-50% images(nv21) stitch horizontally;
            Generate  the timestamps;
            Write the labels-file
PS:
"""
import sys
import os
import time

import cv2
import numpy as np
import itertools
### Common utilities
def safeDirectory(fDir):
    if str == type(fDir):
        if os.path.sep == fDir[-1]:
            safeDir = fDir
        else:
            safeDir = fDir + os.path.sep
    else:
        print("Error type of input!!!")
        sys.exit(0)
    return safeDir

def makeDirs(fDir, fExistencePermitted = True):
    safeDir = fDir
    try:
        if not os.path.exists(safeDir):
            os.makedirs(safeDir)
        else:
            if not fExistencePermitted:
                print("The folder had been existed!!!")
                sys.exit(0)
            else:
                pass
    except Exception as e:
        print("Exception occured!!!")
        print(e)
        sys.exit(0)
    else:
        print("Create: " + safeDir + "    OK")
        return safeDir

### Definition region(Class, Functions, Constants)
class TimeReader():
    def __init__(self, fLocaltime):
        self.tm_sec = fLocaltime.tm_sec
        self.tm_min = fLocaltime.tm_min
        self.tm_hour = fLocaltime.tm_hour

def cutPart(fImage, fBytes, fColumn, fRow, fIsLeft):
    with open(fImage, 'rb') as fr:
        oriData = fr.read()
    if not len(oriData) == fBytes:
        print(len(oriData))
        print("File lenth dismatched: " + fImage)
    else:
        imgYuv = np.fromstring(oriData, dtype = np.uint8)
        imgYuv = np.reshape(imgYuv, (-1, fColumn))
        if fIsLeft:
            newOne = imgYuv[:, 0 : int(fColumn / 2)]
        else:
            newOne = imgYuv[:, int(fColumn / 2) : fColumn]
    return newOne

if "__main__" == __name__:
    print(sys.version)
    timeStampFormat = "%Y-%m-%d %H:%M:%S"
    print(time.strftime(timeStampFormat, time.localtime()))
### Parameters region
    cvImgSaver = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    cSrcDir = "/media/devin/OpenImage600/3m普正左"
    cDstDir = "/media/devin/OpenImage600/tmp"
    cDstFile = "DoubleSet3m.txt"
    cols = 1280
    rows = 720
    fileBytes = cols * rows * 3 / 2
    stitchGroup = {}
### Job region
    srcF = safeDirectory(cSrcDir)
    dstF = safeDirectory(cDstDir)
    makeDirs(dstF)

    if os.path.exists(dstF + cDstFile):
        pass
    else:
        with open(dstF + cDstFile, 'a') as fw:
            tmpS4 = "Case".ljust(16) + "        " + "Left".ljust(16) + "        " \
            + "Right" + "\r\n"
            fw.write(tmpS4)

    for rt, dirs, files in os.walk(srcF):
        for tmp in files:
            tmpS0 = os.path.dirname(os.path.join(rt, tmp))
            tmpS1 = tmpS0.replace(srcF, '').split(os.path.sep)[0]
            if tmpS1 in stitchGroup.keys():
                if tmpS0 == stitchGroup[tmpS1]:
                    pass
                else:
                    print("Not only one for hints!!!")
                    sys.exit(0)
            else:
                stitchGroup[tmpS1] = tmpS0

    for i in itertools.permutations(stitchGroup.keys(), 2):
        if (i[0] > i[1]):
            tmpS0 = i[0] + "-X-" + i[1]
        else:
            tmpS0 = i[1] + "-X-" + i[0]
        tmpS0 = dstF + tmpS0 + os.path.sep
        print(tmpS0)
        filesA = []
        filesB = []

        for rt, dirs, files in os.walk(stitchGroup[i[0]]):
            for name in files:
                filesA.append(os.path.join(rt, name))
        for rt, dirs, files in os.walk(stitchGroup[i[1]]):
            for name in files:
                filesB.append(os.path.join(rt, name))
        filesA.sort()
        filesB.sort()
        tmpMin = min(len(filesA), len(filesB))
        filesA = filesA[-tmpMin:]
        filesB = filesB[-tmpMin:]
        cnt = 0
        startTime = time.localtime()
        tmpS2 = time.strftime("%m%d%H%M%S", startTime)

        with open(dstF + cDstFile, 'a') as fw:
            tmpS4 = tmpS2.ljust(16) + "        " + i[0].ljust(16) + "        " \
            + i[1] + "\r\n"
            fw.write(tmpS4)

        tmpS1 = tmpS0 + tmpS2 + os.path.sep + "cameraData"
        tmpS1 = safeDirectory(tmpS1)
        tmpS1 = makeDirs(tmpS1)
        startTime = TimeReader(startTime)
        for picA, picB in zip(filesA, filesB):
            a = cutPart(picA, fileBytes, cols, rows, True)
            b = cutPart(picB, fileBytes, cols, rows, True)
            # print(a.shape)
            # print(b.shape)
            newThree = np.hstack([a, b])
            # print(newThree.shape)
            newThree = np.reshape(newThree, (-1, 1))
            # print(newThree.shape)

            if 1000 <= cnt:
                startTime.tm_sec += 1
                cnt -= 1000
            if 60 <= startTime.tm_sec:
                startTime.tm_min += 1
                startTime.tm_sec -= 60
            if 60 <= startTime.tm_min:
                startTime.tm_hour += 1
                startTime.tm_min -= 60

            tmpS3 = str(startTime.tm_hour).zfill(2) + '-' \
                    + str(startTime.tm_min).zfill(2) + '-' \
                    + str(startTime.tm_sec).zfill(2) + '-' + str(cnt).zfill(3)

            if False:
                tmpS5 = tmpS1 + tmpS3 + ".nv21"
                print(tmpS5)
                newThree.tofile(tmpS5)
            else:
                imgYuv = np.reshape(newThree, (-1, cols))
                imgBgr = cv2.cvtColor(imgYuv, cv2.COLOR_YUV2BGR_NV21)
                tmpS5 = tmpS1 + tmpS3 + ".jpg"
                cv2.imwrite(tmpS5, imgBgr, cvImgSaver)
            cnt += 30

    print(os.linesep)
    print(time.strftime(timeStampFormat, time.localtime()))