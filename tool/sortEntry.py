# -*- coding: utf-8 -*-
"""
If there are several objects-labeled in one image.
The label entries should be clustered with the images'name.
"""
import os
import sys
import time
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

srcRoot = "/home/devin/Desktop/tmpEx/"
dstRoot = "/home/devin/Desktop/tmpExLabel/"

def isIntContinue(sortList):
    start = int(sortList[0].split()[0].split('.')[0])
    end = int(sortList[-1].split()[0].split('.')[0])
    index = start
    for line in sortList:
        tmpIndex = int(line.split()[0].split('.')[0])
        if index == tmpIndex or index + 1 == tmpIndex:
            index = tmpIndex
        else:
            print "First mismatching: " + str(index) + ' ' + str(tmpIndex)
            return "Discontinuous! Range:" + str(start) + '~' + str(end)
    return "Continuous! Range:" + str(start) + '~' + str(end)

if not os.path.exists(dstRoot):
    os.makedirs(dstRoot)
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if name.split('.')[-1] in ["txt"]:
                print "READ: " + os.path.join(rt, name)
                with open(os.path.join(rt, name), 'r') as f:
                    oriList = f.readlines()

                legalList = oriList[:]
                for line in oriList:
                    if 1 >= len(line.split()):
                        legalList.remove(line)
                    elif 1 >= len(line.split()[0].split('.')):
                        legalList.remove(line)
                    else:
                        continue
                sortList = sorted(legalList, \
                    key = lambda entry: int(entry.split()[0].split('.')[0]))
                if 0 < len(sortList):
                    print isIntContinue(sortList)
                else:
                    print "This file is illegal!"
                    continue

                dst = os.path.join(rt, name)
                dst = dst.replace(srcRoot, dstRoot)
                dstFolder = os.path.split(dst)[0]
                if not os.path.exists(dstFolder):
                    os.makedirs(dstFolder)
                print "WRITE: " + dst
                with open(dst, 'w') as fw:
                    fw.writelines(sortList)
            else:
                continue
else:
    print "No source!!!"
    sys.exit(0)

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())