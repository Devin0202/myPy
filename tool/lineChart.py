# -*- coding: utf-8 -*-
"""
Draw line chart
"""
import os
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

srcRoute1 = "/home/devin/Desktop/test_set2-recall"
srcRoute2 = "/home/devin/Desktop/test_set2-errorDetect"
dstFile = "/home/devin/myData/20-1.00-Recall-test_set2.txt"
dataDepot = []      # minSize, setThres, timeCost, recall, errorDetect

if os.path.exists(srcRoute2) and os.path.exists(srcRoute1):
    for rt, dirs, files in os.walk(srcRoute1):
        for name in files:
            tmpItem = []
            tmpItem.append(name.split('-')[0])
            tmpItem.append(name.split('-')[1])
            with open(os.path.join(rt, name), 'r') as fr:
                tmpItem.append(fr.readline().split(": ")[1][:-1])
                tmpItem.append(fr.readline().split(": ")[1][:-1])

            otherOne = name.replace("Recall", "ErrorDetect")
            with open(os.path.join(srcRoute2, otherOne), 'r') as fr:
                fr.readline()
                tmpItem.append(fr.readline().split(": ")[1][:-1])

            dataDepot.append(tmpItem)
else:
    print("No Source!!!")
    sys.exit(0)

index = []
for item in dataDepot:
    index.append(item[1])
index = set(index)

xAll = []
yAll = []
for sortL in index:
    x = []
    y = []
    for item in dataDepot:
        if item[1] == sortL:
            x.append(float(item[0]))
            y.append(float(item[2]))
    xx = np.array(x)
    yy = np.array(y)
    indexS = np.lexsort((yy, xx))
    X = []
    Y = []
    for i in indexS:
        X.append(x[i])
        Y.append(y[i])
    xAll.append(X)
    yAll.append(Y)

lineColor = ['b', 'r', 'c', 'm', 'g', 'y', 'k', 'w']
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }
for i in range(0, len(index)):
    plt.plot(xAll[i], yAll[i], lineColor[i] + '-*', \
                label = str(list(index)[i]))
    plt.title("DetectionThreshold: " + str(sorted(index)[0]) + ' ~ ' \
                + str(sorted(index)[-1]), fontdict = font)
    # plt.text(2, 0.65, r'$\cos(2 \pi t) \exp(-t)$', fontdict = font)
    plt.xlabel("MinSidePixels", fontdict = font)
    plt.ylabel("Time Cost (ms)", fontdict = font)
plt.legend(loc = 'upper right')
plt.show()

print os.linesep
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
