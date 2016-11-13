'''
@Code
***************************************
Criminology Data Set                  *
Portland Dictionary Initialization    *
***************************************

@Authors
    * Ryan Schachte
    * Fatima Naveed
    * Rob Stevens
    * Trevor Richardson

@Purpose
    * Calculate the radius R = r
'''
import csv
import math
import datetime

class Feature_Vector:
    '''Calculate the radius R = r'''

    def __init__(self, radius):
        self.radius = radius
        self.feature_dict = {}

    def initialize_feature_dict(self):
        '''Init the feature vector'''

        '''
        STRUCTURE FOR THE FEATURE VECTOR

        1) Xbin
        2) Ybin
        3) Week
        4) Current week 2016
        5) Current week 2015
        6) Current week 2014
        7) Current week 2013
        8) Current week 2012
        9) Past month 2016
        10) Past month 2015
        11) Past month 2014
        12) Past month 2013
        13) Past month 2012
        14) Past year 2016
        15) Past year 2015
        16) Past year 2014
        17) Past year 2013
        18) Past year 2012
        19) All time
        20) All week
        21) All month
        22) All year
        '''

        for x in range(0, 359):
            for y in range(0, 359):
                for week in range(0, 53):
                    self.feature_dict[(x, y, week)] = [0] * 22
                    self.feature_dict[(x, y, week)][0] = x
                    self.feature_dict[(x, y, week)][1] = y
                    self.feature_dict[(x, y, week)][2] = week


    def load_file(self, file):
        '''Load the data'''
        data_set = []
        with open(file, 'r') as mycsvfile:
            reader = csv.reader(mycsvfile)
            reader = list(reader)[1:]
            for item in reader:
                for x in range(1,8):
                    item[x] = int(item[x]) #change everything to int
                data_set.append(item)

        return data_set

    def get_call_count(self, old_data):
        '''Count the calls for each param'''

        YEARS = [16,15,14,13,12]

        for index, row in enumerate(old_data):
            if(not(row[0]=='0')):
                date_data = row[0].split('/')

                date_data[2] = '20' + date_data[2]

                beginning_year = datetime.date(int(date_data[2]), 1, 1 )

                current_date = datetime.date(int(date_data[2]), int(date_data[0]), int(date_data[1]))

                wk_no = math.floor((current_date-beginning_year).days/7)

                sum_total_call = sum(row[3:])

                self.update_week(row[1], row[2], int(wk_no), date_data[2], sum_total_call)


    def update_week(self, xbin, ybin, wk_no, yr, total_call):
        '''Update the total call sum for each respective week'''

        if(yr == '2016'):
            self.feature_dict[(xbin, ybin, wk_no)][3] += total_call
        elif(yr == '2015'):
            self.feature_dict[(xbin, ybin, wk_no)][4] += total_call
        elif(yr == '2014'):
            self.feature_dict[(xbin, ybin, wk_no)][5] += total_call
        elif(yr == '2013'):
            self.feature_dict[(xbin, ybin, wk_no)][6] += total_call
        else:
            self.feature_dict[(xbin, ybin, wk_no)][7] += total_call

def main():
    fv = Feature_Vector(0)

    fv.initialize_feature_dict()

    csv_file = fv.load_file('countable_data.csv')

    fv.get_call_count(csv_file)


if __name__ == "__main__":
    main()
