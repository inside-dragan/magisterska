'''
Created on Mar 31, 2012

@author: dzaharie

vlez so: ln(Sn/Sn-1) i moving average 5
normaliziran vo rang od 0 do 1

categorija: nasoka na moving average 5 (Xn+1)
'''
from mk.com.dragan.data.creators.AbstractDataCreator import AbstractDataCreator
from mk.com.dragan.utils.DataUtils import getMax, getShifted


class LastValuesDataCreator(AbstractDataCreator):
    
    __combinations = None
    
    def __init__(self, preprocessor, combinations, normalize):
        self.__combinations = combinations
        super(LastValuesDataCreator, self).__init__(
            preprocessor, removeStartFrom=getMax(combinations), normalize=normalize)
    
    def _createInputs(self, data):
        result = []
        for combination in self.__combinations:
            inputt = []
            for i in combination:
                inputt.append(getShifted(data, i))
            result.append(inputt)
        return result
    
    def getDescription(self):
        result = super(AbstractDataCreator, self).getDescription()
        result['dataType'] = 'lastValues' 
        result['combinations'] = str(self.__combinations)  
        return result     
        
        
        