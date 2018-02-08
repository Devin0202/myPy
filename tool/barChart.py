# -*- coding: utf-8 -*-
"""
Draw bar chart
"""
import os
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 1st bar
xAll = [0.2, 0.3, 0.4, 0.5]
y1st = [0.9596292318, 0.7621383792, 0.5266300666, 0.2893260548] # recall
y2nd = [0.7183564457, 0.8501201852, 0.9554239188, 0.99375]      # 1 - error

width = 0.4
ind = np.linspace(0.5, 9.5, 4)
fig = plt.figure(1)  
ax  = fig.add_subplot(111)
ax.bar(ind - width / 2, y1st, width, color = 'green', label = "Recall")
ax.bar(ind + width / 2, y2nd, width, color = 'red', label = "1 - Error")
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(xAll)
ax.set_title("Average\nRecall & 1 - Error", bbox = {'facecolor':'0.8', 'pad':5})
plt.grid(True)

plt.xlabel("Lower limit for identification")
plt.ylabel("Percentage")
plt.xlim(0, 13)
plt.ylim(0, 1.1)
plt.yticks(np.linspace(0.0, 1.0, 9))
plt.legend(loc = 'upper right', prop = {'size': 10})
plt.show()

# 2nd bar
# xAll = ["f1", "f3", "hj", "lpz", "lup", "m1", "sy", "wrq", "xx", "zsy"]
# y1st = [1, 0.8604651163, 0.9846153846, 0.9122807018, 0.9545454545, \
#         0.9555555556, 0.9863013699, 1, 0.9425287356, 1] # recall
# y2nd = [0.6081081081, 0.8043478261, 0.9411764706, 0.4227642276, 0.893617021, \
#         1, 0.7384615385, 0.5178571429, 0.5503355705, 0.7068965517]      # 1 - error

# width = 0.4
# ind = np.linspace(0.5, 9.5, 10)
# fig = plt.figure(1)  
# ax  = fig.add_subplot(111)
# ax.bar(ind - width / 2, y1st, width, color = 'green', label = "Recall")
# ax.bar(ind + width / 2, y2nd, width, color = 'red', label = "1 - Error")
# ax.set_xticks(ind + width / 2)
# ax.set_xticklabels(xAll)
# ax.set_title("Lower limit is 0.2", bbox = {'facecolor':'0.8', 'pad':5})
# plt.grid(True)

# plt.xlabel("Personal ID.")
# plt.ylabel("Percentage")
# plt.xlim(0, 13)
# plt.ylim(0, 1.1)
# plt.yticks(np.linspace(0.0, 1.0, 9))
# plt.legend(loc = 'upper right', prop = {'size': 10})
# plt.show()

print os.linesep
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())