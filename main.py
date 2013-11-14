'''
Created on 2013-11-14

@author: kongfy
'''

import csv
import os.path
import math
from NaiveBayes import NaiveBayes

def calculateCenter(Sequence):
    tX = tY = tZ = 0
    l = len(Sequence)
    for (X, Y, Z) in Sequence:
        tX += X
        tY += Y
        tZ += Z
    tX /= l
    tY /= l
    tZ /= l
    return (tX, tY, tZ)

def calculateStdev(Sequence, mean):
    tX = tY = tZ = 0
    l = len(Sequence)
    for (X, Y, Z) in Sequence:
        tX += (X - mean[0]) ** 2
        tY += (Y - mean[1]) ** 2
        tZ += (Z - mean[2]) ** 2
    tX /= l;
    tY /= l;
    tZ /= l;
    tX = math.sqrt(tX)
    tY = math.sqrt(tY)
    tZ = math.sqrt(tZ)
    return (tX, tY, tZ)

def calculateInfo(Sequence):
    result = {}
    result['mean'] = calculateCenter(Sequence)
    result['stdev'] = calculateStdev(Sequence, result['mean'])
    result['count'] = len(Sequence)
    
    return result

def predict(Sample, QuizDevice):
    plist = []
    for DeviceId in trainInfo.iterkeys():
        plist.append(classifier.predict(Sample, DeviceId))
    
    temp = classifier.predict(Sample, QuizDevice)
    count = 0
    for p in plist:
        if p < temp:
            count = count + 1
    return count

if __name__ == '__main__':
    global trainInfo
    trainInfo = {}
    if os.path.exists('trainInfo.csv'):
        trainReader = csv.reader(open('trainInfo.csv', 'r'))
        for [DeviceId, meanX, meanY, meanZ, stdevX, stdevY, stdevZ, count] in trainReader:
            trainInfo[DeviceId] = {'mean' : (float(meanX), float(meanY), float(meanZ)),
                                   'stdev' : (float(stdevX), float(stdevY), float(stdevZ)),
                                   'count' : int(count), 
                                   }
        
    else:
        print 'reading train.csv...'
        trainReader = csv.reader(open('train.csv', 'r'))
        trainReader.next()
    
        trainDict = {}
        for [T, X, Y, Z, DeviceId] in trainReader:
            if not trainDict.has_key(DeviceId):
                trainDict[DeviceId] = []
            trainDict[DeviceId].append((float(X), float(Y), float(Z)))
        
        print 'calculate with train...'    
        for (DeviceId, acceleration) in trainDict.iteritems():
            trainInfo[DeviceId] = calculateInfo(acceleration)
        
        trainInfoFile = open('trainInfo.csv', 'w')
        trainWriter = csv.writer(trainInfoFile)
        for (DeviceId, value) in trainInfo.iteritems():
            trainWriter.writerow([DeviceId] + list(value['mean']) + list(value['stdev']) + [value['count']])
        trainInfoFile.close()
        
    testCenter = {}
    if os.path.exists('testCenter.csv'):
        testReader = csv.reader(open('testCenter.csv', 'r'))
        for [SequenceId, X, Y, Z] in testReader:
            testCenter[SequenceId] = (float(X), float(Y), float(Z))
    else:
        print 'reading test.csv...'
        testReader = csv.reader(open('test.csv', 'r'))
        testReader.next()
        
        testDict = {}
        for [T, X, Y, Z, SequenceId] in testReader:
            if not testDict.has_key(SequenceId):
                testDict[SequenceId] = []
            testDict[SequenceId].append((float(X), float(Y), float(Z)))
            
        print 'calculate with test...'    
        for (SequenceId, acceleration) in testDict.iteritems():
            testCenter[SequenceId] = calculateCenter(acceleration)
        
        testCenterFile = open('testCenter.csv', 'w')
        testWriter = csv.writer(testCenterFile)
        for (SequenceId, value) in testCenter.iteritems():
            testWriter.writerow([SequenceId] + list(value))
        testCenterFile.close()
        
    global classifier
    classifier = NaiveBayes(trainInfo)
    
    print 'reading question.csv...'
    questionReader = csv.reader(open('questions.csv', 'r'))
    questionReader.next()
    
    submissionWriter = csv.writer(open('submisson_naiveBayes.csv', 'w'))
    submissionWriter.writerow(['QuestionId', 'IsTrue'])
    
    print 'fucking busy...'
    for [QuestionId, SequenceId, QuizDevice] in questionReader:
        score = predict(testCenter[SequenceId], QuizDevice)
        submissionWriter.writerow([QuestionId, score])
#        print 'solved %s, %d' % (QuestionId, score)
    
    print 'done!'
    
    
    
    