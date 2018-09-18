# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Register faces in ST private cloud server
"""
import os
import sys
import time
import requests
import urllib
import json
print(sys.version)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

### Defs region
def verifyVersion(serverUrl):
    url = serverUrl + "/verify/version"
    r = requests.get(url)

    print(os.linesep)
    print("verifyVersion Http status: " + str(r.status_code))
    print(r.text)

def verifyDetail(serverUrl):
    url = serverUrl + "/verify/detail"
    r = requests.get(url)

    print(os.linesep)
    print("verifyDetail Http status: " + str(r.status_code))
    print(r.text)

def infoSets(serverUrl):
    url = serverUrl + "/verify/target/gets"
    r = requests.get(url)

    print(os.linesep)
    print("infoSets Http status: " + str(r.status_code))
    print(r.text)

def createFaceSet(serverUrl, setID):
    url = serverUrl + "/verify/target/add"
    # If number of register pics is up to 100w, set "isFastSearch" 1
    isFastSearch = 0
    info = {"dbName" : setID, \
            "fastSearch" : isFastSearch} 
    r = requests.post(url, data = info)

    print(os.linesep)
    print("createFaceSet Http status: " + str(r.status_code))
    print(r.json())

def delFaceSet(serverUrl, setID):
    url = serverUrl + "/verify/target/deletes"
    info = {"dbName" : setID}
    r = requests.post(url, data = info)

    print(os.linesep)
    print("delFaceSet Http status: " + str(r.status_code))
    print(r.json())

def clearFaceSet(serverUrl, setID):
    url = serverUrl + "/verify/target/clear"
    info = {"dbName" : setID}
    r = requests.post(url, data = info)

    print(os.linesep)
    print("clearFaceSet Http status: " + str(r.status_code))
    print(r.json())

def delSingleFace(serverUrl, setID, picId, isPrintInfo):
    url = serverUrl + "/verify/face/deletes"

    info = {"dbName" : setID, \
            "imageId" : picId}

    r = requests.post(url, params = info)

    if (isPrintInfo):
        print(os.linesep)
        print(r.json())
        print("delSingleFace Http status: " + str(r.status_code))

def addSingleFace(serverUrl, setID, facePic, isPrintInfo):
    url = serverUrl + "/verify/face/synAdd"
    notGetFeature = 1
    notGetDetail = 0
    # threshold for faces detecting
    threshold = 0

    imageName = facePic.split('/')[-1].split('.')[0]
    # print(imageName)

    info = {"dbName" : setID, \
            "getFeature" : notGetFeature, \
            "getDetail" : notGetDetail, \
            "qualityThreshold" : threshold}

    outData = {"imageDatas" : (urllib.parse.quote(imageName, \
        encoding = "utf-8"), open(facePic, "rb"))}

    r = requests.post(url, params = info, files = outData)

    if (isPrintInfo):
        print(os.linesep)
        print(r.json())
        print("addSingleFace Http status: " + str(r.status_code))

    if (-1 != r.text.find("errCode")):
        return ''
    elif (-1 == r.text.find("personId")):
        return ''
    else:
        return r.text.split("\"personId\": \"")[-1].split("\", \"")[0]

def addFaces(serverUrl, setID, folder, tokenMapping):
    cntF = 0
    lineList = []
    if os.path.exists(folder):
        for rt, dirs, files in os.walk(folder):
            for name in files:
                if -1 != name.find(".jpg") or -1 != name.find(".JPG") \
                or -1 != name.find(".png") or -1 != name.find(".PNG"):
                    absoluteRoute = os.path.join(rt, name)
                    # print(name)                    
                    print(absoluteRoute)
                    tmpStr = ''
                    tmpStr = addSingleFace(serverUrl, mSetID, absoluteRoute, False)

                    if not ('' == tmpStr):
                        cntF += 1

                    tmpStr = '\"' + tmpStr + '\"' + ", \"" + name.split('.')[0] + '\"'
                    lineList.append(tmpStr)

        with open(tokenMapping, 'w') as fw:
            for sl in lineList:
                fw.write("faceName.put(" + sl + ");" + "\r\n")
    else:
        print("No Source!!!")
        sys.exit(0)
    print("Total faces registered: " + str(cntF))

def searchFace(serverUrl, setID, facePic, isPrintInfo):
    url = serverUrl + "/verify/face/search"
    topK = 1
    # threshold for faces detecting
    threshold = 0

    imageName = facePic.split('/')[-1].split('.')[0]
    # print(imageName)

    info = {"dbName" : setID, \
            "topNum" : topK, \
            "score" : threshold}

    outData = {"imageData" : (urllib.parse.quote(imageName, \
        encoding = "utf-8"), open(facePic, "rb"))}

    r = requests.post(url, params = info, files = outData)

    if (isPrintInfo):
        print(os.linesep)
        print(r.text)
        # print(r.json())
        print("searchFace Http status: " + str(r.status_code))

    tmpStr = r.text.split("filename\": \"")[-1].split("\", \"")[0]
    return urllib.parse.unquote(tmpStr, encoding = "utf-8")

### Params region
mServerUrl = "http://192.168.18.193:9001"
srcRoot = "/home/devin/Desktop/EF/"
mTokenMapping = "/home/devin/Desktop/faceMap2.txt"
mSetID = "HisceneTest0820"

# verifyVersion(mServerUrl)
# verifyDetail(mServerUrl)
# createFaceSet(mServerUrl, mSetID)
clearFaceSet(mServerUrl, mSetID)
# delFaceSet(mServerUrl, mSetID)

# addSingleFace(mServerUrl, mSetID, "/home/devin/Desktop/EF/L林璐.jpg", True)
addFaces(mServerUrl, mSetID, srcRoot, mTokenMapping)
# id = searchFace(mServerUrl, mSetID, "/home/devin/Desktop/faceOri/yunnan/王迅.jpg", True)
# print(id)

# delSingleFace(mServerUrl, mSetID, "9acf4085160345b49af58582a7ed6681", True)
infoSets(mServerUrl)

print(os.linesep)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))