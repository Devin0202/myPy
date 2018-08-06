# -*- coding: utf-8 -*-
"""
Draw Rects for pics serials
"""
import os
import sys
import time
import cv2

def readList(file):
    if not os.path.exists(file):
        print("No rectList!!!")
        sys.exit(0)

    rectList = []
    with open(file, 'r') as fr:
        for lines in fr.readlines():
            # -2 is used to remove " \n"
            rectList.append(lines[0: -2])
    return rectList

def drawRect(picInfo, parentFolder, fps, video = []):
    if not os.path.exists(parentFolder):
        print("No folder!!!")
        sys.exit(0)

    if not (picInfo):
        print("No rectInfo!!!")
        sys.exit(0)

    if (video):
        videoWriter = cv2.VideoWriter(video, \
            cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'), fps, (1280, 720))
    else:
        print("No need for save video!!!")

    for elements in picInfo:
        # -2 is used to remove xxx.jpg and rect numbers
        if 2 > len(elements.split(' ')) \
            and 0 != (len(elements.split(' ')) - 2) % 4:
            continue
        else:
            # print parentFolder + os.path.sep + elements.split(' ')[0]
            frame = cv2.imread(parentFolder + os.path.sep + elements.split(' ')[0])
            if 0 < int(elements.split(' ')[1]):
                for i in range(2, len(elements.split(' ')), 4):
                    sp = frame.shape
                    l = int(sp[1] * float(elements.split(' ')[i]))
                    t = int(sp[0] * float(elements.split(' ')[i + 1]))
                    r = int(sp[1] * (float(elements.split(' ')[i]) \
                        + float(elements.split(' ')[i + 2])))
                    b = int(sp[0] * (float(elements.split(' ')[i + 1]) \
                        + float(elements.split(' ')[i + 3])))

                    cv2.rectangle(frame, (l, t), (r, b), (255, 0, 0), 2)

            if (video):
                videoWriter.write(frame)

            cv2.imshow("video",frame)
            k = cv2.waitKey(int(1000 / fps))
            if (k & 0xff == ord('q')):
                break
            else:
                continue

    if (video):
        videoWriter.release()

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

targetL1 = "/home/devin/Desktop/0727face/ml/ml1"
dst = "/home/devin/Desktop/0727face/ml/"
targetFile = dst + "face++Track-ml107-27-17-47.txt"
videoDst = dst + "face++Track-ml107-27-17-47.avi"
# Do the job!!!
infos = readList(targetFile)
# print infos
drawRect(infos, targetL1, 20, videoDst)

print os.linesep
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())