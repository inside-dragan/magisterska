'''
Created on Jun 10, 2012

@author: dzaharie
'''
import os
import time
from mk.com.dragan.data.creators.ListMovingAveragesDataCreator import ListMovingAveragesDataCreator
from mk.com.dragan.data.postprocessors.CatsBalanser import CatsBalanser
from mk.com.dragan.data.preprocessors.LnDiffPreprocessor import LnDiffPreprocessor
from mk.com.dragan.nupic.config.Params import Params
from mk.com.dragan.nupic.executors.TrainTestTwoLevelsExecutor import TrainTestTwoLevelsExecutor
from mk.com.dragan.nupic.result_generators.TwoLevelsGenerator import TwoLevelsGenerator


def addToFile(text):
    resultFolder = os.getcwd() + '/generated-result'
    if not os.path.exists(resultFolder):
        os.mkdir(resultFolder)     
    f = open(resultFolder + '/result.txt', 'a')
    f.write(text) 
    f.close()
    
Params().BOTTOM_UP_OUT = 300
Params().BOTTOM_UP_OUT_2 = 300

#periods = ['dnevna']
periods = ['saat', 'dnevna']
currencies = ['AUD-USD', 'EUR-USD', 'GBP-CHF', 'GBP-EUR', 'GBP-USD', 'EUR-CHF']
#currencies = ['AUD-USD']
averages = [((6, 5, 4, 3, 2, 1), (10, 8, 6, 4, 2, 1), (13, 9, 6, 4, 2, 1), (32, 16, 8, 4, 2, 1),
            (19, 13, 9, 5, 3, 2), (18, 12, 8, 4, 2, 1), (15, 12, 9, 6, 3, 1), (20, 16, 8, 4, 2, 1))]

executor = TrainTestTwoLevelsExecutor(inputSize=6, numCategories=2, numLevel1=8, numLevel2=2)
generator = TwoLevelsGenerator(executor, numNodesLevel1=8, numNodesLevel2=2)
items = []

startTime = time.time()
for average in averages:
    for period in periods:
        for c in currencies:
            dataCreator = CatsBalanser(ListMovingAveragesDataCreator(LnDiffPreprocessor(c, period, directionCats=True),
                average, normalize=True)) 
            items.append((dataCreator, c))  

for item in items:
    result = generator.generateResult(item[0], item[1])
    info = dataCreator.getDescription()
    print 'tesing combination: ' + item[1] + ' ' + str(info)
    addToFile(item[1] + ' ' + str(info) + '\n')
    addToFile(result + '\n\n\n')
    print result     


endTime = time.time()
print 'execution time: ' + str(endTime - startTime)