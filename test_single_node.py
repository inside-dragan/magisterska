'''
Created on Jun 6, 2012

@author: Dragan
'''
from mk.dragan.data.creators.ListMovingAveragesDataCreator import \
    ListMovingAveragesDataCreator
from mk.dragan.data.postprocessors.CatsBalanser import CatsBalanser
from mk.dragan.data.preprocessors.LnDiffPreprocessor import LnDiffPreprocessor
from mk.dragan.executors.TrainTestExecutor import TrainTestExecutor
from mk.dragan.resultgenerators.OneNodeGenerator import OneNodeGenerator

periods = ['saat', 'dnevna']
currencies = ['AUD-USD', 'EUR-USD', 'GBP-CHF', 'GBP-EUR', 'GBP-USD', 'EUR-CHF']
averages = [(20, 12, 8, 4, 2, 1), (6, 5, 4, 3, 2, 1), (32, 16, 8, 4, 2, 1), (9, 6, 4, 3, 2, 1)]

generator = OneNodeGenerator(TrainTestExecutor(6, 2))
items = []

for average in averages:  
    for period in periods:
        for c in currencies:
            dataCreator = CatsBalanser(ListMovingAveragesDataCreator(LnDiffPreprocessor(c, period, directionCats=True),
                [average], normalize=True)) 
            items.append(dataCreator)     

for item in items:
    generator.generateResult(item)

