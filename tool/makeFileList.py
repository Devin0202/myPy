# -*- coding: utf-8 -*-
"""
Recording all same suffix files with absolute paths in one list(.txt)
"""
import os
import sys
import time
from sys import argv

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

fileList = "FileList.txt"
if 3 > len(argv):
    print("Please input srcRoot(abs route) and file sorts.")
    print("File sort such as: png, txt, jpg, etc.")
    sys.exit(0)
else:
    srcRoot = argv[1]
    fileSort = argv[2:]

if not os.path.exists(srcRoot):
    print("No Source!!!")
    sys.exit(0)
else:
    targetFile = sys.path[0] + os.path.sep + fileList
    print("WRITE:")
    print(targetFile)
    with open(targetFile, 'w') as fw:
        for rt, dirs, files in os.walk(srcRoot):
            for name in files:
                for i in fileSort:
                    sortLength = len(i)
                    if i == name[-sortLength:]:
                        # fw.write(os.path.join(rt, name) + ' ' + rt.split(os.path.sep)[-1])
                        fw.write(os.path.join(rt, name))
                        # fw.write(name)
                        fw.write(os.linesep)
                    else:
                        continue

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
