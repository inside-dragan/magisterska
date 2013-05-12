'''
Created on Feb 19, 2012

@author: Dragan
'''
from mk.com.dragan.utils.CsvUtils import readStringData
from mk.com.dragan.utils.DataUtils import getColumn, convertToNumbers, getDifferences


class ForexrateDataReader(object):
    
    __dates = None
    __data = None
    
    def __init__(self, currency, interval):
        
        fileName = '/Users/draganzahariev/Dropbox/Magisterska/data/forexrate.co.uk/' + interval + '/' + currency + '.csv'
        data = readStringData(fileName, ';')
        self.__data = getColumn(data, 3)
        self.__data = self.__data[1:]
        self.__data = convertToNumbers(self.__data)
        dates = getColumn(data, 0)
        minutes = getColumn(data, 1)
        self.__dates = []
        for d, m in zip(dates, minutes):
            self.__dates.append(d + ' - ' + m)
        self.__dates = self.__dates[1:]
    
    def getData(self):
        return self.__data 
    
    def getDates(self):
        return self.__dates
    
    def getCategories(self):
        category = []
        for d in self.getNextDayDiffs():
            if d == 'no-value':
                category.append(d)
            elif (d > 0):
                category.append(1)
            else:
                category.append(0)
        return category  
    
    def getNextDayDiffs(self):
        diffs = []
        for i, d in enumerate(self.__data):
            if i + 1 >= len(self.__data):
                diffs.append("no-value")
            else:
                diffs.append(self.__data[i + 1] - d)
        return diffs       
    
    def getDirections(self, lag):
        directions = []
        for i, d in enumerate(self.__data):
            if i - lag < 0:
                directions.append('no-value')
            else:
                directions.append(d - self.__data[i - lag])
        return directions
    
    def getDirectionsList(self, size):
        directionsList = []
        for i in range(1, size):
            directionsList.append(self.getDirections(i))
        return directionsList   
    
    def getDifferences(self, lag):
        return getDifferences(self.getData(), lag)
                
    def getDifferencesList(self, size):  
        differencesList = []
        for i in range(1, size):
            differencesList.append(self.getDifferences(i))
        return differencesList         
