import random

from archive import database, models, utilities as utils
import archive.database.create_database.create_views
from archive.database import TestingCursor
import archive.database.seed_tables.seed_tables
from archive.database import test_mouse_table_seed as seed_mouse, \
    exp_one, exp_two, test_blind_review_reviewers_seed as seed_reviewers, \
    test_mouse_table_seed as mouse_seed, test_session_table_seed as session_seed

from archive.models import Experiment
from archive.models import list_all_mice, Mouse
from archive.models import Reviewer
from archive.models import Folder
from archive.models import BlindFolder
from archive.models import Session
from archive.models import Trial


# MOUSE TABLE
def handler_create_mouse_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        archive.database.create_database.create_tables.create_mouse_table(cursor)


def handler_seed_mouse(postgresql):
    for [eartag, birthdate, genotype, sex, _, _, _, _] in seed_mouse:
        genotype = utils.encode_genotype(genotype)
        sex = utils.prep_string_for_db(sex)
        with TestingCursor(postgresql) as cursor:
            archive.database.seed_tables.seed_tables.seed_mouse_table(cursor, eartag, birthdate, genotype, sex)


# EXPERIMENTS TABLE
def handler_create_experiments_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        archive.database.create_database.create_tables.create_experiments_table(cursor)


def handler_seed_experiments(postgresql):
    prepped_exp_one = (utils.prep_string_for_db(exp_one[0]), exp_one[1])
    prepped_exp_two = (utils.prep_string_for_db(exp_two[0]), exp_two[1])
    with TestingCursor(postgresql) as cursor:
        archive.database.seed_tables.seed_tables.seed_experiments_table(cursor, prepped_exp_one, prepped_exp_two)


# PARTICIPANT DETAILS TABLE
def handler_create_participant_details(postgresql):
    handler_create_mouse_table(postgresql)
    handler_create_experiments_table(postgresql)
    with TestingCursor(postgresql) as cursor:
        archive.database.create_database.create_tables.create_participant_details_table(cursor)
        archive.database.create_database.create_views.create_view_all_participants_all_experiments(cursor)


def handler_seed_participant_details(postgresql):
    handler_seed_mouse(postgresql)
    handler_seed_experiments(postgresql)

    with TestingCursor(postgresql) as cursor:
        all_mice = list_all_mice(cursor)
        for eartag in all_mice:
            mouse = Mouse.from_db(eartag, testing=True, postgresql=postgresql)
            for m in mouse_seed:
                if m[0] == mouse.eartag:
                    experiment = Experiment.from_db(m[5], testing=True, postgresql=postgresql)
                    archive.database.seed_tables.seed_tables.seed_participant_details(cursor,
                                                                                      mouse.mouse_id,
                                                                                      experiment.experiment_id,
                                                                                      start_date=m[6],
                                                                                      end_date=m[7])


# REVIEWERS TABLE
def handler_create_reviewers_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        archive.database.create_database.create_tables.create_reviewers_table(cursor)


def handler_seed_reviewers_table(postgresql):
    for [first_name, last_name, toScore, scored] in seed_reviewers:
        with TestingCursor(postgresql) as cursor:
            archive.database.seed_tables.seed_tables.seed_reviewers_table(cursor, first_name, last_name, toScore,
                                                                          scored)


# SESSIONS TABLE
def handler_create_sessions_table(postgresql):
    handler_create_mouse_table(postgresql)
    handler_create_experiments_table(postgresql)
    with TestingCursor(postgresql) as cursor:
        archive.database.create_database.create_tables.create_sessions_table(cursor)


def handler_seed_sessions_table(postgresql):
    handler_seed_mouse(postgresql)
    handler_seed_experiments(postgresql)
    with TestingCursor(postgresql) as cursor:
        for [mouse_eartag, experiment_name] in session_seed.keys():
            all_sessions = session_seed[mouse_eartag, experiment_name]
            mouse = Mouse.from_db(mouse_eartag, testing=True, postgresql=postgresql)
            experiment = Experiment.from_db(experiment_name, testing=True, postgresql=postgresql)
            for [session_date, session_dir] in all_sessions:
                archive.database.seed_tables.seed_tables.seed_sessions_table(cursor,
                                                                             mouse.mouse_id,
                                                                             experiment.experiment_id,
                                                                             utils.convert_date_int_yyyymmdd(
                                                                                 session_date),
                                                                             session_dir)


# FOLDERS TABLE
def handler_create_folders_table(postgresql):
    handler_create_sessions_table(postgresql)
    with TestingCursor(postgresql) as cursor:
        archive.database.create_database.create_tables.create_folders_table(cursor)
        archive.database.create_database.create_views.create_view_folders_all_upstream_ids(cursor)


def handler_seed_folders_table(postgresql):
    handler_seed_sessions_table(postgresql)

    folders = ['Reaches01', 'Reaches02', 'Reaches03']
    with TestingCursor(postgresql) as cursor:
        cursor.execute("SELECT session_id, session_dir FROM sessions;")
        all_sessions = cursor.fetchall()
        for [session_id, session_dir] in all_sessions:
            for folder in folders:
                archive.database.seed_tables.seed_tables.seed_folders_table(cursor, session_id,
                                                                            '/'.join([session_dir, folder]))


# BLIND FOLDERS TABLE
def handler_create_blind_folders_table_only(postgresql):
    with TestingCursor(postgresql) as cursor:
        archive.database.create_database.create_tables.create_blind_folders_table(cursor)


def handler_create_blind_folders_table(postgresql):
    handler_create_folders_table(postgresql)
    handler_create_reviewers_table(postgresql)
    handler_create_blind_folders_table_only(postgresql)


def handler_seed_blind_folders_table_only(cursor):
    cursor.execute("SELECT reviewer_id FROM reviewers;")
    all_reviewer_ids = cursor.fetchall()
    cursor.execute("SELECT folder_id from folders;")
    all_folder_ids = cursor.fetchall()
    for folder_id in all_folder_ids:
        reviewer_id = random.choice(all_reviewer_ids)
        blind_name = utils.random_string_generator(10)
        archive.database.seed_tables.seed_tables.seed_blind_folders_table(cursor, folder_id, reviewer_id, blind_name)


def handler_seed_blind_folders_table(postgresql):
    handler_seed_folders_table(postgresql)
    handler_seed_reviewers_table(postgresql)
    with TestingCursor(postgresql) as cursor:
        handler_seed_blind_folders_table_only(cursor)


# TRIALS TABLE
def handler_create_trials_table(postgresql):
    handler_create_folders_table(postgresql)
    with TestingCursor(postgresql) as cursor:
        archive.database.create_database.create_tables.create_trials_table(cursor)
        archive.database.create_database.create_views.create_view_trials_all_upstream_ids(cursor)


def handler_seed_trials_table(postgresql):
    handler_seed_folders_table(postgresql)

    all_trials = ['trial_1.txt', 'trial_2.txt', 'trial_3.txt', 'trial_4.txt', 'trial_5.txt']
    with TestingCursor(postgresql) as cursor:
        cursor.execute("SELECT * from folders_all_upstream_ids;")
        all_ids = cursor.fetchall()
        for [_, experiment_id, session_id, folder_id] in all_ids:
            folder = Folder.from_db(folder_id=folder_id, testing=True, postgresql=postgresql)
            session = Session.from_db(session_id, testing=True, postgresql=postgresql)
            for trial in all_trials:
                trial_dir = '/'.join([folder.folder_dir, trial])
                archive.database.seed_tables.seed_tables.seed_trials_table(cursor,
                                                                           experiment_id,
                                                                           folder_id,
                                                                           trial_dir,
                                                                           session.session_date)


# BLIND TRIALS TABLE
def handler_create_blind_trials_table(postgresql):
    handler_create_trials_table(postgresql)
    handler_create_reviewers_table(postgresql)
    handler_create_blind_folders_table_only(postgresql)
    with TestingCursor(postgresql) as cursor:
        handler_seed_blind_folders_table_only(cursor)
        archive.database.create_database.create_tables.create_blind_trials_table(cursor)


def handler_seed_blind_trials(postgresql):
    all_trials = ['trial_1.txt', 'trial_2.txt', 'trial_3.txt', 'trial_4.txt', 'trial_5.txt']
    with TestingCursor(postgresql) as cursor:
        handler_seed_blind_folders_table_only(cursor)
        all_blind_names = models.blind_folders.list_all_blind_names(cursor)
    for blind_name in all_blind_names:
        blind_folder = BlindFolder.from_db(blind_name=blind_name, testing=True, postgresql=postgresql)
        reviewer = Reviewer.from_db(reviewer_id=blind_folder.reviewer_id, testing=True, postgresql=postgresql)
        folder = Folder.from_db(folder_id=blind_folder.folder_id, testing=True, postgresql=postgresql)
        for trial_file in all_trials:
            trial = Trial.from_db(trial_dir='/'.join([folder.folder_dir, trial_file]),
                                  testing=True, postgresql=postgresql)
            full_path = '/'.join([reviewer.toScore_dir, blind_name, blind_name + trial_file])
            with TestingCursor(postgresql) as cursor:
                archive.database.seed_tables.seed_tables.seed_blind_trials_table(cursor, trial.trial_id,
                                                                                 trial.folder_id, full_path)
