from models.trials import Trials
from models.reviewer import Reviewer
from blind_review.blinded.common import auxiliary_functions as af

from database.cursors import TestingCursor
import database.create_tables.create_independent_tables as create_id
import database.create_tables.create_trials as create_tr
import database.create_tables.create_blind_review_tables as create_br

import database.seed_tables.seed_trials_table as seed_tr
import database.seed_tables.seed_blind_review as seed_br
from database.seed_tables.seeds import test_blind_review_reviewers_seed as seed_reviewers


def handler_create_reviewers_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_br.create_reviewers_table(cursor)


def handler_seed_reviewers(postgresql):
    for reviewer in seed_reviewers:
        with TestingCursor(postgresql) as cursor:
            seed_br.seed_reviewers_table(cursor, reviewer[0], reviewer[1], reviewer[2], reviewer[3])


def handler_create_blind_trials_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_id.create_mouse_table(cursor)
        create_id.create_experiments_table(cursor)
        create_tr.create_trials_table(cursor)
        create_tr.create_view_all_participants_all_trials(cursor)
        create_br.create_reviewers_table(cursor)
        create_br.create_blind_trials_table(cursor)


def handler_seed_blind_trials(postgresql):
    seed_tr.seed_trials(postgresql)
    handler_seed_reviewers(postgresql)

    with TestingCursor(postgresql) as cursor:
        cursor.execute("SELECT * FROM trials WHERE random() <= 0.5 ORDER BY random() LIMIT 10;")
        test_trials = cursor.fetchall()

        for trial in test_trials:
            current_trial = Trials.from_db(trial[-2], testing=True, postgresql=postgresql)
            current_reviewer = test_reviewers.pop()
            current_reviewer = Reviewer.from_db(current_reviewer[-1], testing=True, postgresql=postgresql)
            seed_br.seed_blind_trials(cursor, current_trial.trial_id, current_reviewer.reviewer_id,
                                      af.random_string_generator(10))
