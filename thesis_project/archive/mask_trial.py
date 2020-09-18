import os

from archive.models import BlindTrial


def mask_session(session_date, reviewer_obj):
    success = False
    masked_trial = BlindTrial(trial_obj.trial_id, reviewer_obj.reviewer_id)

    masked_trial_dir = os.path.join(reviewer_obj.toScore_dir, masked_trial.blind_name)
    os.mkdir(masked_trial_dir)

    return [success, masked_trial]
