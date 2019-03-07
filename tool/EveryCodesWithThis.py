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

def globalStart():
    print(sys.version)
    timeStampFormat = "%Y-%m-%d %H:%M:%S"
    print(time.strftime(timeStampFormat, time.localtime()))
    globalT = timeit.default_timer()
    return globalT

def globalEnd(fGlobalT):
    timeStampFormat = "%Y-%m-%d %H:%M:%S"
    globalElapsed = (timeit.default_timer() - fGlobalT) / 60
    print(os.linesep)
    print(time.strftime(timeStampFormat, time.localtime()))
    print("Finished in {:.2f}m".format(globalElapsed))

### Definition region(Class, Functions, Constants)

if "__main__" == __name__:
    globalT0 = globalStart()
### Parameters region

### Job region
    print("Do something~")

    globalEnd(globalT0)