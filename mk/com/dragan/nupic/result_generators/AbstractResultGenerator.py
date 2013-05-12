'''
Created on Jun 7, 2012

@author: dzaharie
'''
from mk.dragan.config.Params import Params
from mk.dragan.config.ResultContainer import ResultContainer
from mk.dragan.utils.CsvUtils import writeData
from mk.dragan.utils.DatabaseUtils import dbgetlist, dbsetlist
import logging
import os
import shutil
import traceback

log = logging.getLogger('Abstract Result Generator')

class AbstractResultGenerator(object):
    
    __resultFolder = None
    _executor = None
    
    def __init__(self, executor):
        self._executor = executor
    
    def _areValidNodes(self):
        raise NotImplementedError()
    def _shouldStopIncreasingMaxDistance(self):
        raise NotImplementedError()
    def _shouldStopDecreasingMaxDistance(self):
        raise NotImplementedError()
    
    def _getLevel1BottomUpOut(self):
        raise NotImplementedError()    
    
    def _getSigmas(self):
        raise NotImplementedError()
    
    def _createData(self, dataCreator):
        outPath = os.getcwd() + '/input'
        if os.path.exists(outPath):
            shutil.rmtree(outPath)
        os.mkdir(outPath)   
        
        writeData(dataCreator.getCat(), outPath + '/cat.csv') 
        inputs = dataCreator.getInputs()
        for i in range(0, len(inputs)):
            writeData(inputs[i], outPath + '/input' + str(i+1) + '.csv')     
    
    def _strResult(self, dictionaryList):
        result = ''
        for dictionary in dictionaryList:
            result += "level 1) %0.6f" % dictionary['max-distance'] + ' '
            result += "%0.6f" % dictionary['sigma'] + ' '
            result += "level 2) %0.6f" % dictionary['max-distance2'] + ' '
            result += "%0.6f" % dictionary['sigma2'] + ' '            
            result += "result) %0.2f" % dictionary['correct'] + ' '
            result += "%0.2f" % dictionary['unknown'] + ' '
            result += '\n'
        return result    
    
    def _isValidNode(self, nodeName):
        coincidences = ResultContainer().coincidences[nodeName]['num']
        largestGroupSize = ResultContainer().coincidences[nodeName]['size-of-largest']
        return coincidences >= 10 and largestGroupSize > 1
    
    def _isValidResult(self):
        perc = ResultContainer().getLatestResult()['correct']
        unknown = ResultContainer().getLatestResult()['unknown']
        return  perc > 55 and unknown < 40
    
    def _shouldStopIncreasingMaxDistanceForNode(self, nodeName):
        if ResultContainer().isEmpty():
            return False
        coincidences = ResultContainer().coincidences[nodeName]['num']
        largestGroupSize = ResultContainer().coincidences[nodeName]['size-of-largest']
        log.info("stop increasing? largestGroupSize=" + str(largestGroupSize) + " coincidences=" + str(coincidences))
        return coincidences < 10 or largestGroupSize * 3 > coincidences;
     
    def _shouldStopDecreasingMaxDistanceForNode(self, nodeName):
        if ResultContainer().isEmpty():
            return False
        largestGroupSize = ResultContainer().coincidences[nodeName]['size-of-largest']
        
        coincidences = ResultContainer().coincidences[nodeName]['num']
        log.info("stop decreasing? largestGroupSize=" + str(largestGroupSize) + " coincidences=" + str(coincidences))
        return largestGroupSize < 2 or coincidences > self._getLevel1BottomUpOut()
    
    def _calculateMaxDistances(self):
        result = []
        maximal = 0.01
        while not self._shouldStopIncreasingMaxDistance():
            Params().MAX_DISTANCE = maximal
            try:
                log.info('calculating max distance. trying: ' + str(maximal))
                self._executor.executeSupervised(execEval=True, execTest=False, execVal=False)
            except RuntimeError:
                log.error('error thrown for maxDistance=' + str(maximal)) 
            maximal *= 2
                
        minimal = 50.0
        while not self._shouldStopDecreasingMaxDistance():
            Params().MAX_DISTANCE = minimal
            try:
                log.info('calculating max distance. trying: ' + str(minimal))
                self._executor.executeSupervised(execEval=True, execTest=False, execVal=False)
            except RuntimeError:
                log.error('error thrown for maxDistance=' + str(minimal)) 
                log.error(traceback.format_exc())
                break #error is thrown because so small maxDistance is not allowed any more
            minimal /= 2
        
        log.info("max distance calculated in the range of: " + str(minimal) + " - " + str(maximal))
        if maximal > minimal:
            step = (maximal - minimal) / 10
            for i in range(0, 11):
                result.append(minimal + step*i)
        return result         
    
    def _initGenerateResult(self, dataCreator):
        if dataCreator != None:
            self._createData(dataCreator)
        Params().BOTTOM_UP_OUT = self._getLevel1BottomUpOut()    
        ResultContainer().clear()            
    
    def generateResult(self, dataCreator):

        self._initGenerateResult(dataCreator)
        result = ''
        pairs = []
        
        maxDistances = dbgetlist('maxDistances', dataCreator.getDescription())
        if not maxDistances:
            maxDistances = self._calculateMaxDistances()
            dbsetlist('maxDistances', dataCreator.getDescription(), maxDistances)
        ResultContainer().clear()
            
        for s in self._getSigmas():
            for d in maxDistances:
                log.info("trying: distance=%s sigma=%s" % (d, s))
                Params().MAX_DISTANCE = d
                Params().SIGMA = s
                try:
                    self._executor.executeSupervised(execEval=True, execTest=False, execVal=False)
                    if (self._isValidResult() and self._areValidNodes()):
                        pairs.append((d, s))
                except RuntimeError:
                    log.error('error thrown for maxDistance=' + str(d) + ' and sigma=' + str(s))
                    log.error(traceback.format_exc())
                    
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
        
        info = dataCreator.getDescription()
        print 'tesing combination: ' + str(info)
        self.addToFile(str(info) + '\n')
        self.addToFile(result + '\n\n\n')
        print result  
        return result    

