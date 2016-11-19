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
        19) All week = All time
        20) All month
        21) All year

        Radii 1

        Features 22 - 39
        In same order starting with current week 2016

        Radii 2

        Features 40 - 57
        same order as above

        Radii 3

        Features 58 - 75
        same order as above

        '''

        for x in range(0, 359):
            for y in range(0, 359):
                for week in range(0, 53):
                    self.feature_dict[(x, y, week)] = [0] * 75
                    self.feature_dict[(x, y, week)][0] = x
                    self.feature_dict[(x, y, week)][1] = y
                    self.feature_dict[(x, y, week)][2] = week


    def load_file(self, file, col_max):
        '''Load the data'''
        data_set = []
        with open(file, 'r') as mycsvfile:
            reader = csv.reader(mycsvfile)
            reader = list(reader)[1:]
            for item in reader:
                for x in range(1,col_max):
                    item[x] = int(item[x]) #change everything to int
                data_set.append(item)

        return data_set

    def get_call_count(self, old_data, lookup_dict):
        '''Count the calls for each param'''

        YEARS = [16,15,14,13,12]

        for index, row in enumerate(old_data):
            if(not(row[0]=='0')):
                date_data = row[0].split('/')

                date_data[2] = '20' + date_data[2]

                beginning_year = datetime.date(int(date_data[2]), 1, 1 )

                current_date = datetime.date(int(date_data[2]), int(date_data[0]), int(date_data[1]))

                wk_no = lookup_dict[row[0]][0]
                yr_no = lookup_dict[row[0]][1]

                sum_total_call = sum(row[3:])

                self.update_week(row[1], row[2], wk_no, yr_no, sum_total_call, 3)
                self.update_month(row[1], row[2], wk_no, yr_no, sum_total_call, 8)
                self.update_year(row[1], row[2], wk_no, yr_no, sum_total_call, 13)

        self.update_sum_features()

        self.calc_radii()

    def calc_radii(self):
        count = 0
        for x in range(0, 359):
            for y in range(0, 359):
                for week in range(0, 53):
                    #calc Radius for that xbin ybin
                    self.radius_calculation(x,y,week,3)
                    count += 1
                    print count


    def radius_calculation(self, xbin, ybin, wk, radii): # I am counting myself into radius calculations -- make sure take out 0,0 case for that case
        for i in range(0,18):
            for current_radius in range(1, radii + 1):
                for y_range in range(0,current_radius+1):
                    for x_range in range(0,current_radius+1):
                        offset = 3 + 18*current_radius
                        if (x_range == 0 and y_range == 0):
                            self.feature_dict[(xbin, ybin, wk)][i+offset] += self.feature_dict[(xbin+x_range, ybin+y_range, wk)][i + 3]
                        else:
                            if (xbin + x_range >= 0 and ybin + y_range >= 0 and xbin + x_range < 359 and ybin+y_range < 359): #only update if it wont give index out of bounds
                                self.feature_dict[(xbin, ybin, wk)][i + offset] += self.feature_dict[(xbin+x_range, ybin+y_range, wk)][i + 3]

                            if(xbin - x_range >= 0 and ybin - y_range >= 0 and xbin - x_range < 359 and ybin - y_range < 359): #only update if it wont give index out of bounds
                                self.feature_dict[(xbin, ybin, wk)][i + offset] += self.feature_dict[(xbin - x_range, ybin - y_range, wk)][i + 3]


    def update_sum_features(self):
        week_index = 19
        month_index = 20
        year_index = 21

        for x in range(0, 359):
            for y in range(0, 359):
                for week in range(0, 53):
                    self.feature_dict[(x, y, week)][18] = (self.feature_dict[(x, y, week)][3] + self.feature_dict[(x, y, week)][4]+
                                                        self.feature_dict[(x, y, week)][5]+self.feature_dict[(x, y, week)][6]+
                                                        self.feature_dict[(x, y, week)][7])

                    self.feature_dict[(x, y, week)][19] = (self.feature_dict[(x, y, week)][8] + self.feature_dict[(x, y, week)][9] +
                                                        self.feature_dict[(x, y, week)][10] + self.feature_dict[(x, y, week)][11] +
                                                        self.feature_dict[(x, y, week)][12])

                    self.feature_dict[(x, y, week)][20] = (self.feature_dict[(x, y, week)][13] + self.feature_dict[(x, y, week)][14]+
                                                        self.feature_dict[(x, y, week)][15]+self.feature_dict[(x, y, week)][16]+
                                                        self.feature_dict[(x, y, week)][17])


    def update_week(self, xbin, ybin, wk_no, yr, total_call, feature_location):
        '''Update the total call sum for each respective week'''

        if(yr == '2016'):
            self.feature_dict[(xbin, ybin, wk_no)][feature_location] += total_call
        elif(yr == '2015'):
            self.feature_dict[(xbin, ybin, wk_no)][feature_location+1] += total_call
        elif(yr == '2014'):
            self.feature_dict[(xbin, ybin, wk_no)][feature_location+2] += total_call
        elif(yr == '2013'):
            self.feature_dict[(xbin, ybin, wk_no)][feature_location+3] += total_call
        else:
            self.feature_dict[(xbin, ybin, wk_no)][feature_location+4] += total_call

    def get_weeks_to_update(self,wk_no, weeks_forward):
        week_vector = []
        for x in range(1,weeks_forward+1): #generates an array with the weeks we will update
            appender = wk_no + x
            week_vector.append(appender)

        for index in range(0, len(week_vector)): #makes sure we deal with the case we are updating weeks 1-4 for week 52 data
            if week_vector[index] > 52:
                week_vector[index] -= 53


        return week_vector


    def update_month(self, xbin, ybin, wk_no, yr, total_call, feature_location):

        weeks_to_update = self.get_weeks_to_update(wk_no, 4)
        for item in weeks_to_update:
            self.update_week(xbin, ybin, item, yr, total_call, feature_location)


    def update_year(self, xbin, ybin, wk_no, yr, total_call, feature_location):

        weeks_to_update = self.get_weeks_to_update(wk_no, 12)

        for item in weeks_to_update:
            self.update_week(xbin, ybin, item, yr, total_call, feature_location)


    def write_to_file(self):
        with open('update_feature_vector.csv', 'w') as mycsvfile:
            thedatawriter = csv.writer(mycsvfile)
            for row in self.feature_dict:
                thedatawriter.writerow(self.feature_dict[row])


    def lookup_to_dict(self, lookup_csv):
        '''Converts CSV to readable dictionary'''

        lookup_dict = {}

        #DAY WK_NO YR
        for line in lookup_csv:
            lookup_dict[line[0]] = line[1:]

        return lookup_dict



def main():
    fv = Feature_Vector(0)

    fv.initialize_feature_dict()

    csv_file = fv.load_file('countable_data.csv', 8)
    lookup_file = fv.load_file('../date_lookup_table.csv', 3)

    lookup_dict = fv.lookup_to_dict(lookup_file)

    print(lookup_dict['3/15/2012'])
    print(len(lookup_dict))

    fv.get_call_count(csv_file, lookup_dict)
    fv.write_to_file()



if __name__ == "__main__":
    main()
