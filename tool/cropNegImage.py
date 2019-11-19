# -*- coding: utf-8 -*-
"""
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

### Common utilities
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

### Definition region(Class, Functions, Constants)
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

from skimage import io
import math
import random
def getNegs(fImgs, fDstFold, fNegNum, fRadiusRatio):
    if fDstFold:
        dst = makeAbsDirs(fDstFold, fExistencePermitted=True)
    else:
        dst = None

    for j in range(fNegNum):
        for i in fImgs:
            image = io.imread(i)
            # image.shape   HWC
            print(str(image.shape) + '\t' + i.split(os.sep)[-1])
            mn = min(image.shape[0], image.shape[1])
            mxR = mn * fRadiusRatio
            rd = random.uniform(0, 2 * math.pi)
            anchorX = int(image.shape[1] / 2 + mxR * math.cos(rd))
            anchorY = int(image.shape[0] / 2 + mxR * math.sin(rd))

            rd = random.randint(0, 3)
            if 0 == rd:
                length = min(anchorX, anchorY)
                image = image[anchorY - length:anchorY, \
                                anchorX - length:anchorX, :]
            elif 1 == rd:
                length = min(image.shape[1] - anchorX, anchorY)
                image = image[anchorY - length:anchorY, \
                                anchorX:anchorX + length, :]
            elif 2 == rd:
                length = min(anchorX, image.shape[0] - anchorY)
                image = image[anchorY:anchorY + length, \
                                anchorX - length:anchorX, :]
            else:
                length = min(image.shape[1] - anchorX, image.shape[0] - anchorY)
                image = image[anchorY:anchorY + length, \
                                anchorX:anchorX + length, :]

            lastSep = i.rfind(os.sep)
            first = dst
            second = i[lastSep + 1:]
            second = second.split('.')
            second[0] = str(j) + "N" + second[0]
            new = first + ".".join(second)
            io.imsave(new, image)
    return

if "__main__" == __name__:
    globalT0 = globalStart()
### Parameters region
    srcs = range(1, 11)
    src = "/media/devin/Elements/tmp/GesTrain-bak/"
    dst = "/media/devin/Elements/tmp/test/"
### Job region
    print("Do something~")

    for i in srcs:
        rtv = traversFilesInDir(src + str(i))
        getNegs(rtv, dst + str(i), 2, 0.2)

    globalEnd(globalT0)