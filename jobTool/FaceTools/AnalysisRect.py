# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Draw the rects for face detect & recognization
"""
import os
import sys
import time
import cv2
from concurrent.futures import ProcessPoolExecutor, wait
import numpy as np

print(sys.version)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
### Defs region
class FaceRects:
    def __init__(self, faceID):
        self.mFaceID = faceID
        self.faceName = None
        self.detScore = None
        self.recgScore = None
        self.mFaceL = None
        self.mFaceT = None
        self.mFaceR = None
        self.mFaceB = None
        return

class FrameRects:
    def __init__(self, frameID):
        self.mFrameID = frameID
        self.mFile = None
        self.detRects = []
        self.recgRects = []
        self.recgRectsIV = []
        self.recgRectsV = []
        self.recgRectsE = []
        self.recgRectsC = []
        return

    def printSelf(self):
        print(self.mFrameID)
        print(self.mFile)
        for it in self.detRects:
            print("Detection: " + str(it.mFaceID))
            tmpS = str(it.mFaceL) + ' ' + str(it.mFaceT) + ' ' \
            + str(it.mFaceR) + ' ' + str(it.mFaceB)
            print(tmpS)

        for it in self.recgRectsIV:
            print("Invalid: " + str(it.mFaceID))
            tmpS = str(it.mFaceL) + ' ' + str(it.mFaceT) + ' ' \
            + str(it.mFaceR) + ' ' + str(it.mFaceB)
            print(tmpS)

        for it in self.recgRectsV:
            print("Valid: " + str(it.mFaceID))
            tmpS = str(it.mFaceL) + ' ' + str(it.mFaceT) + ' ' \
            + str(it.mFaceR) + ' ' + str(it.mFaceB)
            print(tmpS)
            print(it.faceName)
            print(str(it.recgScore))
        return

def getRectInfo(fOriInfo, fRectsMap):
    tmpI = int(fOriInfo.split(' ')[4])
    tmpR = FaceRects(tmpI)
    tmpR.mFaceL = int(fOriInfo.split()[5])
    tmpR.mFaceT = int(fOriInfo.split()[6])
    tmpR.mFaceR = int(fOriInfo.split()[7])
    tmpR.mFaceB = int(fOriInfo.split()[8])

    idx = fOriInfo.split("|D||frameID: ")[1].split(" status: ")[0]
    if idx not in fRectsMap.keys():
        fRectsMap[idx] = FrameRects(idx)
    return tmpR, idx

def saveAssist(fStoreDst, fReplace, fNewOne):
    storeOne = fStoreDst.replace(fReplace, fNewOne)
    storeRoute = os.path.split(storeOne)
    if not os.path.exists(storeRoute[0]):
        os.makedirs(storeRoute[0])
    return storeOne

def saveRects(fImg, fDst, fDate, fReplace):
    for rects in fDate.detRects:
        cv2.putText(fImg, str(round(100 * rects.detScore, 2)), \
            (rects.mFaceL + 3, rects.mFaceT + 13), cv2.FONT_ITALIC, 0.5, \
            (255, 255, 255), thickness = 1)
        cv2.rectangle(fImg, (rects.mFaceL, rects.mFaceT), \
            (rects.mFaceR, rects.mFaceB), (255, 255, 255), 2)
        faceRoi = fImg[rects.mFaceT:rects.mFaceB, rects.mFaceL:rects.mFaceR]
        tmpStore = fDst.replace(".jpg", "_D.jpg")
        cv2.rectangle(faceRoi, (0, 0), (faceRoi.shape[1], faceRoi.shape[0]), \
            (255, 255, 255), 2)
        cv2.imwrite(tmpStore, faceRoi, cvImgSaver)
        storeRect = saveAssist(tmpStore, fReplace, rectsFolder)
        cv2.imwrite(storeRect, faceRoi, cvImgSaver)

    for rects in fDate.recgRectsC:
        cv2.putText(fImg, str(rects.recgScore), \
            (rects.mFaceL, rects.mFaceT - 10), cv2.FONT_ITALIC, 0.5, \
            (255, 0, 0), thickness = 1)
        cv2.rectangle(fImg, (rects.mFaceL, rects.mFaceT), \
            (rects.mFaceR, rects.mFaceB), (0, 255, 0), 2)
        faceRoi = fImg[rects.mFaceT:rects.mFaceB, rects.mFaceL:rects.mFaceR]
        tmpStore = fDst.replace(".jpg", "_R.jpg")
        cv2.rectangle(faceRoi, (0, 0), (faceRoi.shape[1], faceRoi.shape[0]), \
            (0, 255, 0), 2)
        cv2.imwrite(tmpStore, faceRoi, cvImgSaver)
        storeRect = saveAssist(tmpStore, fReplace, rectsFolder)
        cv2.imwrite(storeRect, faceRoi, cvImgSaver)

    for rects in fDate.recgRectsE:
        cv2.putText(fImg, str(rects.recgScore), \
            (rects.mFaceL, rects.mFaceT - 10), cv2.FONT_ITALIC, 0.5, \
            (255, 0, 0), thickness = 1)
        cv2.rectangle(fImg, (rects.mFaceL, rects.mFaceT), \
            (rects.mFaceR, rects.mFaceB), (0, 0, 255), 2)
        faceRoi = fImg[rects.mFaceT:rects.mFaceB, rects.mFaceL:rects.mFaceR]
        tmpStore = fDst.replace(".jpg", "_E.jpg")
        cv2.rectangle(faceRoi, (0, 0), (faceRoi.shape[1], faceRoi.shape[0]), \
            (0, 0, 255), 2)
        cv2.imwrite(tmpStore, faceRoi, cvImgSaver)
        storeRect = saveAssist(tmpStore, fReplace, rectsFolder)
        cv2.imwrite(storeRect, faceRoi, cvImgSaver)

    for rects in fDate.recgRectsIV:
        cv2.rectangle(fImg, (rects.mFaceL, rects.mFaceT), \
            (rects.mFaceR, rects.mFaceB), (0, 255, 255), 2)
        faceRoi = fImg[rects.mFaceT:rects.mFaceB, rects.mFaceL:rects.mFaceR]
        tmpStore = fDst.replace(".jpg", "_I.jpg")
        cv2.rectangle(faceRoi, (0, 0), (faceRoi.shape[1], faceRoi.shape[0]), \
            (0, 255, 255), 2)
        cv2.imwrite(tmpStore, faceRoi, cvImgSaver)
        storeRect = saveAssist(tmpStore, fReplace, rectsFolder)
        cv2.imwrite(storeRect, faceRoi, cvImgSaver)

    return fImg

def concurrentJob(fTmpS, fOriData, fObj, fNeed = True):
    fTmpS = fTmpS.replace(suffix, ".jpg")
    store = saveAssist(fTmpS, dataFolder, dstImgRoot)
    storeWhole = saveAssist(store, level3Folder, fullImgFolder)
    if not os.path.exists(store):
        imgYuv = np.fromstring(fOriData, dtype = np.uint8)
        imgYuv = np.reshape(imgYuv, (-1, cols))
        imgBgr = cv2.cvtColor(imgYuv, cv2.COLOR_YUV2BGR_NV21)
    else:
        imgBgr = cv2.imread(store, cv2.IMREAD_COLOR)

    saveRects(imgBgr, store, fObj, level3Folder)
    if fNeed:
        cv2.imwrite(store, imgBgr, cvImgSaver)
        cv2.imwrite(storeWhole, imgBgr, cvImgSaver)
    else:
        pass

### Params region
logFolder = "/home/devin/Desktop/TestResults/"
dataFolder = "/media/devin/OpenImage600/face3/"
level3Folder = "cameraData"
rectsFolder = "Rects"
fullImgFolder = "FullImage"
nameMap = {"yanchangjian" : "颜长建", "guangming" : "广明", "yukeke" : "珂珂"}
objs = ["yanchangjian", "guangming", "yukeke"]

cols = 1280
rows = 720
dstImgRoot = "/home/devin/Desktop/tmpPng/"
suffix = ".nv21"
fileBytes = cols * rows * 3 / 2
cvImgSaver = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
needFullImage = False

### Job region
if __name__ == '__main__':
    futuresList = []
    executor = ProcessPoolExecutor(max_workers = 16)
    for obj in objs:
        oriData = None
        tmpList = []
        rectsMap = {}
        dataSet = dataFolder + obj + "/" + level3Folder + "/"
        logSet = logFolder + obj + "/"
        for rt, dirs, files in os.walk(logSet):
            for name in files:
                # print(name)
                with open(os.path.join(rt, name), 'r') as f:
                    for line in f.readlines():
                        if -1 != line.find("status: detectInfo") \
                            or -1 != line.find("status: recgInvalidRoi") \
                            or -1 != line.find("status: recgValidRoi") \
                            or -1 != line.find("file: "):
                            tmpList.append(line)

        for line in tmpList:
            if -1 != line.find("status: detectInfo"):
                tmpR, idx = getRectInfo(line, rectsMap)
                tmpR.detScore = float(line.split()[9])
                rectsMap.get(idx).detRects.append(tmpR)

            if -1 != line.find("status: recgInvalidRoi"):
                tmpR, idx = getRectInfo(line, rectsMap)
                rectsMap.get(idx).recgRectsIV.append(tmpR)

            if -1 != line.find("status: recgValidRoi"):
                tmpR, idx = getRectInfo(line, rectsMap)
                tmpR.faceName = line.split()[10]
                tmpR.recgScore = float(line.split(" score: ")[1])

                if -1 != tmpR.faceName.find(nameMap.get(obj)):
                    rectsMap.get(idx).recgRectsC.append(tmpR)
                else:
                    rectsMap.get(idx).recgRectsE.append(tmpR)

        for it in rectsMap.keys():
            for line in tmpList:
                idx = line.split("|D||frameID: ")[1].split(" file: ")[0]
                if -1 != line.find("file: ") and idx == it:
                    tmpS = line.split("/")[3] + '/'
                    tmpS += line.split("/")[4].split(" status:")[0]
                    # print(tmpS)
                    rectsMap.get(it).mFile = tmpS

        # for it in rectsMap.keys():
        #     rectsMap.get(it).printSelf()
        print(obj + " Record frames Num: " + str(len(rectsMap)))

        if os.path.exists(dataSet):
            for it in rectsMap.keys():
                tmpS = dataSet + rectsMap.get(it).mFile
                objX = rectsMap.get(it)
                if not os.path.exists(tmpS):
                    print("no file: " + tmpS)
                    continue
                else:
                    with open(tmpS, 'rb') as fr:
                        oriData = fr.read()
                        if not len(oriData) == fileBytes:
                            print("Size mismatch: " + tmpS)
                            continue

                    future = executor.submit(concurrentJob, tmpS, oriData, \
                        objX, needFullImage)
                    futuresList.append(future)
        else:
            print("No Source!!!")
            sys.exit(0)
    wait(futuresList)

print(os.linesep)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))