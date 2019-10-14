# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Extract files into one folder
"""
import sys
import os
import time

import shutil
### Definition region(Class, Functions, Constants)
def doJob(fRootDir, fDstDir):
    cnt = 0
    rootDir = fRootDir + os.path.sep
    if os.path.exists(rootDir):
        pass
    else:
        print("No source!!!")
        sys.exit(0)

    dstDir = fDstDir + os.path.sep
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
    else:
        pass

    for rt, dirs, files in os.walk(rootDir):
        for i in files:
            old = os.path.join(rt, i)
            print(old)

            new = rt.split(os.path.sep)[-1]
            # print(new)
            new = dstDir + new + ' ' + i
            print(new)
            print()
            shutil.copyfile(old, new)
            cnt += 1
    return cnt

if "__main__" == __name__:
    print(sys.version)
    timeStampFormat = "%Y-%m-%d %H:%M:%S"
    print(time.strftime(timeStampFormat, time.localtime()))
### Parameters region
    cSrcDir = "/home/devin/Downloads/tmp/hiscene_inspect/"
    cDstDir = "/home/devin/Downloads/tmp/Extract/ChangeIt/"
### Job region
    print(doJob(cSrcDir, cDstDir))

    print(os.linesep)
    print(time.strftime(timeStampFormat, time.localtime()))
