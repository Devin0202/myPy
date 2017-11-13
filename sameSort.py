import os
import time
import random
import shutil
import cv2

srcRoot = "/home/devin/Desktop/mnt/20171112_256144Labels/"
dstRoot = "/home/devin/Desktop/mnt/20171112_256144LabelsSort/"
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
if not os.path.exists(dstRoot):
    os.makedirs(dstRoot)
if os.path.exists(srcRoot):
	for rt, dirs, files in os.walk(srcRoot):
		for name in files:
			if -1 != name.find(".txt"):
				print "READ: " + os.path.join(rt, name)
				with open(os.path.join(rt, name), 'r') as f:
				    oriList = f.readlines()

				sortList = []
				for line in oriList:
					elements = line.split()
					if len(elements) > 0:
						sortList.append(elements[0])
				sortListDone = sorted(set(sortList), key = sortList.index)

				print "WRITE: " + dstRoot + name
				with open(dstRoot + name, 'w') as f:
					for id in sortListDone:
						for line in oriList:
							if 0 == line.find(id):
								f.write(line)
			else:
				continue
else:
	print "No source!!!"
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
