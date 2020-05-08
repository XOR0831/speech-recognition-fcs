# Import
import os
import shutil
import math
# Path to save and load
path = "./Data_Sorted_FCS/"
path_train = "./Train/"
path_test = "./Test/"
# Check if directory exists
if not os.path.exists(path_train):
    # Create directory
    os.makedirs(path_train)
# Check if directory exists
if not os.path.exists(path_test):
    # Create directory
    os.makedirs(path_test)
# Loop every folders in Data_Sorted_FCS
for folders in os.listdir(path):

    print(folders)

    # Check if directory exists
    if not os.path.exists(path_train + folders):
        # Create directory
        os.makedirs(path_train + folders)
    # Check if directory exists
    if not os.path.exists(path_test + folders):
        # Create directory
        os.makedirs(path_test + folders)
    # List all files from folder
    files = os.listdir(path + folders)
    # Get total number of files
    num_files = len(os.listdir(path + folders))
    # Compute number of train data
    train = math.ceil(num_files * 0.8)
    # Compute number of test data
    test = math.floor(num_files * 0.2)
    # Split train data
    files_train = files[:train + 1]
    # Split test data
    files_test = files[train + 1:train+test]
    # Loop every files from train split
    for i in files_train:
        # Move file to train folder
        shutil.move(path + folders + "/" + i, path_train + folders + "/" + i)
    # Loop every files from test split
    for i in files_test:
        # Move file to test folder
        shutil.move(path + folders + "/" + i, path_test + folders + "/" + i)

    
