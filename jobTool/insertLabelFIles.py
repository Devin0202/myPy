# -*- coding: utf-8 -*-
"""
Insert Label files by matching with files' name and node folders' name.
"""
import os
import sys
import time
import shutil
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

srcRoot = "/media/devin/TOSHIBA/1920Resize/3rdLabel/"
folderRoot = "/media/devin/TOSHIBA/1920Resize/Home/"
listFolder = []

if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(folderRoot):
        for folder in dirs:
            listFolder.append(os.path.join(rt, folder))
else:
    print("No Source!!!")
    sys.exit(0)
# print listFolder
print len(listFolder)

cnt = 0
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if name.split('.')[-1] in ["txt"]:
                target = name.split('.')[-2]
                tmp = cnt
                for line in listFolder:
                    if target == line.split('/')[-1]:
                        cnt += 1
                        ori = os.path.join(rt, name)
                        dst = os.path.join(line, name)
                        shutil.copyfile(ori, dst)
                        break
                    else:
                        continue
                if tmp == cnt:
                    print name
                else:
                    continue
            else:
                continue
else:
    print("No Source!!!")
    sys.exit(0)
print cnt

print os.linesep
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())