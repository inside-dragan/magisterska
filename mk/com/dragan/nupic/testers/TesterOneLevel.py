'''
Created on Dec 11, 2011

@author: dzaharie
'''
import logging
from nupic.bindings.network import CreateRuntimeNetwork
from mk.com.dragan.utils.CsvUtils import getNumLines


log = logging.getLogger('Tester One Level')

class TesterOneLevel:
    
    __trainedNetworkFile = None
    __resultsFile = None
    __resultFolder = None
    __numNodes = None
    
    def __init__(self, resultFolder, numNodes):
        self.__trainedNetworkFile = resultFolder + '/network-trained.xml'
        self.__resultsFile = resultFolder + '/result.csv'
        self.__resultFolder = resultFolder
        self.__numNodes = numNodes

    def __executeTest(self, testFilePrefix):
        
        files = []
        for i in range(0, self.__numNodes):
            files.append(testFilePrefix + str(i + 1) + '.csv')

        runtimeNet = CreateRuntimeNetwork(self.__trainedNetworkFile, files=files)
        
        for i, f in enumerate(files):
            runtimeNet.getElement('sensor' + str(i + 1)).execute('loadFile', f)
        
        # We would like to keep the effector outputs, so set the filename 
        # where they will be stored (inside the bundle)
        fileOutputEffector = runtimeNet.getElement('output')
        fileOutputEffector.setParameter("outputFile", self.__resultsFile)
        
        for i, f in enumerate(files):
            runtimeNet.getElement("level1" + str(i + 1) + "output").setParameter("outputFile", self.__resultFolder + '/level1' + str(i + 1) + 'result.csv')
        
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
