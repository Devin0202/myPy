# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       DownSample the images with rate(float) or interval(int)
"""
import os
import sys
import time
import random
import shutil

print(sys.version)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

### Defs region
def preProcess(fDstRoot, fSrcRoot, fNeedNum):
    if not os.path.exists(fDstRoot):
        print(fDstRoot)
        os.makedirs(fDstRoot)
    else:
        print("dstRoot is existed~")
        pass

    imgList = []
    if os.path.exists(fSrcRoot):
        for rt, dirs, files in os.walk(fSrcRoot):
            for name in files:
                if -1 != name.find(".jpg") or -1 != name.find(".JPG") \
                    or -1 != name.find(".png") or -1 != name.find(".PNG"):
                    imgList.append(os.path.join(rt, name))
                    # print(os.path.join(rt,name))
    else:
        print("No Source!!!")
        sys.exit(0)

    imgListSet = set(imgList)
    if len(imgList) == len(imgListSet):
        print("Matching images number: " + str(len(imgListSet)))
        repeatSet = []
    else:
        print("Total names of image: " + str(len(imgList)))
        print("Unique names of image: " + str(len(imgListSet)))
        repeat = []
        for i in imgList:
            if imgList.count(i) > 1:
                repeat.append(i)
        repeatSet = set(repeat)
        print("Repeat elements: " + str(repeatSet))
        sys.exit(0)

    downSample = float(fNeedNum) / len(imgListSet)
    if (downSample > 1):
        print("Data is not enough!!!")
        sys.exit(0)
    else:
        return downSample, repeatSet

def doJob(fDstRoot, fSrcRoot, fFolderLimitNumber, fDownSample, fRepeatSet):
    cnt = 0
    index = 0
    targetFolderList = []
    for rt, dirs, files in os.walk(fSrcRoot):
        for name in files:
            if -1 != name.find(".jpg") or -1 != name.find(".JPG") \
                or -1 != name.find(".png") or -1 != name.find(".PNG"):
                cnt += 1
                absoluteRoute = os.path.join(rt, name)
                # print absoluteRoute
                if fFolderLimitNumber:
                    targetFolder = fDstRoot + os.path.sep \
                                    + str(int(index / fFolderLimitNumber)) \
                                    + os.path.sep
                else:
                    targetFolder = fDstRoot + os.path.sep

                if isinstance(fDownSample, float):
                    if random.uniform(0, 1) <= fDownSample \
                        and name not in fRepeatSet:
                        if not os.path.exists(targetFolder):
                            print(targetFolder)
                            os.makedirs(targetFolder)
                            targetFolderList.append(targetFolder)
                        shutil.copyfile(absoluteRoute, targetFolder + name)
                        index += 1
                    else:
                        continue
                elif isinstance(fDownSample, int):
                    if 0 == cnt % fDownSample and name not in fRepeatSet:
                        if not os.path.exists(targetFolder):
                            print(targetFolder)
                            os.makedirs(targetFolder)
                            targetFolderList.append(targetFolder)
                        shutil.copyfile(absoluteRoute, targetFolder + name)
                        index += 1
                    else:
                        continue
                else:
                    continue
    print("Total images: " + str(cnt))
    print("Total copies: " + str(index))

### Params region
src = "/media/devin/Elements/tmp/Classify/"
dst = "/media/devin/Elements/tmp/GesTrain/"
folderLimitNumber = None
needNum = 1400
### Job region
for i in range(10, 11):
    srcRoot = src + os.sep + str(i) + os.sep
    dstRoot = dst + os.sep + str(i) + os.sep
    ds, repeatSet = preProcess(dstRoot, srcRoot, needNum)
    doJob(dstRoot, srcRoot, folderLimitNumber, ds, repeatSet)

# needNum = 10000
# srcRoot = "/media/devin/Elements/tmp/Classify/N/"
# dstRoot = "/media/devin/Elements/tmp/GesTrain-bak/0/"
# ds, repeatSet = preProcess(dstRoot, srcRoot, needNum)
# doJob(dstRoot, srcRoot, folderLimitNumber, ds, repeatSet)

print(os.linesep)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
