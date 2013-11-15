'''
Created on 2013-11-14

@author: kongfy
'''

import csv
import os.path
import math
from NaiveBayes import NaiveBayes
import cPickle
import sys

def calculateCenter(Sequence):
    tX = tY = tZ = 0
    l = len(Sequence)
    for (T, X, Y, Z) in Sequence:
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
    for (T, X, Y, Z) in Sequence:
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
#    result['mean'] = calculateCenter(Sequence)
#    result['stdev'] = calculateStdev(Sequence, result['mean'])
    result['count'] = len(Sequence)
    result['start_time'] = Sequence[0][0]
    result['end_time'] = Sequence[len(Sequence) - 1][0]
    
    return result

def countSequence(Sequence):
    cX = {}
    cY = {}
    cZ = {}
    for (T, X, Y, Z) in Sequence:
        cX[X] = cX.get(X, 0) + 1
        cY[Y] = cY.get(Y, 0) + 1
        cZ[Z] = cZ.get(Z, 0) + 1
    
    return (cX, cY, cZ)

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
    if os.path.exists('trainInfo.dat'):
        trainInfo = cPickle.load(open('trainInfo.dat', 'r'))
    else:
        print 'reading train.csv...'
        trainReader = csv.reader(open('train.csv', 'r'))
        trainReader.next()
    
        trainDict = {}
        for [T, X, Y, Z, DeviceId] in trainReader:
            if not trainDict.has_key(DeviceId):
                trainDict[DeviceId] = []
            trainDict[DeviceId].append((float(T),
                                        int(round(float(X))),
                                        int(round(float(Y))),
                                        int(round(float(Z))),
                                        ))
        
        print 'calculate with train...'    
        for (DeviceId, acceleration) in trainDict.iteritems():
            trainInfo[DeviceId] = calculateInfo(acceleration)
            trainInfo[DeviceId]['counter'] = countSequence(acceleration)
        
        trainInfoFile = open('trainInfo.dat', 'w')
        cPickle.dump(trainInfo, trainInfoFile)
        trainInfoFile.close()
        
    testInfo = {}
    if os.path.exists('testInfo.dat'):
        testInfo = cPickle.load(open('testInfo.dat', 'r'))
    else:
        print 'reading test.csv...'
        testReader = csv.reader(open('test.csv', 'r'))
        testReader.next()
        
        testDict = {}
        for [T, X, Y, Z, SequenceId] in testReader:
            if not testDict.has_key(SequenceId):
                testDict[SequenceId] = []
            testDict[SequenceId].append((float(T), float(X), float(Y), float(Z)))
            
        print 'calculate with test...'
        for (SequenceId, acceleration) in testDict.iteritems():
            testInfo[SequenceId] = calculateInfo(acceleration)
            testInfo[SequenceId]['mean'] = tuple([int(round(x)) for x in calculateCenter(acceleration)])
        
        
        testInfoFile = open('testInfo.dat', 'w')
        cPickle.dump(testInfo, testInfoFile)
        testInfoFile.close()
        
    global classifier
    classifier = NaiveBayes(trainInfo, (True, True, True))
    
    print 'reading question.csv...'
    questionReader = csv.reader(open('questions.csv', 'r'))
    questionReader.next()
    
    submissionFile = open('submisson.csv', 'w')
    submissionWriter = csv.writer(submissionFile)
    submissionWriter.writerow(['QuestionId', 'IsTrue'])
    
    print 'fucking busy...'
    sys.stdout.write("\r")
    for [QuestionId, SequenceId, QuizDevice] in questionReader:
        if trainInfo[QuizDevice]['end_time'] > testInfo[SequenceId]['start_time']:
#            print 'killed by timestamp '
            score = -1
        else:
            score = predict(testInfo[SequenceId]['mean'], QuizDevice)
        submissionWriter.writerow([QuestionId, score])
        sys.stdout.write("\rsolved %s / 90024" % (QuestionId))
        sys.stdout.flush()
    
    submissionFile.close()
    
    sys.stdout.write("\n")
    print "mession complate!"
    
    