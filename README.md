# Feature_Extraction_OpenSmile  
Codes for extracting features of **IEMOCAP** with **Open Smile tool kit**  
Ouput - csvs file or/and pickle file of extracted features

한국어 안내 (README in Korean) 👉   

## Environment
- Linux
- python 3.8

## Quick Start 

1. Set up OpenSmile toolkit for your server 
  - [Download link](https://github.com/audeering/opensmile/releases)
  - OpenSmile documents : https://audeering.github.io/opensmile/  

2. Clone this repo at your server  
`git clone https://github.com/jade0520/Feature_Extraction_OpenSmile.git`

3. Excute below 
  `bash run.sh`

## Sturcture
1. feature --> csv  
  - extract_wavs

2. csv --> pickle
  - csvs_to_pickle_all : save all data as one pickle 
  - csvs_to_N_fold_pickles_labels : divede labels for cross fold validation (1/5/10 folds & independent/dependent)
  - csvs_to_N_fold_pickle : save feature csvs as array pickles based on devided label folds


## Contact
📫 seo.jiyoung@dsp.inha.ac.kr  
Any comments or opinions are welcome;) 
