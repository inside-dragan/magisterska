'''
Created on Feb 9, 2012

@author: Dragan
'''
from mk.dragan.correlations.CorrelAgent import CorrelAgent
from mk.dragan.utils.CsvUtils import writeData

SIZE = 500

path = 'C:/Users/Dragan/Dropbox/Magisterska/data/forexrate.co.uk/dnevna/EUR - USD'
correlAgent = CorrelAgent('/Q1_1D_2000-2000.csv', path)

correls = correlAgent.correlCategoryToDifferences(SIZE)

    
writeData(correls, path + "/correlation cats to differences Q1_1D_2000.csv", ';')