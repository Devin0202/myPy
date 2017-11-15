import os
import sys
import time
import random
import cv2
import numpy as np

srcRoot = "/home/devin/Desktop/dataAug/"
dstRoot = "/home/devin/Desktop/dataAugEx/"
listImg = [];

def percentage2n(eigVals, percentage):
    sortArray = np.sort(eigVals)   #ascend  
    sortArray = sortArray[-1::-1]  #descend  
    arraySum = sum(sortArray)
    tmpSum = 0
    num = 0
    for i in sortArray:
        tmpSum += i
        num += 1
        if tmpSum >= arraySum * percentage:
            return num

def singleChannelPca(Acc):
    mean = np.mean(Acc, axis = 0)
    scale = Acc - mean
    # print Acc.shape
    # print mean.shape
    # print scale.shape
    cov = np.cov(scale, rowvar = 0)
    print "Cov matrix done " + str(cov.shape)
    eigVals,eigVects = np.linalg.eig(np.mat(cov))
    # print eigVals
    # print eigVals.shape
    print eigVects.shape
    return eigVals, eigVects, mean, scale

def reconstructPca(Acc, percentage, eigVals, eigVects, mean, scale):
    n = percentage2n(eigVals, percentage)
    print "lowD: " + str(n)
    eigValIndice = np.argsort(eigVals)
    n_eigValIndice = eigValIndice[-1 : -(n + 1) : -1]
    n_eigVect = eigVects[:, n_eigValIndice]
    lowDDataMat = scale * n_eigVect
    reconMat = (lowDDataMat * n_eigVect.T) + mean
    print reconMat.shape
    return reconMat

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

if not os.path.exists(dstRoot):
    os.makedirs(dstRoot)

if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if -1 != name.find(".jpg") or -1 != name.find(".JPG") \
                or -1 != name.find(".png") or -1 != name.find(".PNG"):
                absoluteRoute = os.path.join(rt, name)
                listImg.append(absoluteRoute)
else:
    print("No Source!!!")
    sys.exit(0)
print "Total files: " + str(len(listImg))
#print listImg
cnt = 0
batch = len(listImg)
for single in listImg:
    img = cv2.imread(single, cv2.IMREAD_COLOR)
    b, g, r = cv2.split(img)
    oriShape = b.shape
    oriType = b.dtype
    b = b.reshape(1, -1)
    g = g.reshape(1, -1)
    r = r.reshape(1, -1)

    if 0 == cnt % batch:
        bAcc = b
        gAcc = g
        rAcc = r
    else:
        bAcc = np.append(bAcc, b, axis = 0)
        gAcc = np.append(gAcc, g, axis = 0)
        rAcc = np.append(rAcc, r, axis = 0)
    cnt += 1

eigValsB, eigVectsB, meanB, scaleB = singleChannelPca(bAcc)
eigValsG, eigVectsG, meanG, scaleG = singleChannelPca(gAcc)
eigValsR, eigVectsR, meanR, scaleR = singleChannelPca(rAcc)

print time.strftime('PCA finish: %Y-%m-%d %H:%M:%S', time.localtime())

retainStart = 86
index = 0
for retainRecord in range(retainStart, 100, 2):
    retain = retainRecord / 100.0
    print "PCA retain rate: " + str(retain)
    reconB = reconstructPca(bAcc, retain, eigValsB, eigVectsB, meanB, scaleB)
    reconG = reconstructPca(gAcc, retain, eigValsG, eigVectsG, meanG, scaleG)
    reconR = reconstructPca(rAcc, retain, eigValsR, eigVectsR, meanR, scaleR)
    for i in range(0, reconB.shape[0] - 1):
        # print type(reconB[i])
        rb = np.clip(reconB[i], 0.0, 255.0).reshape(oriShape).astype(oriType)
        rg = np.clip(reconG[i], 0.0, 255.0).reshape(oriShape).astype(oriType)
        rr = np.clip(reconR[i], 0.0, 255.0).reshape(oriShape).astype(oriType)
        imgResult = cv2.merge([rb, rg, rr])

        dst = dstRoot + str(retainRecord) + "_" + str(index) + ".png"
        cv2.imwrite(dst, imgResult)
        index += 1

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())