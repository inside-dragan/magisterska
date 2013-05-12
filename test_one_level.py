'''
Created on May 13, 2012

@author: Dragan
'''
from mk.dragan.data.creators.ListMovingAveragesDataCreator import \
    ListMovingAveragesDataCreator
from mk.dragan.data.postprocessors.CatsBalanser import CatsBalanser
from mk.dragan.data.preprocessors.LnDiffPreprocessor import LnDiffPreprocessor
from mk.dragan.executors.TrainTestOneLevelExecutor import \
    TrainTestOneLevelExecutor
from mk.dragan.resultgenerators.OneLevelGenerator import OneLevelGenerator


#periods = ['dnevna']
periods = ['saat']
currencies = ['AUD-USD', 'EUR-USD', 'GBP-CHF', 'GBP-EUR', 'GBP-USD', 'EUR-CHF']
#currencies = ['AUD-USD']
averages = [((6, 5, 4, 3, 2, 1), (10, 8, 6, 4, 2, 1), (12, 9, 6, 4, 2, 1), (32, 16, 8, 4, 2, 1)),
            ((6, 5, 4, 3, 2, 1), (18, 12, 8, 4, 2, 1), (15, 12, 9, 6, 3, 1), (20, 16, 8, 4, 2, 1))]

executor = TrainTestOneLevelExecutor(inputSize=6, numCategories=2, numNodes=4)
generator = OneLevelGenerator(executor, numNodes=4)
dataCreators = []

for average in averages:
    for period in periods:
        for c in currencies:
            dataCreator = CatsBalanser(ListMovingAveragesDataCreator(LnDiffPreprocessor(c, period, directionCats=True),
                average, normalize=True)) 
            dataCreators.append(dataCreator)  

for dataCreator in dataCreators:
    generator.generateResult(dataCreator)

