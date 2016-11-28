#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.linear_model import SGDClassifier
import random
import csv
import nij_accuracy
from sklearn.model_selection import cross_val_score
from sklearn.metrics import fbeta_score, make_scorer
from sklearn.ensemble import GradientBoostingRegressor
import sys


def open_the_file():
    feature_vector = []
    test_feature_vector = []



    print 'Beginning Data Loading Processor..'

    with open('test_train_data.csv', 'rb') as myfile:
        thedatareader = csv.reader(myfile, delimiter=',')
        thedatareader = list(thedatareader)
        count = 0
        for (index, row) in enumerate(thedatareader):
            count += 1
            newRow = [float(x) for x in row]
            if newRow[79] == 2016.0:
                test_feature_vector.append(newRow)
                classs = row[-1]
            else:
                feature_vector.append(newRow)
                classs = row[-1]





    return feature_vector, test_feature_vector



def splitForCrossVal(trainData, k):

    bin_dict = {}

    bin_list = []
    k_split_list = []

    bin_class_list = []
    k_class_list = []

    print "beggining split for cross val"

    for year in range (2014, 2016):
        for week in range(0, 52):
            bin_no = random.randint(0,k-1)
            tup = (float(year), float(week))
            bin_dict[tup] = bin_no

    for bin in range(k):
        del k_split_list[:]
        del k_class_list[:]
        counter = 0
        for row in trainData:
            newRow = row[:80]

            tup = (row[79], row[78])
            if bin_dict[tup] == bin:
                k_split_list.append(newRow)
                k_class_list.append(row[-1])
                counter += 1

        bin_list.append(list(k_split_list))
        bin_class_list.append(list(k_class_list))


    print "done"

    return bin_list, bin_class_list




def stitch_bins(bin_list, bin_index, bin_class_list):
    # print "stitching begins"
    training = []
    validation = []
    train_class = []
    validation_class = []

    for index, list in enumerate(bin_list):
        if index == bin_index:
            validation = list
            validation_class = bin_class_list[index]
        else:
            training += list
            train_class += bin_class_list[index]




    return training, train_class, validation, validation_class


def cross_validation(train_data, k, list_of_bins,list_of_bin_class, parameter, f_r_set):
    PAI_accuracies = []
    PEI_accuracies = []
    accuracy_weights = []
    total_length = float(len(train_data))

    for index in range(k):
        train_set, train_class, validation_set, validation_class = stitch_bins(list_of_bins, index, list_of_bin_class)
        predictions = makeModelandPrediction(train_set, train_class, validation_set, parameter)
        # predictions = makeBoostingPredictions(train_set, train_class, validation_set, parameter)
        PAI_acc, PEI_acc = calcAccuracy(predictions, validation_class, f_r_set, validation_set)
        PAI_accuracies.append(PAI_acc)
        PEI_accuracies.append(PEI_acc)
        acc_weight = len(validation_set) / total_length
        accuracy_weights.append(acc_weight)

        final_PAI_acc = calcWeightedAccuracies(PAI_accuracies, accuracy_weights)
        final_PEI_acc = calcWeightedAccuracies(PEI_accuracies, accuracy_weights)

    return final_PAI_acc, final_PEI_acc

def calcWeightedAccuracies(accuracies, accuracy_weights):

    final_accuracy = 0.0
    for index, acc in enumerate(accuracies):
        if acc >= 0:
            final_accuracy += acc * accuracy_weights[index]

    return final_accuracy


def makeModelandPrediction(train_data, train_label, test_data, parameter):

    # print "making sgd model"

    clf = LogisticRegression(
        penalty='l2',
        dual=False,
        tol=0.0001,
        C=1.0,
        fit_intercept=True,
        intercept_scaling=1,
        class_weight=None,
        random_state=None,
        solver='liblinear',
        max_iter=1,
        multi_class='ovr',
        verbose=10,
        warm_start=False,
        n_jobs=1
    )
    clf.fit(trainData, trainLabel)


    return clf.predict(testData)





def compareParameter(train_data, k, f_r_set, alpha_value):
    params = []
    best_PAI_param = 0
    best_PEI_param = 0

    list_of_bins, list_of_bin_class = splitForCrossVal(train_data, k)

    PAI, PEI = cross_validation(train_data, k, list_of_bins, list_of_bin_class, alpha_value, f_r_set)

    print alpha_value, PAI, PEI

    tup = (alpha_value, PAI, PEI)

def calcAccuracy(prediction, test_label, f_r_set, validation_set):

    split_yrwk_dict = {}

    for index, element in enumerate(validation_set):
        key_tup = (int(validation_set[index][78]), int(validation_set[index][79]))

        if key_tup in split_yrwk_dict:
            data_tup = (int(validation_set[index][76]), int(validation_set[index][77]), int(prediction[index]), int(test_label[index]))
            split_yrwk_dict[key_tup].append(data_tup)
        else:
            split_yrwk_dict[key_tup] = []
            data_tup = (int(validation_set[index][76]), int(validation_set[index][77]), int(prediction[index]), int(test_label[index]))
            split_yrwk_dict[key_tup].append(data_tup)

    avg_PAI = 0.0
    avg_PEI = 0.0
    count = 0.0
    for key, value in split_yrwk_dict.iteritems():
        actual_counts = nij_accuracy.getActualCallsList(key[0], key[1], f_r_set)
        PAI_acc, PEI_acc = nij_accuracy.calcPAI_PEI(value, actual_counts)
        avg_PAI += PAI_acc
        avg_PEI += PEI_acc
        count += 1



    avg_PEI = avg_PEI/count
    avg_PAI = avg_PAI/count

    return avg_PAI, avg_PEI

    #make a dictionary
    #for everything in validationset
    #if I havent seen it (WK YR) make that key first element of list
    #else just append to that list

    #give that to



def crossVal(data, classification):
    clf = SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
       eta0=0.0, fit_intercept=True, l1_ratio=0.15,
       learning_rate='optimal', loss='hinge', n_iter=5, n_jobs=1,
       penalty='l2', power_t=0.5, random_state=None, shuffle=True,
       verbose=0, warm_start=False)
    score = make_scorer(my_custom_loss_func, greater_is_better=True)
    scores = cross_val_score(clf, data, classification, cv=10, scoring=score)
    print scores
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


def my_custom_loss_func(ground_truth, predictions):
    false_positive = 0.0
    true_negative = 0.0
    for index in range(len(predictions)):
        if ground_truth[index] == 0:
            true_negative += 1

        if predictions[index] != ground_truth[index] and ground_truth[index] == 0:
            false_positive += 1

    rate = false_positive / (false_positive + true_negative)
    return rate





def main():


    input_parameter = sys.argv[1]

    total_actual_crime_counts = nij_accuracy.loadCrimeCounts()
    data, test_data = open_the_file()
    compareParameter(data, 10, total_actual_crime_counts, float(input_parameter))


main()