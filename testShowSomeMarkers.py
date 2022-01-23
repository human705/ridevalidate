# import numpy as np
# import matplotlib.pyplot as plt

# xs = np.linspace(-np.pi, np.pi, 30)
# ys = np.sin(xs)
# markers_on = [12, 17, 18, 19]
# plt.plot(xs, ys, '-gD', markevery=markers_on, label='line with select markers')
# plt.legend()
# plt.show()


import matplotlib.pyplot as plt

y = [1, 2, 3, 2, 1, 2, 3, 2, 1]
x = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# plot a line
# plt.plot([0, 10], [0, 10], zorder=1)

# Marker on index of points starting at 0 to the lenght of the list -1
markers_on = [0, 4, 8]
plt.plot(x, y, '-gD', markevery=markers_on, label='line with select markers')

# Plot markers
#plt.scatter(x, y, s=300, color='red', zorder=2)

plt.title("Line with points infront")
plt.grid()

# plt.savefig("scatter_points_order_02.png", bbox_inches='tight')
plt.show()
