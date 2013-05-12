'''
Created on Nov 24, 2011

@author: Dragan
'''
from mk.dragan.analyze.Analyzer import Analyzer
from mk.dragan.analyze.Report import Report
from mk.dragan.networks.BasicUnsupervisedNetwork import BasicUnsupervisedNetwork
from mk.dragan.runners.AbstractRunner import AbstractRunner
from mk.dragan.tester.Tester import Tester
from mk.dragan.utils.CsvUtils import stripFile

class BasicUnsupervisedRunner(AbstractRunner):
    
    def __init__(self, resultFile='result-basic-unsupervised'): 
        super(BasicUnsupervisedRunner, self).__init__(resultFile)  
    
    def run(self, inputSize, numCategories, inputFolder, inputTrainFile, inputTestFile, catTestFile):
        
        self._createFolder()
        network = BasicUnsupervisedNetwork(inputs=inputSize,
                            categories=numCategories,
                            inputFolder=inputFolder,
                            resultFolder=self._resultFolder) 
        network.train(inputTrainFile)
        r = Report(self._resultFolder)
        r.generateReport()

        tester = Tester(self._resultFolder)
        tester.test(inputFolder + '/' + inputTestFile)
        stripFile(self._resultFolder + '/result.csv') ##//TODO fix this
        
        analyzer = Analyzer(self._resultFolder, inputFolder + '/' + catTestFile, inputFolder + '/' + inputTestFile, csvdelimiter=' ')
        analyzer.extractCategories()
        analyzer.createStatistics() 