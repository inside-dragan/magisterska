'''
Created on Nov 24, 2011

@author: Dragan
'''
from mk.dragan.analyze.Analyzer import Analyzer
from mk.dragan.analyze.Report import Report
from mk.dragan.networks.BasicSupervisedNetwork import BasicSupervisedNetwork
from mk.dragan.runners.AbstractRunner import AbstractRunner
from mk.dragan.tester.Tester import Tester
from mk.dragan.utils.CsvUtils import stripFile
from nupic.analysis.visualizer.Visualizer import Visualizer


class BasicSupervisedRunner(AbstractRunner):
    
    def __init__(self, resultFile='result-basic-supervised'): 
        super(BasicSupervisedRunner, self).__init__(resultFile)     
    
    def run(self, inputSize, numCategories, inputFolder, inputTrainFile, inputTestFile, catTrainFile, catTestFile):
       
        self._createFolder()
        network = BasicSupervisedNetwork(inputs=inputSize,
                          categories=numCategories,
                          resultFolder=self._resultFolder,
                          inputFolder=inputFolder)
        
        network.train(inputTrainFile, catTrainFile)
        r = Report(self._resultFolder)
        r.generateReport()
        
        tester = Tester(self._resultFolder)
        tester.test(inputFolder + '/' + inputTestFile)
        stripFile(self._resultFolder + '/result.csv') ##//TODO fix this
        
        analyzer = Analyzer(self._resultFolder, inputFolder + '/' + catTestFile, inputFolder + '/' + inputTestFile, csvdelimiter=' ')
        analyzer.extractCategories()
        analyzer.createStatistics()
    
        v = Visualizer(self._resultFolder + "/network-trained.xml")
        v.visualizeNetwork(openBrowser=False)         
