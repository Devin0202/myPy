# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Arrange Face Recognization results with xlsx
"""
import os
import sys
import time
import subprocess
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

print(sys.version)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

### Defs region

### Params region
xlsFileR = "/home/devin/Desktop/tmp/AllData.xlsx"
indexSheet = "caseIndex"
hint = ["3m", "正", "普"]
matchRows = []
matchCases = []
wr = load_workbook(filename = xlsFileR)
print(wr.sheetnames)
if indexSheet in wr.sheetnames:
    wrs = wr[indexSheet]
    for r in range(2, wrs.max_row + 1):
        searchInfo = []
        for c in range(1, 5):
            searchInfo.append(wrs.cell(r, c).value)
        if (set(hint) == (set(searchInfo) & set(hint))):
            matchRows.append(r)

    for r in matchRows:
        for c in range(5, wrs.max_column + 1):
            matchCases.append(wrs.cell(r, c).value)
else:
    print("No case index sheet!!!")
    sys.exit(0)
print(matchCases)

xlsFileW = "/home/devin/Desktop/tmp/NewOne.xlsx"
if os.path.isfile(xlsFileW):
    ww = load_workbook(filename = xlsFileW)
else:
    ww = Workbook()
newSheet = ""
for it in hint:
    newSheet += it
wws = ww.create_sheet(newSheet, 0)
wws.column_dimensions[get_column_letter(1)].width = 31
for i in range(2, 40):
    wws.column_dimensions[get_column_letter(i)].width = 15
wws["A1"] = "视频片段编号"
wws["A2"] = "视频片段总帧数"
wws["A3"] = "测试所用帧数"
wws["A4"] = "检测有效帧数"
wws["A5"] = "识别有效次(帧)数"
wws["A6"] = "最大单帧加载耗时(ms)"
wws["A7"] = "最大单帧检测耗时(ms)"
wws["A8"] = "最大识别(含无效识别)耗时(ms)"
wws["A9"] = "最大解析耗时(ms)"
wws["A10"] = "平均单帧加载耗时(ms)"
wws["A11"] = "平均单帧检测耗时(ms)"
wws["A12"] = "平均识别(含无效识别)耗时(ms)"
wws["A13"] = "平均解析耗时(ms)"
wws["A14"] = "主观耗时(ms):首识别首检测时差"
wws["A15"] = "有效识别正确率"

for it in wr.sheetnames:
    if indexSheet == it:
        continue
    else:
        wrs = wr[it]
        for c in range(2, wrs.max_column + 1):
            if (wrs.cell(1, c).value) in matchCases:
                writeRow = 1
                writeCol = wws.max_column + 1
                for sheetCell in list(wrs.columns)[c - 1]:
                    wws.cell(writeRow, writeCol).value = sheetCell.value
                    writeRow += 1

for c in range(2, wws.max_column + 1):
    wws.cell(4, 1).value = "检测"
    wws.cell(15, 1).value = "识别"
    wws.cell(14, 1).value = "时间(ms)"
    wws.cell(16, 1).value = "得分"
    if int(wws.cell(4, c).value) > 0:
        wws.cell(4, c).value = float(1)
    else:
        wws.cell(4, c).value = float(0)

    if "NA" == wws.cell(14, c).value:
        wws.cell(14, c).value = float(0)
    else:
        wws.cell(14, c).value = float(wws.cell(14, c).value)

    if float(wws.cell(15, c).value) > 0.0:
        wws.cell(15, c).value = float(1)
    else:
        wws.cell(15, c).value = float(0)

    for r in range(16, wws.max_row + 1):
        wws.cell(16, c).value = float(0)
        if -1 != str(wws.cell(r, c).value).find("correct") \
        and 1 == wws.cell(15, c).value:
            wws.cell(16, c).value = float(wws.cell(r + 2, c).value)
            break

ww.save(xlsFileW)

print(os.linesep)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))