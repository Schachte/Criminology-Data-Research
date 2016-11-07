'''
@Code
******************************
Criminology Data Set         *
Feature Vector Generation    *
******************************

@Authors
    * Ryan Schachte
    * Fatima Naveed
    * Rob Stevens
    * Trevor Richardson

@Purpose
    * Filters the input CSV file to generate an output feature vector CSV
    * Stores data in external cloud mongoDB for easy filtering

@CSV-Format
    * TIME | BIN | STREETCRIME | BURGLARY | AUTO | TOTAL
    * Output data in the following format for each date and for the total
    * counts on each crime type

PRIMARY KEY FORMAT = DATE-x_BIN-y_BIN

@Example-Information
    Example Dictionary Key:
    ----------------------
    3/1/12-128-555
    ----------------------

    Example Row:
    ------------------------------------------------------------------------------------------------------------------------
    CATEGORY|  CALL GROUP | FINAL_CASE_TYPE | CASE_DESC | OCC_DATE | X_COORD | Y_COORD | CENSUS|TRACT | X_BIN | Y_BIN
    ['STREET CRIMES', 'DISORDER', 'DISTP', 'DISTURBANCE - PRIORITY', '3/7/12', '7633710', '710269', '4001', '143', '208']
    ------------------------------------------------------------------------------------------------------------------------

    Useful Information:
    Date = 4
    Xbin = 8
    Ybin = 9
'''

import csv

BURGLARY_TYPES = {
    'BURG':'BURGLARY - COLD',
    'BURGP':'BURGLARY - PRIORITY *H',
    'PROWLP':'PROWLER'
}

STREET_CRIME_TYPES = {
    'ASSLT':'ASSAULT - COLD',
    'ASSLTT':'ASSAULT -PRIORITY',
    'ASSLTW':'ASSAULT WITH WEAPON *H',
    'DIST':'DISTURBANCE - COLD',
    'DISTP':'DISTURBANCE - PRIORITY',
    'DISTW':'DISTURBANCE - WITH WEAPON *H',
    'GANG':'GANG RELATED',
    'ROB':'ROBBERY - COLD',
    'ROBP':'ROBBERY - PRIORITY *H',
    'ROBW':'ROBBERY - WITH WEAPON *H',
    'SHOOT':'SHOOTING - COLD',
    'SHOOTW':'SHOOTING - WITH WEAPON *H',
    'SHOTS':'SHOTS FIRED',
    'STAB':'STABBING COLD',
    'STABW':'STABBING WITH WEAPON *H',
    'VICE':'VICE-DRUGS, LIQUOR, PROSTITUTION, GAMBLING'
}

AUTO_THEFT_TYPES = {
    'RSTLN':'ROLLING STOLEN *H',
    'VEHREC':'VEHICLE RECOVERED',
    'VEHST':'VEHICLE STONE - COLD',
    'VEHSTP':'VEHICLE STOLEN - PRIORITY'
}

complete_crime_counts = {}

#Read in the information
with open('initial_data_bins.csv', 'r') as csvfile:
    plots = csv.reader(csvfile)
    for index, row in enumerate(plots):
        current_string = row[4] + '-' + row[8] + '-' + row[9]
        if (not current_string in complete_crime_counts):
            #TIME | BIN | STREETCRIME | BURGLARY | AUTO | TOTAL
            #Update the dictionary with the count for the current type

            crime_type = row[2]

            
            current_row_data = ['time', 'bin', 'street_crime_int', 'burg_int', 'auto_int', 'total_int']

            if (crime_type in STREET_CRIME_TYPES):
            elif (crime_type in BURGLARY_TYPES):
            elif (crime_type in AUTO_THEFT_TYPES):

            complete_crime_counts[current_string] = [1]
        else:
            print(complete_crime_counts[current_string][0])
            # increment_string =
            # complete_crime_counts[current_string] += 1
            print('')
