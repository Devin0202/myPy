# -*- coding: utf-8 -*-
"""
Extract intersection label
"""
import os
import sys
import time
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

srcFile1 = "/home/devin/Desktop/test_set2-recall/20-1.00-Recall.txt"
srcFile2 = "/home/devin/myData/test_set2/test_set2.txt"
dstFile = "/home/devin/myData/20-1.00-Recall-test_set2.txt"

infoSrc1 = []
infoSrc2 = []
infoDst = []
with open(srcFile1, 'r') as fr:
    infoSrc1 = fr.readlines()
del infoSrc1[0]
del infoSrc1[0]
print len(infoSrc1)
infoSrc1 = set(infoSrc1)
print len(infoSrc1)

with open(srcFile2, 'r') as fr:
    infoSrc2 = fr.readlines()

for item in infoSrc2:
    if item.split()[0] + '\n' in infoSrc1:
        infoDst.append(item)
    else:
        continue

with open(dstFile, 'w') as fw:
    fw.writelines(infoDst)