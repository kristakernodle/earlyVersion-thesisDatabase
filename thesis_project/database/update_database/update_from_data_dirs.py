from data.constants import sharedx_prefix
from pathlib import Path

from models.mouse import Mouse
from models.participant_details import ParticipantDetails
from models.sessions import Session
from models.folders import Folder
from models.trials import Trial


def update_from_data_dirs(experiment):
    if not Path(sharedx_prefix).exists():
        print(f'Path {sharedx_prefix} does not exist. Make sure remote drive is connected.')
        return False

    all_participant_dirs = list(Path(experiment.experiment_dir).glob('et*/'))

    for participant_dir in all_participant_dirs:

        eartag_num = int(participant_dir.name.strip('et'))
        mouse = Mouse.from_db(eartag_num)

        if mouse is None:
            continue
        if eartag_num == 713:
            print('713')
        mouse_details = ParticipantDetails.from_db(eartag_num, experiment.experiment_name)

        if mouse_details is None:
            continue

        training_dir = Path(mouse_details.participant_dir).joinpath('Training')
        all_session_dirs = training_dir.glob(f'et{eartag_num}_*_*T*/')
        for session_dir in all_session_dirs:
            session_date = int(session_dir.name.split('_')[1])
            session = Session(mouse.mouse_id, experiment.experiment_id, str(session_dir), session_date).save_to_db()
            all_folder_dirs = session_dir.glob('Reaches*')
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
