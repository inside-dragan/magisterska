'''
Created on Oct 20, 2011

@author: dzaharie
'''
from __future__ import division
import logging
import numpy
import math

log = logging.getLogger('DataUtils')


def getFirstColumn(data):
    result = []
    for row in data:
        result.append(row[0])
    return result

def getColumn(data, i):
    result = []
    for row in data:
        result.append(row[i])
    return result

def extend(data, itemsInRow):
    result = []
    for i in range(0, len(data) - itemsInRow + 1):
        row = []
        for j in range(i, i + itemsInRow):
            row.append(data[j])
        result.append(row)
    return result

def addZeros(data, groupSize):
    zeros = []
    newData = data
    for i in range(0, len(data[0])):
        zeros.append(0)
    for i in range(1, len(data) + len(data) / groupSize):
        if (i % (groupSize + 1) == 0):
            newData.insert(i - 1, zeros) 
    return newData

def extract23Hours(data):
    d = data[1:]
    for row in d:
        time = int(row[2])
        day = int(row[1])
        if time >= 230000:
            row[2] = str(time - 230000)
        else:
            row[2] = str(time + 240000 - 230000)
            row[1] = str(day - 1)
  
def createDictionary(data):
    d = data[1:]
    total = {}
    for row in d:
        day = int(row[1])
        if total.has_key(day):
            daymap = total[day]
        else:
            daymap = {}
            total[day] = daymap
        hour = int(row[2])
        daymap[hour] = row[3]     
    return total 

def createDays(dictData, hourFrom, hourTo):    
    result = []
    days = dictData.keys()
    days.sort()
    for day in days:
        line = []
        line.append(day)
        for i in range(hourFrom, hourTo, 100):
            if (dictData[day].has_key(i)):
                line.append(dictData[day][i])
            else:
                line.append('')
        result.append(line)    
    return result;

def convertToNumbers(stringList):
    result = []
    for item in stringList:
        try:
            result.append(int(item))
        except ValueError:
            try:
                result.append(float(item))
            except ValueError:
                log.error("error parsing " + item + " to float")            
    return result

def convertToInt(data):
    result = []
    for row in data:
        r = []
        for item in row:
            r.append(int(float(item)))
        result.append(r)
    return result

def normalize(matrixData):
    counter = 0
    summ = 0
    for row in matrixData:
            for item in row:
                if item > 0:
                    counter = counter + 1
                    summ = summ + item
    
    average = summ / counter
    koef = 0.5 / average
    log.info('normalization: average value is ' + str(average) + ', multiplying by ' + str(koef))
    for i in range(0, len(matrixData)):
        for j in range(0, len(matrixData[i])):
            matrixData[i][j] = matrixData[i][j] * koef
            
def normalize0to1(listData):
    a = numpy.array(listData)
    std = a.std()
    mean = a.mean()
    result = []
    for element in listData:
        result.append(1 / (1 + math.exp((mean - element) / std)))
    return result

def getDifferences(listData, lag):
    differences = []
    for i in range(0, len(listData)):
        if i - lag < 0:
            differences.append('no-value')
        else:
            differences.append(listData[i - lag + 1] - listData[i - lag])  
    return differences

def getMovingAverage(listData, size):
    result = []
    for i in range(0, len(listData)):
        if i + 1 - size < 0:
            result.append('no-value')
        else:
            summ = 0
            for j in range(0, size):
                summ += listData[i - j]
            result.append(summ / size)
    return result

def getShifted(listData, num):
    result = []
    if num > 0:
        for i in range(0, num):
            result.append('no-value')
        result.extend(listData)
        result = result[:len(listData)]
    elif num < 0:
        result.extend(listData)
        for i in range(0, -num):
            result.append('no-value')
        result = result[-num:]       
    else:
        result = listData 
    return result

def getDifferencesOfLists(list1, list2):
    result = []
    for l1, l2 in zip(list1, list2):
        if l1 == 'no-value' or l2 == 'no-value':
            result.append('no-value')
        else:
            result.append(l2 - l1)
    return result

def getCategories(listData):
    result = []
    for l in listData:
        if l == 'no-value':
            result.append('no-value')
        elif l >=0:
            result.append(1)
        elif l < 0:
            result.append(0)
        else:
            result.append('no-value')
    return result
    
def getLnDifferences(listData, lag):
    differences = []
    for i in range(0, len(listData)):
        if i - lag < 0:
            differences.append('no-value')
        else:
            differences.append(math.log(listData[i - lag + 1] / listData[i - lag])) 
    return differences

def getMax(matrixx):
    result = matrixx[0][0]
    for row in matrixx:
        for l in row:
            if l > result:
                result = l
    return result
        
