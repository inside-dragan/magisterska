'''
Created on Jun 10, 2012

@author: dzaharie
'''
from mk.dragan.config.Params import Params
from mk.dragan.config.ResultContainer import ResultContainer
from mk.dragan.resultgenerators.AbstractResultGenerator import \
    AbstractResultGenerator
import logging
from mk.dragan.utils.DatabaseUtils import dbgetlist, dbsetlist
import traceback

log = logging.getLogger('Two Levels Generator')

class TwoLevelsGenerator(AbstractResultGenerator):
    
    __sigmas = [0.3]
#    __sigmas = [0.5]

    __numNodesLevel1 = None
    __numNodesLevel2 = None

    def __init__(self, executor, numNodesLevel1, numNodesLevel2):
        super(TwoLevelsGenerator, self).__init__(executor)
        self.__numNodesLevel1 = numNodesLevel1
        self.__numNodesLevel2 = numNodesLevel2

    def _getSigmas(self):
        return self.__sigmas;
        
    def _areValidNodes(self):
        result = True
        for i in range(1, self.__numNodesLevel1 + 1):
            result = result and self._isValidNode('level1' + str(i))
        for i in range(1, self.__numNodesLevel2 + 1):
            result = result and self._isValidNode('level2' + str(i))
        return result
    
    def _shouldStopIncreasingMaxDistance(self):
        result = False
        for i in range(1, self.__numNodesLevel1 + 1):
            result = result or self._shouldStopIncreasingMaxDistanceForNode('level1' + str(i))
        return result
    
    def _shouldStopIncreasingMaxDistance2ForNode(self, nodeName):
        if ResultContainer().isEmpty():
            return False
        coincidences = ResultContainer().coincidences[nodeName]['num']
        largestGroupSize = ResultContainer().coincidences[nodeName]['size-of-largest']
        log.info("stop increasing for level2? largestGroupSize=" + str(largestGroupSize) + " coincidences=" + str(coincidences))
        return coincidences < 10 or largestGroupSize * 3 > coincidences;
    
    def _shouldStopDecreasingMaxDistance2ForNode(self, nodeName):
        if ResultContainer().isEmpty():
            return False
        largestGroupSize = ResultContainer().coincidences[nodeName]['size-of-largest']
        
        coincidences = ResultContainer().coincidences[nodeName]['num']
        log.info("stop decreasing for level2? largestGroupSize=" + str(largestGroupSize) + " coincidences=" + str(coincidences))
        return largestGroupSize < 2 or coincidences > self._getLevel2BottomUpOut()    
    
    def _shouldStopDecreasingMaxDistance(self):
        result = False
        for i in range(1, self.__numNodesLevel1 + 1):
            result = result or self._shouldStopDecreasingMaxDistanceForNode('level1' + str(i))
        return result
    
    def _shouldStopIncreasingMaxDistance2(self):
        result = False
        for i in range(1, self.__numNodesLevel2 + 1):
            result = result or self._shouldStopIncreasingMaxDistance2ForNode('level2' + str(i))            
        return result
    
    def _shouldStopDecreasingMaxDistance2(self):
        result = False
        for i in range(1, self.__numNodesLevel2 + 1):
            result = result or self._shouldStopDecreasingMaxDistance2ForNode('level2' + str(i))            
        return result    

    
    def __calculateMaxDistances2(self, maxDistances):
        result = []
        
        Params().BOTTOM_UP_OUT = self._getLevel1BottomUpOut()
        Params().BOTTOM_UP_OUT_2 = self._getLevel2BottomUpOut()
        Params().SIGMA = 0.33
        
        maxDistance = maxDistances[len(maxDistances) / 2]
        Params().MAX_DISTANCE = maxDistance
        
        maximal = 0.01
        while not self._shouldStopIncreasingMaxDistance2():
            Params().MAX_DISTANCE_2 = maximal
            try:
                log.info('max distance: ' + str(maxDistance) + '. calculating max distance2. trying: ' + str(maximal))
                self._executor.executeSupervised(execEval=True, execTest=False, execVal=False)
            except RuntimeError:
                log.error('max distance: ' + str(maxDistance) + '. error thrown for maxDistance2=' + str(maximal)) 
                log.error(traceback.format_exc())
            maximal *= 2
                
        minimal = 50.0
        while not self._shouldStopDecreasingMaxDistance2():
            Params().MAX_DISTANCE_2 = minimal
            try:
                log.info('calculating max distance2. trying: ' + str(minimal))
                self._executor.executeSupervised(execEval=True, execTest=False, execVal=False)
            except RuntimeError:
                log.error('error thrown for maxDistance2=' + str(minimal)) 
                log.error(traceback.format_exc())
                break #error is thrown because so small maxDistance is not allowed any more
            minimal /= 2
                
        log.info("max distance2 calculated in the range of: " + str(minimal) + " - " + str(maximal))                
        if maximal > minimal:
            step = (maximal - minimal) / 10
            for i in range(0, 11):
                result.append(minimal + step * i)
        return result     
    
    def generateResult(self, dataCreator, currency):
        self._initGenerateResult(dataCreator)
        
        
        result = ''
        pairs = []
        
        Params().MAX_DISTANCE_2 = 1000
        Params().BOTTOM_UP_OUT = 3000
        #we don't care about level 2, just prevent it from throwing exceptions
            
        maxDistances = dbgetlist('maxDistances', dataCreator.getDescription())
        if not maxDistances:
            maxDistances = self._calculateMaxDistances()
            dbsetlist('maxDistances', dataCreator.getDescription(), maxDistances)
            
        maxDistances2 = dbgetlist('maxDistances level2', dataCreator.getDescription())
        if (not maxDistances2):
            maxDistances2 = self.__calculateMaxDistances2(maxDistances)  
            dbsetlist('maxDistances level2', dataCreator.getDescription(), maxDistances2)       
        ResultContainer().clear()
        
        counter = 0;
        for s2 in self._getSigmas():
            for s in self._getSigmas():
                for d2 in maxDistances2: 
                    for d in maxDistances:
                        counter = counter + 1
                        log.info("trying: distance=%s sigma=%s distance2=%s sigma2=%s" % (d, s, d2, s2))
                        log.info(currency + ' ' + str(dataCreator.getDescription()))
                        log.info('trying: round ' + str(counter) + ' out of ' + str(len(self._getSigmas()) * len(self._getSigmas()) * len(maxDistances) * len(maxDistances2)))
                        Params().SIGMA_2 = s2
                        Params().SIGMA = s
                        Params().MAX_DISTANCE_2 = d2
                        Params().MAX_DISTANCE = d
                        try:
                            self._executor.executeSupervised(execEval=True, execTest=False, execVal=False)
                            if (self._isValidResult() and self._areValidNodes()):
                                pairs.append((d, s))
                        except RuntimeError:
                            log.error('error distance=%s sigma=%s distance2=%s sigma2=%s' % (d, s, d2, s2))
                    
        r = ResultContainer().result
        result += 'training results: \n' + self._strResult(r)                                   
        
        ResultContainer().result = []
        for pair in pairs:
            d = pair[0]
            s = pair[1]
            log.info("testing combination: distance=%s sigma=%s" % (d, s))
            Params().MAX_DISTANCE = d
            Params().SIGMA = s
            self._executor.executeSupervised(execEval=False, execTest=True, execVal=False)
        
        r = ResultContainer().result
        result += 'testing results: \n' + self._strResult(r)
        
        found = []
        for line in r:
            if line['unknown'] < 40: #zemi gi samo tie so unknown pomalku od 40%
                found.append(line)
        
        if len(found) > 0:
            maxx = found[0]
            for x in found:
                if x['correct'] > maxx['correct']:
                    maxx = x
                    
            result += 'best testing result: ' + self._strResult([maxx])
            
            ResultContainer().result = []
            Params().MAX_DISTANCE = maxx['max-distance']
            Params().SIGMA = maxx['sigma']
            self._executor.executeSupervised(execEval=False, execTest=False, execVal=True)
            validationResult = ResultContainer().getLatestResult()
            
            result += 'validation result: ' + self._strResult([validationResult])
        
        return result                
    
    def _getLevel1BottomUpOut(self):
        return 3000 / (self.__numNodesLevel1 * self.__numNodesLevel2) 
    
    def _getLevel2BottomUpOut(self):
        return 1000 / self.__numNodesLevel2            
            

