'''
Created on 2013-11-16

@author: kongfy
'''
import csv

if __name__ == '__main__':
    
    trainReader = csv.reader(open('train.csv', 'r'))
    trainReader.next()
    
    fX = open('x.csv', 'w')
    fY = open('y.csv', 'w')
    fZ = open('z.csv', 'w')
    xWriter = csv.writer(fX)
    yWriter = csv.writer(fY)
    zWriter = csv.writer(fZ)
    
    xWriter.writerow(['X'])
    yWriter.writerow(['Y'])
    zWriter.writerow(['Z'])
        
    for [T, X, Y, Z, DeviceId] in trainReader:
        xWriter.writerow([X])
        yWriter.writerow([Y])
        zWriter.writerow([Z])
        
    testReader = csv.reader(open('test.csv', 'r'))
    testReader.next()
    
    for [T, X, Y, Z, SequenceId] in testReader:
        xWriter.writerow([X])
        yWriter.writerow([Y])
        zWriter.writerow([Z])
        
    fX.close()
    fY.close()
    fZ.close()