# -*- coding: utf-8 -*-
"""
Crop the image
"""
import sys
import os
import time
import cv2

print(sys.version)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

### Defs region
def cropResize(fImg, fCropHW, fResizeWH, fCropTL):
    img = cv2.imread(fImg, cv2.IMREAD_COLOR)
    TL = [0, 0]
    if img is None:
        print("Failed: " + fImg)
        return []
    else:
        TL[0] = int(fCropTL[0] * img.shape[0])
        TL[1] = int(fCropTL[1] * img.shape[1])

    if img.shape[0] < fCropHW[0] + TL[0] \
        or img.shape[1] < fCropHW[1] + TL[1] \
        or TL[0] < 0 or TL[1] < 0 \
        or fCropHW[0] < 0 or fCropHW[1] < 0:
        print("Failed: " + fImg)
        return []


    dstImg = img[TL[0] : fCropHW[0] + TL[0] - 1, \
                TL[1] : fCropHW[1] + TL[1] - 1]
    dstImg = cv2.resize(dstImg, fResizeWH)
    return dstImg

### Params region
srcRoot = "/home/devin/Downloads/tmp/PosR4/old/"
dstRoot = "/home/devin/Downloads/tmp/PosR4/oldCS/"
cropSize = (500, 300)
dstSize = (300, 500)
cropTL = (0.20, 0.38)

if not os.path.exists(dstRoot):
    os.makedirs(dstRoot)

### Job region
cnt = 0
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if -1 != name.find(".jpg") or -1 != name.find(".JPG") \
                or -1 != name.find(".png") or -1 != name.find(".PNG"):
                absoluteRoute = os.path.join(rt, name)
                print(absoluteRoute)

                dstFolder = rt.replace(srcRoot, dstRoot)
                if not os.path.exists(dstFolder):
                    os.makedirs(dstFolder)
                    print(dstFolder)

                dstImg = cropResize(absoluteRoute, cropSize, dstSize, cropTL)

                # img = cv2.imread(absoluteRoute, cv2.IMREAD_COLOR)
                # retval = cv2.getRotationMatrix2D((img.shape[1] / 2, \
                #     img.shape[0] / 2), 180, 1)
                # dstImg = cv2.warpAffine(img, retval, (img.shape[1], \
                #     img.shape[0]))

                if [] != dstImg:
                    dstFolder = dstFolder + os.path.sep
                    cv2.imwrite(os.path.join(dstFolder, name), dstImg)
                    cnt += 1
else:
    print("No Source!!!")

print(os.linesep)
print("Total images: " + str(cnt))
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))