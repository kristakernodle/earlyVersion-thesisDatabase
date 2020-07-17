import csv
import os
from pathlib import Path

from data.constants import dbDetails, dbUser_Krista
from database.database import Database
from models.mouse import Mouse
from models.experiments import Experiment
from models.participant_details import ParticipantDetails

from templates.experiment_specific_details import skilled_reaching


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
for participant_detail in all_participant_details:
    detail_id = participant_detail[0]
    mouse_id = participant_detail[1]
    experiment_id = participant_detail[2]
    start_date = participant_detail[3]
    end_date = participant_detail[4]
    particpant_dir = participant_detail[-1]
    exp_spec_details = ''.join(participant_detail[5:-1])
    paw_preference = None
    reaching_box = None
    if 'right' in exp_spec_details:
        paw_preference = 'right'
    elif 'left' in exp_spec_details:
        paw_preference = 'left'
    if '1' in exp_spec_details:
        reaching_box = 1
    elif '2' in exp_spec_details:
        reaching_box = 2
    if paw_preference is None or reaching_box is None:
        print('Something decoded incorrectly')
        print(f'paw preference: {paw_preference}')
        print(f'reaching box: {reaching_box}')
        print(f'exp_spec_details: {exp_spec_details}')
    mouse = Mouse.from_db_by_id(mouse_id)
    experiment = Experiment.from_db_by_id(experiment_id)
    exp_spec_details = skilled_reaching
    exp_spec_details["paw preference"] = paw_preference
    exp_spec_details["reaching box"] = reaching_box
    ParticipantDetails(mouse, experiment, particpant_dir, start_date, end_date,
                       exp_spec_details, detail_id).save_to_db()
