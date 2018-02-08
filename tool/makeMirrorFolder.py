# -*- coding: utf-8 -*-
"""
Copy same hierarchy from source folder to destination folder
"""
import os
import sys
import time
import random
import shutil
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

srcRoot = "/media/devin/Elements/image_datPng/20170904/"
dstRoot = "/home/devin/Desktop/20170904/"
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in dirs:
            newFolder = os.path.join(rt, name)
            newFolder = newFolder.replace(srcRoot, dstRoot)
            print newFolder
            if not os.path.exists(newFolder):
                os.makedirs(newFolder)
else:
    print "No resource!!!"
    sys.exit(0)
# Extend function
targetFile = "dataLabel.txt"
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if -1 != name.find(targetFile):
                old = os.path.join(rt, name)
                new = old.replace(srcRoot, dstRoot)
                print old
                print new
                shutil.copyfile(old, new)
else:
    print "No resource!!!"
    sys.exit(0)
# Extend function
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())