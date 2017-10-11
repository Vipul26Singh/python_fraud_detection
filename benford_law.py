#BenfordsLaw.py

'''This is an untested class to examine data according to Benford's
Law which which describes the distribution of first digits (ignoring leading
zeros) of a data set.
Benford's Law is a probability distribution of the form
log(1 + 1/d) where d is the first digit.
'''

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class BenfordsLaw(object):
    '''This class works on Pandas Dataframes'''

    def __init__(self, matrix, *ignore_columns):
        '''Tells Python what columns of the data frame should be ignored.
        Columns to be ignored should be inputted as a list'''
        self.temp_frame = matrix


    def expected_values_(self):
        '''Calculates the proportion for each digit that we should
        expect to see under Benfords Law'''
        expected = [math.log((1 + float(1)/x), 10) for x in range(1, 10)]
        return expected


    def convert_frame(self):
        '''Method that converts the data frame to a matrix for columns
        with numerical data types'''
        #numerical_columns = list(self.temp_frame.select_dtypes(include=['int64',
                                    #'float64']).columns)
        self.temp_values = self.temp_frame.copy()


    def remove_zeros(self):
        '''Method that pulls out the integers from the data frame and adds them
        to a list if they aren't 0's'''
        self.temp_values = self.temp_values.reshape(self.temp_values.shape[0]*
                                        self.temp_values.shape[1],).tolist()

        # Converting element to strings so I can extract the first digit
        self.temp_values = map(str, self.temp_values)


        def not_decimal(string):
            '''This removes any decimal points in the number and the last
            value of the number. Due to measurement errors, the last digit
            of a float is not expected to adhere to Benford's law. If we remove
            the entire number it will be set at 0.'''
            if '.' in string:
                string = string.replace('.','')[:-1]
                if len(string) == 0:
                    string = '0'
            return string


        def not_zero(string):
            # Recursively removes leading zeros from the string
            # Base cases that catches when first digit isn't one
            # or the number itself is 0, in which case we'll drop it
            if len(string) == 1 or string[0] != '0':
                return string
            else:
                return not_zero(string[1:])

        self.temp_values = map(not_decimal, self.temp_values)
        self.temp_values = map(not_zero, self.temp_values)


    def first_digit(self):
        '''Method that removes all the but the first digit from the list'''
        self.temp_values = map(lambda x: x[0], self.temp_values)
        # Removes zeros from the list
        self.temp_values = [value for value in self.temp_values if value != '0']


    def benfords_test(self):
        self.temp_values = map(int, self.temp_values)
        self.temp_values.sort()
        self.total = len(self.temp_values)
        self.counts = [0]*10
        # A loop that east self.temp_values down to nothing bc that's the
        # cleanest way to do it
        while len(self.temp_values) != 0:
            self.counts[self.temp_values[0]] += 1
            self.temp_values = self.temp_values[1:]
        # First digit in self.counts will always be 0 since I removed zeros
        self.counts = self.counts[1:]
        self.counts = [float(x)/self.total for x in self.counts]


    def view(self, danger_line = False):
        '''Plots the distribution of the data and the expected distribution'''
        '''Make expected curve a parameter'''
        '''Make parameter for danger distribution (red line uniform)'''
        '''danger_line shows the distribution if all numbers appeared
        in a uniform distribution, or .111'''
        expected = self.expected_values_()
        # Smoothing the line
        benford_expected = map(lambda x: math.log(1 + float(1)/x, 10),
                                np.linspace(1, 9, num = 81))
        plt.bar(range(1, 10), self.counts, tick_label = range(1,10),
        align = 'center', width = 0.8, color = 'green',
        hatch = '/', edgecolor = 'green', lw = .5)

        plt.scatter(range(1, 10), expected, color = 'green')
        plt.scatter(range(1, 10), expected, color = 'dimgrey')

        plt.ylim(ymin = 0)

        if danger_line == True:
            plt.plot(range(0, 11), [.111]*11, color = 'bl')
        plt.xlim(xmin = .5, xmax = 9.5)
        plt.show()
        
def calculate_mean_mad(dataFrame):
        data = [''  for x in range(4)]
        data[0] = dataFrame.skew()
        data[1] = dataFrame.mean()
        data[2] = dataFrame.median()
        
        return data
        
   

milk = pd.read_csv('Twitter Users By Friends Count', delimiter = '\t', usecols=[1])
milk = milk.values
milk = milk[0] 
mean = calculate_mean_mad(milk.value)
milk = milk.drop('I79', axis = 1)
moos = milk.values
moo_check = BenfordsLaw(moos)
moo_check.convert_frame()
moo_check.remove_zeros()
moo_check.first_digit()
moo_check.benfords_test()
moo_check.view()

