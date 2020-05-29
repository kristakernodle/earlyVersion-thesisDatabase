from models.mouse import list_all_mice, Mouse
from models.experiments import Experiments
from database.seed_tables.seeds import test_mouse_table_seed
from database.seed_tables.seed_independent_tables import handler_seed_mouse_experiments
from database.cursors import TestingCursor

mouse_seed = test_mouse_table_seed


def seed_participant_details(cursor, mouse_id, experiment_id, start_date, end_date):
    cursor.execute("INSERT INTO participant_details (mouse_id, experiment_id, start_date, end_date) "
                   "VALUES (%s, %s, %s, %s);", (mouse_id, experiment_id, start_date, end_date))


def handler_seed_participant_details(postgresql):
    handler_seed_mouse_experiments(postgresql)
    with TestingCursor(postgresql) as cursor:
        all_mice = list_all_mice(cursor)
        for eartag in all_mice:
            mouse = Mouse.from_db(eartag, testing=True, postgresql=postgresql)
            for m in mouse_seed:
                if m[0] == mouse.eartag:
                    experiment = Experiments.from_db(m[5], testing=True, postgresql=postgresql)
                    seed_participant_details(cursor, mouse.mouse_id, experiment.experiment_id,
                                             start_date=m[6], end_date=m[7])
