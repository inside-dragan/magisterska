'''
Created on Mar 31, 2012

@author: dzaharie

vlez so: ln(Sn/Sn-1) i moving average 5
'''
from mk.dragan.data.creators.AbstractDataCreator import AbstractDataCreator
from mk.dragan.utils.DataUtils import getMovingAverage

class NNType1DataCreator(AbstractDataCreator):
    
    __movingAverageSize = None
    
    def __init__(self, preprocessor, movingAverageSize, normalize):
        self.__movingAverageSize = movingAverageSize
        super(NNType1DataCreator, self).__init__(
            preprocessor, movingAverageSize - 1, normalize)    
    
    
    def _createInputs(self, data):
        average = getMovingAverage(data, self.__movingAverageSize)
        return [[data, average]]
    
    def getDescription(self):
        result = super(AbstractDataCreator, self).getDescription()
        result['dataType'] = 'NNType1' 
        result['combinations'] = self.__movingAverageSize   
        return result   
