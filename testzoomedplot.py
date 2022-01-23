# Implementation of matplotlib function
from matplotlib.axis import Axis
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
y = [1, 2, 3, 2, 1, 2, 3, 2, 1]
x = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ax.plot([1, 2, 3])
# ax.plot(x, y)
markers_on = [2]
ax.plot(x, y, '-gD', markevery=markers_on, label='line with select markers')
ax.set(xlim=(2, 4), ylim=(1, 5), autoscale_on=False, title='Zoom window')

# ax.xaxis.zoom(3)
# ax.margins(0.05)           # Default margin is 0.05, value 0 means fit
# ax.margins(1, 1)           # Values >0.0 zoom out
# ax.margins(x=0, y=-0.25)   # Values in (-0.5, 0.0) zooms in to center

ax.grid()

# fig.suptitle("""matplotlib.axis.Axis.zoom()
# function Example\n""", fontweight="bold")

plt.show()
