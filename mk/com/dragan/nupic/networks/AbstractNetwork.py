'''
Created on Aug 20, 2011

@author: dzaharie
'''
from nupic.bindings.network import CreateRuntimeNetwork
from nupic.network.createnode import CreateNode
from mk.com.dragan.nupic.config.Params import Params


class AbstractNetwork(object):
    
    _resultFolder = None
    _inputs = None
    _runtimeNetwork = None
    _categories = None
    _inputFolder = None
    
    def __init__(self, inputs, categories, inputFolder, resultFolder):
        self._resultFolder = resultFolder
        self._inputs = inputs
        self._categories = categories
        self._inputFolder = inputFolder
        self._runtimeNetwork = self._createRuntimeNetwork()
        
    def _createSensor(self):
        return CreateNode("VectorFileSensor",
                      phase=0,
                      dataOut=self._inputs)
                      
    def _createCategorySensor(self, phase=1):
        return CreateNode("VectorFileSensor",
                              phase=phase,
                              dataOut=1)
                      
    def _createNode(self, phase):
        return CreateNode("Zeta1Node",
                          phase=phase,
                          spatialPoolerAlgorithm=Params().SPATIAL_POOLER_ALGORITHM,
                          symmetricTime=Params().SYMETRIC_TIME,
                          detectBlanks=Params().DETECT_BLANKS,
                          sigma=Params().SIGMA,
                          transitionMemory=Params().TRANSITION_MEMORY,
                          topNeighbors=Params().TOP_NEIGHBOURS,
                          maxGroupSize=Params().MAX_GROUP_SIZE,
                          temporalPoolerAlgorithm=Params().TEMPORAL_POOLER_ALGORITHM,
                          bottomUpOut=Params().BOTTOM_UP_OUT,
                          maxDistance=Params().MAX_DISTANCE)     
        
    def _createNode_2(self, phase):
        return CreateNode("Zeta1Node",
                          phase=phase,
                          spatialPoolerAlgorithm=Params().SPATIAL_POOLER_ALGORITHM_2,
                          symmetricTime=Params().SYMETRIC_TIME,
                          detectBlanks=Params().DETECT_BLANKS,
                          sigma=Params().SIGMA_2,
                          transitionMemory=Params().TRANSITION_MEMORY,
                          topNeighbors=Params().TOP_NEIGHBOURS,
                          maxGroupSize=Params().MAX_GROUP_SIZE,
                          temporalPoolerAlgorithm=Params().TEMPORAL_POOLER_ALGORITHM,
                          bottomUpOut=Params().BOTTOM_UP_OUT_2,
                          maxDistance=Params().MAX_DISTANCE_2)           
    
    def _createTopNode(self, phase):
        return CreateNode("Zeta1TopNode",
                        phase=phase,
                        spatialPoolerAlgorithm=Params().SPATIAL_POOLER_ALGORITHM_TOP,
                        mapperAlgorithm=Params().MAPPER_ALGORITHM,
                        categoriesOut=self._categories)
    
    def _createEffector(self, phase):
        return CreateNode("VectorFileEffector",
                          phase=phase)        
    
    def _createRuntimeNetwork(self):
        filename = self._resultFolder + '/network-runtime.xml'
        net = self._createNetwork()
        net.save(filename)
        return CreateRuntimeNetwork(filename)
    
    def _createNetwork(self):
        pass 
    
    def train(self, trainDataFile, categoriesFile):
        pass
    
