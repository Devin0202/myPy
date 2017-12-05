import os
import sys
import time
import random
import shutil
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

srcRoot = "/media/devin/Elements1/onlypalm_labelmergedata/Lab/"
dstRoot = "/media/devin/Elements1/onlypalm_labelmergedata/LabIntegration/"
if not os.path.exists(dstRoot):
    os.makedirs(dstRoot)

imgList = []
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if -1 != name.find(".jpg") or -1 != name.find(".JPG") \
                or -1 != name.find(".png") or -1 != name.find(".PNG"):
                imgList.append(name)
else:
    print("No Source!!!")
    sys.exit(0)

imgListSet = set(imgList)
if len(imgList) == len(imgListSet):
    print "Matching images number: " + str(len(imgListSet))
    repeatSet = []
else:
    print "Total names of image: " + str(len(imgList))
    print "Unique names of image: " + str(len(imgListSet))
    repeat = []
    for i in imgList:
        if imgList.count(i) > 1:
            repeat.append(i)
    repeatSet = set(repeat)
    print "Repeat elements: " + str(repeatSet)
    # sys.exit(0)

downSample = 1.0
cnt = 0
index = 0
folderLimitNumber = 3000
targetFolderList = []
for rt, dirs, files in os.walk(srcRoot):
    for name in files:
        if -1 != name.find(".jpg") or -1 != name.find(".JPG") \
            or -1 != name.find(".png") or -1 != name.find(".PNG"):
            cnt += 1
            absoluteRoute = os.path.join(rt, name)
            # print absoluteRoute
            if random.uniform(0, 1) <= downSample and name not in repeatSet:
                targetFolder = dstRoot + str(index / folderLimitNumber) \
                                + os.path.sep
                if not os.path.exists(targetFolder):
                    print targetFolder
                    os.makedirs(targetFolder)
                    targetFolderList.append(targetFolder)
                shutil.copyfile(absoluteRoute, targetFolder + name)
                index += 1
print "Total images: " + str(cnt)
print "Total copies: " + str(index)
# Extend function
labelList = []
for rt, dirs, files in os.walk(srcRoot):
    for name in files:
        if -1 != name.find("dataLabel.txt"):
            with open(os.path.join(rt, name), 'r') as fr:
                labelList.extend(fr.readlines())
print len(labelList)
if 0 < len(labelList):
    for route in targetFolderList:
        dstFile = route + "dataLabel.txt"
        print "WRITE:"
        print dstFile
        with open(dstFile, 'w') as fw:
            for rt, dirs, files in os.walk(route):
                for name in files:
                    for lineRead in labelList:
                        if 0 == lineRead.find(name):
                            fw.write(lineRead)
else:
    print "Only assembling images"
# Extend function
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())