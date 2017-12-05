# -*- coding: utf-8 -*-
import os
import time
import random
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

srcRoot = "/media/devin/Elements/headRestoreDeAnti/20170912/"
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if 0 == name.find("new_dataLabel.txt"):
                with open(os.path.join(rt, name), 'r') as f:
                    oriList = f.readlines()

                newFile = os.path.join(rt, "dataLabel.txt")
                print "WRITE: " + newFile
                with open(newFile, 'w') as f:
                    for line in oriList:
                        elementsF = line.split()
                        if len(elementsF) > 0 and os.path.exists(os.path.join(rt, elementsF[0])):
                            newEle = [elementsF[0], str(int(elementsF[6]) + 1), elementsF[2], \
                                        elementsF[3], elementsF[4], elementsF[5]]
                            singleLine = ""
                            for tmpElement in newEle:
                                singleLine += str(tmpElement) + ' '
                            # print singleLine
                            f.write(singleLine + "\r\n")
else:
    print("No Source!!!")

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())