# Importing Modules
import pandas as pd
import numpy as np


# * Importing the csv file of the first participant. The dataframe should contain the Item/Frame Number
# * and all of the columns except for columns 2-4 since that is force data at the predetermined times.
# * uses pandas in order to get the csv file into a dataframe and numpy is used to splice the columns
# * that are going to be used.

# TODO: remember to make sure that nrows is deleted so that the entire dataset is uploaded, not just three rows
# TODO: The data converts to NaN after 767, so the dataset should be until 767

data = pd.read_csv(
    r'C:\Users\Isiah Turner\OneDrive\Documents\Final Project 2022\S1_DP_01_WM.csv',
    sep='\t', index_col="ITEM", usecols=np.r_[0, 4:190], skiprows=4, nrows=3)

# Visualizing the dataset to make sure orientation is correct
#TODO:dfNew = data.rename(columns = {'X': 'Foot Strike (X)', 'X.1': 'Event (X)', 'X.2': 'Foot Off (X)'})
print(data)
