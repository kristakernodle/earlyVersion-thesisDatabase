import os
from pathlib import Path

from data.constants import dbDetails, dbUser_Krista
from database.database import Database
from models.mouse import Mouse
from models.experiments import Experiment
from models.participant_details import ParticipantDetails

from templates.experiment_specific_details import skilled_reaching
from utilities import read_table_csv_to_list

Database.initialize(**dbDetails, **dbUser_Krista)

project_base_dir = Path(__file__).parent.parent.parent
backup_csv_path = os.path.join(project_base_dir, 'data', 'database_backup_csv')

tables_to_populate = ['mouse', 'experiments', 'participant_details']

# MOUSE TABLE
all_mouses = read_table_csv_to_list(backup_csv_path, 'mouse')
for [mouse_id, eartag, birthdate, genotype, sex] in all_mouses:
    eartag = int(eartag)
    birthdate = ''.join(birthdate.split('-'))
    Mouse(eartag, int(birthdate), genotype, sex).save_to_db()

# EXPERIMENTS TABLE
all_experiments = read_table_csv_to_list(backup_csv_path, 'experiments')
for [experiment_id, experiment_dir, experiment_name] in all_experiments:
    Experiment(experiment_name, experiment_dir).save_to_db()

# PARTICIPANT DETAILS TABLE
all_participant_details = read_table_csv_to_list(backup_csv_path, 'participant_details')
for participant_detail in all_participant_details:
    detail_id = participant_detail[0]
    mouse_id = participant_detail[1]
    experiment_id = participant_detail[2]
    start_date = participant_detail[3]
    start_date = int(''.join(start_date.split('-')))
    end_date = participant_detail[4]
    end_date = int(''.join(end_date.split('-')))
    participant_dir = participant_detail[-1]
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
    for item in all_mouses:
        if mouse_id in item:
            mouse = Mouse.from_db(int(item[1]))
            break
    for item in all_experiments:
        if experiment_id in item:
            experiment = Experiment.from_db(item[-1])
            break
    exp_spec_details = skilled_reaching
    exp_spec_details["paw preference"] = paw_preference
    exp_spec_details["reaching box"] = reaching_box
    ParticipantDetails(mouse=mouse, experiment=experiment, participant_dir=participant_dir, start_date=start_date,
                       end_date=end_date, exp_spec_details=exp_spec_details).save_to_db()
