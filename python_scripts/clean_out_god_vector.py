import csv
import time
def open_the_file():
    feature_vector = []
    with open('../update_feature_vector.csv', 'rb') as myfile:
        thedatareader = csv.reader(myfile, delimiter=',')
        for row in thedatareader:
            feature_vector.append(row)
    return feature_vector

def clean_god_vector(original_god_vector):

    data_0      = 0
    data_1      = 0
    data_other  = 0

    #Store the updated CSV with counts
    with open('actual_week_call_counts.csv', 'w') as mycsvfile:
        for row in original_god_vector:
            #Write data if all year count greater than 0
            if (int(row[20]) > 0):
                if int(row[3]) == 0:
                    data_0 += 1
                if int(row[4]) == 0:
                    data_0 += 1
                if int(row[5])== 0:
                    data_0 += 1
                if int(row[3])== 1:
                    data_1 += 1
                if int(row[4])== 1:
                    data_1 += 1
                if int(row[5])== 1:
                    data_1 += 1
                if int(row[3])> 1:
                    data_other += 1
                if int(row[4])> 1:
                    data_other += 1
                if int(row[5])> 1:
                    data_other += 1
                mycsvfile.write(str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',2016,' + str(row[3]) + "\n")
                mycsvfile.write(str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',2015,' + str(row[4]) + "\n")
                mycsvfile.write(str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',2014,' + str(row[5]) + "\n")

    print("0: %.5f"%(data_0))
    print("1: %.5f"%(data_1))
    print("other: %.5f"%(data_other))

    print("Percentage of 0's %.4f"%((float(data_0)/(data_0 + data_1 + data_other))*100))
    print("Percentage of 1's %.4f"%((float(data_1)/(data_0 + data_1 + data_other))*100))
    print("Percentage of others %.4f"%((float(data_other)/(data_0 + data_1 + data_other))*100))

def main():

    #Load in the god vec
    original_god_vector = open_the_file()

    #Write where rad 0 all calls
    clean_god_vector(original_god_vector)

main()
