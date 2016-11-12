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
    * Initialize the empty rectangles for the Portland Map
'''


class Portland_Init:
    '''Init the map for all the empty bins in Portland'''

    def __init__(self, x_high, x_low, y_high, y_low, cell_area):
        self.x_high     = x_high
        self.x_low      = x_low
        self.y_high     = y_high
        self.y_low      = y_low
        self.cell_area  = cell_area

    def calculate_bins(self):
        '''Get the number of bins we need to initialize'''

        x_bin_count = (self.x_high - self.x_low)/self.cell_area
        y_bin_count = (self.y_high - self.y_low)/self.cell_area

        return x_bin_count, y_bin_count

    def init_portland_map(self):
        '''Load up the default cells into the dict'''

        #Get the x/y bin values
        x_bin, y_bin = self.calculate_bins()

        #Init portland map dictionary
        portland_map = {}

        #Init Phase
        for x_bins in range(0, 359):
            for y_bins in range(0, 359):
                portland_map[(0,x_bins, y_bins)] = [0, x_bins, y_bins, 0, 0, 0, 0, 0]

        return portland_map
