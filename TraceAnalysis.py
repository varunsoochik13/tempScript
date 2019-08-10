import os
import math
import numpy as np
import csvWrite as csvWriter
import Liu as yao
from argparse import ArgumentParser

#parser = ArgumentParser(description='Parsing the results')

#parser.add_argument(
 #   '--path',
 #   '-p',
 #   dest='dir_path',
 #   action='store',
 #  help='Directory where traces are',
 #   required=False,
 #   )


#args = parser.parse_args()

def summary_results(listOfNumbers, traceName,filename):
    
    videoBitrate = []
    rate = []
    stallList = []
    representationIndex = []
    maxRate = 0
    lineCounter = 0
    initialDelay = 0
    numOfStalls = 0
    totalStallDuration = 0
    numSeg = 0
    avgRate = 0
    prevRate = -1
    numOfSwitches = 0
    
    for line in listOfNumbers:
        lineCounter += 1
        resultsPerLine = list(map(float, line.split(',')[0:17]))

        numSeg = len(listOfNumbers)
        segmentDuration = resultsPerLine[3]
        representationIndex.append(resultsPerLine[0])
        videoBitrate.append(resultsPerLine[2])

        if lineCounter == 1:
            initialDelay = resultsPerLine[1]
        if lineCounter > 1:
            #if resultsPerLine[1] > 0:
            stallList.append(resultsPerLine[1])
            if resultsPerLine[1] > 0:
                numOfStalls += 1
            totalStallDuration += resultsPerLine[1]
        
    for i in range(0,len(representationIndex)):
        if(prevRate == -1):
            prevRate = representationIndex[i]
        rateDiff = representationIndex[i] - prevRate
        prevRate = representationIndex[i]
        if(rateDiff != 0):
            numOfSwitches += 1
    maxRate = max(videoBitrate)
    avgRate = np.mean(videoBitrate)

    if sum(stallList) == 0.0:
            yao.Yao_QoE_Estimation(listOfNumbers,traceName,filename)

def open_trace(traceName,filename):
    f = open(traceName, 'r')
    allLines = f.readlines()
    return summary_results(allLines[1:] , traceName,filename)

if __name__ == '__main__':

    for (dirname, dirnames, filenames) in os.walk(r'C:\Users\varun\OneDrive\Thesis\temp\temp_ds'):
        for filename in filenames:
            nameOfFile = os.path.join(dirname, filename)
            newBatch = open_trace(nameOfFile,filename)
            