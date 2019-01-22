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
    status = 1
    while (0 != status):
        cmd = "adb" + iAdbDevices + "shell input keyevent 224"
        (status, output) = myGetstatusoutput(cmd)
        logWriter.printLog("startJob-Invoke cmd status: " + str(status))
        time.sleep(5)

    status = 1
    while (0 != status):
        cmd = "adb" + iAdbDevices + "shell am start -n " + appObj \
                + " -e mode TestCase"
        (status, output) = myGetstatusoutput(cmd)
        logWriter.printLog("App start cmd status: " + str(status))
        time.sleep(5)

    while (1):
        status = 1
        while (0 != status):
            cmd = "adb" + iAdbDevices + "shell ps|findstr  \"" + iAppID + "\""
            (status, output) = myGetstatusoutput(cmd)
            logWriter.printLog("startJob-ps|findstr cmd status: " + str(status))
            time.sleep(5)
        if "" == output:
            logWriter.printLog("Wait app start: " + str(status))
            time.sleep(10)
        else:
            logWriter.printLog("App start: " + str(output))
            break
    return

def preJobEx(pushThing, dstSuffix, dataDst, logDst, iAdbDevices):
    cmd = "adb" + iAdbDevices + "shell rm -rf " + logDst + "/*"
    (status, output) = myGetstatusoutput(cmd)
    return

def preJob(pushThing, dstSuffix, dataDst, logDst, iAdbDevices):
    status = 1
    while (0 != status):
        cmd = "adb" + iAdbDevices + "shell rm -rf " + logDst + "/*"
        (status, output) = myGetstatusoutput(cmd)
        logWriter.printLog("rm logDst cmd status: " + str(status))
        time.sleep(5)

    status = 1
    while (0 != status):
        cmd = "adb" + iAdbDevices + "shell rm -rf " + dataDst + "/*"
        (status, output) = myGetstatusoutput(cmd)
        logWriter.printLog("rm dataDst cmd status: " + str(status))
        time.sleep(5)

    if False:
        cmd = "adb" + iAdbDevices + "push " + pushThing + " " + dataDst + "/" \
                + dstSuffix
        logWriter.printLog("PushOne: " + cmd)
    else:
        cmd = "adb" + iAdbDevices + " shell cp -r " + pushThing + " " + dataDst
        logWriter.printLog("CopyOne: " + cmd)

    status = 1
    while (0 != status):
        (status, output) = myGetstatusoutput(cmd)
        logWriter.printLog("Prepare data cmd status: " + str(status))
        time.sleep(10)
    return

def postJob(logLocal, logRemote, iAdbDevices):
    if not os.path.exists(logLocal):
        os.makedirs(logLocal)

    status = 1
    while (0 != status):
        cmd = "adb" + iAdbDevices + "pull " + logRemote + " " + logLocal
        (status, output) = myGetstatusoutput(cmd)
        logWriter.printLog("pull log cmd status: " + str(status))
        time.sleep(5)
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

def myGetstatusoutput(cmd, timeOut = 90):
    STDOUT = -2
    try:
        data = subprocess.check_output(cmd, timeout=timeOut, shell=True, text=True, stderr=STDOUT)
        exitcode = 0
    except subprocess.CalledProcessError as ex:
        data = ex.output
        exitcode = ex.returncode
    except subprocess.TimeoutExpired as te:
        data = "myGetstatusoutput exception: " + ' ' + str(te.timeout) + "s " + str(te.stderr)
        exitcode = -1
        logWriter.printLog(data)
    if data[-1:] == '\n':
        data = data[:-1]
    return exitcode, data
			
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
    (status, output) = myGetstatusoutput(cmd)
    logWriter.printLog(obj)
    dirs = []
    lines = output.split("\n")
    for i in lines:
        dirs.append(i)

    logWriter.printLog(dirs)
    for name in dirs:
        if name in folderDoneList:
            continue

        timeoutLimit = 0
        pushOne = dataSet + '/' + name
        preJob(pushOne, name, cDataDst, cLogDst, cAdbDevices)

        rtv = False
        while (not rtv):
            localCnt = 0
            logWriter.printLog("App start~")
            startJob(cAdbDevices, cAppObj, cAppID)
            while (1):
                cmd = "adb" + cAdbDevices + "shell ps|findstr  \"" \
                    + cAppID + "\""
                (status, output) = myGetstatusoutput(cmd)
                logWriter.printLog("Running-ps|findstr cmd status: " + str(status))

                if "" == output:
                    logWriter.printLog("App finished~")
                    localCnt = 0
                    timeoutLimit = 0
                    break
                else:
                    localCnt += 1
                    logWriter.printLog("App running: " + str(output))
                    status = 1
                    while (0 != status):
                        cmd = "adb" + cAdbDevices \
                            + "shell input keyevent 224"
                        (status, output) = myGetstatusoutput(cmd)
                        logWriter.printLog("Running-Invoke cmd status: " + str(status))
                        time.sleep(2)
                    time.sleep(10)

                    if (30 < localCnt):
                        logWriter.printLog("App timeout: " + name)
                        timeoutLimit += 1
                        break;
                    else:
                        pass

            status = 1
            while (0 != status):
                cmd = "adb" + cAdbDevices + "shell am force-stop \"" \
                + cAppID + "\""
                (status, output) = myGetstatusoutput(cmd)
                logWriter.printLog("force-stop cmd status: " + str(status))
                time.sleep(3)
            status = 1
            while (0 != status):
                cmd = "adb" + cAdbDevices + "shell am kill \"" \
                + cAppID + "\""
                (status, output) = myGetstatusoutput(cmd)
                logWriter.printLog("kill cmd status: " + str(status))
                time.sleep(3)
            if (0 == timeoutLimit):
                rtv = postJob(cLocalResults + obj, cLogDst, cAdbDevices)
            else:
                if (0 != timeoutLimit):
                    rtv = False
                    logWriter.printLog("Try again: " + obj + ' ' + name)
                else:
                    rtv = True
                    logWriter.printLog("Skip!!!: " + obj + ' ' + name)

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