'''
Created on Oct 1, 2011

@author: dzaharie
'''
import csv
import logging
import os
from mk.com.dragan.utils.StringUtils import rbefore

log = logging.getLogger('CsvUtils')

def getNumLines(filePath):
    f = open(filePath)
    result = sum(1 for line in f)
    f.close()
    return result

def readFloatData(filePath, delimiter = ','):
    result = []
    f = open(filePath)
    reader = csv.reader(f, delimiter=delimiter)
    for row in reader:
        r = []
        for item in row:
            try:
                r.append(int(item))
            except ValueError:
                try:
                    r.append(float(item))
                except ValueError:
                    log.error("error parsing " + item + " to float")
        result.append(r)
    f.close()
    return result

def readIntData(filePath, delimiter = ','):
    result = []
    f = open(filePath)
    reader = csv.reader(f, delimiter=delimiter)
    for row in reader:
        r = []
        for item in row:
            try:
                r.append(int(item))
            except ValueError:
                log.error("error parsing " + item + " to int")
        result.append(r)
    f.close()
    return result

def readStringData(filePath, delimiter = ','):
    result = []
    f = open(filePath)
    reader = csv.reader(f, delimiter=delimiter)
    for row in reader:
        r = []
        for item in row:
            r.append(item)
        result.append(r)
    f.close()
    return result

def writeData(data, filePath, delimiter = ','):
    path = rbefore(filePath, '/')
    if not os.path.exists(path):
        os.makedirs(path)
    out = open(filePath, 'wb')
    writer = csv.writer(out, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
    for line in data:
        writer.writerow(line)    
    out.close()

def stripFile(filePath):
    f = open(filePath)
    out = open('stripFile_temp', 'wb')
    for line in f:
        out.write(line.strip() + '\n')
    f.close()
    out.close()
    os.remove(filePath)
    os.rename('stripFile_temp', filePath)
    
def isNullArray(stringArray):
    for element in stringArray:
        try:
            element = float(element)
            if element != 0.0:
                return False
        except ValueError:
            return False
    return True
        