'''
Created on May 12, 2012

@author: Dragan
'''
from mk.com.dragan.data.readers.ForexrateDataReader import ForexrateDataReader
from mk.com.dragan.utils.DataUtils import getShifted, getDifferencesOfLists, getCategories


class AbstractPreprocessor(object):
    
    __d = None
    __directionCats = None
    __currency = None
    __interval = None
    
    def __init__(self, currency, interval, directionCats):
        self.__directionCats = directionCats
        self.__currency = currency
        self.__interval = interval
        self.__d = ForexrateDataReader(currency, interval)
        
    def _trim(self, lista):
        pass
    
    def _getData(self):
        return self.__d.getData()
    
    def getCats(self):
        data = self._getData()
        dataNext = getShifted(data, -1)
        
        if self.__directionCats:
            diff = getDifferencesOfLists(data, dataNext)
            cats = getCategories(diff)
        else:
            cats = dataNext
        return self._trim(cats)  
      
    def getDates(self):
        return self._trim(self.__d.getDates())    
    
    def getDescription(self):
        result = {}
        if self.__directionCats:
            result['direction'] = 'directed'
        else:
            result['direction'] = 'notDirected'
#        result['currency'] = self.__currency #not needed for now
        result['interval'] = self.__interval
        return result
          