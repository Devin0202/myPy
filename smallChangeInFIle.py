import os
import time
import random
import shutil
import cv2

srcRoot = "/home/devin/Desktop/mnt/20171107/TrainData/Facehead/"
targetFile = "dataLabel.txt"

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

if os.path.exists(srcRoot):
	for rt, dirs, files in os.walk(srcRoot):
		for name in files:
			if name == targetFile:
				with open(os.path.join(rt, name), 'r') as f:
				    oriList = f.readlines()

				tmpSplit = os.path.join(rt, name).split('/')
				print os.path.join(rt, name)
				newName = os.path.join(rt, tmpSplit[-2] + ".txt")
				print newName

				sortList = []
				for line in oriList:
					elements = line.split()
					if len(elements) > 0:
						sortList.append(elements[0])
				sortListDone = sorted(set(sortList), key = sortList.index)

				with open(newName, 'w') as f:
					for id in sortListDone:
						for line in oriList:
							if 0 == line.find(id):
								elements = line.split()
								dstLine = elements[0] + ' ' + str(int(elements[6]) + 1) + ' ' + elements[2] + ' ' + elements[3] + ' ' + elements[4] + ' ' + elements[5]
								f.write(dstLine + "\r\n")
			else:
				continue
else:
	print "No source!!!"
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
