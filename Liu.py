import math
import os
import numpy as np
import csvWrite as csvWriter
def Yao_QoE_Estimation(listOfNumbers,traceName,filename):


    names = [
        'initDelayPenalty',
        'stallImpairment',
        'levelVariationImpairment',
        'P1',
        'P2',
        'C1',
        'C2',
        'StallDuration',
        'NoOfStall',
        'avgVqm',
        'avgRepresentationLevel',
        'P21',
        'P22',
        'K',
        'QoE',
        'SubjectiveMOS'
    ]
    #ends
    #model parameters
    alpha = 3.2
    a = 3.35
    b = 3.98
    c = 2.5
    d = 1800
    k = 0.15
    B1 = 73.6
    B2 = 1608
    mu = 0.05
    C1 = 0.15
    C2 = 0.82

    videoBitrate = []
    representationIndex = []  
    lineCounter = 0
    initDelayPenalty = 0.0
    stallImpairment = 0.0
    levelVariationImpairment = 0.0
    totalStallDuration = 0.0
    numOfStall = 0
    vqmList = []
    numSeg = len(listOfNumbers)
    D = [0.0] * numSeg
    P1 = 0.0
    P2 = 0.0
    R = 0.0
    MOS = 0.0
    avgRepLevel = 0.0
    avgVqm = 0.0
    P21 = 0.0
    P22 = 0.0
    for line in listOfNumbers:
        lineCounter += 1
        resultPerLine = list(map(float, line.split(',')[0:17]))
        vqmList.append(resultPerLine[13])
        segmentDuration = resultPerLine[3]
        representationIndex.append(resultPerLine[0])
        videoBitrate.append(resultPerLine[2])
        if lineCounter == 1:
            initDelayPenalty = min(alpha * resultPerLine[1] , 100)
        
        if lineCounter > 1:
            if resultPerLine[1] > 0:
                totalStallDuration += float(resultPerLine[1])
                numOfStall += 1
    

    avgVqm = np.average(vqmList)
    avgRepLevel = np.average(representationIndex)
    stallImpairment =  a * totalStallDuration + b * numOfStall - c * math.sqrt(totalStallDuration * numOfStall)

    for i in range(1,numSeg):
        if(abs(vqmList[i] - vqmList[i-1]) < mu):
            D[i] = D[i - 1] + 1
        else:
            D[i] = 0.0
        if((vqmList[i] - vqmList[i-1]) >  0):

            P22 += abs(vqmList[i] - vqmList[i-1]) ** 2

            P2 += abs(vqmList[i] - vqmList[i - 1]) ** 2

        elif ((vqmList[i] - vqmList[i-1]) <  0):

            P21 += abs(vqmList[i] - vqmList[i-1]) ** 2

    for i in range(0,numSeg):
        P1 += vqmList[i] * math.exp(k * segmentDuration * D[i])
    
    P1 = P1 / numSeg
    P2 = P2 / numSeg
    
    levelVariationImpairment = B1 * P1 + B2 * P2

    R = 100 - initDelayPenalty - stallImpairment - levelVariationImpairment + C1 * initDelayPenalty * math.sqrt(stallImpairment+levelVariationImpairment) + C2 * math.sqrt(stallImpairment * levelVariationImpairment)
    #composition = C1 * initDelayPenalty * math.sqrt(stallImpairment+levelVariationImpairment) + C2 * math.sqrt(stallImpairment * levelVariationImpairment)
    #R = 100 - ( -0.78*initDelayPenalty + 0.53*stallImpairment + 0.61*levelVariationImpairment +
    # 0.32*(C1 * initDelayPenalty * math.sqrt(stallImpairment+levelVariationImpairment) +
     #  C2 * math.sqrt(stallImpairment * levelVariationImpairment)) -19.9 )
    

    
    
    
    
    c1_t = initDelayPenalty * math.sqrt(stallImpairment+levelVariationImpairment)
    c2_t = math.sqrt(stallImpairment * levelVariationImpairment)
    #R = 100 - (initDelayPenalty - stallImpairment - levelVariationImpairment + C1 * initDelayPenalty * math.sqrt(stallImpairment+levelVariationImpairment) + C2 * math.sqrt(stallImpairment * levelVariationImpairment))
    #R = 100 - (initDelayPenalty + stallImpairment + levelVariationImpairment + C1 * initDelayPenalty * math.sqrt(stallImpairment+levelVariationImpairment) + C2 * math.sqrt(stallImpairment * levelVariationImpairment))
    MOS = 1 + 0.035 * R + 7 * 10**-6 * R * (R - 60) * (100 - R) 

    datacsv = f = open(r'C:\Users\varun\OneDrive\Thesis\temp\dataset\data.csv', 'r')
    liness = f.readlines()
    lines = liness[1:]
    for s in lines:

        resulttt = s.split(',')[0:2]

        if(resulttt[0]==filename):
            SubMos = resulttt[1]
            break
    result = [
        initDelayPenalty,
        stallImpairment,
        levelVariationImpairment,
        P1,
        P2,
        c1_t,
        c2_t,
        totalStallDuration,
        numOfStall,
        avgVqm,
        avgRepLevel,
        P21,
        P22,
        k,
        R,
        SubMos
    ]
    fileName, file_extension = os.path.splitext(__file__)
    csvWriter.writeResultCsv(names,result,traceName,fileName)
    #ends

