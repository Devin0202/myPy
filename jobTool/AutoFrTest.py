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
def preJob(pushThing, dstSuffix, dataDst, logDst, appObj):
    cmd = "adb shell rm -rf " + logDst + "/*"
    (status, output) = subprocess.getstatusoutput(cmd)

    cmd = "adb shell rm -rf " + dataDst + "/*"
    (status, output) = subprocess.getstatusoutput(cmd)

    cmd = "adb push " + pushThing + " " + dataDst + "/" + dstSuffix
    (status, output) = subprocess.getstatusoutput(cmd)

    cmd = "adb shell input keyevent 224"
    (status, output) = subprocess.getstatusoutput(cmd)
    time.sleep(5)

    cmd = "adb shell am start -n " + appObj
    (status, output) = subprocess.getstatusoutput(cmd)
    time.sleep(25)
    return

def postJob(logLocal, logRemote):
    if not os.path.exists(logLocal):
        os.makedirs(logLocal)

    cmd = "adb pull " + logRemote + " " + logLocal
    (status, output) = subprocess.getstatusoutput(cmd)
    return

### Params region
cLocalResults = "/home/devin/Desktop/TestResults/"
cDataDst = "/sdcard/TestData"
cLogDst = "/sdcard/TestLog"
cAppObj = "com.megvii.test/com.facepp.demo.LoadingActivity"
cAppID = "com.megvii.test"
dataFolder = "/media/devin/OpenImage600/faces/"
objs = ["yanchangjian", "guangming", "yukeke"]
objs = ["daiyi", "sunhaiyan", "xinglj"]

folderDoneList = \
["0830111934", "0830110842", "0830110943", "0830111019", "0830111052", \
"0830111206", "0830111231", "0830111321", "0830111348", "0830111417", \
"0830111449", "0830111513", "0830111539", "0830111606", "0830111630", \
"0830111653", "0830111718"]

### Job region
for obj in objs:
    dataSet = dataFolder + obj + "/cameraData"
    for rt, dirs, files in os.walk(dataSet):
        for name in dirs:
            if name in folderDoneList:
                continue

            pushOne = os.path.join(rt, name)
            print("Push: " + pushOne)
            preJob(pushOne, name, cDataDst, cLogDst, cAppObj)

            while (1):
                cmd = "adb shell ps|grep -E \"" + cAppID + "\""
                (status, output) = subprocess.getstatusoutput(cmd)
                # print(status)
                # print(output)
                if "" == output:
                    print("App finished~")
                    break
                else:
                    print("App running~")
                    cmd = "adb shell input keyevent 224"
                    (status, output) = subprocess.getstatusoutput(cmd)
                    time.sleep(30)

            postJob(cLocalResults + obj, cLogDst)
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