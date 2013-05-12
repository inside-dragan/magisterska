'''
Created on Nov 24, 2011

@author: Dragan
'''
import os
import shutil
class AbstractRunner(object):
    
    _resultFolder = None
    
    def __init__(self, resultFile): 
        self._resultFolder = os.getcwd() + '/' + resultFile 
    
    def _createFolder(self):
        if os.path.exists(self._resultFolder):
            shutil.rmtree(self._resultFolder)
        os.mkdir(self._resultFolder)    