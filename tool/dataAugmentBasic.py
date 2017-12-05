import os
import time
import random
import cv2
import numpy as np

srcRoot = "/home/devin/Desktop/dataAug/"
dstRoot = "/media/devin/Elements/forServer/negHeadBasic/"
listImg = [];

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
print "Src files: " + str(len(listImg))
#print listImg

cnt = 0
# one in multX out
multX = 11
for single in listImg:
    img = cv2.imread(single, cv2.IMREAD_COLOR)
    w = img.shape[1]
    h = img.shape[0]

    for i in range(0, multX):
        if 0 != i:
            ration = random.uniform(0.65, 1.35)
            bias = random.randint(-50, 50)
            # ration = 0.5
            # bias = 0
            # print ration
            b, g, r = cv2.split(img)
            if 0 == random.randint(0, 1):
                b = cv2.equalizeHist(b)
            if 0 == random.randint(0, 1):
                g = cv2.equalizeHist(g)
            if 0 == random.randint(0, 1):
                r = cv2.equalizeHist(r)
            img = cv2.merge([b, g, r])

            img = cv2.blur(img, (random.randint(3, 5), random.randint(3, 5)))
            for xi in xrange(0, w):
                for xj in xrange(0, h):
                    tmp = int(img[xj, xi, 0] * ration + bias)
                    tmp = int(random.gauss(1.0, random.uniform(0.0, 0.1)) * tmp)
                    if tmp > 255:
                        tmp = 255
                    if tmp < 0:
                        tmp = 0;
                    img[xj, xi, 0] = tmp

                    tmp = int(img[xj, xi, 1] * ration + bias)
                    tmp = int(random.gauss(1.0, random.uniform(0.0, 0.1)) * tmp)
                    if tmp > 255:
                        tmp = 255
                    if tmp < 0:
                        tmp = 0;
                    img[xj, xi, 1] = tmp

                    tmp = int(img[xj, xi, 2] * ration + bias)
                    tmp = int(random.gauss(1.0, random.uniform(0.0, 0.1)) * tmp)
                    if tmp > 255:
                        tmp = 255
                    if tmp < 0:
                        tmp = 0;
                    img[xj, xi, 2] = tmp
        
        location = single.rfind('/')
        if -1 != location:
            dst = dstRoot + str(cnt) + single[(location + 1) :]
            cv2.imwrite(dst, img)
        cnt += 1

print "Make number: " + str(cnt)
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())