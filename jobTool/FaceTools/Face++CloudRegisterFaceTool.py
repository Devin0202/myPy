# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Register faces in face++ public cloud server
Reference:  https://console.faceplusplus.com.cn/documents/4888401
"""
import os
import sys
import time
import requests
import urllib
print(sys.version)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

### Defs region
def createFaceSet(key, secret, setID, createInfo):
    url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/create"
    info = {"api_key" : key, \
            "api_secret" : secret, \
            "outer_id" : setID, \
            "user_data" : createInfo} 
    r = requests.post(url, data = info)

    print(os.linesep)
    print("createFaceSet Http status: " + str(r.status_code))
    print(r.json())

def renameFaceSet(key, secret, setID, newID):
    url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/update"
    info = {"api_key" : key, \
            "api_secret" : secret, \
            "outer_id" : setID, \
            "new_outer_id" : newID} 
    r = requests.post(url, params = info)

    print(os.linesep)
    print("renameFaceSet Http status: " + str(r.status_code))
    print(r.json())

def updateFaceSetDisplayName(key, secret, setID, displayName):
    url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/update"
    info = {"api_key" : key, \
            "api_secret" : secret, \
            "outer_id" : setID, \
            "display_name" : displayName} 
    r = requests.post(url, params = info)

    print(os.linesep)
    print("updateFaceSetDisplayName Http status: " + str(r.status_code))
    print(r.json())

def updateFaceSetUserdata(key, secret, setID, userdata):
    url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/update"
    info = {"api_key" : key, \
            "api_secret" : secret, \
            "outer_id" : setID, \
            "user_data" : userdata} 
    r = requests.post(url, params = info)

    print(os.linesep)
    print("updateFaceSetUserdata Http status: " + str(r.status_code))
    print(r.json())

def updateFaceSetTags(key, secret, setID, tags):
    url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/update"
    info = {"api_key" : key, \
            "api_secret" : secret, \
            "outer_id" : setID, \
            "tags" : tags} 
    r = requests.post(url, params = info)

    print(os.linesep)
    print("FaceSet自定义标签组成的字符串，用来对FaceSet分组。最长255个字符")
    print("最长255个字符，多个 tag 用逗号分隔，每个 tag 不能包括字符^@,&=*'\"")
    print("updateFaceSetTags Http status: " + str(r.status_code))
    print(r.json())

def delFaceSet(key, secret, setID, isEnforced):
    url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/delete"
    if (isEnforced):
        checkEmpty = 0
    else:
        checkEmpty = 1

    info = {"api_key" : key, \
            "api_secret" : secret, \
            "outer_id" : setID, \
            "check_empty" : checkEmpty} 
    r = requests.post(url, data = info)

    print(os.linesep)
    print("delFaceSet Http status: " + str(r.status_code))
    print(r.json())

def infoSingleSet(key, secret, setID):
    url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/getdetail"
    info = {"api_key" : key, \
            "api_secret" : secret, \
            "outer_id" : setID} 
    r = requests.post(url, data = info)

    print(os.linesep)
    print("infoSingleSet Http status: " + str(r.status_code))
    print(r.json())

def infoSets(key, secret):
    url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/getfacesets"
    info = {"api_key" : key, \
            "api_secret" : secret} 
    r = requests.post(url, data = info)

    print(os.linesep)
    print("infoSets Http status: " + str(r.status_code))
    print(r.json())

def detectSingleFace(key, secret, singleImage, imageName, isPrintInfo):
    url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
    outData = {"image_file" : (urllib.parse.quote(imageName, encoding = "utf-8"), \
        open(singleImage, "rb"))}
    info = {"api_key" : key, "api_secret" : secret} 
    r = requests.post(url, params = info, files = outData)

    if (isPrintInfo):
        print(os.linesep)
        print(r.json())
        print("detectSingleFace Http status: " + str(r.status_code))

    token = r.text.split("face_token\": \"")
    if (2 > len(token)):
        print("Detect Error: " + singleImage)
        return ''
    else:
        token = token[1]
        if (1 > len(token)):
            print("Detect Error: " + singleImage)
            return ''
        else:
            token = token.split("\"}]}")[0]
            return token

def delSingleFace(key, secret, setID, faceToken, isPrintInfo):
    url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface"
    info = {"api_key" : key, \
            "api_secret" : secret, \
            "outer_id" : setID, \
            "face_tokens" : faceToken} 
    r = requests.post(url, params = info)

    if (isPrintInfo):
        print(os.linesep)
        print(r.json())
        print("delSingleFace Http status: " + str(r.status_code))

def addSingleFace(key, secret, setID, faceToken, isPrintInfo):
    url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/addface"
    info = {"api_key" : key, \
            "api_secret" : secret, \
            "outer_id" : setID, \
            "face_tokens" : faceToken} 
    r = requests.post(url, params = info)

    if (isPrintInfo):
        print(os.linesep)
        print(r.json())
        print("addSingleFace Http status: " + str(r.status_code))

def addFaces(key, secret, setID, folder, tokenMapping):
    cntF = 0
    lineList = []
    if os.path.exists(folder):
        for rt, dirs, files in os.walk(folder):
            for name in files:
                if -1 != name.find(".jpg") or -1 != name.find(".JPG") \
                or -1 != name.find(".png") or -1 != name.find(".PNG"):
                    absoluteRoute = os.path.join(rt, name)
                    # print(name)
                    cntF += 1
                    rtToken = detectSingleFace(key, secret, \
                                absoluteRoute, name, False)
                    if ('' == rtToken):
                        print("Null!!!")
                    else:
                        print(absoluteRoute + " token: " + rtToken)
                        addSingleFace(mKey, mSecret, mSetID, rtToken, False)
                        tmpStr = '\"' + rtToken + '\"' + ", \"" + name.split('.')[0] + '\"'
                        lineList.append(tmpStr)

        with open(tokenMapping, 'w') as fw:
            for sl in lineList:
                fw.write("faceName.put(" + sl + ");" + "\r\n")
    else:
        print("No Source!!!")
        sys.exit(0)
    infoSingleSet(mKey, mSecret, mSetID)
    print("Total faces registered: " + str(cntF))

def searchSingleFace(key, secret, singleImage, fSetId, isPrintInfo):
    url = "https://api-cn.faceplusplus.com/facepp/v3/search"
    outData = {"image_file" : (urllib.parse.quote("test.jpg", encoding = "utf-8"), \
        open(singleImage, "rb"))}
    info = {"api_key" : key, "api_secret" : secret, "outer_id" : fSetId} 
    r = requests.post(url, params = info, files = outData)

    if (isPrintInfo):
        print(os.linesep)
        print(r.json())
        print("searchSingleFace Http status: " + str(r.status_code))

    tmp = r.json()["results"]
    print(tmp[0]["face_token"])
    print(tmp[0]["confidence"])

    tmp = r.json()["faces"]
    print(tmp[0]["face_rectangle"]["top"])
    print(tmp[0]["face_rectangle"]["left"])
    print(tmp[0]["face_rectangle"]["height"])
    print(tmp[0]["face_rectangle"]["width"])

### Params region
srcRoot = "/home/devin/Desktop/EF/"
mTokenMapping = "/home/devin/Desktop/faceMap2.txt"

mKey = "6uekRquo16PxOV9qTju6N08m4Iv3ypem"
mSecret = "hqQF28bU8sGIlfLWHBKmnVdLE6Tz0AlK"
mSetID = "HisceneTest0704"
mCreateInfo = "Faces registered by python3 requests"

### Sample Jobs region
# createFaceSet(mKey, mSecret, mSetID, mCreateInfo)
# addFaces(mKey, mSecret, mSetID, srcRoot, mTokenMapping)

# renameFaceSet(mKey, mSecret, mSetID, "Test2")
# renameFaceSet(mKey, mSecret, "Test2", mSetID)
# updateFaceSetDisplayName(mKey, mSecret, mSetID, "Hiscene Shanghai Employees")
# updateFaceSetUserdata(mKey, mSecret, mSetID, "Full functions: " + mCreateInfo)
# updateFaceSetTags(mKey, mSecret, mSetID, "Male,Female,Midlife")

# delSingleFace(mKey, mSecret, mSetID, "85f2c9ff8187a67cbfb146f02f7cd083", True)

# delFaceSet(mKey, mSecret, mSetID, True)

# faceToken = detectSingleFace(mKey, mSecret, "/home/devin/Desktop/3.jpg", "杨华.jpg", True)
# addSingleFace(mKey, mSecret, mSetID, faceToken, True)

infoSets(mKey, mSecret)
infoSingleSet(mKey, mSecret, mSetID)

while (1):
    searchSingleFace(mKey, mSecret, "/home/devin/Downloads/tmpJpg/baoyuandong/Rects/0830170059/17-01-03-746_E.jpg", \
        mSetID, False)
    time.sleep(2)

print(os.linesep)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))