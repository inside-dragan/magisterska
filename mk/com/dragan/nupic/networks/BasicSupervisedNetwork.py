'''
Created on Aug 21, 2011

Ne moze da se definira bottomUpOut, fiksno e na 1000
Ne moze da se definira topNeighbours, fiksno e na 2
I maxGroupSize ne sum siguren dali moze da se definira

@author: dzaharie
'''
import logging
from nupic.bindings.network import Network
from nupic.network.helpers import AddZeta1Level, AddClassifierNode, \
    TrainBasicNetwork, AddSensor
from mk.com.dragan.nupic.config.Params import Params
from mk.com.dragan.nupic.networks.AbstractNetwork import AbstractNetwork


log = logging.getLogger('BasicSupervisedNetwork')

class BasicSupervisedNetwork(AbstractNetwork):
    
    __net = None
    
    def _createNetwork(self):
        net = Network()
        AddSensor(net, featureVectorLength = self._inputs)
        AddZeta1Level(net, numNodes = 1)
        AddClassifierNode(net, numCategories = self._categories)
        
        net['level1'].setParameter('maxDistance', Params().MAX_DISTANCE)
        net['level1'].setParameter('maxGroupSize', Params().MAX_GROUP_SIZE)
        return net;
        
    def train(self, trainDataFile, categoriesFile):
        net = self._createNetwork()
        net = TrainBasicNetwork(
                    net,
                    dataFiles = [self._inputFolder + "/" + trainDataFile],
                    categoryFiles = [self._inputFolder + "/" + categoriesFile])
        
        filename = self._resultFolder + '/network-trained.xml'
        net.save(filename)
        log.info('training complete.')
        self.__net = net  
