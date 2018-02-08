import os
import time
import sys
import struct
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

mapFile = "/home/devin/Desktop/mapXY.txt"
srcRoot = "/media/devin/Elements/dy/20170907Label/"
targetFile = "dataLabel.txt"
biasW = 150
biasH = 150
mapW = 1600
mapH = 900
limitW = 1280
limitH = 720

mapXY = []
with open(mapFile, 'rb') as fr:
    while True:
        tmp = fr.read(2)
        if '' != tmp:
            tmp = struct.unpack('h', tmp)
            mapXY.append(tmp[0])
        else:
            break
print "Table length: " + str(len(mapXY))
mapStride = len(mapXY) / 2

listMain = []
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if targetFile == name:
                listMain.append(os.path.join(rt, name))
            else:
                continue
else:
    print "No Main source!!!"
    sys.exit(0)
print "READ:"
for item in listMain:
    print item

for item in listMain:
    with open(item, 'r') as fr:
        infoList = fr.readlines()

    dstFile = os.path.split(item)[0] + os.path.sep + "new_" + targetFile
    print "WRITE:"
    print dstFile
    elb = 0
    ehb = 0
    lpe = 0
    with open(dstFile, 'w') as fw:
        for line in infoList:
            elements = line.split()
            if 0 < len(elements):
                srcImg = os.path.split(item)[0] + os.path.sep + elements[0]
                # print srcImg
                if not os.path.exists(srcImg):
                    ltX = int(elements[2])
                    ltY = int(elements[3])
                    rbX = int(elements[2]) + int(elements[4])
                    rbY = int(elements[3]) + int(elements[5])
                    # print ltX
                    # print ltY
                    # print rbX
                    # print rbY
                    new_ltX = mapXY[(biasH + ltY) * mapW + (biasW + ltX)];
                    new_ltY = mapXY[(biasH + ltY) * mapW + (biasW + ltX) \
                                    + mapStride];
                    new_rbX = mapXY[(biasH + rbY) * mapW + (biasW + rbX)];
                    new_rbY = mapXY[(biasH + rbY) * mapW + (biasW + rbX) \
                                    + mapStride];

                    if new_ltX < 0 or new_ltY < 0 or new_rbY < 0 \
                        or new_rbX < 0:
                        elb += 1
                        continue
                    if new_rbX >= limitW or new_rbY >=limitH:
                        ehb += 1
                        continue
                    if new_rbY < new_ltY or new_rbX < new_ltX:
                        lpe += 1
                        continue

                    elements[2] = str(new_ltX)
                    elements[3] = str(new_ltY)
                    elements[4] = str(new_rbX - new_ltX)
                    elements[5] = str(new_rbY - new_ltY)
                    elements[1] = '0'
                    output = elements[0] + ' ' + elements[1] + ' ' \
                            + elements[2] + ' ' + elements[3] + ' ' \
                            + elements[4] + ' ' + elements[5] + ' ' \
                            + elements[6]
                    fw.write(output)
                    fw.write("\r\n")
    print "Exceed low boundary: " + str(elb)
    print "Exceed high boundary: " + str(ehb)
    print "Logic of positions error: " + str(lpe)

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())