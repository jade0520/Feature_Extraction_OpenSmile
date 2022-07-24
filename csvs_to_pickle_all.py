import os
import pickle
from tool.csv_tools  import csv2nparr
import argparse

parser = argparse.ArgumentParser(description='get pickle for featues') 
parser.add_argument('--csvs_dir', type=str, help='<Required> Set path to save extracted csv files', default = './csvs', required=True) 
parser.add_argument('--pickle_dir', type=str, help='<Required> Set path to save pickle files', default = './jars', required=True) 
args = parser.parse_args()

csvs_list = os.listdir(args.csvs_dir) # Get id list in a session
dataset = {}
for csv_name in csvs_list:
    # Get data per session
    feat_idx = csv_name.find("_Ses")
    feat_name = csv_name[:feat_idx]
    id_ = csv_name[feat_idx+1:].split('.')[0]
    csv_path =args.csvs_dir + csv_name
    arr = csv2nparr(csv_path)

    if feat_name not in dataset.keys():
        # add new dictionary for new feat name
        dataset[feat_name] = {}

    dataset[feat_name][id_] = arr

feat_name_list = list(dataset.keys())

# save as pickle
for feat_name in feat_name_list:
    pickle_path = args.pickle_dir + feat_name + '_IEMOCAP.pickle'
    with open(pickle_path, 'wb') as handle:
        pickle.dump(dataset[feat_name], handle, protocol=pickle.HIGHEST_PROTOCOL)  
