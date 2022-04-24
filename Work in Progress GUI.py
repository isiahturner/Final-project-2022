# Importing modules that are needed throughout the script
from tkinter import *
from tkinter import ttk
from pathlib import Path
import os
import pandas as pd
import numpy as np
import fontstyle
import matplotlib.pyplot as plt
import cv2


# Retrieving the working directory that is going to be looped through
cwd = os.getcwd()

# Setting the directory to the current working directory so the file name can be concatenated
# to open each file individually
directory = os.getcwd()

# Creating a generator object that contains all of the excel files in the directory
# Asterisks is a wild card, so is saying take any file name that has .blahblah
# Could do sub wildcards i.e baseball.xlsx
files = Path(directory).glob('*.csv')

# Creating an empty list to append the results for each file, each part of list
# will be a data series
filesToCombine = {}
maxCols = {}

# Looping through the generator object and interact with each file
for file in files:
    # Print out file to make sure you are interacting with the correct file
    print(file)

    # Reads in the excel file as a dataframe
    #patientInfo = pd.read_excel(r'{filename}'.format(filename=file))
    columnCheck = pd.read_csv(r'{filename}'.format(
        filename=file), sep='\\t', skiprows=[0, 2, 3, 4], engine='python')
    # Takes the imported dataframe and isolates the last names into a data series

    filesToCombine[f'{file}'] = columnCheck
    #maxCols[f'{file}'] = len(columnCheck.columns)
    # Using the function that filters the last name based on the letter you want

    # Convert the list of filtered names into a data series

    # Add the new data series to the list
print(filesToCombine.keys())
print('_____' * 10)
imageList = []


def visualizeForces(data5, titleName):
    # ! Potentially set it up as 2 columns and 1 row so I can stack multiple people on top

    x = list(np.arange(0, len(data5.iloc[:]['FP1'])))
    for counter in range(len(x)):
        # x[counter] = x[counter]/1000
        x[counter] = (x[counter]/len(x)) * 100

    bodyWeight = data5.iloc[0]['FP1.2'] + data5.iloc[0]['FP2.2']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.plot(x, data5.iloc[:]['FP1'], label='Sagittal Forces')
    ax1.plot(x, data5.iloc[:]['FP1.1'], label='Frontal Forces')
    ax1.plot(x, data5.iloc[:]['FP1.2'], label='Longitudinal Forces')

    ax2.plot(x, data5.iloc[:]['FP2'], label='Sagittal Forces')
    ax2.plot(x, data5.iloc[:]['FP2.1'], label='Frontal Forces')
    ax2.plot(x, data5.iloc[:]['FP2.2'], label='Longitudinal Forces')

    ax1.set_title(titleName + ' - Force Plate 1')
    ax1.set_xlabel('Percentage of Movement (%)')
    ax1.set_ylabel('Force (N)')

    ax1.set_ylim(-100, 1000)
    y = np.array([0, 200, 400, 600, 800, 1000])
    ticks = [round(0/bodyWeight, 3), round(200/bodyWeight, 3), round(400/bodyWeight, 3), round(600/bodyWeight, 3),
             round(800/bodyWeight, 3), round(1000/bodyWeight, 3)]
    ax1.set_yticks(y, ticks)

    ax1.legend()

    ax2.set_title(titleName + ' - Force Plate 2')
    ax2.set_xlabel('Percentage of Movement (%)')
    ax2.set_ylabel('Force (N)')
    ax2.set_ylim(-100, 1000)
    ax2.legend()

    minForcePlate1 = min(data5.iloc[:]['FP1.2'])
    minForcePlate2 = min(data5.iloc[:]['FP2.2'])
    peakForcePlate1 = max(data5.iloc[:]['FP1.2'])
    peakForcePlate2 = max(data5.iloc[:]['FP2.2'])

    minMaxTiming1 = []
    minMaxTiming2 = []
    for counter in range(len(data5.iloc[:]['FP1.2'])):
        if data5.iloc[counter]['FP1.2'] == minForcePlate1 or data5.iloc[counter]['FP1.2'] == peakForcePlate1:
            minMaxTiming1.append(counter)

        if data5.iloc[counter]['FP2.2'] == minForcePlate2 and len(minMaxTiming2) < 2:
            minMaxTiming2.append(counter)
        elif data5.iloc[counter]['FP2.2'] == peakForcePlate2 and len(minMaxTiming2) < 2:
            minMaxTiming2.append(counter)

    timeToPeakFP1 = abs(minMaxTiming1[0] - minMaxTiming1[1])/1000
    timeToPeakFP2 = abs(minMaxTiming2[0] - minMaxTiming2[1])/1000
    forceProduction1 = (peakForcePlate1 - minForcePlate1)/timeToPeakFP1
    forceProduction2 = (peakForcePlate2 - minForcePlate2)/timeToPeakFP2

    return fig, peakForcePlate1, peakForcePlate2, forceProduction1, forceProduction2


def forceComparison(**kwargs):
    # The function brings in as many data sets as you want as keyword arguments
    figureList = []

    for titleName, dataset in kwargs.items():
        # Do something
        # Perform the initial report

        # Initializing and converting the event times to a frame to be used within the function for startRange and endRange
        footStrike = int((dataset.iloc[0]['Foot Strike']) * 200)
        ballRelease = int((dataset.iloc[0]['Event']) * 200)
        followThrough = int((dataset.iloc[0]['Foot Off']) * 200)

        # Creating a pandas series to find the number of rows. This lets me find the total frame length
        # and the total time of the trial

        df = dataset.iloc[:]['RBHD'].dropna()
        maxFrameLength = len(df)
        trialLength = maxFrameLength / 200

        # Running the function that visualizes the forces and gives peak force
        currentFigure, peakForce1, peakForce2, forceRateFP1, forceRateFP2 = visualizeForces(
            dataset, f'{titleName}')
        bodyWeight = dataset.iloc[0]['FP1.2'] + dataset.iloc[0]['FP2.2']
        # print(peakForce1 / bodyWeight)
        # print(peakForce2/bodyWeight)
        figureList.append(currentFigure)

        # Visualizing/Communicating the total frame length and the trial times
        print(fontstyle.apply('Trial Information', 'BOLD/BLACK/WHITE_BG'))
        print(f'The file for {titleName} is {maxFrameLength} frames long')
        print(f'The trial is {trialLength} seconds')
        print(" ")
        print(fontstyle.apply('Time of Events', 'BOLD/BLACK/WHITE_BG'))
        print(f'Start of Movement: {footStrike/200}s')
        print(f'Ball Release: {ballRelease/200}s')
        print(f'Follow Through: {followThrough/200}s')
        print(" ")
        print(fontstyle.apply('Force Data', 'BOLD/BLACK/WHITE_BG'))
        print(
            f'Lead Leg Peak Force: {peakForce1: .3f} N or {bodyWeight/peakForce1: .3f} times the body weight')
        print(
            f'Rear Leg Peak Force: {peakForce2: .3f} N or {bodyWeight/peakForce2: .3f} times the body weight')
        print(
            f'Force Production Rate (Force Plate 1): {forceRateFP1: .3f} N/s')
        print(
            f'Force Production Rate (Force Plate 2): {forceRateFP2: .3f} N/s')
        print('_____' * 10)

    return figureList


def calculate(*args):
    try:
        forceComparison(
            S1=filesToCombine[filename1.get()], S2=filesToCombine[filename2.get()])
        ttk.Label(mainframe, text='SUCCESS').grid(column=3, row=1)
        # ttk.Entry(mainframe, text = '')
        plt.show()
    except ValueError:
        print('Error')
        pass


# Setting up the main application window and giving the window a title
rootWindow = Tk()
rootWindow.title('Force Comparison')

# Create a widget frame, root is the window we are working with
# and padding adds extra space around the inside of the frame
mainframe = ttk.Frame(rootWindow, padding="3 3 12 12")

# Place the newly created widget frame in the windows application
# by using grid. Columnconfigure and rowconfigure tells Tk to
# that the frame should expand to fill any extra space if the window
# is resized.
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
rootWindow.columnconfigure(0, weight=1)
rootWindow.rowconfigure(0, weight=1)

# Creating the entry widget. First we need to create the widget and
# then place the widget on screen. So ttk.Entry lets us specify its
# parent frame (so the widget frame in this case), these are the
# children widget. The Width value is how wide we want the entry,
# so the number of characters in this case. The textvariable is
# what is being entered by the entry widget. So whenever the entry
# changes, Tk will automatically update the global variable 'feet'.
# For python, the variables used for textvariables needs to be an
# instance of the StringVar class.
filename1 = StringVar()
filename1Entry = ttk.Entry(mainframe, width=50, textvariable=filename1)


filename2 = StringVar()
filename2Entry = ttk.Entry(mainframe, width=50, textvariable=filename2)

# Placing the entries onto the GUI stacked on top of each other
filename1Entry.grid(column=1, row=1, stick=(W, E))
filename2Entry.grid(column=1, row=2, stick=(W, E))

# Adding spacing and a status bar
ttk.Label(mainframe, text='').grid(column=1, row=3)
ttk.Label(mainframe, text='STATUS:').grid(column=2, row=1, stick=(W, E))

# Creating the button that creates the calculations
ttk.Button(mainframe, text="Calculate", command=calculate).grid(
    column=1, row=4, sticky=W)


# Goes through all of the widgets contained in the content frame and adds
# padding around each.
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# This part tells Tk to put focus on our entry widget. That way, the cursor will
# start in that field, so users don't have to click on it before starting to type
filename1Entry.focus()

# This part tells Tk that if a user presses the Return/Enter key, it should call our
# calculate routine (the same as if they pressed the calculate button)
rootWindow.bind("<Return>", calculate)

# Starting the event loop
rootWindow.mainloop()

# OVERALL NEED TO CHANGE:
# 1. How to handle the imported data, dictionary makes it less flexible/automated at the moment
# 2. Need to adjust the visualizingForces function to call on the datasets more effectively
# 3. Definitely need to fix the interaction with handling figures/images, will help with
# GUI work. Maybe display then close based off loop count, etc
# 4. Export the report instead of printing to the terminal, will make it easier to visualize
# 5. When presenting the data on graph, plan out the subplots() better and potentially wait
# to display them until all of the figures are created.
# 6. Could also store the data in a new file every time it is generated instead and then work
# from there.
# 7. Separate a lot of the work into more functions potentially.
