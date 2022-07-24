from tool.helper import *
import random

def get_fold_speaker_independet(id_keys, N_fold = 1):

    if N_fold < 1 :
        print(N_fold, "is invalid fold number")
        return 

    total_amount = len(id_keys)#5531

    # Shuffle
    random.seed('2022')
    random.shuffle(id_keys)
    print("dataset shuffled")
    
    if N_fold == 1 : 
        # No cross fold validation

        train_amount = total_amount//10*8
        val_amount = (total_amount - train_amount)//2
        test_amount = total_amount - train_amount - val_amount

        train_key = id_keys[:train_amount]
        val_key = id_keys[train_amount:train_amount + val_amount]
        test_key = id_keys[train_amount + val_amount :]

        return [(train_key,"train"), (val_key,"val"), (test_key,"test")]
    
    folds = []
    fold_amount = total_amount // N_fold
    for n in range(N_fold - 1):
        folds.append((id_keys[:fold_amount], str(n)))
        del id_keys[:fold_amount]
    folds.append((id_keys, str(n+1))) # last fold

    return folds

def get_fold_speaker_dependent(id_keys, N_fold = 5):
    # speaker dependent --> split dataset depending on speaker id

    if N_fold != 5 and N_fold != 10 :
        print(N_fold, "is invalid fold number")
        return 

    folds = []

    # fold per session or speaker
    get_fold_num = {10:get_ID, 5:get_sess} 
    folds_keys = [[] for _ in range(N_fold)]
        
    for id_ in id_keys:
        fold_num = get_fold_num[N_fold](id_)
        folds_keys[fold_num].append(id_)

    total_amount = len(id_keys)#5531
    fold_amount = total_amount // N_fold
    for n in range(N_fold):
        folds.append((folds_keys[n], str(n)))

    return folds