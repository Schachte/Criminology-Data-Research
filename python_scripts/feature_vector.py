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

class Feature_Vector:
    '''Calculate the radius R = r'''

    def __init__(self, radius):
        self.radius = radius
        self.feature_dict = {}

    def initialize_feature_dict(self):
        for x in range(0, 359):
            for y in range(0, 359):
                for week in range(0, 52):
                    self.feature_dict[(x, y, week)] = [0] * 22
                    self.feature_dict[(x, y, week)][0] = x
                    self.feature_dict[(x, y, week)][1] = y
                    self.feature_dict[(x, y, week)][2] = week


    def load_file(self, file):
        data_set = []
        with open(file, 'r') as mycsvfile:
            reader = csv.reader(mycsvfile)
            for item in reader:
                data_set.append(item)

        return data_set

    # def get_call_count(self, x, y, week, year_back):



def main():
    fv = Feature_Vector(0)

    fv.initialize_feature_dict()
    fv.load_file('countable_data.csv')


if __name__ == "__main__":
    main()
