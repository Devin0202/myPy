# -*- coding: utf-8 -*-
"""
Convert NV21 to png
"""
import os
import sys
import time
import cv2
import shutil
import numpy as np
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

cols = 1280
rows = 720
srcRoot = "/home/devin/Desktop/tmp/0830111052/"
dstRoot = "/home/devin/Desktop/tmp/0830111052png/"
suffix = ".nv21"
lenSuffix = len(suffix)
fileBytes = cols * rows * 3 / 2
cvImgSaver = [int(cv2.IMWRITE_PNG_COMPRESSION), 3]
index = 0

if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if len(name) - lenSuffix == name.find(suffix):
                with open(os.path.join(rt, name), 'r') as fr:
                    oriData = fr.read()
                    if not len(oriData) == fileBytes:
                        print(os.path.join(rt, name))
                        continue

                imgYuv = np.fromstring(oriData, dtype = np.uint8)
                imgYuv = np.reshape(imgYuv, (-1, cols))
                imgBgr = cv2.cvtColor(imgYuv, cv2.COLOR_YUV2BGR_NV21)
                store = name.replace(suffix, ".png")
                store = os.path.join(rt, store)
                store = store.replace(srcRoot, dstRoot)
                storeRoute = os.path.split(store)

                if not os.path.exists(storeRoute[0]):
                    os.makedirs(storeRoute[0])
                cv2.imwrite(store, imgBgr, cvImgSaver)
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

print(os.linesep)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))