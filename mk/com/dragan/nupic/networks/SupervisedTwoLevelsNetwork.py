'''
Created on Dec 11, 2011

@author: dzaharie
'''
from mk.dragan.networks.AbstractNetwork import AbstractNetwork
from nupic.bindings.network import Network, Zeta1Train
from mk.dragan.utils.CsvUtils import getNumLines

from mk.dragan.utils.loggingDef import logging

log = logging.getLogger('Supervised Two Levels Network')

class SupervisedTwoLevelsNetwork(AbstractNetwork):
    
    __numLevel1 = None
    __numLevel2 = None
    
    def __init__(self, inputs, categories, inputFolder, resultFolder, numLevel1, numLevel2):
        self.__numLevel1 = numLevel1
        self.__numLevel2 = numLevel2
        super(SupervisedTwoLevelsNetwork, self).__init__(inputs, categories, inputFolder, resultFolder) 
    
    def _createNetwork(self):
        net = Network()
        
        for i in range(1, self.__numLevel1 + 1):
            net.add("sensor" + str(i), self._createSensor())
            
        for i in range(1, self.__numLevel1 + 1):
            net.add("level1" + str(i), self._createNode(1))
            net.add("level1" + str(i) + "output", self._createEffector(2))            

        for i in range(1, self.__numLevel2 + 1):
            net.add("level2" + str(i), self._createNode_2(2))
            net.add("level2" + str(i) + "output", self._createEffector(3))

        net.add("category", self._createCategorySensor(2))
        net.add("topNode", self._createTopNode(3));
        net.add("output", self._createEffector(4))
        
        for i in range(1, self.__numLevel1 + 1):
            net.link(source="sensor" + str(i), 
                     sourceOutputName="dataOut", 
                     destination="level1" + str(i), 
                     destinationInputName="bottomUpIn")   
            
        for i in range(1, self.__numLevel1 + 1):
            net.link(source="level1" + str(i),
                     sourceOutputName="bottomUpOut",
                     destination="level2" + str((i-1)/(self.__numLevel1/self.__numLevel2) + 1),
                     destinationInputName="bottomUpIn")
            net.link(source="level1" + str(i),
                     sourceOutputName="bottomUpOut",
                     destination="level1" + str(i) + "output",
                     destinationInputName="dataIn")            
               
        for i in range(1, self.__numLevel2 + 1):
            net.link(source="level2" + str(i),
                     sourceOutputName="bottomUpOut",
                     destination="topNode",
                     destinationInputName="bottomUpIn")
            net.link(source="level2" + str(i),
                     sourceOutputName="bottomUpOut",
                     destination="level2" + str(i) + "output",
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
        for i in range(1, self.__numLevel1 + 1):
            sensors.append(self._runtimeNetwork.getElement("sensor" + str(i)))
            trainDataFiles.append(self._inputFolder + '/' + trainDataPrefix + str(i) + '.csv')
        categoriesFile = self._inputFolder + '/' + categoriesFile
        
        for sensor, trainDataFile in zip(sensors, trainDataFiles):
            sensor.execute("loadFile", trainDataFile)       
        categorySensor.execute("loadFile", categoriesFile)
  
        counter = getNumLines(trainDataFiles[0])
        log.info('number of vectors for training: ' + str(counter))
        
        # Make sure the sensors start at the beginning of the file.
        for i, sensor in enumerate(sensors):
            log.info('training level1' + str(i+1) + '...')
            sensor.setParameter("position", "0")
            categorySensor.setParameter("position", "0")
            self._runtimeNetwork.run(Zeta1Train("level1" + str(i+1), counter), ["sensor" + str(i+1), "level1" + str(i+1)])
        
        nodes = []
        for i in range(1, self.__numLevel1 + 1):
            nodes.append("sensor" + str(i))
            nodes.append("level1" + str(i))
        for i in range(1, self.__numLevel2 + 1):
            nodes.append('level2' + str(i))

        for j in range(1, self.__numLevel2 + 1):
            for sensor in sensors:
                sensor.setParameter("position", "0")
            categorySensor.setParameter("position", "0")
            log.info('training level2' + str(j) + '...')
            self._runtimeNetwork.run(Zeta1Train("level2" + str(j), counter), nodes) 

        
        for sensor in sensors:
            sensor.setParameter("position", "0")       
        categorySensor.setParameter("position", "0")
        nodes.append('topNode')
        nodes.append('category')
        log.info('training topNode...')
        self._runtimeNetwork.run(Zeta1Train("topNode", counter), nodes)

        filename = self._resultFolder + '/network-trained.xml'
        self._runtimeNetwork.save(filename)
        self._runtimeNetwork.cleanupBundleWhenDone()
        log.info('training complete.')  
