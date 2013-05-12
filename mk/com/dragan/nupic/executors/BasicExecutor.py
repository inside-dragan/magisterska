'''
Created on Nov 20, 2011

@author: Dragan
'''
from mk.dragan.executors.AbstractExecutor import AbstractExecutor
from mk.dragan.runners.BasicSupervisedRunner import BasicSupervisedRunner
from mk.dragan.runners.BasicUnsupervisedRunner import BasicUnsupervisedRunner
from mk.dragan.runners.HtmSupervisedRunner import HtmSupervisedRunner
from mk.dragan.runners.SupervisedRunner import SupervisedRunner
from mk.dragan.runners.UnsupervisedRunner import UnsupervisedRunner



class BasicExecutor(AbstractExecutor):
    
    __inputSize = None
    __numCategories = None
    
    __inputTrainFile = None
    __inputTestFile = None
    __catTrainFile = None
    __catTestFile = None
    
    def __init__(self, inputSize, numCategories, inputTrainFile, inputTestFile, catTrainFile, catTestFile):
        super(BasicExecutor, self).__init__()
        self.__inputSize = inputSize
        self.__numCategories = numCategories
        self.__inputTrainFile = inputTrainFile
        self.__inputTestFile = inputTestFile
        self.__catTrainFile = catTrainFile
        self.__catTestFile = catTestFile
    
    def executeSupervised(self):  
        super(BasicExecutor, self).executeSupervised()
        runner = SupervisedRunner()
        runner.run(self.__inputSize, self.__numCategories, self._inputFolder, self.__inputTrainFile, self.__inputTestFile, self.__catTrainFile, self.__catTestFile)
        
    def executeUnsupervised(self):  
        super(BasicExecutor, self).executeUnsupervised() 
        runner = UnsupervisedRunner()
        runner.run(self.__inputSize, self.__numCategories, self._inputFolder, self.__inputTrainFile, self.__inputTestFile, self.__catTestFile)
        
    def executeBasicSupervised(self):  
        super(BasicExecutor, self).executeBasicSupervised()
        runner = BasicSupervisedRunner()
        runner.run(self.__inputSize, self.__numCategories, self._inputFolder, self.__inputTrainFile, self.__inputTestFile, self.__catTrainFile, self.__catTestFile)        
        
    def executeBasicUnsupervised(self):  
        super(BasicExecutor, self).executeBasicUnsupervised() 
        runner = BasicUnsupervisedRunner()
        runner.run(self.__inputSize, self.__numCategories, self._inputFolder, self.__inputTrainFile, self.__inputTestFile, self.__catTestFile)
        
    def executeHtmSupervised(self):  
        super(BasicExecutor, self).executeHtmSupervised() 
        runner = HtmSupervisedRunner()
        runner.run(self.__inputSize, self.__numCategories, self._inputFolder, self.__inputTrainFile, self.__inputTestFile, self.__catTrainFile, self.__catTestFile)
    
    
