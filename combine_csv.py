import pandas as pd
import glob
import os
# Check we are in the correct directory
print(os.getcwd())
csvfilename = "cloudperfcombined" + ".csv"
path = "S:/pythoncode/myprojects/work/datagathering/data/json/results"
os.chdir(path)
print(os.getcwd())
# go through all csv files and create single csv file
all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
print(all_filenames)
# combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], sort=False)
# export to csv
combined_csv.to_csv(csvfilename, index=False, encoding='utf-8-sig')