'''
Created on Oct 20, 2011

@author: dzaharie
'''
from mk.dragan.utils.CsvUtils import readFloatData, writeData, readStringData
from mk.dragan.utils.DataUtils import addZeros, getFirstColumn, extend


def createWithZerosFile(inputFile, resultFile, groupSize, delimiter=','):   
    data = readFloatData(inputFile, delimiter);
    newData = addZeros(data, groupSize)
    writeData(newData, resultFile, delimiter)

def createExtendedFile(inputFile, resultFile, itemsInRow, delimiter=','):
    twoDinput = readStringData(inputFile, delimiter)
    inputData = getFirstColumn(twoDinput)
    result = extend(inputData, itemsInRow)
    writeData(result, resultFile, delimiter)
    
def split80to20(inputFile, result80, result20, delimiter=','):
    data = readStringData(inputFile, delimiter)
    separator = len(data)*80/100
    res80 = data[:separator]
    res20 = data[separator:]
    writeData(res80, result80, delimiter)
    writeData(res20, result20, delimiter)
    
def split60to20to20(inputFile, result60, result20first, result20second, result10, delimiter=','):
    data = readStringData(inputFile, delimiter)
    
    separator1 = len(data)*60/100
    separator2 = len(data)*80/100
    
    separator10 = len(data) * 10/100
    res60 = data[:separator1]
    res20first = data[separator1:separator2]
    res20second = data[separator2:]
    res10 = data[:separator10]
    writeData(res60, result60, delimiter)
    writeData(res20first, result20first, delimiter)   
    writeData(res20second, result20second, delimiter) 
    writeData(res10, result10, delimiter)