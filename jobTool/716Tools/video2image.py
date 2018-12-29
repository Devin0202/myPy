# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Make serials images
"""
import os
import sys
import time
import cv2
import numpy

### Defs region
def doIt(files, dst, start):
    # print(files)
    cap = cv2.VideoCapture(files)
    if not cap.isOpened():
        print("No Source!!!")
        sys.exit(0)
        
    if not os.path.exists(dst):
        os.makedirs(dst)

    frameCnt = 0
    fps = cap.get(5)
    print (fps)
    print (int(cap.get(3)))
    print (int(cap.get(4)))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow("video",frame)
            k = cv2.waitKey(int(1000 / fps))

            if (frameCnt > start):
                cv2.imwrite(dst + '/' + str(frameCnt - start) + ".jpg", frame, \
                                    [int(cv2.IMWRITE_JPEG_QUALITY), 100])

            frameCnt += 1
            if (k & 0xff == ord('q')):
                break
            else:
                continue
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    return frameCnt

### Params region
srcRoot = "/media/devin/Elements/Process716/Dst1114/"

### Job region
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            txtName = os.path.join(rt, name)
            if -1 != txtName.find(".txt"):
                with open(txtName, 'r') as fr:
                    datas = fr.readlines()
                    if 6 == len(datas):
                        tarFile = datas[1].splitlines()[0]
                        tarIndex = int(datas[2].splitlines()[0])
                        srcFile = datas[4].splitlines()[0]
                        srcIndex = int(datas[5].splitlines()[0])

                        print(tarFile + ': ' + str(tarIndex))
                        dst = tarFile[: -4]
                        print(dst)
                        doIt(tarFile, dst, tarIndex)

                        print(srcFile + ': ' + str(srcIndex))
                        dst = srcFile[: -4]
                        print(dst)
                        doIt(srcFile, dst, srcIndex)
                    else:
                        print("Wrong txt file: " + txtName)
                        exit(0)

print(os.linesep)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))