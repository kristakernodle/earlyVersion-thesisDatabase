from archive.data.constants import sharedx_prefix
from pathlib import Path

from archive.models import Mouse
from archive.models import ParticipantDetails
from archive.models import Session
from archive.models import Folder
from archive.models import Trial


def update_from_data_dirs(experiment):
    if not Path(sharedx_prefix).exists():
        print(f'Path {sharedx_prefix} does not exist. Make sure remote drive is connected.')

    all_participant_dirs = list(Path(experiment.experiment_dir).glob('et*/'))

    for participant_dir in all_participant_dirs:

        eartag_num = int(participant_dir.name.strip('et'))
        mouse = Mouse.from_db(eartag_num)

        if mouse is None:
            continue

        mouse_details = ParticipantDetails.from_db(eartag_num, experiment.experiment_name)

        if mouse_details is None:
            continue

        if experiment.experiment_name == 'skilled-reaching':
            training_dir = Path(mouse_details.participant_dir).joinpath('Training')
            all_session_dirs = training_dir.glob(f'et{eartag_num}_*_*T*/')
        elif experiment.experiment_name == 'grooming':
            training_dir = Path(mouse_details.participant_dir)
            all_session_dirs = training_dir.glob(f'et{eartag_num}_*_*G*/')
        else:
            print('Need information about training and session directories for this the_experiment')

        for session_dir in all_session_dirs:
            session_date = int(session_dir.name.split('_')[1])
            session = Session(mouse.mouse_id, experiment.experiment_id, str(session_dir), session_date).save_to_db()

            if experiment.experiment_name == 'skilled-reaching':
                all_folder_dirs = session_dir.glob('Reaches*')
            elif experiment.experiment_name == 'grooming':
                continue
            else:
                print('Need information about folder and trial directories for this the_experiment')

            for folder_dir in all_folder_dirs:
                folder = Folder(session.session_id, str(folder_dir)).save_to_db()
                all_trial_dirs = folder_dir.glob('*R*.mp4')

                if len(list(all_trial_dirs)) == 0:
                    all_trial_dirs = folder_dir.glob('*R*.MP4')

                for trial_dir in all_trial_dirs:
                    Trial(experiment.experiment_id,
                          folder.folder_id,
                          str(trial_dir),
                          session.session_date).save_to_db()