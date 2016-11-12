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
from init_portland import Portland_Init

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

def main():

    #init the portland
    HIGHEST_X_COORD = 7762614
    LOWEST_X_CORD   = 7547902

    HIGHEST_Y_COORD = 787862
    LOWEST_Y_COORD  = 602723

    CELL_AREA       = 600

    portland = Portland_Init(HIGHEST_X_COORD, LOWEST_X_CORD, HIGHEST_Y_COORD, LOWEST_Y_COORD, CELL_AREA)

    #Get the initialized portland map
    complete_crime_counts = portland.init_portland_map()

    #Read in the information
    with open('../initial_data_bins.csv', 'r') as csvfile:

        #Pull in the data
        plots = csv.reader(csvfile)

        plots = list(plots)[1:]

        #Loop through each row
        for index, row in enumerate(plots):

            #Parse out the unique identifier
            # current_string = row[4] + '-' + current_x_bin + '-' + current_y_bin

            current_x_bin = int(row[8])
            current_y_bin = int(row[9])

            current_string = (row[4], current_x_bin, current_y_bin)

            '''CHECK IF THE X_BIN/Y_BIN combo exsists in the current_string_tuple'''
            if ((0, current_x_bin, current_y_bin) in complete_crime_counts):
                #TIME | BIN | STREETCRIME | BURGLARY | AUTO | TOTAL
                #Update the dictionary with the count for the current type

                #Delete the dict k/v entry and replace it
                del(complete_crime_counts[(0, current_x_bin, current_y_bin)])

                complete_crime_counts[current_string] = []

                #Extract the current crime type from the row
                crime_type = row[2]

                #date | x_bin | y_bin | street_crime | burglary_crime | auto_crime | other | total_crime
                current_row_data = [row[4], current_x_bin, current_y_bin, 0, 0, 0, 0, 0]

                if (crime_type in STREET_CRIME_TYPES):
                    '''STREET CRIME'''
                    current_row_data[3] += 1
                elif (crime_type in BURGLARY_TYPES):
                    '''BURGLARY CRIME'''
                    current_row_data[4] += 1
                elif (crime_type in AUTO_THEFT_TYPES):
                    '''AUTO-THEFT CRIME'''
                    current_row_data[5] += 1
                else:
                    '''OTHER'''
                    current_row_data[6] += 1

                #Update the total crime count for the date/bin
                current_row_data[7] += 1

                complete_crime_counts[current_string] = current_row_data

            elif(not current_string in complete_crime_counts):
                '''NEVER SEEN THE DATE LOCATION PAIR'''
                #Extract the current crime type from the row
                crime_type = row[2]

                #date | x_bin | y_bin | street_crime | burglary_crime | auto_crime | other | total_crime
                current_row_data = [row[4], row[8], row[9], 0, 0, 0, 0, 0]

                if (crime_type in STREET_CRIME_TYPES):
                    '''STREET CRIME'''
                    current_row_data[3] += 1
                elif (crime_type in BURGLARY_TYPES):
                    '''BURGLARY CRIME'''
                    current_row_data[4] += 1
                elif (crime_type in AUTO_THEFT_TYPES):
                    '''AUTO-THEFT CRIME'''
                    current_row_data[5] += 1
                else:
                    '''OTHER'''
                    current_row_data[6] += 1

                #Update the total crime count for the date/bin
                current_row_data[7] += 1

                complete_crime_counts[current_string] = current_row_data
            else:
                '''SEEN THE DATE LOCATION PAIR => UPDATING'''
                
                #Extract the current crime type from the row
                crime_type = row[2]

                current_row_data = complete_crime_counts[current_string]

                if (crime_type in STREET_CRIME_TYPES):
                    '''STREET CRIME'''
                    current_row_data[3] += 1
                elif (crime_type in BURGLARY_TYPES):
                    '''BURGLARY CRIME'''
                    current_row_data[4] += 1
                elif (crime_type in AUTO_THEFT_TYPES):
                    '''AUTO-THEFT CRIME'''
                    current_row_data[5] += 1
                else:
                    '''OTHER'''
                    current_row_data[6] += 1

                #Update the total crime count for the date/bin
                current_row_data[7] += 1

                #Update the
                complete_crime_counts[current_string] = current_row_data

    #Store the updated CSV with counts
    with open('countable_data.csv', 'w') as mycsvfile:
        header = 'date,xbin,ybin,street_crime,burglary_crime,auto_crime,other,total_crime'
        thedatawriter = csv.writer(mycsvfile)
        thedatawriter.writerow(header)
        for row in complete_crime_counts:
            thedatawriter.writerow(complete_crime_counts[row])


if __name__ == "__main__":
    main()
