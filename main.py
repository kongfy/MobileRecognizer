import csv

def distance(a, b):
    result = 0;
    for i in range(3):
        result += (a[i] - b[i]) ** 2;
    return result;

def center(Sequence):
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

if __name__ == '__main__':
    print 'reading train.csv...'
    trainReader = csv.reader(open('train.csv', 'r'))
    trainReader.next()

    trainDict = {}
    for [T, X, Y, Z, DeviceId] in trainReader:
        if not trainDict.has_key(DeviceId):
            trainDict[DeviceId] = [];
        trainDict[DeviceId].append((float(X), float(Y), float(Z)))
    
    print 'calculate with train...'    
    trainCenter = {}
    for (DeviceId, acceleration) in trainDict.iteritems():
        trainCenter[DeviceId] = center(acceleration)
        
    print 'reading test.csv...'
    testReader = csv.reader(open('test.csv', 'r'))
    testReader.next();
    
    testDict = {}
    for [T, X, Y, Z, SequenceId] in testReader:
        if not testDict.has_key(SequenceId):
            testDict[SequenceId] = [];
        testDict[SequenceId].append((float(X), float(Y), float(Z)))
        
    print 'calculate with test...'    
    testCenter = {}
    for (SequenceId, acceleration) in testDict.iteritems():
        testCenter[SequenceId] = center(acceleration)
    
    print 'reading question.csv...'
    questionReader = csv.reader(open('questions.csv', 'r'))
    questionReader.next()
    
    submissionWriter = csv.writer(open('submisson.csv', 'w'))
    submissionWriter.writerow(['QuestionId', 'IsTrue']);
    
    print 'fucking busy...'
    for [QuestionId, SequenceId, QuizDevice] in questionReader:
        score = -distance(testCenter[SequenceId], trainCenter[QuizDevice]);
        submissionWriter.writerow([QuestionId, score])
        print 'solved %s, %f' % (QuestionId, score)
    
    print 'done!'
    
    
    
    