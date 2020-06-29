import utilities as util
from database.seed_tables.seeds import test_mouse_table_seed, exp_one, exp_two


def seed_mouse_table(a_cursor):
    for mouse in test_mouse_table_seed:
        genotype = util.encode_genotype(mouse[2])
        sex = util.prep_string_for_db(mouse[3])

        a_cursor.execute("INSERT INTO mouse"
                         "    (scored_dir, birthdate, genotype, sex) "
                         "VALUES"
                         "    (%s, %s, %s, %s);", (mouse[0], mouse[1], genotype, sex))


def seed_experiments_table(a_cursor):
    prepped_exp_one = (util.prep_string_for_db(exp_one[0]), exp_one[1])
    prepped_exp_two = (util.prep_string_for_db(exp_two[0]), exp_two[1])
    a_cursor.execute("INSERT INTO experiments (experiment_name, experiment_dir) VALUES (%s, %s);", prepped_exp_one)
    a_cursor.execute("INSERT INTO experiments (experiment_name, experiment_dir) VALUES (%s, %s);", prepped_exp_two)


def seed_participant_details(cursor, mouse_id, experiment_id, start_date, end_date):
    cursor.execute("INSERT INTO participant_details (mouse_id, experiment_id, start_date, end_date) "
                   "VALUES (%s, %s, %s, %s);", (mouse_id, experiment_id, start_date, end_date))


def seed_reviewers_table(cursor, first_name, last_name, toScore_dir, scored_dir):
    cursor.execute("INSERT INTO reviewers (first_name, last_name, toScore_dir, scored_dir) "
                   "VALUES (%s, %s, %s, %s);", (first_name, last_name, toScore_dir, scored_dir))


def seed_sessions_table(cursor, mouse_id, experiment_id, session_date, session_dir):
    cursor.execute("INSERT INTO sessions (mouse_id, experiment_id, session_date, session_dir) "
                   "VALUES (%s, %s, %s, %s);", (mouse_id, experiment_id, session_date, session_dir))


def seed_trials_table(cursor, mouse_id, experiment_id, trial_date, trial_dir):
    cursor.execute("INSERT INTO trials (experiment_id, mouse_id, trial_dir, trial_date) "
                   "VALUES (%s, %s, %s, %s);", (experiment_id, mouse_id, trial_dir, trial_date))


def seed_blind_trials_table(cursor, trial_id, reviewer_id, blind_name):
    cursor.execute("INSERT INTO blind_trials (trial_id, reviewer_id, blind_name) "
                   "VALUES (%s, %s, %s);", (trial_id, reviewer_id, blind_name))
