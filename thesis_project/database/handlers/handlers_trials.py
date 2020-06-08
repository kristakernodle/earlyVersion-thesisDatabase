from models.mouse import list_all_mice, Mouse
from models.experiments import Experiments
import utilities as utils

from database.cursors import TestingCursor
import database.create_tables.create_independent_tables as create_id
import database.create_tables.create_trials as create_tr

import database.seed_tables.seed_independent_tables as seed_id
import database.seed_tables.seed_trials_table as seed_tr
from database.seed_tables.seeds import test_mouse_table_seed as mouse_seed, test_trial_table_seed as trial_seed


def handler_create_trials_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_id.create_mouse_table(cursor)
        create_id.create_experiments_table(cursor)
        create_tr.create_trials_table(cursor)
        create_tr.create_view_all_participants_all_trials(cursor)


def handler_seed_trials(postgresql):
    with TestingCursor(postgresql) as cursor:
        seed_id.seed_mouse_table(cursor)
        seed_id.seed_experiments_table(cursor)

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
                        seed_tr.seed_trials(cursor, mouse.mouse_id, experiment.experiment_id,
                                            utils.convert_date_int_yyyymmdd(trial_date), trial_dir)
