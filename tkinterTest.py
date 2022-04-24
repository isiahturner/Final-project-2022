# from tkinter import Tk, Label
# root = Tk()
# w = Label(root, text="Hello, world!")
# w.pack()
# root.mainloop()

from tkinter import ttk
from tkinter import *


def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass


# This is how tkinter is commonly loaded in
# ! Imports all of the modules within tkinter and
# ! specifically loads in the themed widgets submodule

# Setting up the main application window and giving
# the window a title
root = Tk()
root.title('Feet to Meters')

# Create a widget frame, root is the window we are working with
# and padding adds extra space around the inside of the frame
mainframe = ttk.Frame(root, padding="3 3 12 12")

# Place the newly created widget frame in the windows application
# by using grid. Columnconfigure and rowconfigure tells Tk to
# that the frame should expand to fill any extra space if the window
# is resized.
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Creating the entry widget. First we need to create the widget and
# then place the widget on screen. So ttk.Entry lets us specify its
# parent frame (so the widget frame in this case), these are the
# children widget. The Width value is how wide we want the entry,
# so the number of characters in this case. The textvariable is
# what is being entered by the entry widget. So whenever the entry
# changes, Tk will automatically update the global variable 'feet'.
# For python, the variables used for textvariables needs to be an
# instance of the StringVar class.
feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)

# Now that we created the widget, we need to have it placed on screen.
# Tk doesn't know where you want the widgets placed relative to other
# widgets. So we use the grid to place the entry widget on the mainframe
# widget. Sticky option describes how the widget should line up within
# the grid cell, using compass directions. So w (west) means to anchor the
# widget to the left side of the cell.
feet_entry.grid(column=2, row=1, stick=(W, E))

# Creating the widget for the resulting number of meters we calculate
meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

# Creating a widget for the calculate button
ttk.Button(mainframe, text="Calculate", command=calculate).grid(
    column=3, row=3, sticky=W)

# Creating 3 static labels to make it clear how to use the application.
# Need to create and then place each label in the appropriate cell in the grid.
ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

# Goes through all of the widgets contained in the content frame and adds
# padding around each.
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# This part tells Tk to put focus on our entry widget. That way, the cursor will
# start in that field, so users don't have to click on it before starting to type
feet_entry.focus()

# This part tells Tk that if a user presses the Return/Enter key, it should call our
# calculate routine (the same as if they pressed the calculate button)
root.bind("<Return>", calculate)

# Starting the event loop
root.mainloop()
