'''
Created on May 12, 2012

@author: Dragan
'''
from mk.com.dragan.data.preprocessors.AbstractPreprocessor import AbstractPreprocessor


class SimplePreprocessor(AbstractPreprocessor):
        
    def _trim(self, lista):
        return lista[:-1]
    
    def getData(self):
        return self._trim(self._getData())
