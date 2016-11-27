#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import math
import random
import csv
import time

from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import SGDClassifier

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import svm

def open_the_file():
	feature_vector = {}

	print 'Beginning Data Loading Processor..'

	with open('test_train_data.csv', 'rb') as myfile:
		thedatareader = csv.reader(myfile, delimiter=',')
		thedatareader = list(thedatareader)
		# print(len(thedatareader))
		for (index, row) in enumerate(thedatareader):
			if (index < 3000000):
				newRow = [float(x) for x in row]

				# print(newRow[76], newRow[77], newRow[78],newRow[79], len(newRow))
				key = (int(newRow[76]), int(newRow[77]), int(newRow[78]), int(newRow[79]))
				feature_vector[key] = newRow

				if index % 2000 == 0:
					print '%.2f complete..' % (float(index)
							/ len(thedatareader) * 100)
			else:
				break

	return feature_vector

def SVM_PRED(trainData, trainLabel, testData):

	X = trainData
	y = trainLabel
	# rbf_feature = RBFSampler(gamma=1, random_state=1)
	# X_features = rbf_feature.fit_transform(X)
	clf = SGDClassifier()
	clf.fit(trainData, trainLabel)
	SGDClassifier(
		alpha=.9,
		average=False,
		class_weight=None,
		epsilon=0.1,
		eta0=0.0,
		fit_intercept=True,
		l1_ratio=0.15,
		learning_rate='optimal',
		loss='hinge',
		n_iter=5,
		n_jobs=1,
		penalty='l2',
		power_t=0.5,
		random_state=None,
		shuffle=True,
		verbose=10,
		warm_start=False)

	return clf.predict(testData)


def LOGISTIC_REG_PRED(trainData, trainLabel, testData):

	X = trainData
	y = trainLabel
	# rbf_feature = RBFSampler(gamma=1, random_state=1)
	# X_features = rbf_feature.fit_transform(X)
	clf = LogisticRegression()
	clf.fit(trainData, trainLabel)
	LogisticRegression(
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

	return clf.predict(testData)

def splitIntoTrainTest(data, percent):
	numberOfRows = math.ceil(len(data) * percent)
	test_data = []
	test_class = []
	train_data = []
	train_class = []

	print 'numberOfRows to use is....%d' % numberOfRows

	train_information = []
	test_information = []

	total_dat = []

	for info in data:
			total_dat.append(info)

	print(len(total_dat))
	print(total_dat)

	random.shuffle(total_dat)

	for index, info in enumerate(total_dat):
		if (index < numberOfRows):
			train_information.append(info)
		else:
			test_information.append(info)


	for x in train_information:
		train_data.append(data[x][0:len(data[x]) - 1])
		if data[x][-1] == 1:
			train_class.append(1)
		else:
			train_class.append(0)

	for x in test_information:
		test_data.append(data[x][0:len(data[x]) - 1])
		if data[x][-1] == 1:
			test_class.append(1)
		else:
			test_class.append(0)


	print 'The length of testData/testClass == %d & %d' \
		% (len(test_data), len(test_class))
	print 'The length of trainData/trainClass == %d & %d' \
		% (len(train_data), len(train_class))

	return (train_data, train_class, test_data, test_class)


def calcAccuracy(prediction, testLabel):
	count = 0.0
	for index in range(len(prediction)):
		if prediction[index] == testLabel[index]:
			count += 1.0

	accuracy = count / float(len(prediction))

	print(accuracy)

def calcAccuracyTrev(prediction, testLabel):
	count = 0.0
	total = 0.0
	for index in range(len(prediction)):
		if prediction[index] == testLabel[index]:
			if testLabel != 0:
				total += 1.0
				count+=1.0
		else:
			total += 1.0
	accuracy = count / total
	print accuracy

def calcAccuracyFalsePositive(prediction, testLabel):
	false_positive = 0.0
	true_negative = 0.0
	for index in range(len(prediction)):
		if testLabel[index] == 0:
			true_negative += 1

		if prediction[index] != testLabel[index] and testLabel[index] == 0:
			false_positive += 1

	rate = false_positive / (false_positive + true_negative)
	print rate

def calcAccuracyFalseNegative(prediction, testLabel):
	false_negative = 0.0
	true_positive = 0.0
	for index in range(len(prediction)):
		if testLabel[index] == 1:
			true_positive += 1

		if prediction[index] != testLabel[index] and testLabel[index] == 1:
			false_negative += 1

	rate = false_negative / (false_negative + true_positive)
	print rate


def printAllErrors(prediction, testLabel):
	print('ORIGINAL CALCACCURACY')
	calcAccuracy(prediction, testLabel)
	print('TREVOR CALCACCURACY')
	calcAccuracyTrev(prediction, testLabel)
	print('F+ CALCACCURACY')
	calcAccuracyFalsePositive(prediction, testLabel)
	print('F- CALCACCURACY')
	calcAccuracyFalseNegative(prediction, testLabel)

def main():
	data = open_the_file()

	while(1):
		print('The number of keys is %d'%(len(data)))
		trainData, trainLabel, testData, testLabel = splitIntoTrainTest(data, .7)
		prediction = svm.SVM_PRED(trainData, trainLabel, testData)


# main()
