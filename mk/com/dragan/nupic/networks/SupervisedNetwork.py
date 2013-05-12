'''
Created on May 24, 2011

@author: admin
'''
from mk.dragan.utils.CsvUtils import getNumLines
from mk.dragan.networks.AbstractNetwork import AbstractNetwork
from nupic.bindings.network import Network, Zeta1Train
from mk.dragan.utils.loggingDef import logging

log = logging.getLogger('SupervisedNetwork')

class SupervisedNetwork(AbstractNetwork):
        

    def _createNetwork(self):
        net = Network()
        net.add("sensor", self._createSensor())
        net.add("category", self._createCategorySensor())
        net.add("level1", self._createNode(1))
        net.add("topNode", self._createTopNode(2))
        net.add("output", self._createEffector(3))
        
        net.link(source="sensor", 
                 sourceOutputName="dataOut", 
                 destination="level1", 
                 destinationInputName="bottomUpIn")

        net.link(source="level1", 
                 sourceOutputName="bottomUpOut", 
                 destination="topNode", 
                 destinationInputName="bottomUpIn")
                 
        net.link(source="category", 
                 sourceOutputName="dataOut", 
                 destination="topNode", 
                 destinationInputName="categoryIn")

        net.link(source="topNode", 
                 sourceOutputName="categoriesOut", 
                 destination="output", 
                 destinationInputName="dataIn")

        return net
    
    def train(self, trainDataFile, categoriesFile):
        sensor = self._runtimeNetwork.getElement("sensor")
        categorySensor = self._runtimeNetwork.getElement("category")

        trainDataFile = self._inputFolder + '/' + trainDataFile
        categoriesFile = self._inputFolder + '/' + categoriesFile
        sensor.execute("loadFile", trainDataFile)
        categorySensor.execute("loadFile", categoriesFile)
  
        counter = getNumLines(trainDataFile)
        log.info('number of vectors for training: ' + str(counter))
        
        # Make sure the sensors start at the beginning of the file.
        sensor.setParameter("position", "0")
        categorySensor.setParameter("position", "0")

        self._runtimeNetwork.run(Zeta1Train("level1", counter), ["sensor", "level1"])
        
        # Make sure the sensors start at the beginning of the file.
        sensor.setParameter("position", "0")
        categorySensor.setParameter("position", "0")
  
        self._runtimeNetwork.run(Zeta1Train("topNode", counter), ["sensor", "level1", "topNode", "category"])

        filename = self._resultFolder + '/network-trained.xml'
        self._runtimeNetwork.save(filename)
        self._runtimeNetwork.cleanupBundleWhenDone()
        log.info('training complete.')
        
