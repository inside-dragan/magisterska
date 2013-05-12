'''
Created on Aug 28, 2011

Ne moze da se definira bottomUpOut, fiksno e na 1000
Ne moze da se definira topNeighbours, fiksno e na 2
I maxGroupSize ne sum siguren dali moze da se definira

@author: dzaharie
'''
from mk.dragan.networks.AbstractNetwork import AbstractNetwork
from mk.dragan.config.Params import Params
from mk.dragan.utils.CsvUtils import getNumLines
from nupic.bindings.network import Network, Zeta1Train
from nupic.network.helpers import AddZeta1Level, AddClassifierNode, AddSensor
from mk.dragan.utils.loggingDef import logging

log = logging.getLogger('BasicUnsupervisedNetwork')    

class BasicUnsupervisedNetwork(AbstractNetwork):
    
    __net = None
    
    def _createNetwork(self):
        net = Network()
        AddSensor(net, featureVectorLength=self._inputs)
        AddZeta1Level(net, numNodes=1)
        AddClassifierNode(net, numCategories=self._categories)
        
        net['level1'].setParameter('maxDistance', Params().MAX_DISTANCE)
        net['level1'].setParameter('maxGroupSize', Params().MAX_GROUP_SIZE)
        return net;
        
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
        
#    def test(self, dataFile, categoriesFile):
#        net = self.__net
#        accuracy = RunBasicNetwork(net,
#                        dataFiles     = [self._inputFolder + "/" + dataFile],
#                        categoryFiles = [self._inputFolder + "/" + categoriesFile],
#                        resultsFile   = self._resultFolder + "/same_data_test_results.txt")       
#        print "accuracy:", accuracy *100, "%"    
