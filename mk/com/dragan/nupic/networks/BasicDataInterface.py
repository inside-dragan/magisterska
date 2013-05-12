'''
Created on Aug 30, 2011

@author: dzaharie
'''
from nupic.network.DataInterface import DataInterface
class BasicDataInterface(DataInterface):
    
    
    def __init__(self, inputFileName=None, sizeInput=None, catFileName=None, sizeCats=None):
        DataInterface.__init__(self)
        self.addParam("format", default=None)
        self.addParam("sensorDims", default=sizeInput)
        self.addParam("numCat", default=sizeCats)
#        self.addParam("trainedFilename", default='dragan.xml')
        self.setValue("files", [inputFileName, catFileName, ''])
    def getPrefixedDataFiles(self): return self.getValue("files")
        
    
