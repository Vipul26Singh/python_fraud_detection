import numpy as np
import pandas as pd #to read files
import matplotlib.pyplot as plt
import scipy.stats

class BenfordsLaw:
    
    def __init__(self, processData):
        self.data = np.sort(processData, 0)
        self.size = len(self.data)
        self.mean = np.sum(self.data, 0)/float(self.size)
        
       
        #self.mean = self.mean[0]
        self.median = self.data[int(self.size/2)]
        
        print(type(self.median))
        if(type(self.median) is np.ndarray):
            self.median = self.median[0]
        
        medianDiff = np.subtract(self.data, self.median)
        medianDiff = np.sort(medianDiff)
        self.mad = medianDiff[int(len(medianDiff)/2)]
        
        if(type(self.mad) is list):
            self.mad = self.mad[0]
        
        self.skew = scipy.stats.skew(self.data)
        
        if(type(self.skew) is list):
            self.skew = self.skew[0]
        

        print("Mean:", self.mean)
        print("Median:", self.median)
        print("Skewness:", self.skew)
        print("Mad:", self.mad)
    
    def getMean(self):
        return self.mean
    
    def getMedian(self):
        return self.median
        
    def getMad(self):
        return self.mad
    
    def getSkew(self):
        return self.skew
    
    def getDigitPlace(self, digit, place):
        digit = abs(digit)
            
        return int(str(digit)[place-1])
    
    def plotGraph(self, valueList, xLabel, title):
        objects = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
        y_pos = np.arange(len(objects))

        plt.bar(y_pos, valueList, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Probability of '+xLabel+' in %')
        plt.xlabel(xLabel)
        plt.title(title)

    
    def getLabel(self, digit):
        return str(digit)+" digit"
        
    def generateBenfordGraph(self, title, place = 1):
        digitCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
        for x in np.nditer(self.data):
            placeValue = self.getDigitPlace(x, place)
            
            digitCount[placeValue] = digitCount[placeValue]+1
        
        for i in range(len(digitCount)):
            digitCount[i] = (digitCount[i]*100)/float(self.size)
        
        digitCount = digitCount[1:]
        self.plotGraph(digitCount, self.getLabel(place), title);

"""
print('\033[1m'+"Fund Raising Loan"+'\033[0m')
data = pd.read_csv('fundraising_loans.csv', header=0, usecols=[4])

data = data.values

"""
print('\033[1m'+"Apple Returns"+'\033[0m')
data = pd.read_csv('AppleReturns.csv', header=0, usecols=[0])               
data = data.values

data = data*100000

benLaw = BenfordsLaw(data)

benLaw.generateBenfordGraph("Apple Returns")