from database.database import Database
from data.constants import dbDetails, dbUser_Krista

from models.experiments import Experiment
from models.folders import Folder

Database.initialize(**dbDetails, **dbUser_Krista)

experiment_name = 'skilled-reaching'
reviewer_name = 'Krista K'
num_folders_to_mask = 1

sr_exp = Experiment.from_db(experiment_name)
all_folders = Folder.list_all_folders(sr_exp.experiment_id)

all_blind_folders = models.blind_folders.list_all_blind_folders(sr_exp.experiment_id)
