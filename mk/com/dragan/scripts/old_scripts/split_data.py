'''
Created on Dec 10, 2011

@author: dzaharie
'''
from mk.dragan.utils.CsvUtils import readStringData, writeData
path = 'C:/Users/dzaharie/Dropbox/Magisterska/data/forextester.com/EURUSD'

data = readStringData(path + '/EURUSD.csv')
result = [['<TICKER>', '<DTYYYYMMDD>', '<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']]
for row in data:
    if row[1].startswith('2005') or row[1].startswith('2006'):
        result.append(row)
        
writeData(result, path + '/EURUSD-05-06.csv')
