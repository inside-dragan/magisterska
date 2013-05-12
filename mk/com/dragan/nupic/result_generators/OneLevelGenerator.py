'''
Created on May 15, 2012

@author: dzaharie
'''
import logging
from mk.dragan.resultgenerators.AbstractResultGenerator import AbstractResultGenerator

log = logging.getLogger('One Level Generator')

class OneLevelGenerator(AbstractResultGenerator):
    
    __sigmas = [0.001, 0.003, 0.01, 0.03, 0.06, 0.1, 0.15, 0.2, 0.3, 0.5]
#    __sigmas = [0.1]

    __numNodes = None

    def __init__(self, executor, numNodes):
        super(OneLevelGenerator, self).__init__(executor)
        self.__numNodes = numNodes
    
    def _getSigmas(self):
        return self.__sigmas;
        
    def _areValidNodes(self):
        result = True
        for i in range(1, self.__numNodes + 1):
            result = result and self._isValidNode('level1' + str(i))
        return result
    
    def _shouldStopIncreasingMaxDistance(self):
        result = False
        for i in range(1, self.__numNodes + 1):
            result = result or self._shouldStopIncreasingMaxDistanceForNode('level1' + str(i))
        return result
    
    def _shouldStopDecreasingMaxDistance(self):
        result = False
        for i in range(1, self.__numNodes + 1):
            result = result or self._shouldStopDecreasingMaxDistanceForNode('level1' + str(i))
        return result
    
    def _getLevel1BottomUpOut(self):
        return 3000 / self.__numNodes      
            
