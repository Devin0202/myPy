import os
import time
import random
from skimage import io,data,transform

srcRootList = ["/media/devin/wy/20171107palm/top/bright/",
                "/media/devin/wy/20171107palm/top/dark/",
                "/media/devin/wy/20171107palm/top/normal/"]
dstRootList = ["/media/devin/wy/20171107palmResize/top/bright/",
                "/media/devin/wy/20171107palmResize/top/dark/",
                "/media/devin/wy/20171107palmResize/top/normal/"]

# srcRoot = "/media/devin/wy/20171107palm/palm/fore/dark/palm/"
# dstRoot = "/media/devin/wy/20171107palmResize/palm/fore/dark/palm/"
rowSize = 1080
colSize = 1920
rowSizeOri = 1344
colSizeOri = 2400
rowRation = rowSize / float(rowSizeOri)
colRation = colSize / float(colSizeOri)
index = 0
downSample = 1
allLines = []
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

if len(srcRootList) != len(dstRootList):
    print "List Error!"
else:
    for (srcRoot, dstRoot) in zip(srcRootList, dstRootList):
        print srcRoot
        print dstRoot
        if not os.path.exists(dstRoot):
            os.makedirs(dstRoot)
        if os.path.exists(srcRoot):
            for rt, dirs, files in os.walk(srcRoot):
                for name in files:
                    if -1 != name.find(".jpg") or -1 != name.find(".JPG") \
                        or -1 != name.find(".png") or -1 != name.find(".PNG"):
                        if random.uniform(0, 1) <= downSample:
                            absoluteRoute = os.path.join(rt, name)
                            #print absoluteRoute
                            img = io.imread(absoluteRoute)
                            if 0 < img.size:
                                rowRation = rowSize / float(img.shape[0])
                                colRation = colSize / float(img.shape[1])
                                if colSizeOri != img.shape[1] or rowSizeOri != img.shape[0]:
                                    print "Wrong shape: " + str(img.shape[0]) + str(img.shape[1])
                                    continue
                                dst = transform.resize(img, (rowSize, colSize))
                                io.imsave(dstRoot + name, dst)
                                #io.imsave(dstRoot + str(index) + '_' + name, dst)
                                index += 1
                                if 10000 < index:
                                    break
                    # Just for Hiscene Palm
                    if -1 != name.find("dataLabel.txt"):
                        absoluteRoute = os.path.join(rt, name)
                        inputF = open(absoluteRoute, 'r')
                        try:
                            allLines = inputF.readlines()
                        finally:
                            inputF.close()

                        outputF = open(dstRoot + name, 'w')
                        outLines = []
                        try:
                            for line in allLines:
                                tmp = line.split(' ')
                                tmp[2] = str(int(int(tmp[2]) * colRation))
                                tmp[3] = str(int(int(tmp[3]) * colRation))
                                tmp[4] = str(int(int(tmp[4]) * rowRation))
                                tmp[5] = str(int(int(tmp[5]) * rowRation))
                                outLines.append(tmp[0] + ' ' + tmp[1] + ' ' + tmp[2] + ' ' + tmp[3] + ' ' + tmp[4] + ' ' + tmp[5] + "\r\n")
                            outputF.writelines(outLines)
                        finally:
                            outputF.close()
        else:
            print("No Source!!!")

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())