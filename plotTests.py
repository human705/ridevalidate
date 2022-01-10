import pandas as pd
import json
import copy
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import scipy.fftpack
# import numpy as np
# import pylab as plt
import statsmodels.api as sm


# def smoothFFT(_x, _y):
#     N = 100
#     # x = np.linspace(0,2*np.pi,N)
#     # y = np.sin(x) + np.random.random(N) * 0.2

#     w = scipy.fftpack.rfft(_y)
#     f = scipy.fftpack.rfftfreq(N, _x[1]-_x[0])
#     spectrum = w**2
#     cutoff_idx = spectrum < (spectrum.max()/5)
#     w2 = w.copy()
#     w2[cutoff_idx] = 0
#     y2 = scipy.fftpack.irfft(w2)

#     return y2


def smoothConvolve(y, box_pts):
    box = np.ones(box_pts)/box_pts
    # modes = ['full', 'same', 'valid']
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


# from scipy.signal import savgol_filter
# yhat = savgol_filter(y, 51, 3) # window size 51, polynomial order 3
# savitzky_golay
def mySmoothingPlot(_myData):
    # plt.style.use('fivethirtyeight')
    # Read list of objects
    data = pd.DataFrame(_myData)

    x = data['KM']
    y = data['SLOPE']
    windowSize = 21  # Myst be odd number
    polyOrder = 3
    # yhat = savitzky_golay(y, 51, 3) # window size 51, polynomial order 3
    # window size 51, polynomial order 3
    yhat = savgol_filter(y, windowSize, polyOrder)

    plt.plot(x, y, color='blue', label='original')
    plt.plot(x, yhat, color='red', label='zavgol')
    plt.plot(x, smoothConvolve(y, 19), 'g-', lw=2, label='convolve')
    # plt.plot(x, smoothFFT(x, y), color='yellow', lw=2)

    # lowess = sm.nonparametric.lowess(y, x, frac=0.1)
    # plt.plot(x, y, '+')
    # plt.plot(lowess[:, 0], lowess[:, 1], color='yellow')

    plt.legend()
    plt.title('Slope at time')
    plt.xlabel('Time (Secs)')
    plt.ylabel('Slope')
    plt.tight_layout()
    plt.show()


def mySlopePlot(_myData):
    plt.style.use('fivethirtyeight')

    # Read list of objects
    data = pd.DataFrame(_myData)
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
