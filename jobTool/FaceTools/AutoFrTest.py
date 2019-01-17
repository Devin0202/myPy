# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Batch running for Face Recognization test
"""
import os
import sys
import time
import subprocess

print(sys.version)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
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
            print("Wait app start: " + status)
            time.sleep(10)
        else:
            print("App start: " + output)
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

    if True:
        cmd = "adb" + iAdbDevices + "push " + pushThing + " " + dataDst + "/" \
                + dstSuffix
        print("PushOne: " + cmd)
    else:
        cmd = "adb" + iAdbDevices + " shell cp -r " + "/sdcard/TestFull/" \
                + pushThing.split("/")[-1] + " " + dataDst
        print("CopyOne: " + cmd)

    (status, output) = subprocess.getstatusoutput(cmd)
    time.sleep(30)
    return

def postJob(logLocal, logRemote, iAdbDevices):
    if not os.path.exists(logLocal):
        os.makedirs(logLocal)

    cmd = "adb" + iAdbDevices + "pull " + logRemote + " " + logLocal
    (status, output) = subprocess.getstatusoutput(cmd)
    print(str(output))

    if -1 != output.find("0 files pulled."):
        return False
    else:
        return True

### Params region
cAdbDevices = " -s 2255a361 "
dataFolder = "/media/devin/OpenImage600/face3/"
objs = ["sunhaiyan", "xinglj", "baoyuandong"]
objs = ["yanchangjian"]

cDataDst = "/sdcard/TestData"
cLogDst = "/sdcard/TestLog"
cAppID = "com.megvii.test"
cAppObj = "com.megvii.test/com.facepp.demo.LoadingActivity"
cLocalResults = "/home/devin/Desktop/tmp/"

folderDoneList = \
[]

### Job region
for obj in objs:
    dataSet = dataFolder + obj + "/cameraData"
    for rt, dirs, files in os.walk(dataSet):
        for name in dirs:
            if name in folderDoneList:
                continue

            pushOne = os.path.join(rt, name)
            preJob(pushOne, name, cDataDst, cLogDst, cAdbDevices)

            if True:
                rtv = False
                while (not rtv):
                    print("App start~")
                    startJob(cAdbDevices, cAppObj, cAppID)
                    while (1):
                        cmd = "adb" + cAdbDevices + "shell ps|grep -E \"" \
                        + cAppID + "\""
                        (status, output) = subprocess.getstatusoutput(cmd)
                        # print(status)
                        # print(output)
                        if "" == output:
                            print("App finished~")
                            break
                        else:
                            print("App running: " + output)
                            cmd = "adb" + cAdbDevices \
                                + "shell input keyevent 224"
                            (status, output) = subprocess.getstatusoutput(cmd)
                            time.sleep(15)
                    rtv = postJob(cLocalResults + obj, cLogDst, cAdbDevices)
            else:
                for suffix in ["first/", "second/", "third/"]:
                    cLocalOriResults = cLocalResults
                    cLocalOriResults += suffix
                    if not os.path.exists(cLocalOriResults):
                        os.makedirs(cLocalOriResults)

                    preJobEx(pushOne, name, cDataDst, cLogDst, cAdbDevices)

                    rtv = False
                    while (not rtv):
                        print(suffix + ": App start~")
                        startJob(cAdbDevices, cAppObj, cAppID)
                        while (1):
                            cmd = "adb" + cAdbDevices + "shell ps|grep -E \"" \
                                    + cAppID + "\""
                            (status, output) = subprocess.getstatusoutput(cmd)
                            # print(status)
                            # print(output)
                            if "" == output:
                                print("App finished~")
                                break
                            else:
                                print("App running: " + output)
                                cmd = "adb" + cAdbDevices \
                                    + "shell input keyevent 224"
                                (status, output) = subprocess.getstatusoutput(cmd)
                                time.sleep(30)
                        rtv = postJob(cLocalOriResults + obj, cLogDst, cAdbDevices)

            folderDoneList.append(name)
            print("Folders Done~")
            for it in folderDoneList:
                print("\"" + it + "\",", end = ' ')
            print()
            print(time.strftime('%H:%M:%S', time.localtime()))
            print(obj + " " + str(len(folderDoneList)) + ": " + name + " done~")
    folderDoneList = []

print(os.linesep)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
