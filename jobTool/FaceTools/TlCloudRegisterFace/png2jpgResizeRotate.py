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
import shutil
from PIL import Image
from PIL.Image import NEAREST, BILINEAR, BICUBIC, LANCZOS, BOX, HAMMING

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
def whatFormat(filename):
    try:
        i = Image.open(filename)
        if "PNG" != i.format and 'JPEG' != i.format:
            print("Not png and jpeg")
        return i.format
    except IOError:
        print("Error image type")
        sys.exit(0)


if "__main__" == __name__:
    globalT0 = globalStart()
### Parameters region
    import cv2
    import random

    # src = "/media/devin/DL01/20200210_result/"
    # dst = "/media/devin/DL01/20200315_result/"
    src = "/home/devin/Downloads/tmp/error/1/R/20200210/"
    dst = "/home/devin/Downloads/tmp/error/1/R/20200210EX/"

    resolution = True
    rotation = True
### Job region
    makeAbsDirs(dst)
    cnt = 0
    pics = traversFilesInDir(src)
    for i in pics:
        imgFormat = whatFormat(i)
        if "PNG" == imgFormat:
            newOne = dst + i.split(os.path.sep)[-2]
            makeAbsDirs(newOne)
            newOne += os.path.sep + i.split(os.path.sep)[-1].split('.')[0] + ".jpg"
            img = Image.open(i)
            img.convert('RGB').save(newOne, quality=75)
        elif 'JPEG' == imgFormat:
            newOne = dst + i.split(os.path.sep)[-2]
            makeAbsDirs(newOne)
            newOne += os.path.sep + i.split(os.path.sep)[-1].split('.')[0] + ".jpg"
            shutil.copyfile(i, newOne)
        else:
            print("Error image type")
            sys.exit(0)
        if resolution:
            img = Image.open(newOne)
            tmp = max(img.size)
            if 1280 < tmp:
                ration = 1280 / tmp
                new_size = (int(img.size[0] * ration), int(img.size[1] * ration))
                im = img.resize(new_size, resample=BILINEAR)
                im.save(newOne, quality=75)
        if rotation:
            img = Image.open(newOne)
            im = img.rotate(90, expand=True)
            im.save(newOne, quality=75)

        print(i)
        print(imgFormat)
        # if 0 == cnt % 2:
        #     ingredients = i.split(os.sep)
        #     ingredients[offset] = ingredients[offset].replace('.', '')
        #     if 10 < len(ingredients[offset]):
        #         ingredients[offset] = ingredients[offset][:10]

        #     cpPath = os.sep.join(ingredients)
        #     cpPath = cpPath.replace(src, dst)
        #     makeAbsDirs(os.path.dirname(cpPath))

        #     shutil.copyfile(i, cpPath)
        #     print(cpPath)
        # cnt += 1

    """Make w == h for valid image condition"""
    # for i in pics:
    #     imgBgr = cv2.imread(i)
    #     if imgBgr.shape[1] != imgBgr.shape[0]:
    #         print(imgBgr.shape)
    #         mvPath = i.replace(src, dst)
    #         makeAbsDirs(os.path.dirname(mvPath))

    #         shutil.move(i, mvPath)
    #         print(mvPath)
    #         cnt += 1

    """Check folders'names with gesture"""
    # random.shuffle(pics)
    # record = set()
    # for i in pics:
    #     ingredients = i.split(os.sep)
    #     picName = ingredients[-1]
    #     gesPattern = ingredients[-2]
    #     person = ingredients[-3]

    #     id = gesPattern + person
    #     if id in record:
    #         pass
    #     else:
    #         record.add(id)
    #         cpPath = dst + '/'.join(['', gesPattern, person + '_' + picName])
    #         makeAbsDirs(os.path.dirname(cpPath))
    #         shutil.copyfile(i, cpPath)
    #         print(cpPath)
    #         cnt += 1

    print()
    globalEnd(globalT0)