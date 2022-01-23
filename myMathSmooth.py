import pandas as pd
import math
import copy
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def smoothAltitude(_samples):
    myNewList = []
    # Read list of objects
    data = pd.DataFrame(_samples)
    # Replace any NaN with 0.0
    data.fillna(0, inplace=True)
    y = data['ALT']
    windowSize = 5  # Myst be odd number
    polyOrder = 2
    # yhat = savitzky_golay(y, 51, 3) # window size 51, polynomial order 3
    # window size 51, polynomial order 3
    yhat = savgol_filter(y, windowSize, polyOrder)
    data['NewAlt'] = yhat
    data.drop('ALT', axis=1, inplace=True)
    data.rename(columns={'NewAlt': 'ALT'}, inplace=True)
    # print(data)
    myNewList = data.to_dict('records')
    # myNewList = data.values.tolist()
    # for item in range(1, len(myNewList)):
    #     if (item['WATTS'] < 0):
    #         item['WATTS'] = 0

    return myNewList


def replacePower(_myData):
    myNewList = []
    # Read list of objects
    data = pd.DataFrame(_myData)
    # Replace any NaN with 0.0
    data.fillna(0, inplace=True)
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
    # Replace any NaN with 0.0
    data.fillna(0, inplace=True)
    # print(data)
    y = data['SLOPE']
    windowSize = 21  # Myst be odd number
    polyOrder = 3
    # yhat = savitzky_golay(y, 51, 3) # window size 51, polynomial order 3
    # window size 51, polynomial order 3
    yhat = savgol_filter(y, windowSize, polyOrder)
    data['NewSlope'] = yhat
    data.drop('SLOPE', axis=1, inplace=True)
    data.rename(columns={'NewSlope': 'SLOPE'}, inplace=True)
    # data['HR'] = data['HR'].astype(int)
    # data['HR'] = data['HR'].apply(pd.to_numeric(data['HR'],
    #                                             errors='ignore', downcast='integer'))
    # data = pd.to_numeric(data['HR'], errors='ignore', downcast='integer')
    # print(data)

    myNewList = data.to_dict('records')
    # for item in myNewList:
    #     if (math.isnan(item['HR'])):
    #         item['HR'] = 0
    #     else:
    #         item['HR'] = int(item['HR'])
    #     if (math.isnan(item['CAD'])):
    #         item['CAD'] = 0
    #     else:
    #         item['CAD'] = int(item['CAD'])
    # myNewList = data.values.tolist()
    return myNewList
    # i = 1
