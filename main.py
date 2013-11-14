import csv
import os.path
from string import center

def distance(a, b):
    result = 0
    for i in range(3):
        result += (a[i] - b[i]) ** 2
    return result

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

def predict(SequenceId, QuizDevice):
    
    distances = []
    for a in trainCenter.itervalues():
        temp = -1
        for b in testDict[SequenceId]:
            d = distance(a, b)
            if temp < 0 or d < temp:
                temp = d
        distances.append(temp)
    
    limit = -1
    for a in testDict[SequenceId]:
        d = distance(a, trainCenter[QuizDevice])
        if limit < 0 or d < limit:
            limit = d;
        
    count = 0
    for d in distances:
        if d >= limit:
            count += 1
    return count

if __name__ == '__main__':
    global trainCenter
    trainCenter = {}
    if os.path.exists('trainCenter.csv'):
        trainReader = csv.reader(open('trainCenter.csv', 'r'))
        for [DeviceId, X, Y, Z] in trainReader:
            trainCenter[DeviceId] = (float(X), float(Y), float(Z))
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
            trainCenter[DeviceId] = calculateCenter(acceleration)
        
        trainCenterFile = open('trainCenter.csv', 'w')
        trainWriter = csv.writer(trainCenterFile)
        for (DeviceId, center) in trainCenter.iteritems():
            trainWriter.writerow([DeviceId] + list(center))
        trainCenterFile.close()
        
    print 'reading test.csv...'
    testReader = csv.reader(open('test.csv', 'r'))
    testReader.next()
    
    global testDict
    testDict = {}
    for [T, X, Y, Z, SequenceId] in testReader:
        if not testDict.has_key(SequenceId):
            testDict[SequenceId] = []
        testDict[SequenceId].append((float(X), float(Y), float(Z)))
    
    print 'reading question.csv...'
    questionReader = csv.reader(open('questions.csv', 'r'))
    questionReader.next()
    
    submissionWriter = csv.writer(open('submisson.csv', 'w'))
    submissionWriter.writerow(['QuestionId', 'IsTrue'])
    
    print 'fucking busy...'
    for [QuestionId, SequenceId, QuizDevice] in questionReader:
        score = predict(SequenceId, QuizDevice)
        submissionWriter.writerow([QuestionId, score])
        print 'solved %s, %d' % (QuestionId, score)
    
    print 'done!'

    