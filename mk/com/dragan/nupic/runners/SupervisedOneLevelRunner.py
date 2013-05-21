'''
Created on Dec 11, 2011

@author: dzaharie
'''
from nupic.analysis.visualizer.Visualizer import Visualizer
from mk.com.dragan.nupic.analyze.Analyzer import Analyzer
from mk.com.dragan.nupic.analyze.Report import Report
from mk.com.dragan.nupic.config.ExecConfig import VISUALIZE
from mk.com.dragan.nupic.networks.SupervisedOneLevelNetwork import SupervisedOneLevelNetwork
from mk.com.dragan.nupic.runners.AbstractRunner import AbstractRunner
from mk.com.dragan.nupic.testers.TesterOneLevel import TesterOneLevel
from mk.com.dragan.utils.CsvUtils import stripFile


class SupervisedOneLevelRunner(AbstractRunner):
    
    __numNodes = None
    
    
    def __init__(self, numNodes, folderSuffix): 
        self.__numNodes = numNodes
        resultFile = 'result-supervised-' + str(numNodes) + '-1-' + folderSuffix
        super(SupervisedOneLevelRunner, self).__init__(resultFile)
        
    def run(self, inputSize, numCategories, inputFolder, trainFilePrefix, testFilePrefix, catTrainFile, catTestFile):
        
        self._createFolder()
        network = SupervisedOneLevelNetwork(inputs=inputSize,
                  categories=numCategories,
                  resultFolder=self._resultFolder,
                  inputFolder=inputFolder,
                  numNodes=self.__numNodes)
        network.train(trainFilePrefix, catTrainFile)
        levelNodes = []
        for i in range(1, self.__numNodes + 1):
            levelNodes.append('level1' + str(i))
        r = Report(self._resultFolder, levelNodes=levelNodes, topNode="topNode")
        r.generateReport()
        
        tester = TesterOneLevel(self._resultFolder, self.__numNodes)
        tester.test(inputFolder + '/' + testFilePrefix)
        stripFile(self._resultFolder + '/result.csv') ##//TODO fix this
        
        analyzer = Analyzer(self._resultFolder, inputFolder + '/' + catTestFile, inputFolder + '/' + testFilePrefix + '1.csv', csvdelimiter=' ')
        analyzer.extractCategories()
        analyzer.createStatistics()
    
        if VISUALIZE:
            v = Visualizer(self._resultFolder + "/network-trained.xml")
            v.visualizeNetwork(openBrowser=False) 
