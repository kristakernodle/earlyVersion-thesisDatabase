import csv
import os
from pathlib import Path

from data.constants import dbDetails, dbUser_Krista
from database.database import Database
from models.mouse import Mouse
from models.experiments import Experiment
from models.participant_details import ParticipantDetails


def read_table_csv_to_list(backup_folder_path, table_name):
    table_filename = table_name + '.csv'
    table_dir = os.path.join(backup_folder_path, table_filename)
    with open(table_dir) as f:
        contents = list(csv.reader(f))
    return contents


Database.initialize(**dbDetails, **dbUser_Krista)

project_base_dir = Path(__file__).parent.parent.parent
backup_csv_path = os.path.join(project_base_dir, 'data', 'database_backup_csv')

tables_to_populate = ['mouse', 'experiments', 'participant_details']

# MOUSE TABLE
all_mouses = read_table_csv_to_list(backup_csv_path, 'mouse')
for [mouse_id, eartag, birthdate, genotype, sex] in all_mouses:
    Mouse(eartag, birthdate, genotype, sex, mouse_id).save_to_db()

# EXPERIMENTS TABLE
all_experiments = read_table_csv_to_list(backup_csv_path, 'experiments')
for [experiment_id, experiment_dir, experiment_name] in all_experiments:
    Experiment(experiment_name, experiment_dir, experiment_id).save_to_db()

# PARTICIPANT DETAILS TABLE
all_participant_details = read_table_csv_to_list(backup_csv_path, 'participant_details')
