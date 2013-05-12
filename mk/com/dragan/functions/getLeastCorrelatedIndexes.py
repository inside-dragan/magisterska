'''
Created on Jan 28, 2012

@author: Dragan
'''
def calculateIndexes(correlFunction, maxIndex):
    result = ['placeholder to make list 1-based', 1]
    
    correlFunction.insert(0, 'placeholder to make list 1-based')
    while result[-1] < maxIndex:
        maxValue = index = -1
        for k in range(result[-1] + 1, maxIndex + 1):
            summary = 0;
            for i in range(1, len(result)):
                summary += abs(correlFunction[k - result[i]])
            x = abs(correlFunction[k]) / summary
            if x > maxValue:
                index = k
                maxValue = x
        result.append(index)
    return result[1:];
    
    