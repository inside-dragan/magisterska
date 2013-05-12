'''
Created on Dec 11, 2011

@author: dzaharie
'''
from mk.dragan.analyze.Analyzer import Analyzer
from mk.dragan.analyze.Report import Report
from mk.dragan.runners.AbstractRunner import AbstractRunner
from mk.dragan.utils.CsvUtils import stripFile
from nupic.analysis.visualizer.Visualizer import Visualizer
from mk.dragan.config.ExecConfig import VISUALIZE
from mk.dragan.tester.TesterTwoLevels import TesterTwoLevels
from mk.dragan.networks.SupervisedTwoLevelsNetwork import SupervisedTwoLevelsNetwork

class SupervisedTwoLevelsRunner(AbstractRunner):
    
    __numLevel1 = None
    __numLevel2 = None    
    
    def __init__(self, numLevel1, numLevel2, folderSuffix): 
        resultFile = 'result-supervised-' + str(numLevel1) + '-' + str(numLevel2) +'-1-' + folderSuffix
        self.__numLevel1 = numLevel1
        self.__numLevel2 = numLevel2        
        super(SupervisedTwoLevelsRunner, self).__init__(resultFile)
    
    def run(self, inputSize, numCategories, inputFolder, trainFilePrefix, testFilePrefix, catTrainFile, catTestFile):
        
        self._createFolder()
        network = SupervisedTwoLevelsNetwork(inputs=inputSize,
                  categories=numCategories,
                  resultFolder=self._resultFolder,
                  inputFolder=inputFolder,
                  numLevel1=self.__numLevel1,
                  numLevel2=self.__numLevel2)
        network.train(trainFilePrefix, catTrainFile)
        
        levelNodes = []
        for i in range(1, self.__numLevel1 + 1):
            levelNodes.append('level1' + str(i))
        for i in range(1, self.__numLevel2 + 1):
            levelNodes.append('level2' + str(i))
        r = Report(self._resultFolder, levelNodes=levelNodes, topNode="topNode")
        r.generateReport()
        
        tester = TesterTwoLevels(self._resultFolder, numLevel1=self.__numLevel1, numLevel2=self.__numLevel2)
        tester.test(inputFolder + '/' + testFilePrefix)
        stripFile(self._resultFolder + '/result.csv') ##//TODO fix this
        
        analyzer = Analyzer(self._resultFolder, inputFolder + '/' + catTestFile, inputFolder + '/' + testFilePrefix + '1.csv', csvdelimiter=' ')
        analyzer.extractCategories()
        analyzer.createStatistics()
    
        if VISUALIZE:
            v = Visualizer(self._resultFolder + "/network-trained.xml")
            v.visualizeNetwork(openBrowser=False) 