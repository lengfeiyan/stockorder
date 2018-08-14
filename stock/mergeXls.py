# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 12:54:50 2018

@author: lengfeiyan
"""

import xlrd
import xlwt
import os

def getFileList(path):
    fileList = []
    files = os.listdir(path)
    for f in files:
        if(os.path.isfile(path + '/' + f)):
            if f[-3:] == 'xls':
                fileList.append(f)
    return fileList

def mergeTxt(path,destFile):
    originFileList = getFileList(path)
    
    destWorkbook = xlwt.Workbook()
    destSheet = destWorkbook.add_sheet('sheet 1')
    currentRow = 0
    for originFile in originFileList:
        print(path + '/' + originFile)
        file_object = open(path + '/' + originFile,'rU',encoding='gbk')
        try: 
            for line in file_object:
                if len(line) < 6:
                    continue
                line.replace('\n','')
                lineArr = line.split('\t')
                print(lineArr)
                destSheet.write(currentRow,0,currentRow)
                destSheet.write(currentRow,1,originFile[:-4])
                destSheet.write(currentRow,2,lineArr[0])
                destSheet.write(currentRow,3,lineArr[1])
                currentRow = currentRow + 1
        finally:
            file_object.close()
            
    destWorkbook.save(destFile)
    
def mergeXls(path,destFile):
    originFileList = getFileList(path)
    
    destWorkbook = xlwt.Workbook()
    destSheet = destWorkbook.add_sheet('sheet 1')
    currentRow = 0
    for originFile in originFileList:
        print(path + '/' + originFile)
        originWorkbook = xlrd.open_workbook(path + '/' + originFile)
        originSheet = originWorkbook.sheet_by_index(0)
        rows = originSheet.get_rows()
        for row in rows:
            destSheet.write(currentRow,0,currentRow)
            destSheet.write(currentRow,1,originFile[:-4])
            destSheet.write(currentRow,2,row[0].value)
            destSheet.write(currentRow,3,row[1].value)
            currentRow = currentRow + 1
            
    destWorkbook.save(destFile)

if __name__ == '__main__':
    mergeXls('C:\\Users\\lengfeiyan\\Desktop\\新板块\\\新建文件夹','merge2.xls')
