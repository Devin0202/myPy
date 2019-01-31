# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Batch running for Face Recognization test
PS:         Please change the codes in subprocess.py
            In "def run(...)":
            stdout, stderr = process.communicate()
            -> stdout, stderr = process.communicate(timeout = timeout)
"""
import os
import sys
import time
import subprocess

### Defs region
def startJob(iAdbDevices, appObj, iAppID):
    cmd = "adb" + iAdbDevices + "shell input keyevent 224"
    safeExecute(cmd, "startJob-Invoke cmd status: ", 5)

    cmd = "adb" + iAdbDevices + "shell am start -n " + appObj \
                + " -e mode TestCase"
    safeExecute(cmd, "App start cmd status: ", 5)

    while (1):
        cmd = "adb" + iAdbDevices + "shell pgrep \"" + iAppID + "\""
        output = safeExecute(cmd, "startJob-pgrep cmd status: ", 5)
        if "" == output:
            logWriter.printLog("Wait app start: " + str(status))
            time.sleep(10)
        else:
            logWriter.printLog("App start: " + str(output))
            break
    return

def preJob(pushThing, dstSuffix, dataDst, logDst, iAdbDevices):
    cmd = "adb" + iAdbDevices + "shell rm -rf " + logDst + "/*"
    safeExecute(cmd, "rm logDst cmd status: ", 5)

    cmd = "adb" + iAdbDevices + "shell rm -rf " + dataDst + "/*"
    safeExecute(cmd, "rm dataDst cmd status: ", 5)

    if (isSDmode):
        cmd = "adb" + iAdbDevices + " shell cp -r " + pushThing + " " + dataDst
        logWriter.printLog("CopyOne: " + cmd)
        safeExecute(cmd, "Prepare data cmd status: ", 10)
    else:
        cmd = "adb" + iAdbDevices + "push " + pushThing + " " + dataDst + "/" \
                + dstSuffix
        logWriter.printLog("PushOne: " + cmd)
        safeExecute(cmd, "Prepare data cmd status: ", 10, 500)
    return

def postJob(logLocal, logRemote, iAdbDevices):
    if not os.path.exists(logLocal):
        os.makedirs(logLocal)

    cmd = "adb" + iAdbDevices + "pull " + logRemote + " " + logLocal
    output = safeExecute(cmd, "Prepare data cmd status: ", 5)
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
        if (isDos):
            data = subprocess.check_output(cmd, timeout = timeOut, shell = True, \
                text = True, stderr = STDOUT)
        else:
            data = subprocess.check_output(cmd, timeout = timeOut, shell = True, \
                universal_newlines = True)
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

def safeExecute(fCmd, fCmdInfo, fWaitTime, fCmdTimeOut = 90):
    status = 1
    while (0 != status):
        cmd = fCmd
        (status, output) = myGetstatusoutput(cmd, fCmdTimeOut)
        logWriter.printLog(fCmdInfo + str(status))
        time.sleep(fWaitTime)
    return output

### Params region
cAdbDevices = " -s 92d426e9 "
dataFolder = "/storage/C03C-16FC/FaceCases/"
objs = ["baoyuandong", "daiyi", "peiyi", "sunhaiyan", "xinglj", "zhuyawen"]
cDataDst = "/sdcard/TestData"
cLogDst = "/sdcard/TestLog"
cAppID = "com.megvii.test"
cAppObj = "com.megvii.test/com.facepp.demo.LoadingActivity"
cLocalResults = "/home/devin/Downloads/tmp/"
recordLogFolder = "/home/devin/Downloads/tmp"
isDos = False
isSDmode = False

folderDoneList = \
[]
logWriter = EasyLog(recordLogFolder)
### Job region
logWriter.printLog(sys.version)
logWriter.printLog(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
for obj in objs:
    dirs = []
    logWriter.printLog(obj)
    dataSet = dataFolder + obj + "/cameraData"
    if (isSDmode):
        cmd = "adb" + cAdbDevices + "shell ls " + dataSet
        (status, output) = myGetstatusoutput(cmd)

        lines = output.split("\n")
        for i in lines:
            if (isDos):
                dirs.append(i)
            else:
                tmp = i.split(" ")
                for j in tmp[: -1]:
                    dirs.append(j)
    else:
        for rt, folders, files in os.walk(dataSet):
            for i in folders:
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
                cmd = "adb" + cAdbDevices + "shell pgrep \"" \
                    + cAppID + "\""
                (status, output) = myGetstatusoutput(cmd)
                logWriter.printLog("Running-pgrep cmd status: " + str(status))

                if "" == output:
                    logWriter.printLog("App finished~")
                    localCnt = 0
                    timeoutLimit = 0
                    break
                else:
                    avgFreq = 0;
                    localCnt += 1
                    logWriter.printLog("App running: " + str(output))
                    cmd = "adb" + cAdbDevices + "shell input keyevent 224"
                    safeExecute(cmd, "Running-Invoke cmd status: ", 2)

                    prefix = "/sys/devices/system/cpu/"
                    suffix = "/cpufreq/cpuinfo_cur_freq"
                    cmd = "adb" + cAdbDevices + "shell cat " + prefix + "cpu0" \
                            + suffix
                    output = safeExecute(cmd, "get__cur_freq0: ", 2)
                    avgFreq += int(output)
                    cmd = "adb" + cAdbDevices + "shell cat " + prefix + "cpu1" \
                            + suffix
                    output = safeExecute(cmd, "get__cur_freq1: ", 2)
                    avgFreq += int(output)
                    cmd = "adb" + cAdbDevices + "shell cat " + prefix + "cpu2" \
                            + suffix
                    output = safeExecute(cmd, "get__cur_freq2: ", 2)
                    avgFreq += int(output)
                    cmd = "adb" + cAdbDevices + "shell cat " + prefix + "cpu3" \
                            + suffix
                    output = safeExecute(cmd, "get__cur_freq3: ", 2)
                    avgFreq += int(output)

                    logWriter.printLog("cpuinfo_cur_freq: " + str(avgFreq / 4))
                    cmd = "adb" + cAdbDevices + "shell cat /sys/devices/system/cpu/online"
                    output = safeExecute(cmd, "get_cpu_online: ", 2)
                    logWriter.printLog("Cpu_online: " + str(output))
                    time.sleep(10)

                    if (90 < localCnt):
                        logWriter.printLog("App timeout: " + name)
                        timeoutLimit += 1
                        break;
                    else:
                        pass

            cmd = "adb" + cAdbDevices + "shell am force-stop \"" + cAppID + "\""
            safeExecute(cmd, "force-stop cmd status: ", 3)
            cmd = "adb" + cAdbDevices + "shell am kill \"" + cAppID + "\""
            safeExecute(cmd, "kill cmd status: ", 3)

            if (0 == timeoutLimit):
                rtv = postJob(cLocalResults + obj, cLogDst, cAdbDevices)
            else:
                if (1 == timeoutLimit):
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