'''
Created on Feb 26, 2012

@author: dzaharie
'''
class ResultContainer(object):
    _instance = None
    
    result = []
    coincidences = {}
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ResultContainer, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    
    def addResult(self, result):
        self.result.append(result)
        
    def getLatestResult(self):
        return self.result[-1]
    
    def clear(self):
        self.result = []
        self.coincidences = {}
        
    def isEmpty(self):
        return self.result == [] or self.coincidences == {}
    
