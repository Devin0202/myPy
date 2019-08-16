# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Convert NV21 to jpg or png
"""
import os
import sys
import time
import cv2
import shutil
import numpy as np
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

cols = 222
rows = 222
# cols = 1280
# rows = 720
# cols = 640
# rows = 480
# cols = 640
# rows = 720
needVideo = False
srcRoot = "/home/devin/Downloads/tmp/"
dstRoot = "/home/devin/Downloads/tmpJpg/"
suffix = ".nv21"
lenSuffix = len(suffix)
fileBytes = cols * rows * 3 / 2

# cvImgSaver = [int(cv2.IMWRITE_PNG_COMPRESSION), 90]
# suffixReplace = ".png"
cvImgSaver = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
suffixReplace = ".jpg"

prefix = time.strftime("%Y%m%d%H%M", time.localtime())
index = 0
dstList = []
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if len(name) - lenSuffix == name.find(suffix):
                with open(os.path.join(rt, name), 'rb') as fr:
                    oriData = fr.read()
                    if not len(oriData) == fileBytes:
                        print(len(oriData))
                        print("Lenth dismatched: " + os.path.join(rt, name))
                        continue

                imgYuv = np.fromstring(oriData, dtype = np.uint8)
                imgYuv = np.reshape(imgYuv, (-1, cols))
                # imgBgr = cv2.cvtColor(imgYuv, cv2.COLOR_YUV2BGR_I420)
                imgBgr = cv2.cvtColor(imgYuv, cv2.COLOR_YUV2BGR_NV21)
                store = prefix + name.replace(suffix, suffixReplace)
                store = os.path.join(rt, store)
                store = store.replace(srcRoot, dstRoot)
                storeRoute = os.path.split(store)

                if not os.path.exists(storeRoute[0]):
                    os.makedirs(storeRoute[0])
                cv2.imwrite(store, imgBgr, cvImgSaver)
                dstList.append(store)
                index += 1
            else:
                old = os.path.join(rt, name)
                new = old.replace(srcRoot, dstRoot)
                storeRoute = os.path.split(new)

                if not os.path.exists(storeRoute[0]):
                    os.makedirs(storeRoute[0])
                shutil.copyfile(old, new)

            sys.stdout.write("\r" + str(index) + '/' + str(len(files)))
            sys.stdout.flush()
else:
    print("No Source!!!")
    sys.exit(0)

if (needVideo):
    if not os.path.exists(dstRoot):
        os.makedirs(dstRoot)

    videoWriter = cv2.VideoWriter(dstRoot + "/video.avi", \
        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (cols, rows))

    dstList.sort()
    for line in dstList:
         imgBgr = cv2.imread(line)
         videoWriter.write(imgBgr)
    videoWriter.release()
else:
    print()
    print("No need for save video!!!")

print(os.linesep)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
