from database.database import Database
from data.constants import dbDetails, dbUser_Krista

import utilities as utils
from models.experiments import Experiment
from models.folders import Folder
from models.blind_folders import BlindFolder
from models.reviewers import Reviewer

Database.initialize(**dbDetails, **dbUser_Krista)

experiment_name = 'skilled-reaching'
reviewer_name = 'Krista K'
num_folders_to_mask = 1

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
for folders_to_mask in all_not_blind_folders:
    all_blind_names = BlindFolder.list_all_blind_names()
    blind_name = utils.random_string_generator(10)
    while blind_name in all_blind_names:
        blind_name = utils.random_string_generator(10)
        BlindFolder(folder.folder_id, reviewer.reviewer_id, blind_name)  # .save_to_db()
