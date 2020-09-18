from pathlib import Path
import csv

from archive.models import Folder
from archive.models import Reviewer
from archive.models import BlindFolder
from archive.models import Trial
from archive.models import BlindTrial
from archive.database import Database
from archive.data.constants import dbDetails, dbUser_Krista

Database.initialize(**dbDetails, **dbUser_Krista)
scrambled_mask_keys_file = Path('/Users/Krista/Desktop/master_file_keys_scrambled.csv')
with open(scrambled_mask_keys_file) as f:
    scrambled_mask_keys = list(csv.reader(f))

for (LED_detection_output_csv, reviewer_fullname, blind_name) in scrambled_mask_keys:
    csv_num = LED_detection_output_csv.split('_')[-1]
    csv_num = csv_num.strip('.csv')
    folder_dir = Path(LED_detection_output_csv).parent.joinpath(f'Reaches{csv_num}')
    folder = Folder.from_db(str(folder_dir))
    reviewer = Reviewer.from_db(reviewer_fullname)
    blind_folder = BlindFolder(folder.folder_id, reviewer.reviewer_id, blind_name).save_to_db()
    all_trial_dirs_for_folder = Trial.list_trial_dir_for_folder(folder.folder_id)
    count = 0
    for trial_dir in all_trial_dirs_for_folder:
        count += 1
        if len(str(count)) < 2:
            blind_trial_num = f'0{count}'
        else:
            blind_trial_num = str(count)
        blind_trial_full_path = Path(reviewer.toScore_dir).joinpath(
            f'{blind_folder.blind_name}/{blind_folder.blind_name}_R{blind_trial_num}.mp4')
        trial = Trial.from_db(trial_dir)
        blind_trial = BlindTrial(trial.trial_id, folder.folder_id, str(blind_trial_full_path)).save_to_db()

all_mask_keys_file = Path('/Users/Krista/Desktop/blindScoring/.mask_keys/master_file_keys.csv')
with open(all_mask_keys_file) as f:
    all_mask_keys = list(csv.reader(f))

not_scrambled_mask_keys = list()
for mask_key in all_mask_keys:
    if mask_key in scrambled_mask_keys:
        continue
    not_scrambled_mask_keys.append(mask_key)

for (LED_detection_output_csv, reviewer_fullname, blind_name) in not_scrambled_mask_keys:
    csv_num = LED_detection_output_csv.split('_')[-1]
    csv_num = csv_num.strip('.csv')
    folder_dir = Path(LED_detection_output_csv).parent.joinpath(f'Reaches{csv_num}')
    folder = Folder.from_db(str(folder_dir))
    reviewer = Reviewer.from_db(reviewer_fullname)
    blind_folder = BlindFolder(folder.folder_id, reviewer.reviewer_id, blind_name).save_to_db()
    all_trial_dirs_for_folder = Trial.list_trial_dir_for_folder(folder.folder_id)
    count = 0
    for trial_dir in sorted(all_trial_dirs_for_folder):
        count += 1
        if len(str(count)) < 2:
            blind_trial_num = f'0{count}'
        else:
            blind_trial_num = str(count)
        blind_trial_full_path = Path(reviewer.toScore_dir).joinpath(
            f'{blind_folder.blind_name}/{blind_folder.blind_name}_R{blind_trial_num}.mp4')
        trial = Trial.from_db(trial_dir)
        blind_trial = BlindTrial(trial.trial_id, folder.folder_id, str(blind_trial_full_path)).save_to_db()
