# importing tkinter as tk to prevent any overlap with built in methods.
import tkinter as tk
# filedialog is used in this case to save the file path selected by the user.
from tkinter import filedialog

root = tk.Tk()
file_path = ""


def open_and_prep():
    # global is needed to interact with variables in the global name space
    global file_path
    # askopefilename is used to retrieve the file path and file name.
    file_path = filedialog.askopenfilename()


def process_open_file():
    global file_path
    # do what you want with the file here.
    if file_path != "":
        # opens file from file path and prints each line.
        with open(file_path, "r") as testr:
            for line in testr:
                print(line)


# create Button that link to methods used to get file path.
tk.Button(root, text="Open file", command=open_and_prep).pack()
# create Button that link to methods used to process said file.
tk.Button(root, text="Print Content", command=process_open_file).pack()

root.mainloop()


You question would be better received if you had provided any code you attempted to write for the GUI portion of your question. I know(as well as everyone else who posted on your comments) that tkinter is well documented and has countless tutorial sites and YouTube videos.

However if you have tried to write code using tkinter and just don't understand what is going on, I have written a small basic example of how to write up a GUI that will open a file and print out each line to the console.

This won't right out answer your question but will point you in the right direction.

This is a non-OOP version that judging by your existing code you might better understand.

# importing tkinter as tk to prevent any overlap with built in methods.
# filedialog is used in this case to save the file path selected by the user.

root = tk.Tk()
file_path = ""


def open_and_prep():
    # global is needed to interact with variables in the global name space
    global file_path
    # askopefilename is used to retrieve the file path and file name.
    file_path = filedialog.askopenfilename()


def process_open_file():
    global file_path
    # do what you want with the file here.
    if file_path != "":
        # opens file from file path and prints each line.
        with open(file_path, "r") as testr:
            for line in testr:
                print(line)


# create Button that link to methods used to get file path.
tk.Button(root, text="Open file", command=open_and_prep).pack()
# create Button that link to methods used to process said file.
tk.Button(root, text="Print Content", command=process_open_file).pack()

root.mainloop()


# With this example you should be able to figure out how to open your file and process it within a tkinter GUI.
# For a more OOP option:


# this class is an instance of a Frame. It is not required to do it this way.
# this is just my preferred method.

class ReadFile(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        # we need to make sure that this instance of tk.Frame is visible.
        self.pack()
        # create Button that link to methods used to get file path.
        tk.Button(self, text="Open file", command=self.open_and_prep).pack()
        # create Button that link to methods used to process said file.
        tk.Button(self, text="Print Content",
                  command=self.process_open_file).pack()

    def open_and_prep(self):
        # askopefilename is used to retrieve the file path and file name.
        self.file_path = filedialog.askopenfilename()

    def process_open_file(self):
        # do what you want with the file here.
        if self.file_path != "":
            # opens file from file path and prints each line.
            with open(self.file_path, "r") as testr:
                for line in testr:
                    print(line)


if __name__ == "__main__":
    # tkinter requires one use of Tk() to start GUI
    root = tk.Tk()
    TestApp = ReadFile()
    # tkinter requi
