import sys
import os
import time
import random
import shutil

srcFolder = "/media/devin/wy/20171108HeadandPalm/"
targetL1 = "dataLabel.txt"
targetL2 = "dataLabelHead.txt"
dstL = "dataLabelHP.txt"
fileL1 = []
fileL2 = []
absoluteRoute1 = []
absoluteRoute2 = []
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

cnt = 0
if os.path.exists(srcFolder):
    for rt, dirs, files in os.walk(srcFolder):
        for name in files:
            if -1 != name.find(targetL1):
                absoluteRoute1 = os.path.join(rt, name)
                absoluteRoute2 = absoluteRoute1.replace(targetL1, targetL2)
                dstFolder = absoluteRoute1.replace(targetL1, '')
                print dstFolder
                # print absoluteRoute1
                if os.path.exists(absoluteRoute2):
                    cnt += 1
                    # print absoluteRoute2
                    with open(absoluteRoute1, 'r') as f:
                        fileL1 = f.readlines()
                    with open(absoluteRoute2, 'r') as f:
                        fileL2 = f.readlines()
                    if 0 >= len(fileL1) or 0 >= len(fileL2):
                        print "Missing labels!!!"
                        continue

                    with open(dstFolder + dstL, 'w') as f:
                        for singleLine1 in fileL1:
                            elements1 = singleLine1.split()
                            if not os.path.exists(os.path.join(rt, elements1[0])):
                                # print "Not exist: " + os.path.join(rt, elements1[0])
                                continue
                            # print singleLine1
                            shortDistance = sys.float_info.max
                            matchElements = []
                            for singleLine2 in fileL2:
                                if 0 == singleLine2.find(elements1[0]):
                                    elements2 = singleLine2.split()
                                    # print singleLine2                                
                                    tmp = (float(elements2[2]) - float(elements1[2]) + 0.5 * (float(elements2[4]) - float(elements1[4]))) ** 2 \
                                            + (float(elements2[3]) - float(elements1[3]) + 0.5 * (float(elements2[5]) - float(elements1[5]))) ** 2
                                    if tmp < shortDistance:
                                        shortDistance = tmp
                                        matchElements = [elements2[2], elements2[3], elements2[4], elements2[5]]

                            if 0 < len(matchElements):
                                saveElements = [elements1[2], elements1[3], elements1[4], elements1[5]]
                                saveElements[0] = saveElements[0] if int(saveElements[0]) < int(matchElements[0]) else matchElements[0]
                                saveElements[1] = saveElements[1] if int(saveElements[1]) < int(matchElements[1]) else matchElements[1]
                                tmp = int(elements1[2]) + int(elements1[4]) if int(elements1[2]) + int(elements1[4]) > int(matchElements[0]) + int(matchElements[2]) \
                                        else int(matchElements[0]) + int(matchElements[2])
                                saveElements[2] = str(tmp - int(saveElements[0]) + 1)
                                tmp = int(elements1[3]) + int(elements1[5]) if int(elements1[3]) + int(elements1[5]) > int(matchElements[1]) + int(matchElements[3]) \
                                        else int(matchElements[1]) + int(matchElements[3])
                                saveElements[3] = str(tmp - int(saveElements[1]) + 1)
                                # print saveElements
                                tmp = elements1[0] + ' ' + elements1[1] + ' ' + saveElements[0] + ' ' + saveElements[1] + ' ' + saveElements[2] \
                                        + ' ' + saveElements[3] + "\r\n"
                                f.write(tmp)

                # if random.uniform(0, 1) <= downSample:
                #     shutil.copyfile(absoluteRoute, dstRoot + str(index) + '_' + name)
                #     index += 1
else:
    print("No Source!!!")

print "Total label pair: " + str(cnt)
# print "Total copies: " + str(index)
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
