'''
Created on May 12, 2012

@author: Dragan
'''
from mk.com.dragan.data.readers.ForexrateDataReader import ForexrateDataReader
from mk.com.dragan.utils.DataUtils import getShifted, getDifferencesOfLists, getCategories


class AbstractPreprocessor(object):
    
    __dataReader = None
    __directionCats = None

    def __init__(self, dataReader, directionCats):
        self.__directionCats = directionCats
        self.__dataReader = dataReader

    def _trim(self, lista):
        pass

    def _getData(self):
        return self.__dataReader.data

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
        return self._trim(self.__dataReader.dates)
