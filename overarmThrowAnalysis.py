# Importing Modules
import pandas as pd
import numpy as np
import math


def sagittalSegmentAngle(dataset, colX1, colZ1, colX2, colZ2):
    # * The function finds the segment angle within the sagittal plane (x direction) of the motion
    # * capture data. Calculates the segment length of interest by using the distance formula involving
    # * two marker points across the entire collection and calculates an angle by putting the segment length
    # * in reference to the ground to create a 90 degree triangle to find the missing angle.
    # * The function takes in 5 inputs and 3 outputs. Starting with dataset, the calculations
    # * are based off the inputted data and the data is expected to be a dataframe created using pandas.
    # * The type of data contained within the dataframe should be either int or float. colX1, colZ1 are
    # * the two columns that contain the X and Z direction data for the first desired marker (i.e 'RSK1' for X
    # * 'RSK1.2) and colX2, colZ2 are the two columns that contain the X and Z direction data for the second
    # * desired marker. The colX1, colZ1, colX2, colZ2 inputs must be strings aligned with the column names
    # * that are used within the passed dataframe. The outputs are lists containing float type objects
    # * for segment lengths, the calculated adjacent lengths and calculated angles using cosine.

    # Initializing variables
    segmentAngleList = []
    segmentLengthList = []
    adjacentLengthList = []

    # Running a for loop so that each value of x and z are synced up between the two desired
    # marker points in the cluster. Will creates lists for segment length, the calculated
    # adjacent length and the calculated angle.
    for value in range(len(dataset.iloc[:][colX1])):
        x1 = dataset.iloc[value][colX1]
        z1 = dataset.iloc[value][colZ1]

        x2 = dataset.iloc[value][colX2]
        z2 = dataset.iloc[value][colZ2]

        # Inputting variables into distance formula to find the length of the segment
        segmentLength = math.sqrt(((x2 - x1)**2) + ((z2 - z1)**2))
        segmentLengthList.append(segmentLength)

        # Inputting variables into distance formula to calculate the adjacent length
        # in order to find the angle
        adjacentLength = math.sqrt(((x2 - x1)**2) + ((z2 - z2)**2))
        adjacentLengthList.append(adjacentLength)

        # Using cosine to calculate the angle for the entire segment
        calculatedAngle = math.acos(adjacentLength/segmentLength)
        segmentAngleList.append(math.degrees(calculatedAngle))

        # A check to make sure that the function iterated all the way through
        if value > 765:
            print("Distance has been calculated")

    return segmentAngleList, segmentLengthList, adjacentLengthList


# * Importing the csv file of the first participant. The dataframe should contain all of the columns after
# * the event columns. The dataframe's columns are organized by markers (i.e LFHD contains the data for
# * the left head marker in the x-direction). Used np.r_[list], translates slice objects to concatenation
# * along the first axis, so creates an array along the first axis. Pandas adds a number (1, 2, ... , N)
# * to the column name when dealing with duplicate names. Will add (.1, .2, ... , .N) to the end if column
# * name ends in an integer.
data = pd.read_csv(
    r'C:\Users\Isiah Turner\OneDrive\Documents\Final Project 2022\S1_DP_01_WM.csv',
    sep='\t', usecols=np.r_[4:190], skiprows=[0, 2, 3, 4], nrows=767)

# Visualizing the dataset to make sure orientation is correct

# print(data)

testAngle, testSeg, testAdj = sagittalSegmentAngle(
    data, 'RSK1', 'RSK1.2', 'RSK3', 'RSK3.2')

print(testAngle[0:5])
print(testSeg[0:5])
print(testAdj[0:5])
