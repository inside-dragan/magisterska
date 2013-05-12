'''
Created on Feb 18, 2012

@author: Dragan
'''
from scipy.stats.stats import pearsonr
from mk.com.dragan.data.readers.ForexrateDataReader import ForexrateDataReader


class CorrelAgent(object):
    
    __dataReader = None
    
    def __init__(self, inputFile, path='C:/Users/Dragan/Dropbox/Magisterska/data/forexrate.co.uk/dnevna'):
        self.__dataReader = ForexrateDataReader(path + inputFile)
        
    def __getCorrelations(self, arrayFrom, arraysTo):
        correls = []
        for arrayTo in arraysTo:
            correls.append([pearsonr(arrayFrom, arrayTo)[0]])
        return correls   
    
    '''
    Returns array of correlations, with lag from 1 to size.
    The correlations are: category to directions
    '''
    def correlCategoryToDirections(self, size):
        categories = self.__dataReader.getCategories()
        directions = self.__dataReader.getDirectionsList(size)
        
        cats = categories[size:-1]
        dirs = []
        for d in directions:
            dirs.append(d[size:-1])
        return self.__getCorrelations(cats, dirs)   
    
        '''
    Returns array of correlations, with lag from 1 to size.
    The correlations are: (next day minus today) to directions
    '''
    def correlNextDayDiffToDirections(self, size):     
        differences = self.__dataReader.getNextDayDiffs()
        directions = self.__dataReader.getDirectionsList(size)
        
        diffs = differences[size:-1]
        dirs = []
        for d in directions:
            dirs.append(d[size:-1])
        return self.__getCorrelations(diffs, dirs)  
    
    def correlCategoryToDifferences(self, size):
        categories = self.__dataReader.getCategories()
        differences = self.__dataReader.getDifferencesList(size)
        
        cats = categories[size:-1]
        diffs = [] 
        for d in differences:
            diffs.append(d[size:-1])
        return self.__getCorrelations(cats, diffs)  
