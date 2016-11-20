'''
@Code
***************************************
Criminology Data Set                  *
Training and Testing Dataset Creation *
***************************************

@Authors
    * Ryan Schachte
    * Fatima Naveed
    * Rob Stevens
    * Trevor Richardson

@Purpose
    * Take the feature dictionary and produce feature
    * vectors from it for training and testing
'''

import csv
import math
import datetime
from audioop import avg
from cmath import sqrt

'''
 Creates the feature vector given the appropriate god vectors
 Note: 'Current' year is given by the following:
 2016: 3
 2015: 4
 2014: 5

 Structure is as follows:
 0-15: radius 0 data (see code for data points)
 16-31: radius 1 data
 32-47: radius 2 data
 48-63: radius 3 data
 64-66: All-time data
 67-70: Identifying data
 71: Classification
'''
def get_feature_vectors(year, god_vector_this_week, god_vector_last_week, god_vector_2_weeks, god_vector_next_week, classifier_limit):
    this_year_features = []
    year2 = year
    year1 = year
    yearf = year

    if god_vector_this_week[2] <= 0:
        year1 = year + 1

    if god_vector_this_week[2] <= 1:
        year2 = year + 1

    if god_vector_this_week[2] >= 51:
        yearf = year - 1

    #Add week data to feature vector
    this_year_features.append(god_vector_2_weeks[year2])         #2 weeks ago (most recent data)
    this_year_features.append(god_vector_2_weeks[year2 + 1])     #2 weeks ago (1 year ago)
    this_year_features.append(god_vector_2_weeks[year2 + 2])     #2 weeks ago (2 years ago)
    this_year_features.append(god_vector_last_week[year1 + 1])   #last week (1 year ago)
    this_year_features.append(god_vector_last_week[year1 + 2])   #last week (2 years ago)
    this_year_features.append(god_vector_this_week[year + 1])   #this week (1 year ago)
    this_year_features.append(god_vector_this_week[year + 2])   #this week (2 years ago)
    this_year_features.append(god_vector_next_week[yearf + 1])   #next week (1 year ago)
    this_year_features.append(god_vector_next_week[yearf + 2])   #next week (2 years ago)


    #Add month data to feature vector
    this_year_features.append(god_vector_2_weeks[year2 + 6])         #last month, 2 weeks ago (most recent data)
    this_year_features.append(god_vector_2_weeks[year2 + 6 + 1])     #last month, 2 weeks ago (1 year ago)
    this_year_features.append(god_vector_2_weeks[year2 + 6 + 2])     #last month, 2 weeks ago (2 years ago)
    this_year_features.append(god_vector_next_week[yearf + 6 + 1])   #last month, next week (1 year ago)
    this_year_features.append(god_vector_next_week[yearf + 6 + 2])   #last month, next week (2 years ago)

    #Add Year data to feature vector
    this_year_features.append(god_vector_2_weeks[year2 + 11])         #1 year as of 2 weeks ago (most recent data)
    this_year_features.append(god_vector_this_week[year + 11 + 1])   #2 years ago as of this week


    #Add radius 1 to feature vector
    #Add week data to feature vector
    this_year_features.append(god_vector_2_weeks[year2 + 18])         #2 weeks ago (most recent data)
    this_year_features.append(god_vector_2_weeks[year2 + 18 + 1])     #2 weeks ago (1 year ago)
    this_year_features.append(god_vector_2_weeks[year2 + 18 + 2])     #2 weeks ago (2 years ago)
    this_year_features.append(god_vector_last_week[year1 + 18 + 1])   #last week (1 year ago)
    this_year_features.append(god_vector_last_week[year1 + 18 + 2])   #last week (2 years ago)
    this_year_features.append(god_vector_this_week[year + 18 + 1])   #this week (1 year ago)
    this_year_features.append(god_vector_this_week[year + 18 + 2])   #this week (2 years ago)
    this_year_features.append(god_vector_next_week[yearf + 18 + 1])   #next week (1 year ago)
    this_year_features.append(god_vector_next_week[yearf + 18 + 2])   #next week (2 years ago)


    #Add month data to feature vector
    this_year_features.append(god_vector_2_weeks[year2 + 18 + 6])         #last month, 2 weeks ago (most recent data)
    this_year_features.append(god_vector_2_weeks[year2 + 18 + 6 + 1])     #last month, 2 weeks ago (1 year ago)
    this_year_features.append(god_vector_2_weeks[year2 + 18 + 6 + 2])     #last month, 2 weeks ago (2 years ago)
    this_year_features.append(god_vector_next_week[yearf + 18 + 6 + 1])   #last month, next week (1 year ago)
    this_year_features.append(god_vector_next_week[yearf + 18 + 6 + 2])   #last month, next week (2 years ago)

    #Add Year data to feature vector
    this_year_features.append(god_vector_2_weeks[year2 + 18 + 11])         #1 year as of 2 weeks ago (most recent data)
    this_year_features.append(god_vector_this_week[year + 18 + 11 + 1])   #2 years ago as of this week


    #Add radius 2 to feature vector
    #Add week data to feature vector
    this_year_features.append(god_vector_2_weeks[year2 + 36])         #2 weeks ago (most recent data)
    this_year_features.append(god_vector_2_weeks[year2 + 36 + 1])     #2 weeks ago (1 year ago)
    this_year_features.append(god_vector_2_weeks[year2 + 36 + 2])     #2 weeks ago (2 years ago)
    this_year_features.append(god_vector_last_week[year1 + 36 + 1])   #last week (1 year ago)
    this_year_features.append(god_vector_last_week[year1 + 36 + 2])   #last week (2 years ago)
    this_year_features.append(god_vector_this_week[year + 36 + 1])   #this week (1 year ago)
    this_year_features.append(god_vector_this_week[year + 36 + 2])   #this week (2 years ago)
    this_year_features.append(god_vector_next_week[yearf + 36 + 1])   #next week (1 year ago)
    this_year_features.append(god_vector_next_week[yearf + 36 + 2])   #next week (2 years ago)


    #Add month data to feature vector
    this_year_features.append(god_vector_2_weeks[year2 + 36 + 6])         #last month, 2 weeks ago (most recent data)
    this_year_features.append(god_vector_2_weeks[year2 + 36 + 6 + 1])     #last month, 2 weeks ago (1 year ago)
    this_year_features.append(god_vector_2_weeks[year2 + 36 + 6 + 2])     #last month, 2 weeks ago (2 years ago)
    this_year_features.append(god_vector_next_week[yearf + 36 + 6 + 1])   #last month, next week (1 year ago)
    this_year_features.append(god_vector_next_week[yearf + 36 + 6 + 2])   #last month, next week (2 years ago)

    #Add Year data to feature vector
    this_year_features.append(god_vector_2_weeks[year2 + 36 + 11])         #1 year as of 2 weeks ago (most recent data)
    this_year_features.append(god_vector_this_week[year + 36 + 11 + 1])   #2 years ago as of this week


    #Add radius 3 to feature vector
    #Add week data to feature vector
    this_year_features.append(god_vector_2_weeks[year2 + 36])         #2 weeks ago (most recent data)
    this_year_features.append(god_vector_2_weeks[year2 + 36 + 1])     #2 weeks ago (1 year ago)
    this_year_features.append(god_vector_2_weeks[year2 + 36 + 2])     #2 weeks ago (2 years ago)
    this_year_features.append(god_vector_last_week[year1 + 36 + 1])   #last week (1 year ago)
    this_year_features.append(god_vector_last_week[year1 + 36 + 2])   #last week (2 years ago)
    this_year_features.append(god_vector_this_week[year + 36 + 1])   #this week (1 year ago)
    this_year_features.append(god_vector_this_week[year + 36 + 2])   #this week (2 years ago)
    this_year_features.append(god_vector_next_week[yearf + 36 + 1])   #next week (1 year ago)
    this_year_features.append(god_vector_next_week[yearf + 36 + 2])   #next week (2 years ago)


    #Add month data to feature vector
    this_year_features.append(god_vector_2_weeks[year2 + 36 + 6])         #last month, 2 weeks ago (most recent data)
    this_year_features.append(god_vector_2_weeks[year2 + 36 + 6 + 1])     #last month, 2 weeks ago (1 year ago)
    this_year_features.append(god_vector_2_weeks[year2 + 36 + 6 + 2])     #last month, 2 weeks ago (2 years ago)
    this_year_features.append(god_vector_next_week[yearf + 36 + 6 + 1])   #last month, next week (1 year ago)
    this_year_features.append(god_vector_next_week[yearf + 36 + 6 + 2])   #last month, next week (2 years ago)

    #Add Year data to feature vector
    this_year_features.append(god_vector_2_weeks[year2 + 36 + 11])         #1 year as of 2 weeks ago (most recent data)
    this_year_features.append(god_vector_this_week[year + 36 + 11 + 1])   #2 years ago as of this week


    #Add all time to feature vector
    this_year_features.append(god_vector_this_week[year + 15])     #2 weeks ago (most recent data)
    this_year_features.append(god_vector_this_week[year + 16])     #2 weeks ago (1 year ago)
    this_year_features.append(god_vector_this_week[year + 17])     #2 weeks ago (2 years ago)


    #Add identifying data
    this_year_features.append(god_vector_this_week[0])  #xbin
    this_year_features.append(god_vector_this_week[1])  #ybin
    this_year_features.append(god_vector_this_week[2])  #week number
    this_year_features.append(2019 - year)              #year


    #Add class
    classification = 0
    if god_vector_this_week[year] > classifier_limit:   #classified as a hot spot if weekly crime
        classification = 1                              #exceeds two standard deviations above the mean

    this_year_features.append(classification)

    return this_year_features


def open_the_file():
    feature_vector = {}
    with open('update_feature_vector.csv', 'rb') as myfile:
        thedatareader = csv.reader(myfile, delimiter=',')
        for row in thedatareader:
            newRow = [float(x) for x in row]
            key = (int(newRow[0]), int(newRow[1]), int(newRow[2]))
            feature_vector[key] = newRow

    return feature_vector

'''
Gets the mean of all areas which have had crime since 2012
result: 1.24030983454  (ran on 11/18/16)
'''
def get_crime_mean(feature_vector):
    total_sum = 0.0
    count = 0


    for x in feature_vector:
        if feature_vector[x][18] != 0:
            total_sum += feature_vector[x][4] + feature_vector[x][5] + feature_vector[x][6]+ feature_vector[x][7]
            count += 4
            if feature_vector[x][2] <= 25:
                total_sum += feature_vector[x][3]
                count += 1

    avg = total_sum / count

    return avg

'''
gets the standard deviation for all areas which have had crime since 2012
result: 2.64611157716 (ran on 11/18/16)
'''
def get_crime_standard_deviation(feature_vector, avg):
    total_sum = 0.0
    count = 0

    for x in feature_vector:
        if feature_vector[x][18] != 0:
            total_sum += (feature_vector[x][4]-avg)**2 + (feature_vector[x][5]-avg)**2 + (feature_vector[x][6]-avg)**2 + (feature_vector[x][7]-avg)**2
            count += 4
            if feature_vector[x][2] <= 25:
                total_sum += (feature_vector[x][4]-avg)**2
                count += 1


    return math.sqrt(total_sum / count)

'''
calculates standard deviation and mean
'''
def get_crime_stats(feature_vector):

    avg = get_crime_mean(feature_vector)
    print avg

    stdev = get_crime_standard_deviation(feature_vector, avg)
    print stdev

    return avg + (2*stdev)


def write_features_to_file(feature_vector, classifier_limit):
    with open('test_train_data.csv', 'w') as mycsvfile:
        thedatawriter = csv.writer(mycsvfile)
        for row in feature_vector:
            if feature_vector[row][18] != 0:
                xbin = row[0]
                ybin = row[1]
                weeknum = row[2]

                if weeknum == 52:
                    continue

                god_vector_this_week = feature_vector[(xbin, ybin, weeknum,)]
                god_vector_last_week = feature_vector[(xbin, ybin, (weeknum - 1) % 52,)]
                god_vector_2_weeks = feature_vector[(xbin, ybin, (weeknum - 2) % 52,)]
                god_vector_next_week = feature_vector[(xbin, ybin, (weeknum + 1) % 52,)]

                year_2014 = get_feature_vectors(5, god_vector_this_week, god_vector_last_week, god_vector_2_weeks, god_vector_next_week, classifier_limit)
