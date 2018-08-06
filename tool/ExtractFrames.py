# -*- coding: utf-8 -*-
"""
Extract frames from video
"""
import os
import sys
import time
import cv2

targetL1 = "/home/devin/Downloads/2018-0726/"
dst = "/home/devin/Downloads/2018-0726/111/"
targetFile = dst + "1.txt"

def doIt(files, dst, start):
    cap = cv2.VideoCapture(files)
    if not cap.isOpened():
        print("No Source!!!")
        sys.exit(0)
        
    if not os.path.exists(dst):
        os.makedirs(dst)

    frameCnt = start
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    print (fps)
    print (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)))
    print (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

    with open(targetFile, 'a') as fw:
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                cv2.imshow("video",frame)
                k = cv2.waitKey(int(1000 / fps))

                # frameCnt += 1
                # if (0 == frameCnt % 2):
                #     continue

                cv2.imwrite(dst + '/' + str(frameCnt) + ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                #cv2.imwrite(dst + '/' + str(frameCnt) + ".png", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

                fw.write(str(frameCnt) + ".jpg")
                fw.write(os.linesep)

                if (k & 0xff == ord('q')):
                    break
                else:
                    continue
            else:
                break

    cap.release()
    cv2.destroyAllWindows()
    return frameCnt

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

startNum = 0
filesNum = 0
if os.path.exists(targetL1):
    for rt, dirs, files in os.walk(targetL1):
        for name in files:
            filesNum += 1
            print(os.path.join(rt, name))
            tmp = os.path.join(rt, name)
            startNum = doIt(tmp, dst, startNum)

print(filesNum)
print os.linesep
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())