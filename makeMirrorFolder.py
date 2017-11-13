import os
import time
import random
import shutil

srcRoot = "/media/devin/Elements/Headface/"
dstRoot = "/home/devin/Desktop/headFaceNewLabel/"

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in dirs:
        	newFolder = os.path.join(rt, name)
        	newFolder = newFolder.replace(srcRoot, dstRoot)
        	print newFolder
        	if not os.path.exists(newFolder):
        		os.makedirs(newFolder)

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
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
