'''
Created on May 10, 2012

@author: dzaharie
'''
import numpy
from mk.com.dragan.utils.DataUtils import normalize0to1


class AbstractDataCreator(object):
    
    __data = None
    __dates = None
    __inputs = None
    __cat = None
    
    __preprocessor = None
    __normalize = None
    
    def __init__(self, preprocessor, removeStartFrom, normalize):
        
        self.__preprocessor = preprocessor
        self.__normalize = normalize
        self.__dates = preprocessor.getDates()[removeStartFrom:]
        self.__cat = preprocessor.getCats()[removeStartFrom:]
        
        self.__data = preprocessor.getData()
        inputs = self._createInputs(self.__data)
        self.__inputs = []
        for inp in inputs:
            inputt = []
            for line in inp:
                l = line[removeStartFrom:]
                if normalize:
                    l = normalize0to1(l)
                inputt.append(l)
            self.__inputs.append(inputt)
        
    def getCat(self):
        return numpy.transpose([self.__cat])
    
    def _createInputs(self, dataLine):
        pass
    
    def getData(self):
        result = []
        for inp in self.__inputs:
            result.extend(inp)
        result.append(self.__cat)
        return numpy.transpose(result)        
    
    def getInputs(self):
        result = []
        for inp in self.__inputs:
            result.append(numpy.transpose(inp))
        return result
            
    def getDataWithDates(self):
        result = []
        for inp in self.__inputs:
            result.extend(inp)
        result.append(self.__cat)
        result.insert(0, self.__dates)
        return numpy.transpose(result)

    def getCatWithDates(self):
        result = [self.__dates, self.__cat]
        return numpy.transpose(result)

    def getCatWithDatesDict(self):
        result = {}
        for i, j in zip(self.__dates, self.__cat):
           result[i] = j
        return result
    
    def getDescription(self):
        result = self.__preprocessor.getDescription()   
        if self.__normalize:
            result['normalization'] = 'normalized' 
        else:
            result['normalization'] = 'notNormalized'  
        return result
