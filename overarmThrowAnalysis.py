# Importing modules that are needed throughout the script
from pathlib import Path
import os
import matplotlib
import pandas as pd
import numpy as np
import fontstyle
import matplotlib.pyplot as plt

# Defining the functions


def graphSegment(dataset, colX1, colZ1, colX2, colZ2, startRange, endRange, titleName, firstLine=0, secondLine=0, thirdLine=0):
    # * The function plots the segment between two markers to visualize the segment's movement over time.
    # * Due to the amount of data points, the function is created so you can splice the dataset to visualize
    # * the moments that you want to. The function is designed so that it only plots the segments that don't cross over
    # * the x-distance for the first point, that way the segments are easier to track over time. The function takes in 11
    # * inputs and returns a figure. Starting with dataset, the columns are based off the inputted data and the data is
    # * expected to be a dataframe created using pandas. The type of data contained within the dataframe should be either int or float.
    # * colX1, colZ1 are the two columns that contain the X and Z direction data for the first desired marker
    # * (i.e 'RSK1' for X 'RSK1.2 for Z) and colX2, colZ2 are the two columns that contain the X and Z direction data for
    # * the second desired marker. The colX1, colZ1, colX2, colZ2 inputs must be strings aligned with the column names
    # * that are used within the passed dataframe. startRange should be where you want to begin mapping the segment and
    # * endRange should be where you want to stop mapping the segment. Both startRange and endRange should be inputted
    # * as integers. The firstLine, secondLine and thirdLine keyword arguments are placeholders, the values will be inputted
    # * when used along with the segmentComparison function (will change based on each dataframe being worked through
    # * The output is a figure containing the segments over time and the plot should be saved to a variable when calling
    # * the function.

    # Creating the figure and axes that is going to be plotted on.

    fig, ax = plt.subplots()
    ax.set_xlabel('Displacement X-direction (m)')
    ax.set_ylabel('Displacement Z-direction (m)')

    # Manually cleaning up the imported columns by dropping the NaN values from the entire column
    dataset[colX1] = dataset[colX1].dropna()
    dataset[colZ1] = dataset[colZ1].dropna()
    dataset[colX2] = dataset[colX2].dropna()
    dataset[colZ2] = dataset[colZ2].dropna()

    # Looping through the desired portion of the segment's motion and creating a line based off the two
    # points. The newly create segment is then plotted for each frame the loop goes through.

    for i in range(startRange, endRange):
        # Initializing the x and z data points that will be used for the segment. Created a separate condition for
        # the ball motion capture data because the data changes a significant amount between datasets. So instead of
        # plotting by pieces, the ball's entire column is plotted.
        if colX1 == 'Ball' or colZ1 == 'Ball.2':
            x1 = dataset.iloc[i][colX1]
            z1 = dataset.iloc[i][colZ1]

            x2 = dataset.iloc[i][colX2]
            z2 = dataset.iloc[i][colZ2]

            xPoints = [x1, x2]
            zPoints = [z1, z2]

            # Plotting the two points in space on the graph, should be for the X and Z direction in this example
            ax.plot(xPoints, zPoints, 'bo', linestyle='-')
            ax.set_title(f'{titleName} + {colX1}')

        # Initializes the x and z data points that will be used for the segment. The data in the else statement
        # is for all data columns that are not for the ball
        else:
            x1 = dataset.iloc[i][colX1]
            z1 = dataset.iloc[i][colZ1]

            x2 = dataset.iloc[i][colX2]
            z2 = dataset.iloc[i][colZ2]

            xPoints = [x1, x2]
            zPoints = [z1, z2]

            # Plotting the two points in space on the graph, should be for the X and Z direction in this example
            ax.plot(xPoints, zPoints, 'bo', linestyle='-')
            ax.set_title(f'{titleName} - {colX1[0:-1]}')

            # Plotting the lines for each graph depending on the ranges imported into the function. When the frame
            # matches with the start of the movement, ball release and follow through times reported by the dataframe,
            # the corresponding event's line will be drawn. Goal is for the event lines to autoscale.

            if i == firstLine - 1:
                verticalLineX = [x1, x1]
                verticalLineZ = [round(min(dataset[startRange:endRange][colZ1].dropna()), 3), round(
                    max(dataset[startRange:endRange][colZ2].dropna()), 3)]
                ax.plot(verticalLineX, verticalLineZ, 'go',
                        linestyle='-', label='Start of Movement')

            elif i == secondLine - 1:
                verticalLineX = [x1, x1]
                verticalLineZ = [round(min(dataset[startRange:endRange][colZ2].dropna()), 3), round(
                    max(dataset[startRange:endRange][colZ1].dropna()), 3)]
                ax.plot(verticalLineX, verticalLineZ, 'ro',
                        linestyle='-', label='Ball Release')

            elif i == thirdLine - 1:
                verticalLineX = [x1, x1]
                verticalLineZ = [round(min(dataset[startRange:endRange][colZ2].dropna()), 3), round(
                    max(dataset[startRange:endRange][colZ1].dropna()), 3)]
                ax.plot(verticalLineX, verticalLineZ, 'ko',
                        linestyle='-', label='Follow Through')

    # After all of the plotting has been completed, adding in a legend for each line that
    # has been added
    ax.legend()

    # Returning the figure
    return fig


def visualizeForces(data, titleName):
    # * The function plots the analog data for two force plates within one dataset, the plot will have 2 subplots
    # * next to each other. This function can work for any length of a trial and takes 2 inputs. The first input
    # * for data is a dataframe created using the pandas module. The dataframe will splice a dataseries for each
    # * force plate. These series will be used to calculate peak forces, rate of force production and bodyweight for
    # * each subject. The function's second input titleName is so the title of the plot can be automated, especially
    # * when used with the forceComparison function that loops through the number of arguments inputted into it. The
    # * 5 outputs of the function are a figure with 2 subplots, the peak force for the both force plates and rate of
    # * force production for each force plate.

    # Creating a list for the x axis that contains the frame number for each data point
    x = list(np.arange(0, len(data.iloc[:]['FP1'])))

    # Going through x-axis list to transform it into a percentage based x-axis
    for counter in range(len(x)):
        x[counter] = (x[counter]/len(x)) * 100

    # Creating the figure we are going to plot on, the figure will have 2 subplots placed
    # next to each other
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Plotting all of the forces for the first force plate onto the first subplot
    ax1.plot(x, data.iloc[:]['FP1'], label='Sagittal Forces')
    ax1.plot(x, data.iloc[:]['FP1.1'], label='Frontal Forces')
    ax1.plot(x, data.iloc[:]['FP1.2'], label='Longitudinal Forces')

    ax1.set_title(titleName + ' - Force Plate 1')
    ax1.set_xlabel('Percentage of Movement (%)')
    ax1.set_ylabel('Force (N)')
    ax1.set_ylim(-100, 1000)
    ax1.legend()

    # Plotting all of the forces for the second force plate onto the second subplot
    ax2.plot(x, data.iloc[:]['FP2'], label='Sagittal Forces')
    ax2.plot(x, data.iloc[:]['FP2.1'], label='Frontal Forces')
    ax2.plot(x, data.iloc[:]['FP2.2'], label='Longitudinal Forces')

    ax2.set_title(titleName + ' - Force Plate 2')
    ax2.set_xlabel('Percentage of Movement (%)')
    ax2.set_ylabel('Force (N)')
    ax2.set_ylim(-100, 1000)
    ax2.legend()

    # Calculating the subject's bodyweight to normalize the force recorded on the force plates
    bodyWeight = data.iloc[0]['FP1.2'] + data.iloc[0]['FP2.2']

    # Resetting the y ticks for both subplots. Designed to be the normalized to the subject's
    # body weight (i.e: 1.5 times their body weight during ball release)
    y = np.array([0, 200, 400, 600, 800, 1000])
    ticks = [round(0/bodyWeight, 3), round(200/bodyWeight, 3), round(400/bodyWeight, 3), round(600/bodyWeight, 3),
             round(800/bodyWeight, 3), round(1000/bodyWeight, 3)]
    ax1.set_yticks(y, ticks)
    ax2.set_yticks(y, ticks)

    # Calculating the min and max for each force plate
    minForcePlate1 = min(data.iloc[:]['FP1.2'])
    minForcePlate2 = min(data.iloc[:]['FP2.2'])
    peakForcePlate1 = max(data.iloc[:]['FP1.2'])
    peakForcePlate2 = max(data.iloc[:]['FP2.2'])

    # Calculating the rate of force production, so how fast did they go from minimum force to maximum force

    # Creating a list to store the frames that the minimum and maximum force occurred, use to calculate
    # the change in time from min to max
    minMaxFramesFP1 = []
    minMaxFramesFP2 = []

    # Looping through each frame and saving the frames that either peak force occurs or minimum force occurs.
    # If the value at the frame matches the values initiated above, then the value is saved
    for counter in range(len(data.iloc[:]['FP1.2'])):
        if data.iloc[counter]['FP1.2'] == minForcePlate1 or data.iloc[counter]['FP1.2'] == peakForcePlate1:
            minMaxFramesFP1.append(counter)

        if data.iloc[counter]['FP2.2'] == minForcePlate2 and len(minMaxFramesFP2) < 2:
            minMaxFramesFP2.append(counter)
        elif data.iloc[counter]['FP2.2'] == peakForcePlate2 and len(minMaxFramesFP2) < 2:
            minMaxFramesFP2.append(counter)

    # Physically calculating the amount of time it takes to go from min to max
    timeToPeakFP1 = abs(minMaxFramesFP1[0] - minMaxFramesFP1[1])/1000
    timeToPeakFP2 = abs(minMaxFramesFP2[0] - minMaxFramesFP2[1])/1000

    # Physically calculating the force produced in the amount of time it takes to go from min to max
    forceProduction1 = (peakForcePlate1 - minForcePlate1)/timeToPeakFP1
    forceProduction2 = (peakForcePlate2 - minForcePlate2)/timeToPeakFP2

    # Returning the figure containing both force plate data, the peak of both force plates and how
    # fast it took to reach peak force for both force plates

    return fig, peakForcePlate1, peakForcePlate2, forceProduction1, forceProduction2


def forceComparison(**kwargs):
    # * The function brings in as many data sets as you want as keyword arguments. The value for each keyword argument
    # * needs to be a pandas dataframe. Should be able to access this through a dictionary created when running through
    # * the current directory at the beginning of the script. Could also import your own dictionary containing the dataframes.
    # * Important to note that the name of the keys are important because those are what is used for the title for each plot
    # * when calling the visualizeForces function.

    # Creating an empty list to store all of the figures for each subject, that way each one can be accessed individually
    # later on.
    figureList = []

    # Looping through the keyword arguments and pulling the dataset and title name from each pair
    for titleName, dataset in kwargs.items():

        # Initializing and converting the event times to a frame to be used within the function for startRange and endRange
        footStrike = int((dataset.iloc[0]['Foot Strike']) * 200)
        ballRelease = int((dataset.iloc[0]['Event']) * 200)
        followThrough = int((dataset.iloc[0]['Foot Off']) * 200)

        # Creating a pandas series to find the number of rows. Finds the total frame length
        # and the total time of the trial
        df = dataset.iloc[:]['RBHD'].dropna()
        maxFrameLength = len(df)
        trialLength = maxFrameLength / 200

        # Running the visualizeForces function and appending the figure to a list that keeps track of the figures.
        currentFigure, peakForce1, peakForce2, forceRateFP1, forceRateFP2 = visualizeForces(
            dataset, f'{titleName}')
        bodyWeight = dataset.iloc[0]['FP1.2'] + dataset.iloc[0]['FP2.2']
        figureList.append(currentFigure)

        # Creating a report to the user for the subject's forces
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


def segmentComparison(**kwargs):
    # * The function brings in as many data sets as you want as keyword arguments and works the same as forceComparison function
    # * Takes in as many key-value pairs as possible, keys need to be name of title you want and value is the dataframe
    # * connected to that subject.

    # Creating an empty list to store all of the figures for each subject, that way each one can be accessed individually
    # later on.
    figureList = []

    # Looping through the keyword arguments and pulling the dataset and title name from each pair
    for titleName, dataset in kwargs.items():

        # Initializing and converting the event times to a frame to be used within the function for startRange and endRange
        footStrike = int((dataset.iloc[0]['Foot Strike']) * 200)
        ballRelease = int((dataset.iloc[0]['Event']) * 200)
        followThrough = int((dataset.iloc[0]['Foot Off']) * 200)
        print(f'{footStrike}!')

        # Creating a pandas series to find the number of rows. This lets me find the total frame length
        # and the total time of the trial
        df = dataset.iloc[:]['RBHD'].dropna()
        maxFrameLength = len(df)
        trialLength = maxFrameLength / 200

        # Visualizing/Communicating the total frame length and the trial times
        print(f'The file for {titleName} is {maxFrameLength} frames long')
        print(f'The trial is {trialLength} seconds')
        print(" ")
        print(f'Start of Movement: {footStrike/200}s')
        print(f'Ball Release: {ballRelease/200}s')
        print(f'Follow Through: {followThrough/200}s')

        print(f'{footStrike}!')
        print('_____' * 10)

        # Running the visualizeForces function and appending the figure to a list that keeps track of the figures.
        currentFigure = graphSegment(dataset, 'RFR1', 'RFR1.2', 'RFR3', 'RFR3.2', 0, footStrike,
                                     titleName, firstLine=footStrike, secondLine=ballRelease, thirdLine=followThrough)
        figureList.append(currentFigure)

    return figureList


# Retrieving the working directory that is going to be looped through
cwd = os.getcwd()

# Setting the directory to the current working directory so the file name can be concatenated
# to open each file individually
directory = os.getcwd()

# Creating a generator object that contains all of the excel files in the directory
# Asterisks is a wild card, so is saying take any file name that has .blahblah
# Could do sub wildcards i.e baseball.xlsx
files = Path(directory).glob('*.csv')

# Creating an empty dictionary to append the results for each file, each value of dictionary
# will be a data series
filesToCombine = {}

# Looping through the generator object and interact with each file
for file in files:

    # Print out file to make sure you are interacting with the correct file
    print(file)

    # Reads in the excel file as a dataframe
    columnCheck = pd.read_csv(r'{filename}'.format(
        filename=file), sep='\\t', skiprows=[0, 2, 3, 4], engine='python')

    # Takes the imported dataframe and isolates the last names into a data series
    filesToCombine[f'{file}'] = columnCheck

# Printing the keys for future reference when using the comparison function's **kwargs input
print(" ")
for key in filesToCombine.keys():
    print(key)
# print(filesToCombine.keys())
print('_____' * 10)

# print(
#     filesToCombine['C:\\Users\\Isiah Turner\\OneDrive\\Documents\\Final project 2022\\S1_DP_04_M.csv'])
# # Calling the forceComparison function for 3 participants

forceFigures = forceComparison(S104=filesToCombine['C:\\Users\\Isiah Turner\\OneDrive\\Documents\\Final project 2022\\S1_DP_04_M.csv'],
                               S1DP01=filesToCombine['C:\\Users\\Isiah Turner\\OneDrive\\Documents\\Final project 2022\\S1_DP_01_WM.csv'],
                               S1DP13=filesToCombine['C:\\Users\\Isiah Turner\\OneDrive\\Documents\\Final project 2022\\S1_DP_13_O.csv'])

# segmentFigures = segmentComparison(S104 = filesToCombine['c:\\Users\\Isiah Turner\\OneDrive\\Documents\\Final project 2022\\S1_DP_04_M.csv'],
# S1DP02 = filesToCombine['c:\\Users\\Isiah Turner\\OneDrive\\Documents\\Final project 2022\\S1_DP_01_WM.csv'],
# S1DP13 = filesToCombine['c:\\Users\\Isiah Turner\\OneDrive\\Documents\\Final project 2022\\S1_DP_13_O.csv'])

# Showing all of the figures created using the function
plt.show()
