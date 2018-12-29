import os
import time
import random
import shutil
import cv2
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

srcRoot = "/media/devin/Elements/716/Device/20181117/tar/"
nameList = []
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            nameList.append(name)
else:
    print("No source!!!")

nameList.sort()
idx = 0
for line in nameList:
    # newName = line.replace(line.split(".jpg")[0], str(idx))
    newName = line.replace(line.split(".bmp")[0], str(idx).zfill(4))
    os.rename(srcRoot + line, srcRoot +  newName)
    idx += 1
    print(srcRoot + newName)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))