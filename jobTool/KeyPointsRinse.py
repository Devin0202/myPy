# -*- coding: utf-8 -*-
"""Brief
Language: python3
Goal: 手势关节点-手势语义 数据清洗工具
PS: KeyPointsRinse.py支持按键操作
    'd'            表示当前数据异常, 进行剔除
    '<-'左方向键    回退至前一份数据
    其余按键        表示当前数据正常, 保留
"""
import sys
import os
import time
import timeit
import re
import concurrent.futures

"""Common utilities
Functions:
1. safeDirectory
2. makeAbsDirs
3. globalStart
4. globalEnd
5. traversFilesInDir
"""
def safeDirectory(fDir):
    if str == type(fDir):
        safeDir = re.sub(os.path.sep + "{2,}", os.path.sep, fDir)
        if os.path.sep == safeDir[-1]:
            pass
        else:
            safeDir += os.path.sep
    else:
        print("Error type of input!!!")
        sys.exit(0)
    return safeDir

def makeAbsDirs(fDir, fExistencePermitted = True):
    safeDir = safeDirectory(fDir)
    if os.path.isabs(safeDir):
        try:
            if not os.path.exists(safeDir):
                os.makedirs(safeDir)
            else:
                if not fExistencePermitted:
                    print("The folder had been existed!!!")
                    sys.exit(0)
                else:
                    pass
        except Exception as e:
            print(e)
            sys.exit(0)
        else:
            print("Create: " + safeDir + "    OK")
            return safeDir
    else:
        print("Please use absolute path!!!")
        sys.exit(0)

def globalStart():
    print("LocalSystem: " + os.name)
    print("Python Ver: " + sys.version)
    timeStampFormat = "%Y-%m-%d %H:%M:%S"
    print(time.strftime(timeStampFormat, time.localtime()))
    globalT = timeit.default_timer()
    print()
    return globalT

def globalEnd(fGlobalT):
    timeStampFormat = "%Y-%m-%d %H:%M:%S"
    globalElapsed = (timeit.default_timer() - fGlobalT) / 60
    print()
    print(time.strftime(timeStampFormat, time.localtime()))
    print("Finished in {:.2f}m".format(globalElapsed))

def concurrentWork(fMaxload, fFn, *fArgs, \
    isProcess = True, isConcurrent = True):
    if isConcurrent:
        if isProcess:
            executor = \
            concurrent.futures.ProcessPoolExecutor(max_workers = fMaxload)
        else:
            executor = \
            concurrent.futures.ThreadPoolExecutor(max_workers = fMaxload)
        results = list(executor.map(fFn, *fArgs))
    else:
        results = list(map(fFn, *fArgs))
    return results

def traversFilesInDir(fSrcRoot, fBlackList=[]):
    rtv = []
    srcRoot = safeDirectory(fSrcRoot)
    if os.path.exists(srcRoot):
        for rt, dirs, files in os.walk(srcRoot):
            for name in files:
                if rt in fBlackList:
                    continue
                else:
                    rtv.append(os.path.join(rt, name))
    else:
        print("Please use correct path!!!")
        sys.exit(0)
    return rtv
"""Definition region

Class:

Constants:

Functions:
1. 
"""
from typing import List
import cv2
import numpy as np
class infoLoader():
    pattern = {1:"ok", 2:"fist", 3:"L", 4:"R", 5:"U", \
                6:"D", 7:"palm", 8:"yeah", 9:"open", 10:"close"}
    bgColor = tuple(reversed((0, 0, 0)))
    lineColor = tuple(reversed((255, 255, 0)))
    circleColor = tuple(reversed((0, 255, 0)))
    textColor = tuple(reversed((0, 255, 255)))
    lineConnect = [(0, 1), (1, 2), (2, 3), (3, 4), \
                    (0, 5), (5, 6), (6, 7), (7, 8), \
                    (0, 9), (9, 10), (10, 11), (11, 12), \
                    (0, 13), (13, 14), (14, 15), (15, 16), \
                    (0, 17), (17, 18), (18, 19), (19, 20)]
    def __init__(self):
        self.valid = False
        self.originData: str = None
        self.imgW = None
        self.imgH = None
        self.imgLabel = None
        """keyPoint format uses (x, y), x with width, y with height"""
        self.keyPoints: List[(float, float)] = []
    
    def list2info(self, fLine, checkLen) -> bool:
        infos = fLine.split()
        if checkLen == len(infos):
            self.valid = True
            self.originData = fLine
            self.imgW = int(infos[1])
            self.imgH = int(infos[2])
            self.imgLabel = int(infos[0])
            self.keyPoints.clear()
            for i in range(3, len(infos), 2):
                centerX = int(float(infos[i]) * self.imgW)
                centerY = int(float(infos[i + 1]) * self.imgH)
                self.keyPoints.append((centerX, centerY))
            return True
        else:
            self.valid = False
            return False

    def drawKeyPoints(self, fCount, printOrder=False, printLine=True):
        if self.valid:
            matColor = np.zeros((self.imgH, self.imgW, 3), np.uint8)
            matColor[:] = self.bgColor
            drawSize = min(self.imgH, self.imgW) // 256
            fontSize = min(self.imgH, self.imgW) / 800

            pointCnt = 0
            for i in self.keyPoints:
                # cv2.putText(matColor, "Cnt: " + str(fCount), \
                #             (0, int(fontSize * 25)), \
                #             cv2.FONT_HERSHEY_SIMPLEX, fontSize, \
                #             self.textColor, thickness=drawSize)
                cv2.putText(matColor, \
                            "Pattern: " + self.pattern[self.imgLabel], \
                            (self.imgH // 2, int(fontSize * 60)), \
                            cv2.FONT_HERSHEY_SIMPLEX, fontSize, \
                            self.textColor, thickness=drawSize)
                cv2.circle(matColor, i, \
                            drawSize, self.circleColor, thickness=drawSize)

                if printOrder:
                   cv2.putText(matColor, str(pointCnt), \
                            i, \
                            cv2.FONT_HERSHEY_SIMPLEX, fontSize, \
                            self.textColor, thickness=drawSize)
                else:
                    pass
                pointCnt += 1

            if printLine:
                lineSize = drawSize // 2
                for i in self.lineConnect:
                    cv2.line(matColor, self.keyPoints[i[0]], \
                            self.keyPoints[i[1]], self.lineColor, \
                            thickness=lineSize)
            else:
                pass

            cv2.imshow("Image", matColor)
            keyPress = cv2.waitKey(0)
            # print(keyPress)
            if ord('d') == keyPress:
                print("Delete: ", self.originData)
                return 'd#' + self.originData
            elif 81 == keyPress:
                return "back"
            else:
                return 'a#' + self.originData
        else:
            return ""

def loadFromTxt(fText: str, fDst) -> str:
    dotLoc = fText.rfind('.')
    if -1 != dotLoc and "txt" == fText[dotLoc + 1:]:
        with open(fText, 'r') as fr:
            lines = fr.readlines()
        
        loader = infoLoader()
        checkData = set()
        lineNum = 0
        while lineNum < len(lines):
            line = lines[lineNum]
            """45 = label + width + height + 2 * (21 keyPoints)"""
            if loader.list2info(line, 45):
                tmp = loader.drawKeyPoints(lineNum)
                if "back" == tmp:
                    lineNum -= 1
                    lineNum = 0 if lineNum < 0 else lineNum
                elif "" == tmp:
                    lineNum += 1
                else:
                    sp = tmp.split('#')
                    if 2 == len(sp):
                        if 'a' == sp[0]:
                            checkData.add(sp[1])
                        elif 'd' == sp[0]:
                            checkData.discard(sp[1])
                        else:
                            pass
                    lineNum += 1
            else:
                print("invalid: ", tmp)
                lineNum += 1
            # print(len(checkData))

        slashLoc = fText.rfind(os.sep)
        newFile = fDst + "valid_" + fText[slashLoc + 1:]
        with open(newFile, 'w') as fw:
            tmp = "".join(checkData)
            fw.writelines(tmp)
        return "OK: " + fText
    else:
        return "NOT \".txt\": " + fText


if "__main__" == __name__:
    globalT0 = globalStart()
### Parameters region
    src = "/home/devin/Downloads/tmp/"
    dst = "/home/devin/Downloads/tmpNew/"
    blacklist = [""]
### Job region
    print("Do something~")
    makeAbsDirs(dst)
    objList = traversFilesInDir(src)
    for i in objList:
        rtv = loadFromTxt(i, dst)
        print(rtv)
    globalEnd(globalT0)
