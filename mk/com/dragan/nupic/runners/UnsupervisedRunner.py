'''
Created on Nov 24, 2011

@author: Dragan
'''
from mk.com.dragan.nupic.analyze.Analyzer import Analyzer
from mk.com.dragan.nupic.analyze.Report import Report
from mk.com.dragan.nupic.networks.UnsupervisedNetwork import UnsupervisedNetwork
from mk.com.dragan.nupic.runners.AbstractRunner import AbstractRunner
from mk.com.dragan.nupic.testers.Tester import Tester
from mk.com.dragan.utils.CsvUtils import stripFile


class UnsupervisedRunner(AbstractRunner):
    
    def __init__(self, resultFile='result-unsupervised'): 
        super(UnsupervisedRunner, self).__init__(resultFile)              
    
    def run(self, inputSize, numCategories, inputFolder, inputTrainFile, inputTestFile, catTestFile):
        self._createFolder()
        network = UnsupervisedNetwork(inputs=inputSize,
                            categories=numCategories,
                            inputFolder=inputFolder,
                            resultFolder=self._resultFolder) 
        network.train(inputTrainFile)
        r = Report(self._resultFolder, levelNodes=["level1"], topNode="topNode")
        r.generateReport()
        
        tester = Tester(self._resultFolder)
        tester.test(inputFolder + '/' + inputTestFile)
        stripFile(self._resultFolder + '/result.csv') ##//TODO fix this
        
        analyzer = Analyzer(self._resultFolder, inputFolder + '/' + catTestFile, inputFolder + '/' + inputTestFile, csvdelimiter=' ')
        analyzer.extractCategories()
        analyzer.createStatistics()      