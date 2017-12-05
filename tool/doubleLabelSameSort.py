import os
import time
import sys
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

srcRootMain = "/media/devin/Elements1/20171104/"
srcRootSlave = ""
targetFile = "dataLabelHead.txt"
targetFilePalm = "dataLabel.txt"
dstFile = "merge.txt"
listMain = []

if os.path.exists(srcRootMain):
    for rt, dirs, files in os.walk(srcRootMain):
        for name in files:
            if targetFile == name:
                listMain.append(os.path.join(rt, name))
            else:
                continue
else:
    print "No Main source!!!"
    sys.exit(0)

listSlave = []
if "" == targetFilePalm and "" != srcRootSlave:
    if os.path.exists(srcRootSlave):
        for rt, dirs, files in os.walk(srcRootSlave):
            for name in files:
                for sf in listMain:
                    if sf == os.path.join(rt, name).replace(srcRootSlave, \
                        srcRootMain):
                        listSlave.append(os.path.join(rt, name))
    else:
        print "No Slave source!!!"
        sys.exit(0)
else:
    for sf in listMain:
        file = sf.replace(targetFile, targetFilePalm)
        if os.path.exists(file):
            listSlave.append(file)
        else:
            print "Label files mismatch!!!"
            sys.exit(0)

if len(listSlave) == len(listMain):
    print "Match label files: " + str(len(listMain))
else:
    print "Label files mismatch!!!"
    sys.exit(0)
# print "READ: " + str(listMain)
# print "READ: " + str(listSlave)

for (x, y) in zip(listMain, listSlave):
    print "READ:"
    print x
    print y

    with open(x, 'r') as f:
        xListTmp = f.readlines()

    xList = []
    for single in xListTmp:
        single = single.replace(" 3 "," 0 ")
        xList.append(single)

    with open(y, 'r') as f:
        yList = f.readlines()

    wholeList = xList + yList
    wholeIndex = []
    for tmp in wholeList:
        sp = tmp.split()
        if 0 < len(sp):
            wholeIndex.append(sp[0])
    sortList = sorted(set(wholeIndex), key = wholeIndex.index)

    print "WRITE:"
    if "" == targetFilePalm and "" != srcRootSlave:
        newFile = y.replace(targetFile, dstFile)
    else:
        newFile = y.replace(targetFilePalm, dstFile)
    print newFile

    with open(newFile, 'w') as fw:
        for tmp in sortList:
            for line in wholeList:
                if 0 == line.find(tmp):
                    fw.write(line)
                else:
                    continue

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())