'''
Created on May 14, 2012

@author: dzaharie
'''
import logging

log = logging.getLogger('Categories Balanser')

class CatsBalanser(object):
    
    __dataCreator = None
    __zeros = None
    __ones = None
    
    def __init__(self, dataCreator):
        self.__dataCreator = dataCreator
        cats = dataCreator.getCat()
        
        zeros = []
        ones = []
        for i, cat in enumerate(cats):
            if cat == 0:
                zeros.append(i)
            elif cat == 1:
                ones.append(i)
            else:
                log.error('category found which is neither 0 nor 1')
        lz = len(zeros)
        lo = len(ones)
        if lz > lo:
            zeros = zeros[:lo]
        elif lo > lz:
            ones = ones[:lz]
            
        self.__zeros = zeros
        self.__ones = ones
        
    def __getBalansed(self, data):
        result = []
        for z, o in zip(self.__zeros, self.__ones):
            result.append(data[z])
            result.append(data[o])
        return result
        
    def getData(self):
        return self.__getBalansed(self.__dataCreator.getData())
    
    def getInputs(self):
        result = []
        for inp in self.__dataCreator.getInputs():
            result.append(self.__getBalansed(inp))
        return result;
    
    def getCat(self):
        return self.__getBalansed(self.__dataCreator.getCat())
    
    def getDataWithDates(self):
        return self.__getBalansed(self.__dataCreator.getDataWithDates())

    def getCatWithDates(self):
        return self.__getBalansed(self.__dataCreator.getCatWithDates())
    
    def getDataWithLetterCategories(self):
        data = self.__getBalansed(self.__dataCreator.getDataWithLetterCategories())
        size = len(data[0])

        header = []
        for i in range(1, size):
            header.append('value' + str(i))
        header.append('category')

        data.insert(0, header)
        return data
    
    def getDescription(self):
        result = self.__dataCreator.getDescription()
        result['postprocess'] = 'catBalansed'
        return result    

    
            
