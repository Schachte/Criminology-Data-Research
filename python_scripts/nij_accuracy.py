'''
NIJ Accuracy Implementation

'''
import heapq

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
        if row[2] == week and row[3] == year:
            final_data[(row[0], row[1])] = row[4]
    return final_data

def calcPAI (testData, predictions, actual_calls):
    '''Calculates the prediction accuracy index'''

    #Number of cells total in the grid
    A = len(predictions)

    #Number of hotspots that we predict
    a = predictions.count(1)

    #Number of total calls total
    N = sum(actual_calls.values())

    #Number of calls in the regions that were predicted as hotspots
    n = 0
    for index, value in enumerate(predictions):
        if value == 1:
            n += actual_calls[(testData[index][76], testData[index][77])]

    return (float(n)/N)/(float(a)/A)

def calcPEI(testData, predictions, actual_calls):
    PAI = calcPAI(testData, predictions, actual_calls)

    #Number of cells total in the grid
    A = len(predictions)

    #Number of hotspots that we predict
    a = predictions.count(1)

    #Number of total calls total
    N = sum(actual_calls.values())

    n_star = sum(heapq.nlargest(a, actual_calls.values()))

    return PAI / ((float(n_star)/N)/(float(a)/A))


def main():

    #Load the god_vector




main()
