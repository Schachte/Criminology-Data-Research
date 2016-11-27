'''
NIJ Accuracy Implementation

'''
import heapq
from collections import Counter

def loadCrimeCounts():
    data_set = []
    with open("actual_week_call_counts.csv", 'r') as mycsvfile:
        for row in mycsvfile:
            data_set.append(row.split(","))
    return data_set

def getActualCallsList(week, year, data):
    '''Get the actual calls based on a week/year filter'''

    final_data = {}
    for row in data:
        if int(row[2]) == week and int(row[3]) == year:
            final_data[(int(row[0]), int(row[1]))] = int(row[4])
    return final_data

def calcPAI_PEI(predictions, actual_calls):

    #Number of cells total in the grid
    A = len(predictions)

    #Number of total calls total
    N = sum(actual_calls.values())

    #Number of calls in the regions that were predicted as hotspots
    n = 0
    # Number of hotspots that we predict
    a = 0
    for index, value in enumerate(predictions):
        #print(value[0], value[1])
        if value[2] == 1:
            n += actual_calls[(value[0], value[1])]
            a += 1

    PAI = (float(n)/N)/(float(a)/A)

    n_star = sum(heapq.nlargest(a, actual_calls.values()))

    PEI = PAI / ((float(n_star)/N)/(float(a)/A))

    return PAI, PEI
