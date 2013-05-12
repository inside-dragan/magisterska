'''
Created on Feb 21, 2012

@author: Dragan
'''
import os
import shutil

import numpy

from mk.dragan.data.ForexrateDataReader import ForexrateDataReader
from mk.dragan.utils.CsvUtils import writeData
from mk.dragan.utils.DataUtils import normalize


path = '/home/dragan/Dropbox/Magisterska/data/forexrate.co.uk/dnevna'
outPath = os.getcwd() + '/input'

if os.path.exists(outPath):
    shutil.rmtree(outPath)
os.mkdir(outPath) 
        
r = ForexrateDataReader(path + '/Bank of America.csv')

items = []
items.append([1, 2, 3, 4])
items.append([5, 6, 7, 8])
items.append([9, 10, 11, 12])
items.append([13, 14, 15, 16])
SIZE = 16

tempDirs = r.getDifferencesList(SIZE + 1)
dirs1 = []

dirsList = []
for item in items:
    dirs = []
    for i in item:
        dirs.append(tempDirs[i - 1])
    dirsList.append(dirs)


cats = r.getCategories()

for dirs in dirsList:
    for i in range(0, len(dirs)):
        dirs[i] = dirs[i][SIZE:-1]

for dirs in dirsList:  
    normalize(dirs)
cats = cats[SIZE:-1]

inputs = []
for dirs in dirsList:
    inputs.append(numpy.transpose(dirs))
o = numpy.transpose([cats])

if len(inputs) == 1:
    writeData(inputs[0], outPath + '/input.csv')
else:
    for i, inputData in enumerate(inputs):
        writeData(inputData, outPath + '/input' + str(i + 1) + '.csv')
writeData(o, outPath + '/cat.csv')  
