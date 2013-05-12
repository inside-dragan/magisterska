'''
Created on Dec 6, 2011

@author: dzaharie
'''
import numpy

from mk.dragan.utils.CsvUtils import readStringData, writeData, readFloatData
from mk.dragan.utils.DataUtils import createDays, createDictionary, convertToInt
from mk.dragan.utils.loggingDef import logging


log = logging.getLogger('Create Data') 



def createRowPerDay(inputFile, resultFile, starttime, endtime):
    data = readStringData(inputFile)
    s = createDictionary(data)
    daysRaw = createDays(s, starttime, endtime)
    
    #fill enpty cells with value from the previous cell
    for day in daysRaw:
        for i in range(2, len(day)):
            if day[i] == '':
                day[i] = day[i-1]
    
    #remove days without data (usually weekends)
    days = []
    for day in daysRaw:
        if not '' in day:
            days.append(day)
    writeData(days, resultFile)#'/row-per-day.csv'
    log.info('file with one row per day created.')


def readCategories(categoriesFile):
    categories = {}
    catData = readStringData(categoriesFile)
    catData = catData[1:]
    for row in catData:
        try:
            day = int(row[1])
            cat = int(row[10])
            categories[day] = cat
        except ValueError: 
            #do nothing, there will be not category for this day
            pass
    return categories

def addCategories(rowPerDayFile, categoriesDict, resultFile):
    days = readStringData(rowPerDayFile)
    result = []
    for row in days:
        day = int(row[0])
        if categoriesDict.has_key(day):
            row.append(categoriesDict[day])
            result.append(row)
    
    writeData(result, resultFile)
    log.info('file with one row per day plus categories created.')
    
def transpose(rowPerDayCatsFile, size, resultFile):
    data = readFloatData(rowPerDayCatsFile)
    items = []
    for i in range(0, len(data) - size):
        part = []
        for j in range(0, size):
            part.append(data[i + j])
        items.append(part)
        
    newItems = []
    for data in items:
        data = numpy.transpose(data)
        category = data[len(data) - 1][len(data[0]) - 1]
        timeInterval = str(int(data[0][0])) + ' - ' + str(int(data[0][len(data[0]) - 1]))
        data = data[1:len(data) - 1]
        newData = []
        for row in data:
            newRow = row.tolist()
            newRow.append(category)
            newRow.insert(0, timeInterval)
            newData.append(newRow)
        newItems.append(newData)
        
    zeroLine = [' ']
    for i in range(0, size + 1):
        zeroLine.append(0)
        
    result = []
    for item in newItems:
        for row in item:
            result.append(row)
        result.append(zeroLine)      
        
    writeData(result, resultFile)
    log.info('input file with unmodified values created.')
    
    
def modifyToDifferencesToLast(inputFile, resultFile):
    data = readStringData(inputFile)
    
    for row in data:
        if row[0]:
            end = len(row) - 2
            for i in range(1, end):
                row[i] = (float(row[end]) - float(row[i])) / (end - i)
            del(row[end])
    log.info('input file with differences to last item divided by the distance created.')
    writeData(data, resultFile) 
    
def normalize(inputFile, resultFile):   
    data = readStringData(inputFile)
    transposed = numpy.transpose(data)
    result = transposed[1:len(transposed) - 1]
    
    
    result = convertToFloat(result)
    counter = 0
    summ = 0
    for row in result:
        if (row[0]):
            for item in row:
                if item > 0:
                    counter = counter + 1
                    summ = summ + item
    
    average = summ / counter
    koef = 0.5 / average
    log.info('normalization: average value is ' + str(average) + ', multiplying by ' + str(koef))
    for i in range(0, len(result)):
        for j in range(0, len(result[i])):
            result[i][j] = result[i][j] * koef
        
    result.insert(0, transposed[0])
    result.append(transposed[len(transposed) - 1])
    result = numpy.transpose(result)
    writeData(result, resultFile)
    
def createInputCat(inputFile, resultInput, resultCat):
    data = readStringData(inputFile)
    data = numpy.transpose(data)
    inputData = data[1:len(data) - 1]
    inputData = numpy.transpose(inputData)
    for i in range(0, len(inputData)):
        for j in range(0, len(inputData[i])):
            if inputData[i][j] == '0.0':
                inputData[i][j] = '0'
    
    writeData(inputData, resultInput)
    log.info('input.csv file created')
    catData = [data[len(data) - 1]]
    catData = numpy.transpose(catData)
    catData = convertToInt(catData)
    writeData(catData, resultCat)
    log.info('cat.csv file created')
    
    
    
    
    
inputFile = 'C:/Users/dzaharie/Dropbox/Magisterska/data/forextester.com/EURUSD/EURUSD-07-08.csv'
path = 'C:/Users/dzaharie/Dropbox/Magisterska/analizi/cetvrta/2007-2008/4x3'
categoriesFile = 'C:/Users/dzaharie/Dropbox/Magisterska/data/forextester.com/EURUSD/per-day-categories.csv'


createRowPerDay(inputFile, path + '/row-per-day.csv', 120000, 125900)
categories = readCategories(categoriesFile)
addCategories(path + '/row-per-day.csv', categories, path + '/row-per-day-with-cats.csv')
transpose(path + '/row-per-day-with-cats.csv', 13, path + '/input-original-values.csv')
modifyToDifferencesToLast(path + '/input-original-values.csv', path + '/input-differences.csv')
normalize(path + '/input-differences.csv', path + '/input-diff-normalized.csv')
createInputCat(path + '/input-diff-normalized.csv', path + '/input.csv', path + '/cat.csv')

