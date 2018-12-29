# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Trim, resize and fps-adjust for the video 
"""
import os
import sys
import time
import cv2
import numpy

print(sys.version)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
### Defs region
def folderMirror(iSrcRoot, iEntity, iMirror):
    if os.path.sep != iSrcRoot[-1]:
        srcRoot = iSrcRoot + os.path.sep + iEntity
    else:
        srcRoot = iSrcRoot + iEntity

    if os.path.sep != srcRoot[-1]:
        srcRoot += os.path.sep

    # print(srcRoot)
    if os.path.exists(srcRoot):
        for rt, dirs, files in os.walk(srcRoot):
            for name in dirs:
                newFolder = os.path.join(rt, name)
                newFolder = newFolder.replace(iEntity, iMirror)
                print("NewFolders: " + newFolder)
                if not os.path.exists(newFolder):
                    os.makedirs(newFolder)
    else:
        print("No resource!!!")
        sys.exit(0)

def doAll(iRoot, iOri, iDst):
    if os.path.sep != iRoot[-1]:
        srcRoot = iRoot + os.path.sep + iOri
    else:
        srcRoot = iRoot + iOri

    if os.path.sep != srcRoot[-1]:
        srcRoot += os.path.sep

    if os.path.exists(srcRoot):
        for rt, dirs, files in os.walk(srcRoot):
            for name in files:
                inVideoPath = os.path.join(rt, name)
                outVideoPath = inVideoPath.replace(iOri, iDst)
                outVideoPath = outVideoPath.replace("mp4", "avi")
                vc = cv2.VideoCapture(inVideoPath)
                out = cv2.VideoWriter()

                print("NewVideo: " + outVideoPath)
                originFrameRate = float(vc.get(5))
                print(originFrameRate)
                if not vc.isOpened():
                    print("Open video error")
                    sys.exit(0)
                else:
                    num = 0;
                    while True:
                        re, frame = vc.read()
                        num += 1
                        if not re:
                            break;
                        tp = frame[up : frame.shape[0] - down, \
                                    left : frame.shape[1] - right, :]
                        frame = cv2.resize(tp, (cResize[0], cResize[1]))
                        if not out.isOpened():
                            frame_width = frame.shape[1]
                            frame_height = frame.shape[0]
                            out.open(outVideoPath, \
                                cv2.VideoWriter_fourcc('M','J','P','G'), \
                                cFps, (frame_width, frame_height))

                        if 0 < (cFps - originFrameRate):
                            tmp = int(originFrameRate \
                                        / (cFps - originFrameRate) + 0.5)
                            if 0 == num % tmp:
                                out.write(frame)
                        out.write(frame)
                    vc.release()
                    out.release()

### Params region
srcRoot = "/media/devin/Elements/Process716/"
entityFolder = "Ori1114/"
dstFolder = "Dst1114/"

cFps = 25
cResize = [640, 480]
up = 0
down = 0
left = 0
right = 0
TAR  = False
SRC = False
if TAR:
    up = 0
    down = 0
    left = 160
    right = 160

if SRC:
    up = 40
    down = 40
    left = 24
    right = 30

### Job region
folderMirror(srcRoot, entityFolder, dstFolder)
doAll(srcRoot, entityFolder, dstFolder)

print(os.linesep)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))