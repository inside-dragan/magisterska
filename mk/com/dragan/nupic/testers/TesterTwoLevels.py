'''
Created on Feb 18, 2012

@author: dzaharie
'''
import logging
from nupic.bindings.network import CreateRuntimeNetwork
from mk.com.dragan.utils.CsvUtils import getNumLines


log = logging.getLogger('Tester Two Levels')

class TesterTwoLevels:
    
    __trainedNetworkFile = None
    __resultsFile = None
    __resultFolder = None
    __numLevel1 = None
    __numLevel2 = None
    
    def __init__(self, resultFolder, numLevel1, numLevel2):
        self.__trainedNetworkFile = resultFolder + '/network-trained.xml'
        self.__resultsFile = resultFolder + '/result.csv'
        self.__resultFolder = resultFolder
        self.__numLevel1 = numLevel1
        self.__numLevel2 = numLevel2

    def __executeTest(self, testFilePrefix):
        
        files = []
        for i in range(1, self.__numLevel1 + 1):
            files.append(testFilePrefix + str(i) + '.csv')
        runtimeNet = CreateRuntimeNetwork(self.__trainedNetworkFile, files=files)
        
        for i, filename in enumerate(files):
            runtimeNet.getElement('sensor' + str(i+1)).execute('loadFile', filename)
        # We would like to keep the effector outputs, so set the filename 
        # where they will be stored (inside the bundle)
        fileOutputEffector = runtimeNet.getElement('output')
        fileOutputEffector.setParameter("outputFile", self.__resultsFile)
        
        for i in range(1, self.__numLevel1 + 1):
            runtimeNet.getElement("level1" + str(i) + "output").setParameter("outputFile", self.__resultFolder + '/level1' + str(i) + 'result.csv')
        
        for i in range(1, self.__numLevel2 + 1):
            runtimeNet.getElement("level2" + str(i) + "output").setParameter("outputFile", self.__resultFolder + '/level2' + str(i) + 'result.csv')
        
        counter = getNumLines(files[0])
        log.info('number of vectors for testing: ' + str(counter))
        log.info('testing...')
#        try:
#            runtimeNet.getElement('category')
        runtimeNet.run(counter, exclusion=["category"])
#        except:
#            runtimeNet.run(counter, selection=["sensor", "level1", "topNode", "output"])
            
#        fileOutputEffector.execute("flushFile")
#        level11OutputEffector.execute("flushFile")
        runtimeNet.cleanupBundleWhenDone()  
        
    def test(self, testFilePrefix):
        self.__executeTest(testFilePrefix)
