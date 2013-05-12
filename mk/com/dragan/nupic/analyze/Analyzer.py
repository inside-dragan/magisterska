'''
Created on Jul 26, 2011

@author: dzaharie
'''
from mk.dragan.utils.CsvUtils import readFloatData, readIntData, readStringData, \
    isNullArray
from mk.dragan.utils.loggingDef import logging
from mk.dragan.config.ResultContainer import ResultContainer
from mk.dragan.config.Params import Params

log = logging.getLogger('Analyzer')

class Analyzer:
    
    __resultFile = None
    __trueCatsFile = None
    __inputFile = None
    __catsFile = None
    __statisticsFile = None
    
#    __groupSize = None
    __csvdelimiter = None
    
    def __init__(self, folder, trueCatsFile, inputFile, csvdelimiter=' '):
        self.__resultFile = folder + "/result.csv" 
        self.__catsFile = folder + "/categories.csv"
        self.__trueCatsFile = trueCatsFile
        self.__inputFile = inputFile
        self.__statisticsFile = folder + "/statistics.txt"
        self.__csvdelimiter = csvdelimiter

    def extractCategories(self):
        x = readFloatData(self.__resultFile, self.__csvdelimiter)
        
        out = open(self.__catsFile, 'w')
        for i in range(0, len(x)):
            if (max(x[i]) == 0):
                out.write('? \n')
            else:
                out.write(str(x[i].index(max(x[i]))) + '\n')
        out.close()
        log.info(self.__catsFile + ' file created.') 
        
  
    def createStatistics(self):
        res = readStringData(self.__catsFile, self.__csvdelimiter)
        inputData = readStringData(self.__inputFile)
        trueCats = readIntData(self.__trueCatsFile, self.__csvdelimiter)
        
        count = 0
        correct = 0
        unknown = 0
        
        correct0 = 0
        correct1 = 0
        total0 = 0
        total1 = 0
        
        groupCount = 0
        groupCorrect = 0
        groupUnknown = 0
        
        totalPerGroup = 0
        correctPerGroup = 0
        unknownPerGroup = 0
        
        text = ''
        f = open(self.__statisticsFile, 'w')
        for r, i, t in zip(res, inputData, trueCats):
            if isNullArray(i):
                if totalPerGroup > 0:
                    groupCount = groupCount + 1
                    wrongPerGroup = totalPerGroup - (correctPerGroup + unknownPerGroup)
                    if correctPerGroup > unknownPerGroup and correctPerGroup > wrongPerGroup:
                        groupCorrect = groupCorrect + 1
                        text = text + 'AS GROUP: CORRECT \n\n'
                    elif wrongPerGroup > correctPerGroup and wrongPerGroup > unknownPerGroup:
                        text = text + 'AS GROUP: WRONG \n\n'
                    else:
                        groupUnknown = groupUnknown + 1
                        text = text + 'AS GROUP: UNKNOWN \n\n'
                    totalPerGroup = 0
                    correctPerGroup = 0
                    unknownPerGroup = 0
                        
                text = text + str(t[0]) + ' -> ' + r[0] + ' ======== separator \n' 
            elif r[0] == '?':
                count = count + 1
                unknown = unknown + 1
                totalPerGroup = totalPerGroup + 1
                unknownPerGroup = unknownPerGroup + 1
                text = text + str(t[0]) + ' -> ' + r[0] + ' unknown \n'
            elif int(r[0]) == t[0]:
                count = count + 1
                correct = correct + 1
                totalPerGroup = totalPerGroup + 1
                correctPerGroup = correctPerGroup + 1
                text = text + str(t[0]) + ' -> ' + r[0] + '\n'
                if r[0] == '0':
                    correct0 += 1
                if r[0] == '1':
                    correct1 += 1
            else: 
                count = count + 1
                text = text + str(t[0]) + ' -> ' + r[0] + ' wrong \n'
                totalPerGroup = totalPerGroup + 1
            
            if not isNullArray(i):
                if t[0] == 0:
                    total0 += 1
                elif t[0] == 1:
                    total1 += 1
                
        
        if count > unknown:
            percentage = (float(correct) / float(count - unknown)) * 100
        else:
            percentage = 0
        unknownPercentage = float(unknown) * 100 / float(count)
#        if groupCount > groupUnknown:
#            groupPercentage = (float(groupCorrect) / float(groupCount - groupUnknown)) * 100
#        else:
#            groupPercentage = ''           
        f.write('correct: %s%% \n' % percentage)
        f.write('unknown: %s%% \n\n' % unknownPercentage)
        f.write('total: %s \n' % count)
        f.write('total recognized: %s \n' % (count - unknown))
        f.write('correct: %s (zeros: %s/%s, ones: %s/%s) \n' % (correct, correct0, total0, correct1, total1))
        f.write('unknown: %s \n' % unknown)
        
        
#        f.write('==============================\n\n\n')
#        f.write('== per group ==\n')
#        f.write('total: %s \n' % groupCount)
#        f.write('total recognized: %s \n' % (groupCount - groupUnknown))
#        f.write('correct: %s \n' % groupCorrect)
#        if groupCount > 0:
#            f.write('percentage: %s \n' % groupPercentage)        
        
        f.write('==============================\n\n\n')
        f.write(text)
        f.write('==============================\n\n\n')
        f.write('correct: %s%% \n' % percentage)
        f.write('unknown: %s%% \n\n' % unknownPercentage)
        f.write('total: %s \n' % count)
        f.write('total recognized: %s \n' % (count - unknown))
        f.write('correct: %s (zeros: %s/%s, ones: %s/%s) \n' % (correct, correct0, total0, correct1, total1))
        f.write('unknown: %s \n' % unknown)
        f.close()
        
        ResultContainer().addResult({'max-distance': Params().MAX_DISTANCE, 'max-distance2': Params().MAX_DISTANCE_2, 'sigma': Params().SIGMA, 'sigma2': Params().SIGMA_2, 'correct': percentage, 'unknown': unknownPercentage});
        
        log.info(self.__statisticsFile + ' file created')
        log.info('correct: %0.2f%% (%s/%s  unknown: %0.2f%%)' % (percentage, correct, count, unknownPercentage))
            
