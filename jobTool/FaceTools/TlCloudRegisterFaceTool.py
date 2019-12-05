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
import base64
import random
print(sys.version)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

### Defs region
def logIn(serverUrl: str) -> str:
    url = serverUrl + "/static-face/api/auth/login"
    headers = {"content-type":"application/json"}
    info = {"username":"admin", "password":"123456"}
    info = json.dumps(info)
    r = requests.post(url, data=info, headers=headers)

    """Print received information"""
    print(os.linesep)
    print("Log-in Http status: " + str(r.status_code))
    text = json.loads(r.text)

    try:
        getToken = text["data"]["token"]
        text = json.dumps(text, ensure_ascii=False, sort_keys=True, \
                    indent=4, separators=(',', ': '))
        print(text)
    except:
        getToken = ""
        print("Can't get token!!!")

    return getToken

def createFaceSet(serverUrl: str, fToken: str, fExtraInfo: dict=None, \
                    fSetName: str=None, fmaxFaceNum: int=1000):
    url = serverUrl + "/static-face/api/external/v1/face_group"
    headers = {"content-type":"application/json", \
                "Authorization":"Bearer " + fToken}

    if None == fExtraInfo:
        if None == fSetName:
            fExtraInfo = {"id":"people", "scope": "Hiscene"}
        else:
            fExtraInfo = {"id":fSetName}
    elif "id" not in fExtraInfo.keys():
        print("No id for create face set!!!")
    else:
        pass

    recordA = str(time.strftime("%Y-%m-%d", time.localtime()))
    recordB = str(time.strftime("%H-%M-%S", time.localtime()))
    fExtraInfo = json.dumps(fExtraInfo)
    info = {"name":recordB, "maxCount":fmaxFaceNum, "comment":recordA, \
            "integration":fExtraInfo}
    info = json.dumps(info)

    r = requests.post(url, data=info, headers=headers)
    """Print received information"""
    print(os.linesep)
    print("CreateFaceSet Http status: " + str(r.status_code))
    text = json.loads(r.text)
    text = json.dumps(text, ensure_ascii=False, sort_keys=True, \
                    indent=4, separators=(',', ': '))
    print(text)

def delFaceSet(serverUrl: str, fToken: str, fSetId: str):
    url = serverUrl + "/static-face/api/external/v1/face_group/" + str(fSetId)
    headers = {"content-type":"application/json", \
                "Authorization":"Bearer " + fToken}

    r = requests.delete(url, headers=headers)
    """Print received information"""
    print(os.linesep)
    print("DelFaceSet Http status: " + str(r.status_code))
    text = json.loads(r.text)
    text = json.dumps(text, ensure_ascii=False, sort_keys=True, \
                    indent=4, separators=(',', ': '))
    print(text)

def getSetInfo(serverUrl: str, fToken: str, fSetId: str):
    url = serverUrl + "/static-face/api/external/v1/face_group/" + str(fSetId)
    headers = {"content-type":"application/json", \
                "Authorization":"Bearer " + fToken}

    r = requests.get(url, headers=headers)
    """Print received information"""
    print(os.linesep)
    print("GetSetInfo Http status: " + str(r.status_code))
    text = json.loads(r.text)
    text = json.dumps(text, ensure_ascii=False, sort_keys=True, \
                    indent=4, separators=(',', ': '))
    print(text)

def addSingleFace(serverUrl: str, fToken: str, fSetId: str, \
    facePic: str) -> str:
    with open(facePic, "rb") as fr:
        base64_data = base64.b64encode(fr.read())
        photo64 = bytes.decode(base64_data)

    imageName = facePic.split(os.sep)[-1].split('.')[0]
    url = serverUrl + "/static-face/api/external/v1/face/" + str(fSetId)
    headers = {"content-type":"application/json", \
                "Authorization":"Bearer " + fToken}

    info = {"name":imageName, "cardId":random.randint(1, 100000), "typeId":4, \
            "sex":2, "photo":photo64}
    info = json.dumps(info)

    r = requests.post(url, data=info, headers=headers)
    """Print received information"""
    print(os.linesep)
    print("addSingleFace Http status: " + str(r.status_code))
    text = json.loads(r.text)

    try:
        getId = text["data"]["id"]

    except:
        getId = ""
        text = json.dumps(text, ensure_ascii=False, sort_keys=True, \
                    indent=4, separators=(',', ': '))
        print(text)
        print("File: " + facePic)
        print("Can't get face-id!!!")
    return str(getId)

def addFaces(serverUrl: str, fToken: str, fSetId: str, \
    folder: str, tokenMapping):
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
                    tmpStr = addSingleFace(serverUrl, fToken, fSetId, \
                                absoluteRoute)

                    if not ('' == tmpStr):
                        cntF += 1
                        tmpStr = '\"' + tmpStr + '\"' + ", \"" \
                                    + name.split('.')[0] + '\"'
                        lineList.append(tmpStr)

        with open(tokenMapping, 'w') as fw:
            for sl in lineList:
                fw.write("faceName.put(" + sl + ");" + "\r\n")
    else:
        print("No Source!!!")
        sys.exit(0)
    print("Total faces registered: " + str(cntF))

def searchFace(serverUrl: str, fToken: str, fSetId: str, \
    facePic: str, threshold: float=0.5, topk: int=3):
    with open(facePic, "rb") as fr:
        base64_data = base64.b64encode(fr.read())
        photo64 = bytes.decode(base64_data)

    imageName = facePic.split(os.sep)[-1].split('.')[0]
    url = serverUrl + "/static-face/api/external/v1/one_to_group_compare"
    headers = {"content-type":"application/json", \
                "Authorization":"Bearer " + fToken}

    info = {"image":photo64, "integrationGroupId":fSetId, \
            "minMatchingScore":threshold, \
            "maxMatchingCount":topk}
    info = json.dumps(info)

    r = requests.post(url, data=info, headers=headers)
    """Print received information"""
    print(os.linesep)
    print("SearchFace Http status: " + str(r.status_code))
    text = json.loads(r.text)

    text = json.dumps(text, ensure_ascii=False, sort_keys=True, \
                indent=4, separators=(',', ': '))
    print(text)

def delSingleFace(serverUrl: str, fToken: str, faceID: str) -> str:
    url = serverUrl + "/static-face/api/external/v1/face/" + str(faceID)
    headers = {"content-type":"application/json", \
                "Authorization":"Bearer " + fToken}

    r = requests.delete(url, headers=headers)
    """Print received information"""
    print(os.linesep)
    print("DelFaceSet Http status: " + str(r.status_code))
    text = json.loads(r.text)
    text = json.dumps(text, ensure_ascii=False, sort_keys=True, \
                    indent=4, separators=(',', ': '))
    print(text)

### Params region
"""Important!!!"""
defaultSetName = "people"

mServerUrlExt = "http://112.65.179.30:8002"
mServerUrlIner = "http://192.168.18.180:8002"

srcRoot = "/home/devin/Downloads/faceOri/all-CompSet/"
mTokenMapping = "/home/devin/Desktop/" + defaultSetName \
                + "-Tunicorn-FaceMap.txt"

### Job region
token = logIn(mServerUrlExt)

delFaceSet(mServerUrlExt, token, defaultSetName)
createFaceSet(mServerUrlExt, token, fSetName=defaultSetName)
getSetInfo(mServerUrlExt, token, defaultSetName)
addFaces(mServerUrlExt, token, defaultSetName, srcRoot, mTokenMapping)

searchFace(mServerUrlExt, token, defaultSetName, srcRoot + "黄海峰.jpg", 0.1, 2)
# delSingleFace(mServerUrlExt, token, "1293")

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
