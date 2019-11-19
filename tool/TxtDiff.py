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

"""Common utilities
Functions:
1. safeDirectory
2. makeAbsDirs
3. globalStart
4. globalEnd
5. traversFilesInDir
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
"""Definition region

Class:

Constants:

Functions:
1. 
"""
def makeDiff(fMasterFile, fSlaveFile):
    masterSet, slaveSet = None, None
    with open(fMasterFile, 'r') as fr:
        masterSet = set(fr.readlines())

    with open(fSlaveFile, 'r') as fr:
        slaveSet = set(fr.readlines())

    return masterSet - slaveSet

if "__main__" == __name__:
    globalT0 = globalStart()
### Parameters region
    src1 = "/home/devin/MyData/Gesture-21-points/Origin"
    src2 = "/home/devin/MyData/Gesture-21-points/Valid"
    dst = "/home/devin/MyData/Gesture-21-points/Invalid"
### Job region
    originFileList = traversFilesInDir(src1)
    validFileList = traversFilesInDir(src2)
    pairFiles = []

    for i in originFileList:
        pattern = i.split(os.sep)[-1]
        for j in validFileList:
            if -1 == j.find(pattern):
                continue
            else:
                pairFiles.append((i, j))

    dst = makeAbsDirs(dst)
    for i in pairFiles:
        writeSet = makeDiff(i[0], i[1])
        pattern = i[0].split(os.sep)[-1]
        writeFile = dst + "invalid_" + pattern
        with open(writeFile, 'w') as fw:
            fw.writelines(writeSet)

    globalEnd(globalT0)