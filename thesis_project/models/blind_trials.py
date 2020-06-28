from blind_review.blinded.common.auxiliary_functions import random_string_generator


class BlindTrial:

    def __init__(self, trial_id, reviewer_id, blind_name=random_string_generator(10), blind_trial_id=None):
        self.trial_id = trial_id
        self.reviewer_id = reviewer_id
        self.blind_name = blind_name
        self.blind_trial_id = blind_trial_id
