# -*- coding: utf-8 -*-
"""
Language:
Goal:
PS:
"""
import sys
import os
import time

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

if "__main__" == __name__:
    print(sys.version)
    timeStampFormat = "%Y-%m-%d %H:%M:%S"
    print(time.strftime(timeStampFormat, time.localtime()))
### Parameters region

### Job region
    print("Do something~")

    print(os.linesep)
    print(time.strftime(timeStampFormat, time.localtime()))