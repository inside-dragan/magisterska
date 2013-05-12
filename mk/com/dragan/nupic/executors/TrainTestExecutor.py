'''
Created on Nov 25, 2011

@author: dzaharie
'''
from mk.dragan.executors.AbstractExecutor import AbstractExecutor
from mk.dragan.runners.BasicSupervisedRunner import BasicSupervisedRunner
from mk.dragan.runners.BasicUnsupervisedRunner import BasicUnsupervisedRunner
from mk.dragan.runners.HtmSupervisedRunner import HtmSupervisedRunner
from mk.dragan.runners.SupervisedRunner import SupervisedRunner
from mk.dragan.runners.UnsupervisedRunner import UnsupervisedRunner
from mk.dragan.utils.loggingDef import logging

log = logging.getLogger('TrainTestExecutor')

class TrainTestExecutor(AbstractExecutor):
    __inputSize = None
    __numCategories = None
    
    def __init__(self, inputSize, numCategories):
        super(TrainTestExecutor, self).__init__()
        self.__inputSize = inputSize
        self.__numCategories = numCategories
        
    def __createInputFiles(self):
        mainFiles = [self._inputFolder + "/input1.csv", self._inputFolder + "/cat.csv"]
        trainFiles = [self._inputFolder + "/input-train1.csv", self._inputFolder + "/cat-train.csv"]
        testFiles = [self._inputFolder + "/input-test1.csv", self._inputFolder + "/cat-test.csv"]
        validateFiles = [self._inputFolder + "/input-val1.csv", self._inputFolder + "/cat-val.csv"]
        evaluateFiles = [self._inputFolder + "/input-eval1.csv", self._inputFolder + "/cat-eval.csv"]
        
        self._separateFiles(mainFiles, trainFiles, testFiles, validateFiles, evaluateFiles) 
    
    def executeSupervised(self, execEval = True, execTest = True, execVal = True):  
        self.__createInputFiles()
        
        if execEval:
            runner = SupervisedRunner('result-supervised-eval')
            log.info('evaluation test: testing with the train data')
            runner.run(self.__inputSize, self.__numCategories, self._inputFolder, "input-train1.csv", "input-eval1.csv", "cat-train.csv", "cat-eval.csv")
    
        self.__createInputFiles()
        
        if execTest:
            runner = SupervisedRunner('result-supervised-real')
            log.info('real test: testing with new data')
            runner.run(self.__inputSize, self.__numCategories, self._inputFolder, "input-train1.csv", "input-test1.csv", "cat-train.csv", "cat-test.csv")
            
        if execVal:
            runner = SupervisedRunner('result-supervised-val')
            log.info('validation test: testing with new data')
            runner.run(self.__inputSize, self.__numCategories, self._inputFolder, "input-train1.csv", "input-val1.csv", "cat-train.csv", "cat-val.csv")            
        
    def executeUnsupervised(self):  
        super(TrainTestExecutor, self).executeUnsupervised() 
        runner = UnsupervisedRunner()
        runner.run(self.__inputSize, self.__numCategories, self._inputFolder, "input1.csv", "input1.csv", "cat.csv")
        
    def executeBasicSupervised(self):  
        super(TrainTestExecutor, self).executeBasicSupervised()
        runner = BasicSupervisedRunner()
        runner.run(self.__inputSize, self.__numCategories, self._inputFolder, "input1.csv", "input1.csv", "cat.csv", "cat.csv")        
        
    def executeBasicUnsupervised(self):  
        super(TrainTestExecutor, self).executeBasicUnsupervised() 
        runner = BasicUnsupervisedRunner()
        runner.run(self.__inputSize, self.__numCategories, self._inputFolder, "input1.csv", "input1.csv", "cat.csv")
        
    def executeHtmSupervised(self):  
        super(TrainTestExecutor, self).executeHtmSupervised() 
        runner = HtmSupervisedRunner()
        runner.run(self.__inputSize, self.__numCategories, self._inputFolder, "input1.csv", "input1.csv", "cat.csv", "cat.csv")
    