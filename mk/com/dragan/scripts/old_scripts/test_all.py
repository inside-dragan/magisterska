'''
Created on Feb 26, 2012

@author: Dragan
'''
import os
import shutil

from mk.dragan.config.Params import Params
from mk.dragan.config.ResultContainer import ResultContainer
from mk.dragan.executors.TrainTestExecutor import TrainTestExecutor
from mk.dragan.utils.CsvUtils import writeData


statsFolder = os.getcwd() + '/result-merged'
if os.path.exists(statsFolder):
    shutil.rmtree(statsFolder)
os.mkdir(statsFolder)   

maxDistances = [0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1, 1.3, 1.5, 2]
sigmas = [0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7]

#maxDistances = [1.7, 2]
#sigmas = [2]

executor = TrainTestExecutor(
            inputSize=4,
            numCategories=2)

print "evaluation..."
pairs = []
for d in maxDistances:
    for s in sigmas:
        print "distance=%s sigma=%s" % (d, s)
        Params().MAX_DISTANCE = d
        Params().SIGMA = s
        executor.executeSupervised(execEval=True, execTest=False, execVal=False)
        perc = ResultContainer().result['correct']
        unknownPerc = ResultContainer().result['unknown']
        if perc < 58:
            break
        else:
            if perc > 60 and unknownPerc < 80:
                pairs.append((d, s))

print "found appropriate pairs: "
print pairs

print "testing..."
for pair in pairs:
    d = pair[0]
    s = pair[1]
    print "distance=%s sigma=%s" % (d, s)
    Params().MAX_DISTANCE = d
    Params().SIGMA = s
    executor.executeSupervised(execEval=False, execTest=True, execVal=False)

r = ResultContainer().result

to5 = []
to20 = []
to40 = []
to60 = []
above = []

writeData(r, statsFolder + '/results_all.csv')
for line in r: 
    print ["%0.2f" % i for i in line]
    unknown = line[3]
    if unknown < 5:
        to5.append(line)
    elif unknown < 20:
        to20.append(line)
    elif unknown < 40:
        to40.append(line)
    elif unknown < 60:
        to60.append(line)
    elif unknown < 80:
        above.append(line)
        

maxTo5 = None
maxTo20 = None
maxTo40 = None
maxTo60 = None
maxAbove = None

if len(to5) > 0:
    maxTo5 = to5[0]
    for x in to5:
        if x[2] > maxTo5[2]:
            maxTo5 = x
  
if len(to20) > 0:      
    maxTo20 = to20[0]
    for x in to20:
        if x[2] > maxTo20[2]:
            maxTo20 = x    
 
if len(to40) > 0:       
    maxTo40 = to40[0]
    for x in to40:
        if x[2] > maxTo40[2]:
            maxTo40 = x 
    
if len(to60) > 0:    
    maxTo60 = to60[0]
    for x in to60:
        if x[2] > maxTo60[2]:
            maxTo60 = x 
  
if len(above) > 0:      
    maxAbove = above[0]
    for x in above:
        if x[2] > maxAbove[2]:
            maxAbove = x 
        
result = []
print '=== results ==='
if maxTo5 is not None:    
    result.append(maxTo5) 
    print ["%0.2f" % i for i in maxTo5]
if maxTo20 is not None:
    result.append(maxTo20)
    print ["%0.2f" % i for i in maxTo20]
if maxTo40 is not None:
    result.append(maxTo40)
    print ["%0.2f" % i for i in maxTo40]
if maxTo60 is not None:
    result.append(maxTo60)
    print ["%0.2f" % i for i in maxTo60]
if maxAbove is not None:
    result.append(maxAbove)
    print ["%0.2f" % i for i in maxAbove]
                            
writeData(result, statsFolder + '/results_max.csv')


validationResults = []
if maxTo5 is not None:
    ResultContainer().result = []
    Params().MAX_DISTANCE = maxTo5[0]
    Params().SIGMA = maxTo5[1]
    executor.executeSupervised(execEval=False, execTest=False, execVal=True)
    validationResults.append(ResultContainer().result[0])
    
if maxTo20 is not None:
    ResultContainer().result = []
    Params().MAX_DISTANCE = maxTo20[0]
    Params().SIGMA = maxTo20[1]
    executor.executeSupervised(execEval=False, execTest=False, execVal=True)
    validationResults.append(ResultContainer().result[0])
    
if maxTo40 is not None:
    ResultContainer().result = []
    Params().MAX_DISTANCE = maxTo40[0]
    Params().SIGMA = maxTo40[1]
    executor.executeSupervised(execEval=False, execTest=False, execVal=True)
    validationResults.append(ResultContainer().result[0])    
    
if maxTo60 is not None:
    ResultContainer().result = []
    Params().MAX_DISTANCE = maxTo60[0]
    Params().SIGMA = maxTo60[1]
    executor.executeSupervised(execEval=False, execTest=False, execVal=True)
    validationResults.append(ResultContainer().result[0])        

if maxAbove is not None:
    ResultContainer().result = []
    Params().MAX_DISTANCE = maxAbove[0]
    Params().SIGMA = maxAbove[1]
    executor.executeSupervised(execEval=False, execTest=False, execVal=True)
    validationResults.append(ResultContainer().result[0])


print '=== validation results ==='
for line in validationResults:
    print ["%0.2f" % i for i in line]
    
writeData(validationResults, statsFolder + '/results_validation.csv')
