'''
Created on 2013-11-14

@author: kongfy
'''

import math

class NaiveBayes(object):
    def __init__(self, trainInfo, isCategory):
        self.__trainInfo = trainInfo
        self.__isCategory = isCategory
        self.__train()
    
    def __train(self):
        self.__total = 0
        for value in self.__trainInfo.itervalues():
            self.__total = self.__total + value['count']
    
    def predict(self, Sample, targetDevice):
        temp = self.__trainInfo[targetDevice]['count'] / float(self.__total)
        
        for i in range(len(Sample)):
            if self.__isCategory[i]:
                if self.__trainInfo[targetDevice]['counter'][i].has_key(Sample[i]):
                    temp *= self.__trainInfo[targetDevice]['counter'][i][Sample[i]] / float(self.__trainInfo[targetDevice]['count'])
                else:
                    temp *= 1 / float(self.__trainInfo[targetDevice]['count'] + 1)
            else:
                mean = self.__trainInfo[targetDevice]['mean'][i]
                stdev = self.__trainInfo[targetDevice]['stdev'][i]
                var = Sample[i]
                
                gauss = 1 / float(math.sqrt(2*math.pi) * stdev);
                t = var - mean
                gauss *= math.exp(-t**2 / (2*stdev**2))
                temp *= gauss
            
        return temp
        