# -*- coding: utf-8 -*-
"""
Extract front face label
"""
import os
import sys
import time
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

srcFile = "/home/devin/Downloads/test_set2.txt"
dstFile = "/home/devin/Desktop/test_set2.txt"

infoSrc = []
infoDst = []
with open(srcFile, 'r') as fr:
    infoSrc = fr.readlines()

for item in infoSrc:
    if 7 == len(item.split()) and '0' == item.split()[-1]:
        infoDst.append(item)
    else:
        continue

with open(dstFile, 'w') as fw:
    fw.writelines(infoDst)