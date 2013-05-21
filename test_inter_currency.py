from mk.com.dragan.nupic.executors import TrainTestExecutor
from mk.com.dragan.nupic.result_generators import OneNodeGenerator

generator = OneNodeGenerator(TrainTestExecutor(16, 2))
generator.generateResult(item)

