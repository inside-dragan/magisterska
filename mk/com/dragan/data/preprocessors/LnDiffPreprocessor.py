'''
Created on May 12, 2012

@author: Dragan
'''
from mk.com.dragan.data.preprocessors.AbstractPreprocessor import AbstractPreprocessor
from mk.com.dragan.utils.DataUtils import getLnDifferences


class LnDiffPreprocessor(AbstractPreprocessor):
        
    def _trim(self, lista):
        return lista[1:-1]
    
    def getData(self):
        data = getLnDifferences(self._getData(), 1)
        return self._trim(data)
    
    def getDescription(self):
        result = AbstractPreprocessor.getDescription(self)
        result['transformed'] = 'lnDiff'
        return result
