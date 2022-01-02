import pandas as pd
import json
import copy
from matplotlib import pyplot as plt


def testPlotHist(_MyData):
    plt.style.use('fivethirtyeight')

    data = pd.DataFrame(_MyData)
    # print(data.head())
    slope = data['SLOPE']
    secs = data['SECS']

    # bins = [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5]

    # plt.hist(secs, bins=bins, edgecolor='black', log=True)

    # median_age = 29
    # color = '#fc4f30'

    # plt.axvline(median_age, color=color, label='Age Median', linewidth=2)

    plt.plot(secs, slope, color='#444444', label='slope')

    plt.legend()

    plt.title('Slope at time')
    plt.xlabel('Time (Secs)')
    plt.ylabel('Slope')

    plt.tight_layout()

    plt.show()
    test = 1


# f = open('data/GC-FixedAlt.json', encoding='utf-8-sig')
# # f = open('data/2021_12_12_08_56_42.json')

# # returns JSON object as# a dictionary
# data = json.load(f)

# importedSamples = copy.deepcopy(data['RIDE']['SAMPLES'])

# testPlotHist(importedSamples)
