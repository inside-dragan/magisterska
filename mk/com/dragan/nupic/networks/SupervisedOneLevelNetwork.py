'''
Created on Oct 24, 2011

@author: Dragan
'''
import logging
from nupic.bindings.network import Network, Zeta1Train
from mk.com.dragan.nupic.networks.AbstractNetwork import AbstractNetwork
from mk.com.dragan.utils.CsvUtils import getNumLines

log = logging.getLogger('Supervised One Level Network')

class SupervisedOneLevelNetwork(AbstractNetwork):
    
    
    __numNodes = None
    
    def __init__(self, inputs, categories, inputFolder, resultFolder, numNodes):
        self.__numNodes = numNodes
        super(SupervisedOneLevelNetwork, self).__init__(inputs, categories, inputFolder, resultFolder) 
    
    def _createNetwork(self):
        net = Network()
        
        for i in range(1, self.__numNodes + 1):
            net.add("sensor" + str(i), self._createSensor())
                
        net.add("category", self._createCategorySensor())
        
        for i in range(1, self.__numNodes + 1):
            net.add("level1" + str(i), self._createNode(1))
            net.add("level1" + str(i) + "output", self._createEffector(2))
          
        net.add("topNode", self._createTopNode(2))
        net.add("output", self._createEffector(3))
        
        for i in range(1, self.__numNodes + 1):
            net.link(source="sensor" + str(i), 
                     sourceOutputName="dataOut", 
                     destination="level1" + str(i), 
                     destinationInputName="bottomUpIn")
            
        for i in range(1, self.__numNodes + 1):
            net.link(source="level1" + str(i), 
                     sourceOutputName="bottomUpOut", 
                     destination="topNode", 
                     destinationInputName="bottomUpIn")
            net.link(source="level1" + str(i),
                     sourceOutputName="bottomUpOut",
                     destination="level1" + str(i) + "output",
                     destinationInputName="dataIn")        
                 
        net.link(source="category", 
                 sourceOutputName="dataOut", 
                 destination="topNode", 
                 destinationInputName="categoryIn")

        net.link(source="topNode", 
                 sourceOutputName="categoriesOut", 
                 destination="output", 
                 destinationInputName="dataIn")

        return net
    
    def train(self, trainDataPrefix, categoriesFile):
        
        categorySensor = self._runtimeNetwork.getElement("category")
        
        sensors = []
        trainDataFiles = []
        for i in range(1, self.__numNodes + 1):
            sensors.append(self._runtimeNetwork.getElement("sensor" + str(i)))
            trainDataFiles.append(self._inputFolder + '/' + trainDataPrefix + str(i) + '.csv')
        categoriesFile = self._inputFolder + '/' + categoriesFile
        
        for sensor, trainDataFile in zip(sensors, trainDataFiles):
            sensor.execute("loadFile", trainDataFile)
        categorySensor.execute("loadFile", categoriesFile)
  
        counter = getNumLines(trainDataFiles[0])
        log.info('number of vectors for training: ' + str(counter))
        log.info('training...')
        
        # Make sure the sensors start at the beginning of the file.
        for i, sensor in enumerate(sensors):
            sensor.setParameter("position", "0")
            categorySensor.setParameter("position", "0")
            self._runtimeNetwork.run(Zeta1Train("level1" + str(i+1), counter), ["sensor" + str(i+1), "level1" + str(i+1)])
        
        
        # Make sure the sensors start at the beginning of the file.
        for sensor in sensors:
            sensor.setParameter("position", "0")
        categorySensor.setParameter("position", "0")
  
        allNodes = []
        for i in range(1, self.__numNodes + 1):
            allNodes.append('sensor' + str(i))
            allNodes.append('level1' + str(i))
        allNodes.append('topNode')
        allNodes.append('category')
        self._runtimeNetwork.run(Zeta1Train("topNode", counter), allNodes)

        filename = self._resultFolder + '/network-trained.xml'
        self._runtimeNetwork.save(filename)
        self._runtimeNetwork.cleanupBundleWhenDone()
        log.info('training complete.')    