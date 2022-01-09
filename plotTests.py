import pandas as pd
import json
import copy
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def smoothConvolve(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


# from scipy.signal import savgol_filter
# yhat = savgol_filter(y, 51, 3) # window size 51, polynomial order 3
# savitzky_golay
def mySmoothingPlot(_myData):

    # Read list of objects
    data = pd.DataFrame(_myData)
    # x = np.linspace(0,2*np.pi,100)
    # y = np.sin(x) + np.random.random(100) * 0.2

    x = data['SECS']
    y = data['SLOPE']
    # yhat = savitzky_golay(y, 51, 3) # window size 51, polynomial order 3
    yhat = savgol_filter(y, 51, 3)  # window size 51, polynomial order 3

    plt.plot(x, y, color='blue')
    plt.plot(x, yhat, color='red')

    plt.plot(x, smoothConvolve(y, 19), 'g-', lw=2)

    plt.legend()
    plt.title('Slope at time')
    plt.xlabel('Time (Secs)')
    plt.ylabel('Slope')
    plt.tight_layout()
    plt.show()


def mySlopePlot(_MyData):
    plt.style.use('fivethirtyeight')

    # Read list of objects
    data = pd.DataFrame(_MyData)
    # print(data.head())
    slope = data['SLOPE']
    secs = data['SECS']

    # bins = [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5]
    # plt.hist(secs, bins=bins, edgecolor='black', log=True)
    # median_age = 29
    # color = '#fc4f30'
    # plt.axvline(median_age, color=color, label='Age Median', linewidth=2)

    plt.plot(secs, slope, color='blue', label='slope')
    plt.legend()
    plt.title('Slope at time')
    plt.xlabel('Time (Secs)')
    plt.ylabel('Slope')
    plt.tight_layout()

    plt.show()
    test = 1


# f = open('data/GC-FixedAlt.json', encoding='utf-8-sig')
# f = open('data/2021_12_12_08_56_42.json')
# returns JSON object as# a dictionary
# data = json.load(f)
# importedSamples = copy.deepcopy(data['RIDE']['SAMPLES'])
# testPlotHist(importedSamples)
