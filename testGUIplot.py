from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

# plot function is created for
# plotting the graph in
# tkinter window


def myPlot(_x, _xWindow, _y, _yWindow):

    # the figure that will contain the plot 5x5 width x height inches @ 100dpi
    fig = Figure(figsize=(7, 4),
                 dpi=100)

    # list of squares
    y = [i**2 for i in range(101)]

    # adding the subplot
    # The add_subplot() has 3 arguments.
    # The first one being the number of rows in the grid,
    # the second one being the number of columns in the grid and
    # the third one being the position at which the new subplot must be placed.
    # add_subplot(1, 1, 1) is equivalent to fig.add_subplot(111)
    plot1 = fig.add_subplot(111)

    # Center on point x,y with xWindow and yWindow
    # _x = 50
    # _xWindow = 20
    # _y = 2000
    # _yWindow = 500

    x1 = _x - _xWindow
    x2 = _x + _xWindow
    y1 = _y - _yWindow
    y2 = _y + _yWindow

    plot1.set(xlim=(x1, x2), ylim=(y1, y2),
              autoscale_on=False, title='Zoom window')

    # plotting the graph
    plot1.plot(y)

    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master=window)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   window)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


# the main Tkinter window
window = Tk()

# setting the title
window.title('Plotting in Tkinter')

# dimensions of the main window
# Make sure there is space for the plot toolbar
window.geometry("800x700")
# To turn off resizing the root window, you can set
# , where resizing is allowed in the x and y directions respectively.
# window.resizable(0, 0)

# To set a maxsize to window, as noted in the other answer you can set the maxsize attribute or minsize
# although you could just set the geometry of the root window and then turn off resizing. A bit more flexible imo.
window.minsize(750, 650)

# button that displays the plot
plot_button = Button(master=window,
                     command=lambda: myPlot(50, 20, 2000, 300),
                     height=2,
                     width=10,
                     text="Plot")

# place the button
# in main window
plot_button.pack()

# run the gui
window.mainloop()
