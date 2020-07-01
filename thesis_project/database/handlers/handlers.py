import random

import database.create_database.create_tables
import database.create_database.create_views
from database.cursors import TestingCursor
import database.seed_tables.seed_tables
from database.seed_tables.seeds import test_mouse_table_seed as seed_mouse, \
    exp_one, exp_two, test_blind_review_reviewers_seed as seed_reviewers, \
    test_mouse_table_seed as mouse_seed, test_trial_table_seed as trial_seed

import utilities as utils
from models.experiments import Experiments
from models.mouse import list_all_mice, Mouse
from models.reviewers import Reviewer
from models.trials import Trials


# MOUSE TABLE
def handler_create_mouse_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_mouse_table(cursor)


def handler_seed_mouse(postgresql):
    for mouse in seed_mouse:
        genotype = utils.encode_genotype(mouse[2])
        sex = utils.prep_string_for_db(mouse[3])
        with TestingCursor(postgresql) as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
            database.seed_tables.seed_tables.seed_mouse_table(cursor, mouse[0], mouse[1], genotype, sex)


# EXPERIMENTS TABLE
def handler_create_experiments_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_experiments_table(cursor)


def handler_seed_experiments(postgresql):
    prepped_exp_one = (utils.prep_string_for_db(exp_one[0]), exp_one[1])
    prepped_exp_two = (utils.prep_string_for_db(exp_two[0]), exp_two[1])
    with TestingCursor(postgresql) as cursor:
        database.seed_tables.seed_tables.seed_experiments_table(cursor, prepped_exp_one, prepped_exp_two)


# PARTICIPANT DETAILS TABLE
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


# REVIEWER TABLE
def handler_create_reviewers_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_reviewers_table(cursor)


def handler_seed_reviewers(postgresql):
    for reviewer in seed_reviewers:
        with TestingCursor(postgresql) as cursor:
            database.seed_tables.seed_tables.seed_reviewers_table(cursor, reviewer[0], reviewer[1], reviewer[2],
                                                                  reviewer[3])


# SESSIONS TABLE
def handler_create_sessions_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_mouse_table(cursor)
        database.create_database.create_tables.create_experiments_table(cursor)
        database.create_database.create_tables.create_sessions_table(cursor)


def handler_seed_sessions_table(postgresql):
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
                    seed_mouse_all_sessions = trial_seed[(mouse.eartag, experiment.experiment_name)]
                    for session in seed_mouse_all_sessions:
                        session_date, session_dir = session
                        database.seed_tables.seed_tables.seed_sessions_table(cursor, mouse.mouse_id,
                                                                             experiment.experiment_id,
                                                                             utils.convert_date_int_yyyymmdd(
                                                                                 session_date),
                                                                             session_dir)


# TRIALS TABLE
def handler_create_trials_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_mouse_table(cursor)
        database.create_database.create_tables.create_experiments_table(cursor)
        database.create_database.create_tables.create_trials_table(cursor)
        database.create_database.create_views.create_view_all_participants_all_trials(cursor)


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
                        database.seed_tables.seed_tables.seed_trials_table(cursor, mouse.mouse_id,
                                                                           experiment.experiment_id,
                                                                           utils.convert_date_int_yyyymmdd(trial_date),
                                                                           trial_dir)


# BLIND TRIALS TABLE
def handler_create_blind_trials_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        database.create_database.create_tables.create_mouse_table(cursor)
        database.create_database.create_tables.create_experiments_table(cursor)
        database.create_database.create_tables.create_trials_table(cursor)
        database.create_database.create_views.create_view_all_participants_all_trials(cursor)
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
            blind_name = utils.random_string_generator(10)
            current_trial = Trials.from_db(trial[-2], testing=True, postgresql=postgresql)
            current_reviewer = random.choice(seed_reviewers)
            current_reviewer = Reviewer.from_db(current_reviewer[-1], testing=True, postgresql=postgresql)
            database.seed_tables.seed_tables.seed_blind_trials_table(cursor, current_trial.trial_id,
                                                                     current_reviewer.reviewer_id, blind_name)
            all_blind_names.append(tuple([current_trial.trial_id, current_reviewer.reviewer_id, blind_name]))
    return all_blind_names
