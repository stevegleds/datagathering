import pandas as pd
import glob
import os
'''
Uses glob to process files in the directory specified in path and stores combined in file specified in csvfilename.
CSV files should have same column headings. 
'''
# Check we are in the correct directory
print(os.getcwd())
csvfilename = "cloudperfcombined" + ".csv"
path = "S:/pythoncode/myprojects/work/datagathering/data/json/20190430/results"
os.chdir(path)  # Change directory to directory where files are stored
print(os.getcwd())  # check directory has changed correctly.
# go through all csv files and create single csv file
all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
print(all_filenames)
# combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], sort=False)
# export to csv
combined_csv.to_csv(csvfilename, index=False, encoding='utf-8-sig')
