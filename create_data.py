'''
Created on May 10, 2012

@author: dzaharie
'''
import os
import shutil

#import matplotlib.pyplot as plt
from mk.com.dragan.data.creators.LastValuesDataCreator import LastValuesDataCreator
from mk.com.dragan.data.postprocessors.SimpleCatBalanser import SimpleCatsBalanser
from mk.com.dragan.data.preprocessors.LnDiffPreprocessor import LnDiffPreprocessor
from mk.com.dragan.data.readers.ForexRateNewFormatReader import ForexRateNewFormatReader
from mk.com.dragan.utils.CsvUtils import writeData


outPath = os.getcwd() + '/input'

if os.path.exists(outPath):
    shutil.rmtree(outPath)
os.mkdir(outPath)

#n = LastValuesDataCreator(LnDiffPreprocessor(f, directionCats=True), 
#    [[5,4,3,2,1,0]], normalize=True)

currencies = ['AUD-CAD', 'AUD-CHF', 'AUD-JPY', 'AUD-USD', 'CAD-CHF', 'CAD-JPY',
              'EUR-AUD', 'EUR-CHF', 'EUR-GBP', 'EUR-USD', 'GBP-AUD', 'GBP-CAD',
              'GBP-CHF', 'GBP-JPY', 'GBP-USD', 'USD-CAD', 'USD-JPY']


def merge_with(d1, d2):
    res = d1.copy() # "= dict(d1)" for lists of tuples
    for key, val in d2.iteritems(): # ".. in d2" for lists of tuples
        try:
            res[key].append(val)
        except KeyError:
            res[key] = [val]
    return res

dateCatDict = {}
for c in currencies:
    dataReader = ForexRateNewFormatReader(c, 'saat')
    n = LastValuesDataCreator(LnDiffPreprocessor(dataReader, directionCats=True),
                                           [(5, 4, 3, 2, 1, 0)], normalize=True)
    dateCatDict = merge_with(dateCatDict, n.getCatWithDatesDict())


resultList = []

def createWithLetterCategory(row):
    result = row[:]
    if result[-1] == 0:
        result[-1] = 'A'
    elif result[-1] == 1:
        result[-1] = 'B'
    else: raise
    return result
for v in dateCatDict.values():
    if len(v) == len(currencies):
       resultList.append(createWithLetterCategory(v))

balanser = SimpleCatsBalanser()
resultList = balanser.getBalansed(resultList)
resultList.insert(0, currencies)
writeData(resultList, outPath + '/input1.csv', delimiter=',')

# inputMatrix = []
# length = min([len(element) for element in inputList])
# for i in range(0, length):
#     row = []
#     for currencyValues in inputList:
#         row.append(currencyValues[i][0])
#     inputMatrix.append(row)




# writeData(inputMatrix, outPath + '/input1.csv', delimiter=',')



# n = CatsBalanser(LastValuesDataCreator(LnDiffPreprocessor('EUR-CHF', 'saat', directionCats=True),
#                                            [(5, 4, 3, 2, 1, 0)], normalize=True))
# writeData(n.getCat(), outPath + '/output.csv', delimiter=',')

    # writeData(n.getCat(), outPath + '/data-' + c + '.csv', delimiter=',')


    # writeData(n.getCat(), outPath + '/cat.csv')

    #
    # inputs = n.getInputs()
    # for i in range(0, len(inputs)):
    #     writeData(inputs[i], outPath + '/input' + str(i + 1) + '.csv')
    # writeData(n.getData(), outPath + '/data.csv')
    # writeData(n.getDataWithDates(), outPath + '/all-data.csv')


    #writeData(n.getDataWithLetterCategories(), '/home/dragan/Desktop/data-nominal-cats.csv')

    #a = SimplePreprocessor(f, directionCats=True)
    #b = Normalizer(SimplePreprocessor(f, directionCats=True))
    #
    #plt.plot(a.getData()[:10])
    #plt.plot(b.getData()[:10])
    #plt.show()