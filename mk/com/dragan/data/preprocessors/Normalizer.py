'''
Created on May 12, 2012

Raboti tocno samo ako nizata so se normalizira e megju 0 i 1.

@author: Dragan
'''
from mk.com.dragan.utils.DataUtils import normalize0to1


class Normalizer(object):
    
    __preprocessor = None

    def __init__(self, preprocessor):
        self.__preprocessor = preprocessor
        
    def getData(self):
        return normalize0to1(self.__preprocessor.getData())
        
    def getCats(self):
        return self.__preprocessor.getCats()
        
    def getDates(self):
        return self.__preprocessor.getDates()
    
    def getDescription(self):
        result = self.__preprocessor.getDescription()
        result['normalization'] = 'normalized'    
        return result