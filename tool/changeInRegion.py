import os
import time
import random
import shutil
import cv2
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

srcRoot = "/media/devin/Elements/head/20170824/"
targetFile = "dataLabel.txt"
ration = 1.6
pre = time.strftime('%d%H%M', time.localtime())

if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if name == targetFile:
                with open(os.path.join(rt, name), 'r') as f:
                    oriList = f.readlines()
                newName = "bak" + pre + name
                os.rename(os.path.join(rt, name), os.path.join(rt, newName))

                print os.path.join(rt, name)
                with open(os.path.join(rt, name), 'w') as f:
                    for line in oriList:
                        elements = line.split()
                        if len(elements) > 1 and os.path.exists(os.path.join(rt, elements[0])):
                            img = cv2.imread(os.path.join(rt, elements[0]), cv2.IMREAD_COLOR)
                            if img is None:
                                continue
                            col = img.shape[1] - 1
                            row = img.shape[0] - 1

                            tmp1 = int(elements[4])
                            tmp2 = int(elements[5])
                            elements[4] = str(int(int(elements[4]) * ration))
                            elements[5] = str(int(int(elements[4]) / 0.75))
                            elements[2] = str(int(elements[2]) \
                                    - int((int(elements[4]) - tmp1) * 0.5))
                            elements[3] = str(int(elements[3]) \
                                    - int(int(elements[5]) * 0.08))

                            if int(elements[2]) < 0 or int(elements[3]) < 0:
                                continue
                            if int(elements[2]) + int(elements[4]) > col:
                                continue
                            if int(elements[3]) + int(elements[5]) > row:
                                continue

                            singleLine = ""
                            for tmpElement in elements:
                                singleLine += str(tmpElement) + ' '
                            # print singleLine
                            f.write(singleLine + "\r\n")
            else:
                continue
else:
    print "No source!!!"

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())