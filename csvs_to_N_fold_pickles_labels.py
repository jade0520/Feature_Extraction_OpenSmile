# one / five / ten fold 
# speaker independent / dependent

"""
    {id : {label1: ,  label2: , ...}}

    # 세션별 성별 불러오기

    # 라벨 얻기
    ## Arousal : reg, cat
    ## Valence : reg, cat
    ## Script  
    ## Categorical
    ## Dominance: reg, cat
    ## gender
    ## id

    # 라벨 이름을 key로 하여 dict 저장
"""

import numpy as np
import os
import sys
import copy
import math
import pickle
from tool.helper import *
from tool.folds import get_fold_speaker_independet, get_fold_speaker_dependent
import argparse

parser = argparse.ArgumentParser(description='get pickle for featues') 
parser.add_argument('--IEMOCAP_dir', type=str, help='<Required> Set path to "/IEMOCAP_full_release/"', default = './IEMOCAP_full_release/', required=True) 
parser.add_argument('--pickle_dir', type=str, help='<Required> Set path to save pickle files', default = './jars', required=True) 
parser.add_argument('--N_fold', type=int, help='<Required> Set fold number (int)', default = 10, required=True)

parser.add_argument('--speaker_dpendency', action='store_true')
parser.add_argument('--no_speaker_dpendency', dest='speaker_dpendency', action='store_false')
parser.set_defaults(speaker_dpendency=True)

args = parser.parse_args() 

# Labels
emotions_used = {'hap':0, 'exc':0, 'ang':1, 'sad':2, 'neu':3} # Categorical with four emotions
emotions_count = [0,0,0,0]
dim_counts = {'A':{}, 'V':{}, 'D':{}}

sessions = ['Session1', 'Session2', 'Session3', 'Session4','Session5']
dataset = {}
for session in sessions:
    # collect all data from sessions

    path_to_wav = args.IEMOCAP_dir + session + '/sentences/wav/'
    path_to_emotions = args.IEMOCAP_dir + session + '/dialog/EmoEvaluation/'
    path_to_transcriptions = args.IEMOCAP_dir + session + '/dialog/transcriptions/'
    idfolders = os.listdir(path_to_wav)

    files = []
    transcriptions, emotions = {}, {}
    len_files = 0
    for idfolder in idfolders:
        newpath_to_wav = path_to_wav 
        newpath_to_wav += idfolder

        # wav list 따기
        files_ = os.listdir(newpath_to_wav)
        for f in files_:
            # 파일 이름 받기
            if f.endswith(".wav"):
                if f[0] == '.':
                    files.append(f[2:-4])
                else:
                    files.append(f[:-4])

        # wav list 를 key로 하는 dictionary 생성
        transcriptions.update(get_transcriptions(path_to_transcriptions, idfolder + '.txt')) # helper 
        emotions.update(get_emotions(path_to_emotions, idfolder + '.txt')) # 딕셔너리 리스트 [{},{}, {}]
        len_files += len(files_)
    
    #print(emotions['Ses01F_impro02_M013'])
    #print("len_files", len_files, "transcriptions", len(transcriptions), "emotions", len(emotions)) #1819

    trans_keys = transcriptions.keys()
    except_keys = list(set(files) ^ set(trans_keys))
    if len(except_keys):
        for key in except_keys:
            del(transcriptions[key]) 

    #print(">> len_files", len_files, "transcriptions", len(transcriptions), "emotions", len(emotions)) #1819
    # transcription 지우기 

    for id_ in files:   
        # id 하나씩 꺼내기
        datum = {}
        datum["Script"] = transcriptions[id_]  # tasks_name_dict와 통일 필요!!

        # 4가지 감정만 담음
        try : 
            emo = emotions_used[emotions[id_]["emotion"]]
            datum["Categorical"] = emo
            emotions_count[emo] += 1
        except : continue

        datum["Arousal_cat"] = turnTo_3level(emotions[id_]["a"])
        datum["Valence_cat"] = turnTo_3level(emotions[id_]["v"])
        datum["Dominance_cat"] = turnTo_3level(emotions[id_]["d"])
        datum["Arousal_reg"] = emotions[id_]["a"]
        datum["Valence_reg"] = emotions[id_]["v"]
        datum["Dominance_reg"] = emotions[id_]["d"]
        gen = get_gender(id_)          # gender 0,1 = M,W
        datum["Gender"] = gen
        datum["ID"] = get_ID(id_) # id 0~9 -> fold num
        dataset[id_] = datum

        # Count
        try:
            dim_counts['A'][str(datum["Arousal_reg"])] += 1 
        except:
            dim_counts['A'][str(datum["Arousal_reg"])] = 0 

        try:
            dim_counts['V'][str(datum["Valence_reg"])] += 1
        except:
            dim_counts['V'][str(datum["Valence_reg"])] = 0 

        try:
            dim_counts['D'][str(datum["Dominance_reg"])] += 1 
        except:
            dim_counts['D'][str(datum["Dominance_reg"])] = 0 


#print("dataset", len(dataset))
#print("dataset[\"Ses01F_impro02_M013\"]", dataset["Ses01F_impro02_M013"])
#print("emotions_count",emotions_count)
#print("dim counts : {}".format(dim_counts))

# divide amount for each fold
print(args.N_fold, "fold startedgy, dependency:", args.speaker_dpendency)

id_keys =  list(dataset.keys())
fold_keysNnames = get_fold_speaker_dependent(id_keys, args.N_fold) if args.speaker_dpendency else get_fold_speaker_independet(id_keys, N_fold)
                # fold_keysNnames : [(fold1_key_list, fold1_name), ..., (foldN_key_list, foldN_name) )]
for key_list, name in fold_keysNnames:
    print("fold", name, ":", len(key_list))



# create directory for pikles
N_fold_path = args.pickle_dir + str(args.N_fold) + "fold"
N_fold_path += "_D/" if args.speaker_dpendency else "_I/"

if not os.path.exists(N_fold_path):
    os.makedirs(N_fold_path)

for fold_key_list, fold_name in fold_keysNnames:
    fold_dataset = {}
    for key in fold_key_list:
        fold_dataset[key] = dataset[key]
    file_name = N_fold_path+"label_"+ fold_name +".pickle"
    with open(file_name, 'wb') as handle:
        pickle.dump(fold_dataset, handle, protocol=pickle.HIGHEST_PROTOCOL) 


"""
>>> f = open('/home/jyseo/SER_FE/SER_2022/features/jars/10fold/label_0.pickle','rb')
>>> label_dataset = pickle.load(f, encoding="latin1")
>>> label_dataset['Ses02F_script02_2_F005']
{'Script': "God damn it, Augie, don't ask me that.  I hate it when you ask me that.  You always ask me that.  It's insulting.", 'Categorical': 1, 'Arousal_cat': 2, 'Valence_cat': 0, 'Dominance_cat': 2, 'Arousal_reg': 4.5, 'Valence_reg': 1.5, 'Dominance_reg': 4.5, 'Gender': 1, 'ID': 3}
"""
