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

### Params region
folderDoneList = \
["0906152317", "0906112427", "0906112457", "0906112524", "0906112548", \
"0906112611", "0906112639", "0906112726", "0906112749", "0906112818", \
"0906112848", "0906152109", "0906152135", "0906152201", "0906152223", \
"0906152252", "0906152343", "0906152407", "0906152517", "0906152549", \
"0906152617", "0906152656", "0906152724", "0906152815", "0906152850", \
"0906152922", "0906152953", "0906153200", "0906153242", "0906153304"]

dataFolder = "/media/devin/OpenImage600/face3/"
# objs = ["daiyi", "sunhaiyan"]
objs = ["yanchangjian", "yukeke"]

for obj in objs:
    dataSet = dataFolder + obj + "/cameraData"
    for rt, dirs, files in os.walk(dataSet):
        cnt = 0
        for name in dirs:
            if name in folderDoneList:
                continue
            cnt += 1
            pushOne = os.path.join(rt, name)
            print("Push: " + pushOne)

            cmd = "adb shell rm -rf /sdcard/TestLog/*"
            (status, output) = subprocess.getstatusoutput(cmd)

            cmd = "adb shell rm -rf /sdcard/TestData/*"
            (status, output) = subprocess.getstatusoutput(cmd)


            cmd = "adb push " + pushOne + " /sdcard/TestData/" + name
            (status, output) = subprocess.getstatusoutput(cmd)

            cmd = "adb shell input keyevent 224"
            (status, output) = subprocess.getstatusoutput(cmd)
            time.sleep(5)

            cmd = "adb shell am start -n \
            com.megvii.test/com.facepp.demo.LoadingActivity"
            (status, output) = subprocess.getstatusoutput(cmd)
            time.sleep(25)
            while (1):
                cmd = "adb shell ps|grep -E \"com.megvii.test\""
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

            dst = "/home/devin/Desktop/TestResults/" + obj
            if not os.path.exists(dst):
                os.makedirs(dst)
            dataSet = "/sdcard/TestLog"
            cmd = "adb pull " + dataSet + " " + dst
            (status, output) = subprocess.getstatusoutput(cmd)

            folderDoneList.append(name)
            print("Folders Done~")
            for it in folderDoneList:
                print("\"" + it + "\",", end = ' ')

            print()
            print(time.strftime('%H:%M:%S', time.localtime()))
            print(obj + " " + str(len(folderDoneList)) + ": " + name \
                + " done~")
    folderDoneList = []

print(os.linesep)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))