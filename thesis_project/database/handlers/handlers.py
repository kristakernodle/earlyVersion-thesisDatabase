import random

import database.create_database
import database.seed_tables.seed_tables
import utilities as utils
from database.create_database import create_tables as create_tr
from database.cursors import TestingCursor
import database.handlers.handlers
import database.create_database.create_tables
import database.create_database.create_views
from database.seed_tables.seeds import test_blind_review_reviewers_seed as seed_reviewers, \
    test_mouse_table_seed as mouse_seed, test_trial_table_seed as trial_seed
from models.experiments import Experiments
from models.mouse import list_all_mice, Mouse
from models.reviewer import Reviewer
from models.trials import Trials
from utilities import random_string_generator


def handler_create_reviewers_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_reviewers_table(cursor)


def handler_seed_reviewers(postgresql):
    for reviewer in seed_reviewers:
        with TestingCursor(postgresql) as cursor:
            database.seed_tables.seed_tables.seed_reviewers_table(cursor, reviewer[0], reviewer[1], reviewer[2],
                                                                  reviewer[3])


def handler_create_blind_trials_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_mouse_table(cursor)
        database.create_database.create_tables.create_experiments_table(cursor)
        create_tr.create_trials_table(cursor)
        create_tr.create_view_all_participants_all_trials(cursor)
        database.create_database.create_tables.create_reviewers_table(cursor)
        database.create_database.create_tables.create_blind_trials_table(cursor)


def handler_seed_blind_trials(postgresql):
    all_blind_names = []
    handler_seed_trials(postgresql)
    handler_seed_reviewers(postgresql)

    with TestingCursor(postgresql) as cursor:
        cursor.execute("SELECT * FROM trials WHERE random() <= 0.5 ORDER BY random() LIMIT 10;")
        test_trials = cursor.fetchall()

        for trial in test_trials:
            blind_name = random_string_generator(10)
            current_trial = Trials.from_db(trial[-2], testing=True, postgresql=postgresql)
            current_reviewer = random.choice(seed_reviewers)
            current_reviewer = Reviewer.from_db(current_reviewer[-1], testing=True, postgresql=postgresql)
            database.seed_tables.seed_tables.seed_blind_trials(cursor, current_trial.trial_id,
                                                               current_reviewer.reviewer_id, blind_name)
            all_blind_names.append(tuple([current_trial.trial_id, current_reviewer.reviewer_id, blind_name]))
    return all_blind_names


def handler_create_mouse_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_mouse_table(cursor)


def handler_create_experiments_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_experiments_table(cursor)


def handler_create_all_independent_tables(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_mouse_table(cursor)
        database.create_database.create_tables.create_experiments_table(cursor)


def handler_seed_mouse(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.seed_tables.seed_tables.seed_mouse_table(cursor)


def handler_seed_experiments(postgresql):
    with TestingCursor(postgresql) as cursor:
        database.seed_tables.seed_tables.seed_experiments_table(cursor)


def handler_seed_mouse_experiments(postgresql):
    with TestingCursor(postgresql) as cursor:
        database.seed_tables.seed_tables.seed_mouse_table(cursor)
        database.seed_tables.seed_tables.seed_experiments_table(cursor)


def handler_create_participant_details(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_mouse_table(cursor)
        database.create_database.create_tables.create_experiments_table(cursor)
        database.create_database.create_tables.create_participant_details_table(cursor)
        database.create_database.create_views.create_view_all_participants_all_experiments(cursor)


def handler_seed_participant_details(postgresql):
    with TestingCursor(postgresql) as cursor:
        database.seed_tables.seed_tables.seed_mouse_table(cursor)
        database.seed_tables.seed_tables.seed_experiments_table(cursor)

    with TestingCursor(postgresql) as cursor:
        all_mice = list_all_mice(cursor)
        for eartag in all_mice:
            mouse = Mouse.from_db(eartag, testing=True, postgresql=postgresql)
            for m in mouse_seed:
                if m[0] == mouse.eartag:
                    experiment = Experiments.from_db(m[5], testing=True, postgresql=postgresql)
                    database.seed_tables.seed_tables.seed_participant_details(cursor, mouse.mouse_id,
                                                                              experiment.experiment_id,
                                                                              start_date=m[6], end_date=m[7])


def handler_create_trials_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_mouse_table(cursor)
        database.create_database.create_tables.create_experiments_table(cursor)
        create_tr.create_trials_table(cursor)
        create_tr.create_view_all_participants_all_trials(cursor)


def handler_seed_trials(postgresql):
    with TestingCursor(postgresql) as cursor:
        database.seed_tables.seed_tables.seed_mouse_table(cursor)
        database.seed_tables.seed_tables.seed_experiments_table(cursor)

    with TestingCursor(postgresql) as cursor:
        all_mice = list_all_mice(cursor)
        for eartag in all_mice:
            mouse = Mouse.from_db(eartag, testing=True, postgresql=postgresql)
            for m in mouse_seed:
                if m[0] == mouse.eartag:
                    experiment = Experiments.from_db(m[5], testing=True, postgresql=postgresql)
                    seed_mouse_all_trials = trial_seed[(mouse.eartag, experiment.experiment_name)]
                    for trial in seed_mouse_all_trials:
                        trial_date, trial_dir = trial
                        database.seed_tables.seed_tables.seed_trials(cursor, mouse.mouse_id, experiment.experiment_id,
                                                                     utils.convert_date_int_yyyymmdd(trial_date),
                                                                     trial_dir)
