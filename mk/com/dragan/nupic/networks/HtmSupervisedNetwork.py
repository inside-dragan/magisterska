'''
Created on Aug 30, 2011

@author: dzaharie
'''
from mk.dragan.networks.AbstractNetwork import AbstractNetwork
from mk.dragan.networks.BasicDataInterface import BasicDataInterface
from nupic.network.simplehtm import SimpleHTM
from mk.dragan.utils.loggingDef import logging
from mk.dragan.config.Params import Params
log = logging.getLogger('HtmSupervisedNetwork')    



class HtmSupervisedNetwork(AbstractNetwork):
    
    __net = None
    
    def __init__(self, inputs, categories, inputFolder, resultFolder):
        self._resultFolder = resultFolder
        self._inputs = inputs
        self._categories = categories
        self._inputFolder = inputFolder
        
        self.__net = self._createNetwork()
    
    
    def _createNetwork(self):
        levelParams = self.__levelParameterFactory()
        # Now construct the SimpleHTM object using these parameters.
        net = SimpleHTM(levelParams=levelParams)
#        net.setValue("prefix", self._resultFolder + '/')
        net.addParam("trainedFilename", default=self._resultFolder + '/network-trained.xml')
#        net.addParam("untrainedFilename", default=self._resultFolder + '/network-runtime.xml')
        # Create the network from SimpleHTM object
        data = BasicDataInterface(sizeInput=self._inputs, sizeCats=self._categories)
        
        net.createNetwork(data, False)
        return net
        
    def train(self, trainDataFile, categoriesFile):
        
        data = BasicDataInterface(
            sizeInput=self._inputs,
            inputFileName=self._inputFolder + '/' + trainDataFile,
            sizeCats=self._categories,
#            resultFile=self._resultFolder + '/network-trained.xml',
            catFileName=self._inputFolder + '/' + categoriesFile)
        
        self.__net.train(data=data)
        log.info('training complete.')
        
    def visualize(self):
        self.__net.visualize()

    def __levelParameterFactory(self):
        """ Returns a valid "levelParams" structure which can be used to initialize
        a SimpleHTM.  Fills in the node parameters we will not change in our context,
        and allows the user to specify the rest as input arguments.
        """
        
        levelParams = [
          { # Level 0
          },
          { # Level 1
            'levelSize': 1,
            'outputElementCount': Params().BOTTOM_UP_OUT,
            'spatialPoolerAlgorithm': Params().SPATIAL_POOLER_ALGORITHM,
            'sigma': Params().SIGMA,
            'maxDistance': Params().MAX_DISTANCE,
            'symmetricTime': Params().SYMETRIC_TIME,
            'transitionMemory': Params().TRANSITION_MEMORY,
            'topNeighbors': Params().TOP_NEIGHBOURS,
            'maxGroupSize': Params().MAX_GROUP_SIZE,
            'temporalPoolerAlgorithm': Params().TEMPORAL_POOLER_ALGORITHM,
            'detectBlanks': Params().DETECT_BLANKS
          }
        ]
        # Top level
        levelParams.append(
          { 
            'levelSize': 1,
            'spatialPoolerAlgorithm': Params().SPATIAL_POOLER_ALGORITHM_TOP,
            'mapperAlgorithm': Params().MAPPER_ALGORITHM
          })
        return levelParams
