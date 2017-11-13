import os
import time
import random
import shutil

srcRoot = "/media/devin/2421F3BE1AF3E7E0/4acf/top/"
dstRoot = "/home/devin/Desktop/top2339/"

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
if not os.path.exists(dstRoot):
    os.makedirs(dstRoot)

downSample = 0.33
cnt = 0
index = 0
if os.path.exists(srcRoot):
    for rt, dirs, files in os.walk(srcRoot):
        for name in files:
            if -1 != name.find(".jpg") or -1 != name.find(".JPG") \
                or -1 != name.find(".png") or -1 != name.find(".PNG"):
                cnt += 1
                absoluteRoute = os.path.join(rt, name)
                print name
                #print absoluteRoute
                if random.uniform(0, 1) <= downSample:
                    shutil.copyfile(absoluteRoute, dstRoot + str(index) + '_' + name)
                    index += 1
else:
    print("No Source!!!")

print "Total images: " + str(cnt)
print "Total copies: " + str(index)
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
