# -*- coding: utf-8 -*-
"""
Extract frames from video
"""
import os
import sys
import time
import cv2

print(sys.version)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

### Defs region
def doIt(files, dst, start):
    dst = dst + os.path.sep
    cap = cv2.VideoCapture(files)
    if not cap.isOpened():
        print("No Source!!!")
        sys.exit(0)
        
    if not os.path.exists(dst):
        os.makedirs(dst)

    frameCnt = start
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("FPS: " + str(fps))
    print("Width: " + str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))))
    print("Height: " + str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    targetFile = dst + "list.txt"
    with open(targetFile, 'a') as fw:
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                # cv2.imshow("video", frame)
                # k = cv2.waitKey(int(1000 / fps))

                # if (0 == frameCnt % 2):
                #     continue

                cv2.imwrite(dst + '/' + str(frameCnt) + ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                #cv2.imwrite(dst + '/' + str(frameCnt) + ".png", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

                fw.write(str(frameCnt) + ".jpg")
                fw.write(os.linesep)

                # if (k & 0xff == ord('q')):
                #     break
                # else:
                #     continue
                frameCnt += 1
            else:
                break

    cap.release()
    cv2.destroyAllWindows()
    return frameCnt

### Params region
targetL1 = "/home/devin/Downloads/tmp"
dst = "/home/devin/Downloads/tmp"
dst = dst + os.path.sep
startNum = 0
filesNum = 0

### Job region
if os.path.exists(targetL1):
    for rt, dirs, files in os.walk(targetL1):
        for name in files:
            if name.split('.')[-1] in ["mp4"]:
                filesNum += 1
                print(os.path.join(rt, name))
                tmp = os.path.join(rt, name)
                localDst = dst + name.split('.')[0]
                startNum = doIt(tmp, localDst, startNum)
print("Processed: " + str(filesNum))

print(os.linesep)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))