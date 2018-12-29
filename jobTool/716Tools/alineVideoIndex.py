# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       synchronize video start frameNo.
"""
import os
import sys
import time
import cv2
import numpy

### Defs region
def readVideo(iVideoFile):
    index = 0
    vc = cv2.VideoCapture(iVideoFile)
    if not vc.isOpened():
        print('Open video error')
        sys.exit(1)
    while True:
        re, frame = vc.read()
        if not re:
            break
        index += 1
        cv2.imshow(iVideoFile, frame)
        key = cv2.waitKey()
        if 99 == key:    #按键c
            break
        elif 97 == key:    #按键a
            vc.release()
            vc = cv2.VideoCapture(iVideoFile)
            index = 0
    print(iVideoFile, index)
    return index

### Params region
srcRoot = "/media/devin/Elements/Process716/Dst1114/"
dimCmp = ["DimF", "DimZ"]
infraredCmp = ["InfraredF", "InfraredZ"]

cnt0 = 0
cnt1 = 0
### Job region
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            videoName1 = os.path.join(rt, name)
            if -1 != videoName1.find(os.path.sep + dimCmp[0] + os.path.sep):
                txtName = srcRoot + "Dim" + str(cnt0) + ".txt"
                cnt0 += 1
                videoName2 = videoName1.replace(dimCmp[0], dimCmp[1])
                with open(txtName, 'w') as fw:
                    fw.write("Dim Zone")
                    fw.write(os.linesep)
                    fw.write(videoName2)
                    fw.write(os.linesep)
                    index = readVideo(videoName2)
                    fw.write(str(index))

                    fw.write("Dim Full")
                    fw.write(os.linesep)
                    fw.write(videoName1)
                    fw.write(os.linesep)
                    index = readVideo(videoName1)
                    fw.write(str(index))
                    fw.write(os.linesep)
            elif -1 != videoName1.find(os.path.sep + infraredCmp[0] + os.path.sep):
                txtName = srcRoot + "Infrared" + str(cnt1) + ".txt"
                cnt1 += 1
                videoName2 = videoName1.replace(infraredCmp[0], infraredCmp[1])
                with open(txtName, 'w') as fw:
                    fw.write("Infrared Full")
                    fw.write(os.linesep)
                    fw.write(videoName1)
                    fw.write(os.linesep)
                    index = readVideo(videoName1)
                    fw.write(str(index))
                    fw.write(os.linesep)

                    fw.write("Infrared Zone")
                    fw.write(os.linesep)
                    fw.write(videoName2)
                    fw.write(os.linesep)
                    index = readVideo(videoName2)
                    fw.write(str(index))
            cv2.destroyAllWindows()

print(os.linesep)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))