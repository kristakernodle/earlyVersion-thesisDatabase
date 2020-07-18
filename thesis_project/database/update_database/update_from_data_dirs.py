from data.constants import sharedx_prefix
from pathlib import Path
from models.participant_details import ParticipantDetails


def update_from_data_dirs(experiment):
    if not Path(sharedx_prefix).exists():
        print(f'Path {sharedx_prefix} does not exist. Make sure remote drive is connected.')
        return False

    all_participant_dirs = list(Path(experiment.experiment_dir).glob('et*/'))
    # in_db = ParticipantDetails.list_participants(experiment.experiment_name)

    for participant_dir in all_participant_dirs:
        eartag_num = participant_dir.name.strip('et')
        print(eartag_num)
