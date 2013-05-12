'''
Created on May 13, 2012

@author: Dragan
'''
import os
from mk.dragan.data.creators.LastValuesDataCreator import LastValuesDataCreator
from mk.dragan.data.postprocessors.CatsBalanser import CatsBalanser
from mk.dragan.data.preprocessors.LnDiffPreprocessor import LnDiffPreprocessor
from mk.dragan.executors.TrainTestExecutor import TrainTestExecutor
from mk.dragan.resultgenerators.OneNodeGenerator import OneNodeGenerator
from mk.dragan.data.preprocessors.SimplePreprocessor import SimplePreprocessor

resultFolder = os.getcwd() + '/generated-result'
if not os.path.exists(resultFolder):
    os.mkdir(resultFolder) 
    
def addToFile(text):
    f = open(resultFolder + '/result.txt', 'a')
    f.write(text) 
    f.close()

periods = ['saat', 'dnevna', 'nedelna']
currencies = ['AUD-USD', 'EUR-USD', 'GBP-CHF', 'GBP-EUR', 'GBP-USD', 'EUR-CHF']

generator = OneNodeGenerator(TrainTestExecutor(6, 2))
items = []

for period in periods:
    for c in currencies:
        dataCreator = CatsBalanser(LastValuesDataCreator(LnDiffPreprocessor(c, period, directionCats=True), 
            [[5,4,3,2,1,0]], normalize=False)) 
        items.append((dataCreator, c + ' ' + period + ', so LN razlika, posledni 6 vrednosti, nenormaliziran'))
        
for period in periods:
    for c in currencies:
        dataCreator = CatsBalanser(LastValuesDataCreator(LnDiffPreprocessor(c, period, directionCats=True), 
            [[5,4,3,2,1,0]], normalize=True)) 
        items.append((dataCreator, c + ' ' + period + ', so LN razlika, posledni 6 vrednosti, normaliziran'))     
        
for period in periods:
    for c in currencies:
        dataCreator = CatsBalanser(LastValuesDataCreator(SimplePreprocessor(c, period, directionCats=True), 
            [[5,4,3,2,1,0]], normalize=False)) 
        items.append((dataCreator, c + ' ' + period + ', originalni, posledni 6 vrednosti, nenormaliziran'))
        
for period in periods:
    for c in currencies:
        dataCreator = CatsBalanser(LastValuesDataCreator(SimplePreprocessor(c, period, directionCats=True), 
            [[5,4,3,2,1,0]], normalize=True)) 
        items.append((dataCreator, c + ' ' + period + ', originalni, posledni 6 vrednosti, normaliziran'))             



for item in items:
    try:
        result = generator.generateResult(item[0])
        addToFile(item[1] + '\n')
        addToFile(result + '\n\n\n')
        print result
    except: 
        pass

