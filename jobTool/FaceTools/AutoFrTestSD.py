# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Batch running for Face Recognization test
"""
import os
import sys
import time
import subprocess

### Defs region
def startJob(iAdbDevices, appObj, iAppID):
    cmd = "adb" + iAdbDevices + "shell input keyevent 224"
    (status, output) = subprocess.getstatusoutput(cmd)
    time.sleep(5)

    cmd = "adb" + iAdbDevices + "shell am start -n " + appObj \
            + " -e mode TestCase"
    (status, output) = subprocess.getstatusoutput(cmd)
    
    while (1):
        cmd = "adb" + iAdbDevices + "shell ps|grep -E \"" + iAppID + "\""
        (status, output) = subprocess.getstatusoutput(cmd)
        if "" == output:
            logWriter.printLog("Wait app start: " + status)
            time.sleep(10)
        else:
            logWriter.printLog("App start: " + output)
            break
    return

def preJobEx(pushThing, dstSuffix, dataDst, logDst, iAdbDevices):
    cmd = "adb" + iAdbDevices + "shell rm -rf " + logDst + "/*"
    (status, output) = subprocess.getstatusoutput(cmd)
    return

def preJob(pushThing, dstSuffix, dataDst, logDst, iAdbDevices):
    cmd = "adb" + iAdbDevices + "shell rm -rf " + logDst + "/*"
    (status, output) = subprocess.getstatusoutput(cmd)

    cmd = "adb" + iAdbDevices + "shell rm -rf " + dataDst + "/*"
    (status, output) = subprocess.getstatusoutput(cmd)

    if False:
        cmd = "adb" + iAdbDevices + "push " + pushThing + " " + dataDst + "/" \
                + dstSuffix
        logWriter.printLog("PushOne: " + cmd)
    else:
        cmd = "adb" + iAdbDevices + " shell cp -r " + pushThing + " " + dataDst
        logWriter.printLog("CopyOne: " + cmd)

    (status, output) = subprocess.getstatusoutput(cmd)
    time.sleep(10)
    return

def postJob(logLocal, logRemote, iAdbDevices):
    if not os.path.exists(logLocal):
        os.makedirs(logLocal)

    cmd = "adb" + iAdbDevices + "pull " + logRemote + " " + logLocal
    (status, output) = subprocess.getstatusoutput(cmd)
    logWriter.printLog(str(output))

    if -1 != output.find("0 files pulled."):
        return False
    else:
        return True

class EasyLog:
    def __init__(self, fDstFolder):
        if os.path.exists(fDstFolder):
            self.mDetFile = fDstFolder + '/' + "log.txt"
            if os.path.exists(self.mDetFile):
                print("There has old log, please check and remove it!!!")
                self.isWriteFile = False
                sys.exit(0)
            else:
                self.isWriteFile = True
        else:
            self.isWriteFile = False

    def printLog(self, fStr = ""):
        print(fStr)
        if (self.isWriteFile):
            with open(self.mDetFile, 'a') as fw:
                print(fStr, file = fw)
        else:
            pass

### Params region
cAdbDevices = " -s 92d426e9 "
dataFolder = "/storage/C03C-16FC/FaceCases/"
objs = ["baoyuandong", "daiyi", "peiyi", "sunhaiyan", "xinglj", "zhuyawen"]

cDataDst = "/sdcard/TestData"
cLogDst = "/sdcard/TestLog"
cAppID = "com.megvii.test"
cAppObj = "com.megvii.test/com.facepp.demo.LoadingActivity"
cLocalResults = "/home/devin/Desktop/tmp/"
recordLogFolder = "/home/devin/Desktop/tmp/"
logWriter = EasyLog(recordLogFolder)

folderDoneList = \
[]

### Job region
logWriter.printLog(sys.version)
logWriter.printLog(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
for obj in objs:
    dataSet = dataFolder + obj + "/cameraData"
    cmd = "adb" + cAdbDevices + "shell ls " + dataSet
    (status, output) = subprocess.getstatusoutput(cmd)
    logWriter.printLog(obj)
    dirs = []
    lines = output.split("\n")
    for i in lines:
        tmp = i.split(" ")
        for j in tmp[: -1]:
            dirs.append(j)

    logWriter.printLog(dirs)
    for name in dirs:
        if name in folderDoneList:
            continue

        pushOne = dataSet + '/' + name
        preJob(pushOne, name, cDataDst, cLogDst, cAdbDevices)

        rtv = False
        while (not rtv):
            logWriter.printLog("App start~")
            startJob(cAdbDevices, cAppObj, cAppID)
            while (1):
                cmd = "adb" + cAdbDevices + "shell ps|grep -E \"" \
                + cAppID + "\""
                (status, output) = subprocess.getstatusoutput(cmd)
                # logWriter.printLog(status)
                # logWriter.printLog(output)
                if "" == output:
                    logWriter.printLog("App finished~")
                    break
                else:
                    logWriter.printLog("App running: " + output)
                    cmd = "adb" + cAdbDevices \
                        + "shell input keyevent 224"
                    (status, output) = subprocess.getstatusoutput(cmd)
                    time.sleep(20)
            rtv = postJob(cLocalResults + obj, cLogDst, cAdbDevices)

        folderDoneList.append(name)
        logWriter.printLog(time.strftime('%H:%M:%S', time.localtime()))
        logWriter.printLog(obj + " " + str(len(folderDoneList)) + ": " + name + " done~")
        logWriter.printLog("Folders Done:")
        tmpS = ""
        for it in folderDoneList:
            tmpS += "\"" + it + "\"," + ' '
        logWriter.printLog(tmpS)
        logWriter.printLog()
    folderDoneList = []

logWriter.printLog(os.linesep)
logWriter.printLog(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))