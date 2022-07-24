# Reference : https://github.com/KrishnaDN/speech-emotion-recognition-using-self-attention/blob/master/helper.py

import os
import csv
import wave
import sys
import numpy as np
import glob


def get_transcriptions(path_to_transcriptions, filename):
    f = open(path_to_transcriptions + filename, 'r').read()
    f = np.array(f.split('\n'))
    transcription = {}
    for i in range(len(f) - 1):
        g = f[i]
        i1 = g.find(': ')
        i0 = g.find(' [')
        if i0 == -1 : continue  # 구간 배당되지 않은 부분 제거
        ind_id = g[:i0]
        ind_ts = g[i1+2:]
        transcription[ind_id] = ind_ts
    
    return transcription

def get_emotions(path_to_emotions, filename):

    f = open(path_to_emotions + filename, 'r').read()
    f = np.array(f.split('\n'))
    idx = f == ''
    idx_n = np.arange(len(f))[idx]
    emotion = {}
    for i in range(len(idx_n) - 2):
        g = f[idx_n[i]+1:idx_n[i+1]]
        head = g[0]
        i0 = head.find(' - ')
        start_time = float(head[head.find('[') + 1:head.find(' - ')])
        end_time = float(head[head.find(' - ') + 3:head.find(']')])
        actor_id = head[head.find(filename[:-4]) + len(filename[:-4]) + 1:
                        head.find(filename[:-4]) + len(filename[:-4]) + 5]
        emo = head[head.find('\t[') - 3:head.find('\t[')]
        vad = head[head.find('\t[') + 1:]

        v = float(vad[1:7])
        a = float(vad[9:15])
        d = float(vad[17:23])
        
        j = 1
        emos = []
        while g[j][0] == "C":
            head = g[j]
            start_idx = head.find("\t") + 1
            evoluator_emo = []
            idx = head.find(";", start_idx)
            while idx != -1:
                evoluator_emo.append(head[start_idx:idx].strip().lower()[:3])
                start_idx = idx + 1
                idx = head.find(";", start_idx)
            emos.append(evoluator_emo)
            j += 1

        emotion[filename[:-4] + '_' + actor_id] = {'v': v,
                                                'a': a,
                                                'd': d,
                                                'emotion': emo}
    return emotion


def get_gender(id_):
    return 0 if id_[5] == 'M' else  1

def turnTo_3level(label):
    
    if label <= 2 :
        return 0

    elif (2 < label) and (label <= 3.5):
        return 1

    # 6점 넣은 게 있음
    elif (3.5 < label):
        return 2

    else : return label

def get_ID(id_, gender):
    ids = [[0,1],[2,3],[4,5],[6,7],[8,9]]
    sessNum = int(id_[4])-1

    return ids[sessNum][gender]

def get_ID(id_):
    ids = [[0,1],[2,3],[4,5],[6,7],[8,9]]
    sessNum = int(id_[4])-1
    gender =  0 if id_[5] == 'M' else  1
    
    return ids[sessNum][gender]    


def get_sess(id_):
    return int(id_[4])-1