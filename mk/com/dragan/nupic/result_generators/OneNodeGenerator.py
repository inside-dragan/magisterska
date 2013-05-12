'''
Created on May 15, 2012

@author: dzaharie
'''
import logging
from mk.dragan.resultgenerators.AbstractResultGenerator import AbstractResultGenerator

log = logging.getLogger('One Node Generator')

class OneNodeGenerator(AbstractResultGenerator):
    
    __sigmas = [0.001, 0.003, 0.01, 0.03, 0.06, 0.1, 0.15, 0.2, 0.3, 0.5]
#    __sigmas = [0.1]

    
    def _getSigmas(self):
        return self.__sigmas;
        
    def _areValidNodes(self):
        return self._isValidNode('level1')
    
    def _shouldStopIncreasingMaxDistance(self):
        return self._shouldStopIncreasingMaxDistanceForNode('level1')
    
    def _shouldStopDecreasingMaxDistance(self):
        return self._shouldStopDecreasingMaxDistanceForNode('level1')   
    
    def _getLevel1BottomUpOut(self):
        return 3000       
            
