'''
Created on May 24, 2011

@author: admin
'''
import logging
from nupic.bindings.network import Network, Zeta1Train
from mk.com.dragan.nupic.networks.AbstractNetwork import AbstractNetwork
from mk.com.dragan.utils.CsvUtils import getNumLines

log = logging.getLogger('UnupervisedNetwork')

class UnsupervisedNetwork(AbstractNetwork):
    
    def _createNetwork(self):
        net = Network()
        net.add("sensor", self._createSensor())
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
                 
        net.link(source="topNode",
                 sourceOutputName="categoriesOut",
                 destination="output",
                 destinationInputName="dataIn")
                 
        return net
    
    def train(self, trainDataFile):
        sensor = self._runtimeNetwork.getElement("sensor")

        trainDataFile = self._inputFolder + '/' + trainDataFile
        sensor.execute("loadFile", trainDataFile)
  
        counter = getNumLines(trainDataFile)
        log.info('number of vectors for training: ' + str(counter))
        
        # Make sure the sensors start at the beginning of the file.
        sensor.setParameter("position", "0")

        self._runtimeNetwork.run(Zeta1Train("level1", counter), ["sensor", "level1"])
        
        # Make sure the sensors start at the beginning of the file.
        sensor.setParameter("position", "0")
  
        self._runtimeNetwork.run(Zeta1Train("topNode", counter), ["sensor", "level1", "topNode"])

        filename = self._resultFolder + '/network-trained.xml'
        self._runtimeNetwork.save(filename)
        self._runtimeNetwork.cleanupBundleWhenDone()
        log.info('training complete.')
        
