'''
Created on Aug 18, 2011

@author: dzaharie
'''
import logging
from nupic.bindings.network import CreateRuntimeNetwork
import os
from mk.com.dragan.utils.CsvUtils import getNumLines
from mk.com.dragan.utils.StringUtils import after, before


log = logging.getLogger('Tester')

class Tester:
    
    __trainedNetworkFile = None
    __resultsFile = None
    
    def __init__(self, resultFolder):
        self.__trainedNetworkFile = resultFolder + '/network-trained.xml'
        self.__resultsFile = resultFolder + '/result.csv'
    

    def __executeTest(self, testFile):
        
        runtimeNet = CreateRuntimeNetwork(self.__trainedNetworkFile, files=[testFile])
        runtimeNet.getElement('sensor').execute('loadFile', testFile)
        # We would like to keep the effector outputs, so set the filename 
        # where they will be stored (inside the bundle)
        fileOutputEffector = None
        try:
            fileOutputEffector = runtimeNet.getElement('output')
        except RuntimeError:
            #in some networks it is called fileWriter
            fileOutputEffector = runtimeNet.getElement('fileWriter')
            
        fileOutputEffector.setParameter("outputFile", self.__resultsFile)
        
        counter = getNumLines(testFile)
        log.info('number of vectors for testing: ' + str(counter))
        
        try:
            runtimeNet.getElement('category')
            runtimeNet.run(counter, exclusion=["category"])
        except:
            runtimeNet.run(counter, selection=["sensor", "level1", "topNode", "output"])
            
        fileOutputEffector.execute("flushFile")
        runtimeNet.cleanupBundleWhenDone()  
        

    def __testByFile(self, testFile):
        
        category = before(after(testFile, '-cat'), '.csv')
        if not category:
            category = 'unknown'
        f = open(self.__resultsFile, 'a')
        f.write(category + '\n')
        f.close()
        self.__executeTest(testFile)
        
    def testOne(self, testFile):
        self.__testByFile(testFile)
        log.info('testing completed.')
        
    def testAll(self, folder, start=0, end= -1):
        fileNames = os.listdir(folder)
        log.info('testing...')
        old = 0
        if end == -1 :
            end = len(fileNames)
        for i in range(start, end):
            log.info('testing file: ' + fileNames[i])
            self.__testByFile(folder + '/' + fileNames[i], self.__resultsFile)
            new = (i * 100) / (end - start)
            if (new != old):
                log.info(str(new) + '% complete')
                old = new
                
        log.info('testing completed.')
        
    def test(self, testFile):
        self.__executeTest(testFile)
    

