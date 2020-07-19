from pathlib import Path
import csv

from models.folders import Folder
from models.reviewers import Reviewer
from models.blind_folders import BlindFolder
import models.trials

scrambled_mask_keys_file = Path('/Users/Krista/Desktop/master_file_keys_scrambled.csv')
with open(scrambled_mask_keys_file) as f:
    scrambled_mask_keys = list(csv.reader(f))

for (LED_detection_output_csv, reviewer_fullname, blind_name) in scrambled_mask_keys:
    csv_num = LED_detection_output_csv.split('_')[-1]
    csv_num = csv_num.strip('.csv')
    folder_dir = Path(LED_detection_output_csv).parent.joinpath(f'Reaches{csv_num}')
    folder = Folder.from_db(str(folder_dir))
    reviewer = Reviewer.from_db(reviewer_fullname)
    print(BlindFolder(folder.folder_id, reviewer.reviewer_id, blind_name))
    all_trials = models.trials.list_trials_for_folder(folder.folder_id)
