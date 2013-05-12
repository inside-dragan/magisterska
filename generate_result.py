from mk.dragan.executors.TrainTestExecutor import TrainTestExecutor
from mk.dragan.executors.TrainTestOneLevelExecutor import \
    TrainTestOneLevelExecutor
from mk.dragan.executors.TrainTestTwoLevelsExecutor import \
    TrainTestTwoLevelsExecutor
from mk.dragan.resultgenerators.OneLevelGenerator import OneLevelGenerator
from mk.dragan.resultgenerators.OneNodeGenerator import OneNodeGenerator
from mk.dragan.resultgenerators.TwoLevelsGenerator import TwoLevelsGenerator

#single node
#generator = OneNodeGenerator(TrainTestExecutor(6, 2))


#one level network
#executor = TrainTestOneLevelExecutor(inputSize=6, numCategories=2, numNodes=4)
#generator = OneLevelGenerator(executor, numNodes=4)


#two levels network
executor = TrainTestTwoLevelsExecutor(inputSize=3, numCategories=2, numLevel1=4, numLevel2=2)
generator = TwoLevelsGenerator(executor, numNodesLevel1=4, numNodesLevel2=2)


generator.generateResult(dataCreatorInfoPair = (None, "result generated"))