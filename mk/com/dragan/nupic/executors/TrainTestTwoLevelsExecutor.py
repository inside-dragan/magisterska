'''
Created on Dec 11, 2011

@author: dzaharie
'''
import logging
from mk.com.dragan.nupic.executors.AbstractExecutor import AbstractExecutor
from mk.com.dragan.nupic.runners.SupervisedTwoLevelsRunner import SupervisedTwoLevelsRunner

log = logging.getLogger('TrainTest Two Levels Executor')

class TrainTestTwoLevelsExecutor(AbstractExecutor):
    __inputSize = None
    __numCategories = None
    __numLevel1 = None
    __numLevel2 = None
    
    def __init__(self, inputSize, numCategories, numLevel1, numLevel2):
        super(TrainTestTwoLevelsExecutor, self).__init__()
        self.__inputSize = inputSize
        self.__numCategories = numCategories
        self.__numLevel1 = numLevel1
        self.__numLevel2 = numLevel2
        
    def __createInputFiles(self):
        
        mainFiles = []
        trainFiles = []
        testFiles = []
        validateFiles = []
        evaluateFiles = []
        
        for i in range(1, self.__numLevel1 + 1):
            mainFiles.append(self._inputFolder + "/input" + str(i) + ".csv")
            trainFiles.append(self._inputFolder + "/input-train" + str(i) + ".csv")
            testFiles.append(self._inputFolder + "/input-test" + str(i) + ".csv")
            validateFiles.append(self._inputFolder + "/input-val" + str(i) + ".csv")
            evaluateFiles.append(self._inputFolder + "/input-eval" + str(i) + ".csv")
        mainFiles.append(self._inputFolder + '/cat.csv')
        trainFiles.append(self._inputFolder + '/cat-train.csv')
        testFiles.append(self._inputFolder + '/cat-test.csv')
        validateFiles.append(self._inputFolder + '/cat-val.csv')
        evaluateFiles.append(self._inputFolder + '/cat-eval.csv')
        
        self._separateFiles(mainFiles, trainFiles, testFiles, validateFiles, evaluateFiles) 
                   
        
    
    def executeSupervised(self, execEval = True, execTest = True, execVal = True):  
        
        self.__createInputFiles()
        
        if execEval:
            runner = SupervisedTwoLevelsRunner(self.__numLevel1, self.__numLevel2, 'eval')
            log.info('evaluation test: testing with the train data')
            runner.run(self.__inputSize, self.__numCategories, self._inputFolder, "input-train", "input-eval", "cat-train.csv", "cat-eval.csv")
    
        if execTest:
            runner = SupervisedTwoLevelsRunner(self.__numLevel1, self.__numLevel2, 'test')
            log.info('real test: testing with new data')
            runner.run(self.__inputSize, self.__numCategories, self._inputFolder, "input-train", "input-test", "cat-train.csv", "cat-test.csv")    

        if execVal:
            runner = SupervisedTwoLevelsRunner(self.__numLevel1, self.__numLevel2, 'val')
            log.info('validation test: testing with new data')
            runner.run(self.__inputSize, self.__numCategories, self._inputFolder, "input-train", "input-val", "cat-train.csv", "cat-val.csv")      