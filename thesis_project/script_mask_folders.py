from database.database import Database
from data.constants import dbDetails, dbUser_Krista
from pathlib import Path
import utilities as utils
from models.experiments import Experiment
from models.folders import Folder
from models.blind_folders import BlindFolder
from models.reviewers import Reviewer
from models.trials import Trial
from models.blind_trials import BlindTrial
import shutil
import os

Database.initialize(**dbDetails, **dbUser_Krista)

experiment_name = 'skilled-reaching'
reviewer_name = 'Krista K'
num_folders_to_mask = 37

sr_exp = Experiment.from_db(experiment_name)
all_folders = Folder.list_all_folders(sr_exp.experiment_id)
all_blind_folders = BlindFolder.list_all_blind_folders(sr_exp.experiment_id)

all_not_blind_folders = list()
for folder in all_folders:
    for blind_folder in all_blind_folders:
        if folder.folder_id == blind_folder.folder_id:
            break
    if folder.folder_id == blind_folder.folder_id:
        continue
    all_not_blind_folders.append(folder)

folders_to_mask = list()
for ii in range(num_folders_to_mask):
    folders_to_mask.append(all_not_blind_folders.pop())

reviewer = Reviewer.from_db(reviewer_fullname=reviewer_name)
for index, folder in enumerate(folders_to_mask):
    all_blind_names = BlindFolder.list_all_blind_names()
    blind_name = utils.random_string_generator(10)
    while blind_name in all_blind_names:
        blind_name = utils.random_string_generator(10)
    BlindFolder(folder.folder_id, reviewer.reviewer_id, blind_name).save_to_db()
    blind_folder_dir = Path(reviewer.toScore_dir).joinpath(blind_name)
    os.mkdir(blind_folder_dir)
    all_trials = Trial.list_trials_for_folder(folder.folder_id)
    print(f'{index}: {blind_name} - {len(all_trials)}')
    count = 0
    for trial in all_trials:
        count += 1
        if len(str(count)) < 2:
            blind_trial_num = f'0{count}'
        else:
            blind_trial_num = str(count)
        full_path = Path(reviewer.toScore_dir).joinpath(blind_name, f'{blind_name}_R{blind_trial_num}.mp4')
        try:
            shutil.copyfile(trial.trial_dir, str(full_path))
            BlindTrial(trial.trial_id, folder.folder_id, str(full_path)).save_to_db()
        except:
            print(f'ISSUE {folder} {trial} {full_path}')
