# -*- coding: utf-8 -*-
"""
If there are several objects-labeled in one image.
The label entries should be clustered with the images'name.
"""
import os
import sys
import time
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

srcRoot = "/home/devin/Desktop/mnt/20171112_256144Labels/"
dstRoot = "/home/devin/Desktop/mnt/20171112_256144LabelsSort/"
if not os.path.exists(dstRoot):
    os.makedirs(dstRoot)
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if -1 != name.find(".txt"):
                print "READ: " + os.path.join(rt, name)
                with open(os.path.join(rt, name), 'r') as f:
                    oriList = f.readlines()
                sortList = []
                for line in oriList:
                    elements = line.split()
                    if len(elements) > 1:
                        sortList.append(elements[0])
                    else:
                        continue
                sortListDone = sorted(set(sortList), key = sortList.index)
                print "WRITE: " + dstRoot + name
                with open(dstRoot + name, 'w') as f:
                    for id in sortListDone:
                        for line in oriList:
                            if 0 == line.find(id):
                                f.write(line)
                            else:
                                continue
            else:
                continue
else:
    print "No source!!!"
    sys.exit(0)

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())