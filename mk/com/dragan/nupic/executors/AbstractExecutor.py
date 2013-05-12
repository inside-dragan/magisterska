'''
Created on Nov 20, 2011

@author: Dragan
'''
import os
from mk.dragan.utils.loggingDef import logging
from mk.dragan.utils.CsvTransformUtils import split60to20to20

log = logging.getLogger('AbstractExecutor')

class AbstractExecutor(object):
    
    _inputFolder = None

    def __init__(self):
        self._inputFolder = os.getcwd() + '/input'
        
    def executeSupervised(self):  
        pass
    
    def executeUnsupervised(self):  
        pass
        
    def executeBasicSupervised(self):  
        pass
        
    def executeBasicUnsupervised(self):  
        pass 
        
    def executeHtmSupervised(self):  
        pass 
    
    def _separateFiles(self, mainFiles, trainFiles, testFiles, validateFiles, evaluateFiles):
        
        for main, train, test, val, evaluate in zip(mainFiles, trainFiles, testFiles, validateFiles, evaluateFiles):
            if not os.path.exists(train) or not os.path.exists(test) or not os.path.exists(val):
                log.info('separating ' + main + ' to ' + train + ', ' + test + ', ' + val + ' and' + evaluate)
                split60to20to20(main, train, val, test, evaluate)          
        
