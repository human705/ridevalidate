import pandas as pd
import json
import copy
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def replacePower(_myData):
    myNewList = []
    # Read list of objects
    data = pd.DataFrame(_myData)
    y = data['WATTS']
    windowSize = 21  # Myst be odd number
    polyOrder = 3
    # yhat = savitzky_golay(y, 51, 3) # window size 51, polynomial order 3
    # window size 51, polynomial order 3
    yhat = savgol_filter(y, windowSize, polyOrder)
    data['NewWatts'] = yhat
    data.drop('WATTS', axis=1, inplace=True)
    data.rename(columns={'NewWatts': 'WATTS'}, inplace=True)
    # print(data)
    myNewList = data.to_dict('records')
    # myNewList = data.values.tolist()
    for item in range(1, len(myNewList)):
        if (item['WATTS'] < 0):
            item['WATTS'] = 0

    return myNewList


def replaceSlope(_myData):
    # plt.style.use('fivethirtyeight')
    myNewList = []
    # Read list of objects
    data = pd.DataFrame(_myData)
    y = data['SLOPE']
    windowSize = 21  # Myst be odd number
    polyOrder = 3
    # yhat = savitzky_golay(y, 51, 3) # window size 51, polynomial order 3
    # window size 51, polynomial order 3
    yhat = savgol_filter(y, windowSize, polyOrder)
    data['NewSlope'] = yhat
    data.drop('SLOPE', axis=1, inplace=True)
    data.rename(columns={'NewSlope': 'SLOPE'}, inplace=True)
    # print(data)
    myNewList = data.to_dict('records')
    # myNewList = data.values.tolist()
    return myNewList
    # i = 1
