import os
import time
import random
import cv2
import numpy as np

srcRoot = "/home/devin/Desktop/dataAug/"
dstRoot = "/media/devin/Elements/forServer/negHeadPca/"
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

def reconstructPca(Acc, percentage):
    eigVals, eigVects, mean, scale = singleChannelPca(Acc)
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
print "Total files: " + str(len(listImg))
#print listImg

retainStart = 90
for retainRecord in range(retainStart, 100, 1):
    retain = retainRecord / 100.0
    print retain
    cnt = 0
    index = 0
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

        cnt = cnt + 1
        if 0 == cnt % batch:
            print cnt
            reconB = reconstructPca(bAcc, retain)
            reconG = reconstructPca(gAcc, retain)
            reconR = reconstructPca(rAcc, retain)

            for i in range(0, reconB.shape[0] - 1):            
                rb = reconB[i].reshape(oriShape)
                rg = reconG[i].reshape(oriShape)
                rr = reconR[i].reshape(oriShape)
                #print rb
                w = rb.shape[1]
                h = rb.shape[0]
                for xi in xrange(0, w):
                    for xj in xrange(0, h):
                        tmp = rb[xj, xi]
                        if tmp > 255:
                            tmp = 255
                        if tmp < 0:
                            tmp = 0;
                        rb[xj, xi] = tmp

                        tmp = rg[xj, xi]
                        if tmp > 255:
                            tmp = 255
                        if tmp < 0:
                            tmp = 0;
                        rg[xj, xi] = tmp

                        tmp = rr[xj, xi]
                        if tmp > 255:
                            tmp = 255
                        if tmp < 0:
                            tmp = 0;
                        rr[xj, xi] = tmp

                rb = rb.astype(oriType)
                rg = rg.astype(oriType)
                rr = rr.astype(oriType)
                imgResult = cv2.merge([rb, rg, rr])

                dst = dstRoot + str(retainRecord) + "_" + str(index) + ".png"
                cv2.imwrite(dst, imgResult)
                index += 1
            break

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())