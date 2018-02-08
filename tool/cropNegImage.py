import os
import time
import random
import cv2

srcRoot = "/media/devin/Elements1/usbFolder/"
dstRoot = "/media/devin/Elements1/111/"
dstRow = 54
dstCol = 36

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
if not os.path.exists(dstRoot):
    os.makedirs(dstRoot)

downSample = 0.33
cnt = 0
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if -1 != name.find(".jpg") or -1 != name.find(".JPG") \
                or -1 != name.find(".png") or -1 != name.find(".PNG"):
                absoluteRoute = os.path.join(rt, name)
                print absoluteRoute
                img = cv2.imread(absoluteRoute, cv2.IMREAD_COLOR)
                if img is None:
                    continue
                if img.shape[0] < dstRow:
                    continue
                if img.shape[1] < dstCol:
                    continue

                dstFolder = rt.replace(srcRoot, dstRoot)
                if not os.path.exists(dstFolder):
                    os.makedirs(dstFolder)
                    print dstFolder
                dstImg = img[(img.shape[0] - dstRow) / 2 : (img.shape[0] - dstRow) / 2 + dstRow, \
                                (img.shape[1] - dstCol) / 2 : (img.shape[1] - dstCol) / 2 + dstCol]
                cv2.imwrite(os.path.join(dstFolder, name), dstImg)
                cnt += 1
else:
    print("No Source!!!")

print os.linesep
print "Total images: " + str(cnt)
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())