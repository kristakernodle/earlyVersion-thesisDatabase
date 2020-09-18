import thesis_database_pkg.get as get
import blind_review.utilities as util
from thesis_database_pkg import BlindTrial, BlindFolder, Trial
import shutil
from shutil import Error
from pathlib import Path


def mask_trial(trial, masked_trial_dir):
    BlindTrial(trial.trial_id, trial.folder_id, masked_trial_dir).save_to_db()
    try:
        shutil.copy(trial.trial_dir, masked_trial_dir)
        return True
    except Error as err:
        print(err.args[0])
        return False


def mask_folder(reviewer, folder):
    # Try to load the masked_folder
    masked_folder = BlindFolder.from_db(reviewer_id=reviewer.reviewer_id, folder_id=folder.folder_id)

    if masked_folder is None:
        # Generate a unique blind name
        blind_name = util.random_string_generator(10)
        while blind_name in get.list_all_blind_names():
            blind_name = util.random_string_generator(10)
        masked_folder = BlindFolder(folder.folder_id, reviewer.reviewer_id, blind_name).save_to_db()

    masked_folder_dir = Path(reviewer.toScore_dir).joinpath(masked_folder.blind_name)

    for idx, trial_id in enumerate(set(get.list_trial_ids_for_folder(folder))):
        trial_num = str(idx + 1)
        if len(trial_num) < 2:
            trial_num = f'0{trial_num}'
        trial = Trial.from_db(trial_id=trial_id)
        masked_trial_dir = masked_folder_dir.joinpath(f'{masked_folder.blind_name}_{trial_num}.mp4')
        success = mask_trial(trial, masked_trial_dir)
        if not success:
            print("Issues copying")
            break
