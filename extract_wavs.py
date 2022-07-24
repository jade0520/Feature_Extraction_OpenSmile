import os
import argparse

parser = argparse.ArgumentParser(description='extract features(csv) of wavs') 
parser.add_argument('--csvs_dir', type=str, help='<Required> Set path to save extracted csv files', default = './csvs/', required=True)  
parser.add_argument('--IEMOCAP_dir', type=str, help='<Required> Set path to "/IEMOCAP_full_release/"', default = './IEMOCAP_full_release/', required=True) 
parser.add_argument('--OS_path', type=str, help='<Required> Set path to opensmile folder', default = './opensmile/', required=True) 
parser.add_argument('--conf_names','--list', default = ['spectrum/STFT_025_01'] , nargs='+', type=str, help='<Required> Set coniguration list * Must be defined in the "opensmile/config/" directory', required=True) 
args = parser.parse_args() 

IEMOCAP_sessions = ['Session1', 'Session2', 'Session3', 'Session4','Session5']

def get_wav_path(IEMOCAP_dir, file_name) : 
    # return wav path from filename 
    sess = "Session"+ file_name[4]
    idx = file_name.rfind('_')
    id_folder = file_name[:idx]
    
    return  IEMOCAP_dir +sess +'/sentences/wav/' +id_folder +'/' + file_name +'.wav'

for session in IEMOCAP_sessions:
    # Get data per session

    path_to_idfolder = args.IEMOCAP_dir + session + '/sentences/wav/'
    idfolders = os.listdir(path_to_idfolder) # Get id list in a session
    file_names = [] # For all data in a session

    for idfolder in idfolders:
        # Collect all file names in a session
        path_to_wavs = path_to_idfolder + idfolder
        wav_files_list = os.listdir(path_to_wavs)
        for file_name in wav_files_list:
            # get
            if file_name.endswith(".wav"):
                if file_name[0] == '.':
                    file_names.append(file_name[2:-4])
                else:
                    file_names.append(file_name[:-4])

    for file_name in file_names:   
        # extract features for all files
        
        audio_file_path = get_wav_path(args.IEMOCAP_dir, file_name) # set file name to extract

        
        for conf_name in args.conf_names :
            # extact all features from a audio file
            os.system(args.OS_path + "build/progsrc/smilextract/SMILExtract -C " + args.OS_path + "config/" + conf_name +".conf -I " + audio_file_path + " -csvoutput "+ args.csvs_dir + conf_name.split('/')[-1] + "_" + file_name +".csv")