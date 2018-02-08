# -*- coding: utf-8 -*-
"""

"""
import os
import sys
import time
import shutil
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

srcRoot = "/home/devin/Downloads/111/"
target = "reviewlog.txt"
acceptTarget = "accepted.txt"
rejectTarget = "rejected.txt"
dstFile = "summary.txt"
reject = 0.0
accept = 0.0
summarylist = []
summaryHead = []

cnt = 0
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if -1 != name.find(target):
                cnt += 1
                with open(os.path.join(rt, name), 'r') as fr:
                    content = fr.readlines()
                reject += float(content[3].split()[-1])
                accept += float(content[4].split()[-1])
                proportion = float(content[3].split()[-1]) \
                    / (float(content[3].split()[-1]) + float(content[4].split()[-1]))
                summarylist.append(content[1].split()[-1] + "\r\n")
                summarylist.append(content[3])
                summarylist.append("Reject Rate: " + str(proportion) + "\r\n")
                summarylist.append("\r\n")
                # print content[1].split()[-1]
                # print proportion
            elif -1 != name.find(rejectTarget):
                ori = os.path.join(rt, name)
                dstRoot = os.path.join(srcRoot, "rejectFiles");
                if not os.path.exists(dstRoot):
                    os.makedirs(dstRoot)
                dst = os.path.join(dstRoot, name);
                shutil.copyfile(ori, dst)
            elif -1 != name.find(acceptTarget):
                ori = os.path.join(rt, name)
                dstRoot = os.path.join(srcRoot, "acceptFiles");
                if not os.path.exists(dstRoot):
                    os.makedirs(dstRoot)
                dst = os.path.join(dstRoot, name);
                shutil.copyfile(ori, dst)
            else:
                continue

    summaryHead.append("Total reject pics: " + str(reject))
    summaryHead.append("\r\n")
    summaryHead.append("Total acceptable pics: " + str(accept))
    summaryHead.append("\r\n\r\n\r\n")
    summaryHead.append("Details:\r\n")
    with open(os.path.join(srcRoot, dstFile), 'w') as fw:
        fw.writelines(summaryHead)
        fw.writelines(summarylist)
else:
    print("No Source!!!")
    sys.exit(0)
print cnt

print os.linesep
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())