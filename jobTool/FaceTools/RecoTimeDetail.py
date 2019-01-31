# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Statistics of single face recognition time
"""
import sys
import os
import time

import matplotlib
import matplotlib.pyplot as plt

### Definition region(Class, Functions, Constants)
class SetInfo:
    def __init__(self, fName):
        self.obj = fName
        self.filesList = []
        self.recoFrameId = []
        self.recoInfoDict = {}
        self.timeInfoDict = {}
        self.calcInfoDict = {}

    def addFile(self, fFile):
        self.filesList.append(fFile)

    def addFrameId(self, fId):
        self.recoFrameId.append(fId)

    def addRecoInfoDict(self, fLine):
        try:
            frameId = fLine.split(' ')[1]
        except BaseException:
            print("Error line:")
            print(fLine)
        else:
            if frameId in self.recoFrameId:
                if frameId in self.recoInfoDict.keys():
                    pass
                else:
                    self.recoInfoDict[frameId] = []
                self.recoInfoDict[frameId].append(fLine)
            else:
                pass

def getLogSet(fRootDir, fOnes):
    rootDir = fRootDir + os.path.sep
    if os.path.exists(rootDir):
        pass
    else:
        print("No source!!!")
        sys.exit(0)

    setDict = {}
    for rt, dirs, files in os.walk(rootDir):
        for i in files:
            file = os.path.join(rt, i)
            for name in fOnes:
                if name in setDict.keys():
                    pass
                else:
                    newSet = SetInfo(name)
                    setDict[name] = newSet

                tmp = os.path.sep + name + os.path.sep
                if (-1 != file.find(tmp)):
                    setDict[name].addFile(file)
                else:
                    pass
    return setDict

def getSetInfo(fSetDict):
    setDict = fSetDict
    for key in setDict.keys():
        tmpLines = []
        for file in setDict[key].filesList:
            with open(file, 'r') as fr:
                tmpLines.extend(fr.readlines())

        for line in tmpLines:
            if -1 != line.find(" status: recoStart"):
                setDict[key].addFrameId(line.split(' ')[1])
            else:
                pass

        for line in tmpLines:
            setDict[key].addRecoInfoDict(line)
    return setDict

def getTimeInfo(fSetDict):
    setDict = fSetDict
    patternList = [" status: recoStart", " Http connect start", \
    " Http connect end", " requestID = ", " Http post start", \
    " Http getResponseCode ", " Http post end", " requestID: ", \
    " status: Http Response", " status: recoEnd", " status: detectEnd "]
    for key in setDict.keys():
        for fid in setDict[key].recoInfoDict.keys():
            tmpLines = setDict[key].recoInfoDict[fid]
            timeInfo = []
            calCost = None

            for i in range(0, len(patternList)):
                for line in tmpLines:
                    if -1 != line.find(patternList[i]):
                        strNum = line.split("|D||")[0]
                        timeInfo.append(int(strNum))
                    else:
                        pass

                    if -1 != line.find(" faceTimeConsume: "):
                        calCost = line.split(" faceTimeConsume: ")[1].split(' ')[0]
                        calCost = int(float(calCost) * 1000)
                    else:
                        pass

            timeInfo.append(calCost)
            # print(fid)
            # print(timeInfo)
            setDict[key].timeInfoDict[fid] = timeInfo
    return setDict

def calcTimeInfo(fSetDict):
    setDict = fSetDict
    for key in setDict.keys():
        for fid in setDict[key].timeInfoDict.keys():
            if (12 != len(setDict[key].timeInfoDict[fid])):
                pass
            else:
                tmpDict = {}
                tmpList = setDict[key].timeInfoDict[fid]
                tmpDict["detectEnd-recoStart"] = tmpList[0] - tmpList[10]
                tmpDict["recoStart-http connection start"] = tmpList[1] - tmpList[0]
                tmpDict["http connection cost"] = tmpList[2] - tmpList[1]
                tmpDict["connection end-post start"] = tmpList[4] - tmpList[2]
                tmpDict["post cost"] = tmpList[5] - tmpList[4]
                tmpDict["post end-recoEnd"] = tmpList[9] - tmpList[5]
                tmpDict["reco cost"] = tmpList[9] - tmpList[0]
                tmpDict["post without cloudcalc"] = tmpDict["post cost"] - tmpList[11]
                setDict[key].calcInfoDict[fid] = tmpDict
    return setDict

def printBar(fSetDict, fResultDir, fRangeDef):
    setDict = fSetDict
    resultDir = fResultDir + os.path.sep
    drawInfoTotal = {}
    for key in setDict.keys():
        drawInfo = {}
        drawMaxInfo = {}
        print("LogDir: " + str(key))
        for key1 in setDict[key].calcInfoDict.keys():
            for key2, value in setDict[key].calcInfoDict[key1].items():
                if key2 in drawInfoTotal.keys():
                    pass
                else:
                    drawInfoTotal[key2] = []

                if key2 in drawInfo.keys():
                    pass
                else:
                    drawInfo[key2] = []
                if key2 in drawMaxInfo.keys():
                    pass
                else:
                    drawMaxInfo[key2] = []

                drawInfoTotal[key2].append(value)
                drawInfo[key2].append(value)
                drawMaxInfo[key2].append(key1)

                # if ("626880461" == key1):
                #     print(key2)
                #     print(value)

        for key3 in drawInfo.keys():
            saveFile = resultDir + "TotalInfo.txt"
            if not os.path.exists(resultDir):
                os.makedirs(resultDir)
            else:
                pass

            with open(saveFile, 'a') as fw:
                tmpS = "LogDir: " + str(key)
                print(tmpS, file = fw)
                tmpS = "Stage: " + str(key3)
                print(tmpS, file = fw)
                print(tmpS)
                tmpS = "frameId: " \
                + str(drawMaxInfo[key3][drawInfo[key3].index(max(drawInfo[key3]))])
                print(tmpS, file = fw)
                print(tmpS)
                tmpS = "Max time cost: " + str(max(drawInfo[key3])) + " ms"
                print(tmpS, file = fw)
                print(tmpS)
                tmpS = "\r\n"
                print(tmpS, file = fw)
                print()

            saveDir = resultDir + key + os.path.sep
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)
            else:
                pass
            canvas = plt.figure()
            chart = canvas.add_subplot(111)
            rect = chart.bar(range(len(drawInfo[key3])), drawInfo[key3])
            plt.grid(axis = "y", linestyle = "-.")
            listSum = 0
            for i in drawInfo[key3]:
                listSum += i
            x = plt.gca().xaxis.get_ticklocs()
            avg = round(listSum / len(drawInfo[key3]), 2)
            y = [avg for i in range(len(x))]
            plt.plot(x, y, linewidth = 2, color = 'r')
            plt.annotate(str(avg), (x[0], y[0] + max(drawInfo[key3]) / 20), \
                            fontsize = 10)
            chart.set_title(key3, fontsize = 10, bbox = {'facecolor':'0.8', 'pad':2})
            plt.xlabel("Number Of Samples", fontsize = 10)
            plt.ylabel("Time Cost (ms)", fontsize = 10)
            plt.savefig(saveDir + key3 + ".jpg")
            plt.close()
            # plt.show()

    saveDir = resultDir + "TotalBarGraph" + os.path.sep
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    else:
        pass
    saveFile = resultDir + "TotalInfo.txt"
    if not os.path.exists(resultDir):
        os.makedirs(resultDir)
    else:
        pass
    print("LogDir: TotalInfo")
    for key3 in drawInfoTotal.keys():
        rangeList = fRangeDef[key3]
        binList = [0 for _ in range(len(rangeList))]
        for i in drawInfoTotal[key3]:
            if rangeList[0] <= i and rangeList[1] > i:
                binList[0] += 1
            elif rangeList[1] <= i and rangeList[2] > i:
                binList[1] += 1
            elif rangeList[2] <= i and rangeList[3] > i:
                binList[2] += 1
            elif rangeList[3] <= i and rangeList[4] > i:
                binList[3] += 1
            elif rangeList[4] <= i and rangeList[5] > i:
                binList[4] += 1
            elif rangeList[5] <= i and rangeList[6] > i:
                binList[5] += 1
            elif rangeList[6] <= i:
                binList[6] += 1
        canvas = plt.figure(figsize = (10, 5))
        chart = canvas.add_subplot(111)
        rect = chart.bar(range(len(binList)), binList, 0.5, \
            tick_label = [str(rangeList[0]) + '-' + str(rangeList[1]), \
                        str(rangeList[1]) + '-' + str(rangeList[2]), \
                        str(rangeList[2]) + '-' + str(rangeList[3]), \
                        str(rangeList[3]) + '-' + str(rangeList[4]), \
                        str(rangeList[4]) + '-' + str(rangeList[5]), \
                        str(rangeList[5]) + '-' + str(rangeList[6]), \
                                            '>' + str(rangeList[6])])
        plt.xlabel("Distribution (ms)", fontsize = 10)
        plt.ylabel("Count", fontsize = 10)
        chart.set_title(key3 + "\nDistribution", \
            fontsize = 10, bbox = {'facecolor':'0.8', 'pad':4})
        for x,y in zip(range(len(binList)), binList):
            plt.text(x, y, '%.d' %y, ha = "center",va = "bottom")

        plt.savefig(saveDir + key3 + "-Distribution" + ".jpg")
        plt.close()

        canvas = plt.figure(figsize = (60, 15))
        chart  = canvas.add_subplot(111)
        rect = chart.bar(range(len(drawInfoTotal[key3])), \
            drawInfoTotal[key3], 5)
        plt.xlabel("Number Of Samples", fontsize = 40)
        plt.ylabel("Time Cost (ms)", fontsize = 40)
        chart.set_title(key3, fontsize = 40, \
            bbox = {'facecolor':'0.8', 'pad':5})
        plt.grid(axis = "y", linestyle = "-.")

        listSum = 0
        for i in drawInfoTotal[key3]:
            listSum += i
        x = plt.gca().xaxis.get_ticklocs()
        avg = round(listSum / len(drawInfoTotal[key3]), 2)
        y = [avg for i in range(len(x))]
        plt.plot(x, y, linewidth = 5, color = 'r')
        plt.annotate(str(avg), (x[0], y[0] + max(drawInfo[key3]) / 20), \
                    fontsize = 40)

        plt.savefig(saveDir + key3 + ".jpg")
        plt.close()

        with open(saveFile, 'a') as fw:
            tmpS = "LogDir: TotalInfo" 
            print(tmpS, file = fw)
            tmpS = "Stage: " + str(key3)
            print(tmpS, file = fw)
            print(tmpS)
            tmpS = "Max time cost: " + str(max(drawInfoTotal[key3])) + " ms"
            print(tmpS, file = fw)
            print(tmpS)
            tmpS = "\r\n"
            print(tmpS, file = fw)
            print()

def printInfo(fSetDict):
    setDict = fSetDict
    for key in setDict.keys():
        print(key)
        for fid in setDict[key].recoInfoDict.keys():
            if (12 != len(setDict[key].timeInfoDict[fid])):
                print(fid)
                print(len(setDict[key].recoInfoDict[fid]))
                print(len(setDict[key].timeInfoDict[fid]))
                print("Wrong")
            else:
                for key1 in setDict[key].calcInfoDict.keys():
                    print(key1)
                    for key2, value in setDict[key].calcInfoDict[key1].items():
                        print('{key}:{value}'.format(key = key2, value = value))

            # for line in setDict[key].recoInfoDict[fid]:
            #     print(line, end = '')
            # for line in setDict[key].timeInfoDict[fid]:
            #     print(line)

if "__main__" == __name__:
    print(sys.version)
    timeStampFormat = "%Y-%m-%d %H:%M:%S"
    print(time.strftime(timeStampFormat, time.localtime()))
### Parameters region
    cRangeDef = {
            "detectEnd-recoStart" : [0, 400, 800, 1200, 1600, 2000, 2400], \
            "recoStart-http connection start" : [0, 10, 20, 30, 40, 50, 60], \
            "http connection cost" : [0, 10, 60, 100, 300, 1000, 3000], \
            "connection end-post start" : [0, 10, 20, 30, 40, 50, 60], \
            "post cost" : [0, 400, 800, 1200, 1600, 2000, 2400], \
            "post end-recoEnd" : [0, 10, 20, 30, 40, 50, 60], \
            "reco cost" : [0, 400, 800, 1200, 1600, 2000, 2400], \
            "post without cloudcalc" : [0, 200, 400, 800, 1600, 2000, 2400] \
    }
    cResultDir = "/home/devin/Desktop/G200/TmpTest/"
    cLogDir = "/home/devin/Desktop/G200/httpTest/1/"
    cAnalysisOnes = ["daiyi", "peiyi", "baoyuandong", "sunhaiyan", \
                    "xinglj", "zhuyawen", "yukeke", "guangming", "yanchangjian"]
### Job region
    result = getLogSet(cLogDir, cAnalysisOnes)
    result = getSetInfo(result)
    result = getTimeInfo(result)
    result = calcTimeInfo(result)
    printBar(result, cResultDir, cRangeDef)

    print(os.linesep)
    print(time.strftime(timeStampFormat, time.localtime()))