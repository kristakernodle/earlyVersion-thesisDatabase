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
from database.cursors import Cursor

Database.initialize(**dbDetails, **dbUser_Krista)

experiment_name = 'skilled-reaching'
reviewer_name = 'Krista K'

sr_exp = Experiment.from_db(experiment_name)
reviewer = Reviewer.from_db(reviewer_fullname=reviewer_name)
folders_in_toScore = Path(reviewer.toScore_dir).glob('*')
folders_in_scored = Path(reviewer.scored_dir).glob('*_KK.csv')

existing_folder_blind_names = list()
for folder in folders_in_toScore:
    existing_folder_blind_names.append(folder.name.split('_')[0])

all_blind_folders_no_original_file = list()
for blind_name in existing_folder_blind_names:
    print(blind_name)
    blind_folder = BlindFolder.from_db(blind_name=blind_name)
    if blind_folder is None:
        if blind_name == '.DS' or blind_name == '.DS_Store':
            continue
        else:
            all_blind_folders_no_original_file.append(blind_name)
    trials_for_folder = Trial.list_trials_for_folder(blind_folder.folder_id)
    count = 0
    for trial in trials_for_folder:
        count += 1
        blind_trial = BlindTrial.from_db(reviewer_id=reviewer.reviewer_id, trial_id=trial.trial_id)
        if blind_trial is None:
            if len(str(count)) < 2:
                blind_trial_num = f'0{count}'
            else:
                blind_trial_num = str(count)
            full_path = Path(reviewer.toScore_dir).joinpath(blind_name, f'{blind_name}_R{blind_trial_num}.mp4')
            if Path(trial.trial_dir).exists():
                try:
                    shutil.copyfile(trial.trial_dir, str(full_path))
                    BlindTrial(trial.trial_id, blind_folder.folder_id, str(full_path)).save_to_db()
                except:
                    print(f'ISSUE {blind_folder} {trial} {full_path}')
            else:
                print('SharedX drive disconnected')
                break
        elif Path(blind_trial.full_path).exists:
            continue
        elif not Path(blind_trial.full_path).exists:
            shutil.copyfile(trial.trial_dir, blind_trial.full_path)
