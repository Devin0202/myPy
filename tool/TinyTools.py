# -*- coding: utf-8 -*-
"""Brief
Language:
Goal:
PS:
"""
import sys
import os
import time
import timeit
import re
import concurrent.futures

"""
Common utilities
"""
def safeDirectory(fDir):
    if str == type(fDir):
        safeDir = re.sub(os.path.sep + "{2,}", os.path.sep, fDir)
        if os.path.sep == safeDir[-1]:
            pass
        else:
            safeDir += os.path.sep
    else:
        print("Error type of input!!!")
        sys.exit(0)
    return safeDir

def makeAbsDirs(fDir, fExistencePermitted = True):
    safeDir = safeDirectory(fDir)
    if os.path.isabs(safeDir):
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
            print(e)
            sys.exit(0)
        else:
            print("Create: " + safeDir + "    OK")
            return safeDir
    else:
        print("Please use absolute path!!!")
        sys.exit(0)

def globalStart():
    print("LocalSystem: " + os.name)
    print("Python Ver: " + sys.version)
    timeStampFormat = "%Y-%m-%d %H:%M:%S"
    print(time.strftime(timeStampFormat, time.localtime()))
    globalT = timeit.default_timer()
    print()
    return globalT

def globalEnd(fGlobalT):
    timeStampFormat = "%Y-%m-%d %H:%M:%S"
    globalElapsed = (timeit.default_timer() - fGlobalT) / 60
    print()
    print(time.strftime(timeStampFormat, time.localtime()))
    print("Finished in {:.2f}m".format(globalElapsed))

def concurrentWork(fMaxload, fFn, *fArgs, \
    isProcess = True, isConcurrent = True):
    if isConcurrent:
        if isProcess:
            executor = \
            concurrent.futures.ProcessPoolExecutor(max_workers = fMaxload)
        else:
            executor = \
            concurrent.futures.ThreadPoolExecutor(max_workers = fMaxload)
        results = list(executor.map(fFn, *fArgs))
    else:
        results = list(map(fFn, *fArgs))
    return results

"""Definition region

Class:

Constants:

Functions:
1. Traversing files
2. Rename by serials
3. Images flipping horizontally
4. Images padding
"""
def traversFilesInDir(fSrcRoot, fBlackList=[]):
    rtv = []
    srcRoot = safeDirectory(fSrcRoot)
    if os.path.exists(srcRoot):
        for rt, dirs, files in os.walk(srcRoot):
            for name in files:
                if rt in fBlackList:
                    continue
                else:
                    rtv.append(os.path.join(rt, name))
    else:
        print("Please use correct path!!!")
        sys.exit(0)
    return rtv

def renameByNum(fOlds, fStart=0):
    cnt = fStart
    for old in fOlds:
        lastSep = old.rfind(os.sep)
        first = old[:lastSep + 1]
        second = old[lastSep + 1:]
        second = second.split('.')
        second[0] = str(cnt)
        new = first + ".".join(second)
        os.rename(old, new)
        cnt += 1
    return

from skimage import io, util, transform
def saveHorizontalFlip(fImgs, fDstFold=None):
    if fDstFold:
        dst = makeAbsDirs(fDstFold, fExistencePermitted=False)
    else:
        dst = None

    for i in fImgs:
        image = io.imread(i)
        image = image[:, ::-1, :]
        lastSep = i.rfind(os.sep)

        if dst:
            first = dst
        else:
            first = i[:lastSep + 1]

        second = i[lastSep + 1:]
        second = second.split('.')
        second[0] = "hf" + second[0]
        new = first + ".".join(second)
        io.imsave(new, image)
    return

def savePadding(fImgs, fTargetH, fTargetW, fDstFold=None):
    if fDstFold:
        dst = makeAbsDirs(fDstFold, fExistencePermitted=False)
    else:
        dst = None

    for i in fImgs:
        image = io.imread(i)
        hDiff = int(fTargetH - image.shape[0])
        wDiff = int(fTargetW - image.shape[1])

        if hDiff < 0 or wDiff < 0:
            image = transform.resize(image, (fTargetH, fTargetW))
        else:
            hPadding = (hDiff // 2, hDiff - hDiff // 2)
            wPadding = (wDiff // 2, wDiff - wDiff // 2)
            image = util.pad(image, ((0, 0), wPadding, (0, 0)), \
                            mode = 'symmetric')
            image = util.pad(image, (hPadding, (0, 0), (0, 0)), \
                            mode = 'symmetric')

        lastSep = i.rfind(os.sep)
        if dst:
            first = dst
        else:
            first = i[:lastSep + 1]

        second = i[lastSep + 1:]
        second = second.split('.')
        second[0] = "pad" + second[0]
        new = first + ".".join(second)
        io.imsave(new, image)
    return

import cv2
import numpy as np
def makeVideo(fImgs, fTargetH, fTargetW, fDstFold):
    dst = makeAbsDirs(fDstFold, fExistencePermitted=False)
    videoWriter = cv2.VideoWriter(dst + "video.avi", \
                cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), \
                15, (fTargetW, fTargetH))

    rgb_color = (0, 0, 0)
    color = tuple(reversed(rgb_color))
    matBlack = np.zeros((fTargetH, fTargetW, 3), np.uint8)
    matBlack[:] = color
    imgPalm = cv2.imread("/home/devin/MyData/Gesture/Classify-backlight/7/201910241056201910241049653.jpg")
    for i in fImgs:
        imgBgr = cv2.imread(i)
        videoWriter.write(matBlack)
        videoWriter.write(imgPalm)
        videoWriter.write(imgBgr)
    videoWriter.release()

    return


if "__main__" == __name__:
    globalT0 = globalStart()
### Parameters region
    src = "/home/devin/MyData/Gesture/Classify-backlight/7/"
    blacklist = ["/media/devin/Elements/tmp/GesTrain/test/0"]
### Job region
    print("Do something~")

    # rtv = traversFilesInDir(src, fBlackList=blacklist)
    # saveHorizontalFlip(rtv)

    # rtv = traversFilesInDir(src)
    # savePadding(rtv, 720, 720, fDstFold="/media/devin/Elements/tmp/GesTrain/test/0pad")

    rtv = traversFilesInDir(src, fBlackList=blacklist)
    makeVideo(rtv, 720, 720, "/media/devin/Elements/tmp/GesTrain/test/video")

    # rtv = traversFilesInDir(src)
    # renameByNum(rtv, fStart=19000)

    globalEnd(globalT0)
