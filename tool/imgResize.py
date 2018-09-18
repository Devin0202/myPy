# -*- coding: utf-8 -*-
import os
import sys
import time
import random
from skimage import io, data, transform
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

srcRootList = ["/home/devin/Desktop/faceOri/yunnan/"]
dstRootList = ["/home/devin/Desktop/faceOri/yunnanS/"]

rowSize = 720
colSize = 1280
rowSizeOri = 1080
colSizeOri = 1920
rowRation = rowSize / float(rowSizeOri)
colRation = colSize / float(colSizeOri)
index = 0
downSample = 1
allLines = []

if len(srcRootList) != len(dstRootList):
    print "List Error!"
    sys.exit(0)
else:
    for (srcRoot, dstRoot) in zip(srcRootList, dstRootList):
        print srcRoot
        print dstRoot
        if not os.path.exists(dstRoot):
            os.makedirs(dstRoot)
        if os.path.exists(srcRoot):
            for rt, dirs, files in os.walk(srcRoot):
                for name in files:
                    if -1 != name.find(".jpg") or -1 != name.find(".JPG") \
                    or -1 != name.find(".png") or -1 != name.find(".PNG"):
                        if random.uniform(0, 1) <= downSample:
                            absoluteRoute = os.path.join(rt, name)
                            #print absoluteRoute
                            img = io.imread(absoluteRoute)
                            if 0 < img.size:
                                rowRation = rowSize / float(img.shape[0])
                                colRation = colSize / float(img.shape[1])
                                # if colSizeOri != img.shape[1] \
                                # or rowSizeOri != img.shape[0]:
                                #     print "Wrong shape: " \
                                #     + str(img.shape[0]) + str(img.shape[1])
                                #     continue
                                # dstImg = transform.resize(img, (rowSize, colSize))
                                dstImg = transform.resize(img, (img.shape[0] / 2, img.shape[1] / 2))
                                dstImg = transform.resize(img, (img.shape[0] / 2 * 2, img.shape[1] / 2 * 2))
                                dst = absoluteRoute.replace(srcRoot, dstRoot)
                                if not os.path.exists(os.path.split(dst)[0]):
                                    os.makedirs(os.path.split(dst)[0])
                                io.imsave(dst, dstImg)
                                index += 1
                    # Just for Hiscene Palm or Head
                    if -1 != name.find("dataLabel.txt"):
                        absoluteRoute = os.path.join(rt, name)
                        inputF = open(absoluteRoute, 'r')
                        try:
                            allLines = inputF.readlines()
                        finally:
                            inputF.close()

                        dst = absoluteRoute.replace(srcRoot, dstRoot)
                        if not os.path.exists(os.path.split(dst)[0]):
                            os.makedirs(os.path.split(dst)[0])
                        outputF = open(dst, 'w')
                        outLines = []
                        try:
                            for line in allLines:
                                tmp = line.split()
                                tmp[2] = str(int(int(tmp[2]) * colRation))
                                tmp[3] = str(int(int(tmp[3]) * colRation))
                                tmp[4] = str(int(int(tmp[4]) * rowRation))
                                tmp[5] = str(int(int(tmp[5]) * rowRation))
                                outLines.append(tmp[0] + ' ' + tmp[1] + ' ' \
                                    + tmp[2] + ' ' + tmp[3] + ' ' + tmp[4] \
                                    + ' ' + tmp[5] + "\r\n")
                            outputF.writelines(outLines)
                        finally:
                            outputF.close()
        else:
            print("No Source!!!")
            sys.exit(0)

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())