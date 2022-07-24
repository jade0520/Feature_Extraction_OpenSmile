import csv
import numpy as np

def csv2nparr(csvfile):

    # csv to list
    with open(csvfile, 'r') as f:
        rdr = csv.reader(f, delimiter=';')
        feature_list = list(rdr)

    # extract feature
    image_list = []
    for line in feature_list[1:]:
        image_list.append(line[2:])

    # set frame (time) axis to be horizental
    image_arr = np.array(image_list,  dtype=np.float32)

    return image_arr.T

def get_feature_csv(feature_csv_PATH, feat, id):

    csv_path = feature_csv_PATH + feat + "_" + id + ".csv" # ex. STFT_025_01_Ses01F_script01_3_F000.csv
    result_arr = csv2nparr(csv_path)
    # Normalize
    #result_arr = (result_arr - np.min(result_arr))/(np.max(result_arr) - np.min(result_arr))
    
    return result_arr