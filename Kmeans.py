'''
Created on 2013-11-16

@author: kongfy
'''

import random
import pprint
import cPickle

import sys

class Cluster(object):
    
    def __init__(self):
        self.__clusterCenter = cPickle.load(open('clusterCenter.dat', 'r'))
        pprint.pprint(self.__clusterCenter)
    
    def __distance(self, a, b):
        return (a - b)**2
    
    def __transAttribute(self, attrName, value):
        clusterNo = -1
        minDist = -1
        center = self.__clusterCenter[attrName]
        for i in range(len(center)):
            d = self.__distance(center[i], value)
            if minDist < 0 or d < minDist:
                minDist = d
                clusterNo = i
        return clusterNo
    
    def trans(self, sample):
        return (self.__transAttribute('X', sample[0]),
                self.__transAttribute('Y', sample[1]),
                self.__transAttribute('Z', sample[2])
                )
        
import csv

class Kmeans(object):
    
    def __init__(self):
        pass
    
    def __distance(self, a, b):
        return (a - b)**2
    
    def __readcsv(self, filename):
        csvReader = csv.reader(open(filename, 'r'))
        csvReader.next()
        
        attrs = []
        for [attr] in csvReader:
            attrs.append(float(attr))
        return attrs
    
    def __judge(self, value, centers):
        result = -1
        temp = -1
        for (index, center) in enumerate(centers):
            d = self.__distance(value, center)
            if temp < 0 or d < temp:
                result = index
                temp = d
        return result
    
    def train(self, filename, K):
        attrs = self.__readcsv(filename)
        
        centers = random.sample(attrs, K)
        
        runCount = 0
        while True:
            print centers
            flag = True
            
            temp = []
            for i in range(K):
                temp.append([0,0])
            
            for index, attr in enumerate(attrs):
                sys.stdout.write("\rprocessing %s / %s" % (index, len(attrs)))
                sys.stdout.flush()
                index = self.__judge(attr, centers)
                temp[index][0] += attr
                temp[index][1] += 1
            sys.stdout.write('\n')
            
            for (index, total, count) in enumerate(temp):
                newCenter = total / count
                if newCenter != centers[index]:
                    flag = False
                    centers[index] = newCenter
            if flag or runCount >= 2:
                break
            runCount += 1
        return centers
        
if __name__ == '__main__':
    worker = Kmeans()
    clusterCenter = {'X' : worker.train('x.csv', 5),
                     'Y' : worker.train('y.csv', 5),
                     'Z' : worker.train('z.csv', 5),
                     }
    
    f = open('clusterCenter.dat', 'w')
    cPickle.dump(clusterCenter, f)
    f.close()
    