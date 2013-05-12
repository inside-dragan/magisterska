'''
Created on Mar 31, 2012

@author: dzaharie

lista od moving averages

categorija: nasoka na narednata vrednost vo odnost na segasnata
'''
from mk.dragan.data.creators.AbstractDataCreator import AbstractDataCreator
from mk.dragan.utils.DataUtils import getMovingAverage, getMax


class ListMovingAveragesDataCreator(AbstractDataCreator):
    
    __dates = None
    __input = None
    __combinations = None
    
    def __init__(self, preprocessor, combinations, normalize):
        self.__combinations = combinations
        super(ListMovingAveragesDataCreator, self).__init__(
            preprocessor, removeStartFrom=getMax(combinations)-1, normalize=normalize)
        
    def _createInputs(self, data):
        result = []
        for combination in self.__combinations:
            inputs = []
            for movingAverage in combination:
                inputs.append(getMovingAverage(data, movingAverage))
            result.append(inputs)
        return result
    
    def getDescription(self):
        result = AbstractDataCreator.getDescription(self)
        result['dataType'] = 'listMovingAverages' 
        result['combinations'] = str(self.__combinations)   
        return result
