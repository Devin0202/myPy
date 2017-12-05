import os
import sys
import time
import random
import shutil
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

srcRoot = "/media/devin/Elements/headRestoreEx/20170907/"
dstRoot = "/media/devin/Elements/headRestorePng/20170907/"
if not os.path.exists(dstRoot):
    os.makedirs(dstRoot)

imgList = []
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if -1 != name.find("dataLabel.txt"):
                with open(os.path.join(rt, name), 'r') as fr:
                    imgList = fr.readlines()

                tmpRoot = rt
                print "Src image route:"
                print tmpRoot
                for srt, sdirs, sfiles in os.walk(tmpRoot):
                    continue
                for line in imgList:
                    img = line.split('.')[0] + ".dat"
                    if img in sfiles:
                        src = os.path.join(srt, img)
                        dst = src.replace(srcRoot, dstRoot)
                        shutil.copyfile(src, dst)
else:
    print("No Source!!!")
    sys.exit(0)

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())