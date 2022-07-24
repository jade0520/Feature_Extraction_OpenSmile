#!/bin/sh

# wav to csv
python extract_wavs.py\
    --csvs_dir "./test_space/csvs/"\
    --IEMOCAP_dir "./IEMOCAP/IEMOCAP_full_release/"\
    --OS_path "../opensmile/"\
    --conf_names "spectrum/spectrogram" "mfcc/MFCC12_0_D_A"

# csv to pickle
## divide labels first
python csvs_to_N_fold_pickles_labels.py\
    --IEMOCAP_dir "./IEMOCAP/IEMOCAP_full_release/"\
    --pickle_dir "./test_space/jars/"\
    --N_fold 10\
    --speaker_dpendency #or --no_speaker_dpendency

## divide features based on label pickles
python csvs_to_N_fold_pickle.py \
    --csvs_dir "./test_space/csvs/"\
    --pickle_dir "./test_space/jars/"\
    --label_name "10fold_D"\
    --feat_list "spectrogram" "MFCC12_0_D_A"
