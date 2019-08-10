import os
import numpy as np
import csv


def writeResultCsv(names,result,traceName,fileName,comment = None):

    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)

    resultFile = os.path.join(path, fileName + '.csv')
    names.insert(0,'Trace Name')

    if not os.path.isfile(resultFile):
        f = open(resultFile, 'w')
        spamwriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(names)
    else:
        f = open(resultFile, 'a')
    newResultList = list(result)
    newResultList.insert(0,traceName)
    spamwriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(newResultList)
    f.close()