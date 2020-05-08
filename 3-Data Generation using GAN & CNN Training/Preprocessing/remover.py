# Import
import os
# Path to save and load
path = "./Data_Sorted_FCS/"
# empty list for words
words = []
# Loop every folders from Data_Sorted_FCS
for folders in os.listdir(path):
    # Get number of files per folder
    files = len(os.listdir(path + folders))
    # If number of files is greater than
    if files > 200:
        # Print folder
        print(folders, end='-')
        # Compute Train and Test Ratio
        print("Train" + str(files * 0.8) + " Test" + str(files * 0.2))
        # Add to words list
        words.append(folders)
        
    else:
        # Delete the folder and files inside
        os.system("rmdir /Q /S " + "Data_Sorted_FCS\\" + folders)
        print("DELETED")
        

