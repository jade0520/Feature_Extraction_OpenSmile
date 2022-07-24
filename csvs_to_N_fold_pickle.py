import os
import pickle
from tqdm import tqdm

from tool.csv_tools import get_feature_csv

import argparse
parser = argparse.ArgumentParser(description='get pickle for featues') 
parser.add_argument('--csvs_dir', type=str, help='<Required> Set path to save extracted csv files', default = './csvs', required=True) 
parser.add_argument('--pickle_dir', type=str, help='<Required> Set path to save pickle files', default = './jars', required=True) 
parser.add_argument('--label_name', type=str, help='<Required> Set label name to use', default = '10fold_D', required=True)
parser.add_argument('--feat_list','--list', default = ['STFT'] , nargs='+', type=str, help='<Required> Set a features to extract', required=True)
args = parser.parse_args() 

# load label pickle
label_pickle_dir = args.pickle_dir + args.label_name
label_pickle_list = os.listdir(label_pickle_dir)

print(label_pickle_dir)

for pickle_name in label_pickle_list:
    if not pickle_name.startswith("label") : continue
    with open(label_pickle_dir+ '/'+ pickle_name, 'rb') as f:
        label_dataset = pickle.load(f, encoding="latin1")

    id_keys = label_dataset.keys()
    print(pickle_name, len(id_keys), end = ' ')

    for feat in args.feat_list:
        print("for feat", feat)
        # feature 별로 저장
        dataset = {}
        for key in tqdm(id_keys):
            dataset[key] = get_feature_csv(args.csvs_dir, feat, key) # OpenSmile

        # save as pickle
        pickle_path = label_pickle_dir+"/"+ feat + '_'+ pickle_name.split('_')[1]
        with open(pickle_path, 'wb') as handle:
            pickle.dump(dataset, handle, protocol=pickle.HIGHEST_PROTOCOL)  
