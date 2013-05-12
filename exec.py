'''
Created on Nov 25, 2011

@author: dzaharie
'''
#from mk.dragan.config.Params import Params
from mk.com.dragan.nupic.config.Params import Params
from mk.com.dragan.nupic.executors.TrainTestExecutor import TrainTestExecutor
from mk.com.dragan.nupic.executors.TrainTestOneLevelExecutor import TrainTestOneLevelExecutor
from mk.com.dragan.nupic.executors.TrainTestTwoLevelsExecutor import TrainTestTwoLevelsExecutor


Params().MAX_DISTANCE = 0.092207
Params().MAX_DISTANCE_2 = 0.01
Params().SIGMA = 0.33
Params().BOTTOM_UP_OUT = 3000 / (8 * 2)
Params().BOTTOM_UP_OUT_2 = 3000 / 2

executor = TrainTestExecutor(
            inputSize = 6,
            numCategories = 2)

#executor.executeSupervised(execEval=True, execTest=True, execVal=True)

#executor.executeUnsupervised()
#executor.executeBasicUnsupervised()
#executor.executeBasicSupervised()
#executor.executeHtmSupervised()

executor = TrainTestOneLevelExecutor(
            inputSize = 6,
            numCategories = 2,
            numNodes = 2)
#executor.executeSupervised(execEval=True, execTest=True, execVal=True)

executor = TrainTestTwoLevelsExecutor(
            inputSize = 6,
            numCategories = 2,
            numLevel1 = 8,
            numLevel2 = 2)
executor.executeSupervised(execEval=True, execTest=True, execVal=True)


