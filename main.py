import csv

def distance(a, b):
    result = 0;
    for i in range(3):
        result += (a[i] - b[i]) ** 2;
    return result;

def predict(SequenceId, QuizDevice):
    result = -1;
    
    tX = 0
    tY = 0
    tZ = 0
    
    for a in testDict[SequenceId]:
        tX += a[0]
        tY += a[1]
        tZ += a[2]
    
    l = len(testDict[SequenceId])
    tX /= l
    tY /= l
    tZ /= l
    
    for b in trainDict[QuizDevice]:
        d = distance((tX, tY, tZ), b)
        if result < 0 or d < result:
            result = d;
    return result;

if __name__ == '__main__':
    print 'reading train.csv...'
    trainReader = csv.reader(open('train.csv', 'r'))
    trainReader.next()

    trainDict = {}
    for [T, X, Y, Z, DeviceId] in trainReader:
        if not trainDict.has_key(DeviceId):
            trainDict[DeviceId] = [];
        trainDict[DeviceId].append((float(X), float(Y), float(Z)))
        
    print 'reading test.csv...'
    testReader = csv.reader(open('test.csv', 'r'))
    testReader.next();
    
    testDict = {}
    for [T, X, Y, Z, SequenceId] in testReader:
        if not testDict.has_key(SequenceId):
            testDict[SequenceId] = [];
        testDict[SequenceId].append((float(X), float(Y), float(Z)))
    
    print 'reading question.csv...'
    questionReader = csv.reader(open('questions.csv', 'r'))
    questionReader.next()
    
    submissionWriter = csv.writer(open('submisson.csv', 'w'))
    submissionWriter.writerow(['QuestionId', 'IsTrue']);
    
    print 'fucking busy...'
    for [QuestionId, SequenceId, QuizDevice] in questionReader:
        score = -predict(SequenceId, QuizDevice)
        submissionWriter.writerow([QuestionId, score])
        print 'solved %s, %f' % (QuestionId, score)
    
    
    
    
    