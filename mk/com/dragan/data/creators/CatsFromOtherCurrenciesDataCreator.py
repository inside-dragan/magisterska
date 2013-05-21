from mk.com.dragan.data.creators.LastValuesDataCreator import LastValuesDataCreator
from mk.com.dragan.data.preprocessors.LnDiffPreprocessor import LnDiffPreprocessor
from mk.com.dragan.data.readers.ForexRateNewFormatReader import ForexRateNewFormatReader


class CatsFromOtherCurrenciesDataCreator(object):

    def merge_with(d1, d2):
        res = d1.copy() # "= dict(d1)" for lists of tuples
        for key, val in d2.iteritems(): # ".. in d2" for lists of tuples
            try:
                res[key].append(val)
            except KeyError:
                res[key] = [val]
        return res

    def createWithLetterCategory(row):
        result = row[:]
        if result[-1] == 0:
            result[-1] = 'A'
        elif result[-1] == 1:
            result[-1] = 'B'
        else: raise
        return result

    def __init__(self, currencies):

        dateCatDict = {}
        for c in currencies:
            dataReader = ForexRateNewFormatReader(c, 'saat')
            n = LastValuesDataCreator(LnDiffPreprocessor(dataReader, directionCats=True),
                                                   [(5, 4, 3, 2, 1, 0)], normalize=True)
            dateCatDict = self.merge_with(dateCatDict, n.getCatWithDatesDict())


        resultList = []

        for v in dateCatDict.values():
            if len(v) == len(currencies):
               resultList.append(self.createWithLetterCategory(v))
