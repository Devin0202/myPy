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
from urllib3 import encode_multipart_formdata
import openpyxl
from PIL import Image
import shutil

print(sys.version)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

### Defs region
def logInHiscene(serverUrl: str) -> str:
    url = serverUrl + "/manage/login"
    header = {"Content-Type":"application/x-www-form-urlencoded"}
    info = {"account":"admin", "password":"e97f532c556698e8845e0661f807af86"}
    # info = json.dumps(info)
    r = requests.post(url, data=info, headers=header)

    """Print received information"""
    print(os.linesep)
    print("Log-in Http status: " + str(r.status_code))
    text = json.loads(r.text)
    print(text)
    return r.cookies

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
        print(text)
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

errorList = []
def addSingleFaceHiscene(serverUrl: str, facePic: str, cookies, parseStr=None) -> str:
    imgFormat = whatFormat(facePic)
    if "PNG" == imgFormat:
        file = ("facepic.png", open(facePic, 'rb'), "image/png")
    elif 'JPEG' == imgFormat:
        file = ("facepic.jpeg", open(facePic, 'rb'), "image/jpeg")
    else:
        print("Error image type")
        sys.exit(0)

    print(os.path.basename(facePic))

    if None == parseStr:
        #picName = facePic.split(os.sep)[-1].split('.')[0].split()
        picName = os.path.basename(facePic).split('.')[0].split()
        print(picName)
        if 4 == len(picName):
            categoryID = picName[0]
            imageName = picName[1]
        else:
            categoryID = "None"
            imageName = picName[0]
        sexID = picName[-2]
        cardId = picName[-1]
    else:
        imageName = parseStr
        categoryID = "上海化学工业园"
        cardId = os.path.basename(facePic) + ' ' + time.strftime('%d-%H:%M:%S', time.localtime())
        sexID = "Unknown"
        enterprise = gEnterprise

    url = serverUrl + "/manage/faces/add?etpid=" + enterprise
    header = {"Content-Type":"multipart/form-data"}

    # multipart_encoder = MultipartEncoder(
    #     fields = {
    #         "name":imageName, \
    #         "category":categoryID, \
    #         "idNumber":cardId, \
    #         "gender":sexID, \
    #         "enterpriseID":"f943751cf049e21505010001", \
    #         # "hasCriminalRecord":0, \
    #         "face":('pic', open(facePic, 'rb'), 'image/jpeg')
    #     }
    # )

    info = {"name":(None, imageName), \
            "category":(None, categoryID), \
            "idNumber":(None, cardId), \
            "gender":(None, sexID), \
            "enterpriseID":(None, enterprise), \
            "hasCriminalRecord":(None, 0), \
            "face":file \
            }
    # info = json.dumps(info)
    # info = encode_multipart_formdata(info)

    r = requests.post(url, files=info, cookies=cookies)
    """Print received information"""
    # print(r.request.body.decode())
    # state = json.loads(r.text)
    print(os.linesep)
    print("addSingleFace Http status: " + str(r.status_code))
 
    # print(r.text)
    if -1 != r.text.find("入库失败"):
        errorList.append("入库失败: " + imageName + '\t' + facePic)
    
    if not searchFace(gServerUrlExt, gToken, gDefaultSetName, facePic, 0.95, 1):
        errorList.append("入库失败: " + imageName + '\t' + facePic)

    # if "202B017740.jpg" in facePic:
    #     global trig
    #     trig = True
    if trig:
        print("File: " + facePic)
        # target = facePic.replace("/017/", "/017ex/")
        # shutil.copyfile(facePic, target)
    return

def addSingleFace(serverUrl: str, fToken: str, fSetId: str, \
    facePic: str) -> str:
    with open(facePic, "rb") as fr:
        base64_data = base64.b64encode(fr.read())
        photo64 = bytes.decode(base64_data)

    picName = facePic.split(os.sep)[-1].split('.')[0].split()
    if 4 == len(picName):
        imageName = picName[0] + picName[1]
    else:
        imageName = picName[0]
    sexID = 2 if "女" == picName[-2] else 1
    cardId = int(picName[-1])

    url = serverUrl + "/static-face/api/external/v1/face/" + str(fSetId)
    headers = {"content-type":"application/json", \
                "Authorization":"Bearer " + fToken}

    info = {"name":imageName, "cardId":cardId, "typeId":4, \
            "sex":sexID, "photo":photo64}
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

def whatFormat(filename):
    try:
        i = Image.open(filename)
        if "PNG" != i.format and 'JPEG' != i.format:
            print("Not png and jpeg")
        return i.format
    except IOError:
        print("Error image type")
        sys.exit(0)

def formatParse(line: str, kv):
    if None == line:
        print("Image name error!!!")
        sys.exit(0)
    else:
        index = line.split(os.path.sep)[-2] + line.split(os.path.sep)[-1].split('.')[0]
        if index in kv.keys():
            name = kv[index]
            return name
        else:
            return None

def excelLoad(filePath: str):
    if None == filePath:
        print("Excel path error!!!")
        sys.exit(0)
    else:
        dt = {}
        wb = openpyxl.load_workbook(filePath)
        sheet = wb['Sheet1']
        lineNum = 0
        for row in sheet.rows:
            lineNum += 1
            if 3 > lineNum:
                continue
            else:
                pass
            cellNum = 0
            for cell in row:
                cellNum += 1
                if 4 > cellNum:
                    continue
                elif 4 == cellNum:
                    name = str(cell.value)
                elif 5 == cellNum:
                    idx = cell.value.split(os.path.sep)[-2] + cell.value.split(os.path.sep)[-1].split('.')[0]
                    idx = str(idx)
                else:
                    pass
            dt[idx] = name
            print(name + ' ' + idx)
        print("Total lines: " + str(lineNum))
        return dt

def addFaces(serverUrl: str, fToken: str, fSetId: str, \
    folder: str, tokenMapping, cookies, kv=None):
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
                    tmpStr = None
                    info = None
                    if True:
                        info = formatParse(absoluteRoute, kv)
                        if None == info:
                            continue
                        print(info)
                        cntF += 1
                    
                    # tmpStr = addSingleFace(serverUrl, fToken, fSetId, \
                    #             absoluteRoute)
                    addSingleFaceHiscene(serverUrl, absoluteRoute, cookies, info)
                    if None != tmpStr:
                        cntF += 1
                        tmpStr = '\"' + tmpStr + '\"' + ", \"" \
                                    + name.split('.')[0] + '\"'
                        lineList.append(tmpStr)

        if [] != lineList:
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
    # print(text)

    if -1 != text.find("\"success\": false"):
        return False
    else:
        return True

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
trig = False
"""Important!!!"""
defaultSetName = "test0423"

mServerUrlExt = "https://tunicorn.aryun.com"
mServerUrlIner = "http://61.159.136.195:8092"

excelLoc = "/media/devin/OpenImage600/tmp/index.xlsx"

srcRoot = "/media/devin/OpenImage600/tmp/20200316_result/"
# srcRoot = "C:/Users/user/Desktop/1111/test/rlnew/"

dst = "/home/devin/Desktop/"
# dst = "C:/Users/user/Desktop/1111/"

mTokenMapping = dst + defaultSetName + "-Tunicorn-FaceRecord.txt"

### Job region
gServerUrlExt = "http://112.65.179.30:8002"
gToken = logIn(gServerUrlExt)

gDefaultSetName = "7"
gEnterprise = "12bce1f5ce1b081605010001"

# delFaceSet(mServerUrlExt, token, defaultSetName)
# createFaceSet(mServerUrlExt, token, fSetName=defaultSetName)
# getSetInfo(mServerUrlExt, token, defaultSetName)
# addFaces(mServerUrlExt, token, defaultSetName, srcRoot, mTokenMapping)

# searchFace(mServerUrlExt, token, defaultSetName, srcRoot + "黄海峰.jpg", 0.1, 2)
# delSingleFace(mServerUrlExt, token, "1293")


kvDict = excelLoad(excelLoc)
myCookies = logInHiscene(mServerUrlExt)
addFaces(mServerUrlExt, "", defaultSetName, srcRoot, mTokenMapping, \
    cookies = myCookies, kv = kvDict)

if [] != errorList:
    with open(mTokenMapping, 'w') as fw:
        for sl in errorList:
            fw.write(sl + '\n')

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
