from models.mouse import list_all_mice, Mouse
from models.experiments import Experiments

from database.cursors import TestingCursor
import database.create_tables.create_participant_details as create_pd
from database.handlers.handlers_independent_tables import handler_create_all_independent_tables
from database.seed_tables.seed_independent_tables import handler_seed_mouse_experiments
from database.seed_tables.seed_participant_details import seed_participant_details

from database.seed_tables.seeds import test_mouse_table_seed as mouse_seed


def handler_create_participant_details(postgresql):
    handler_create_all_independent_tables(postgresql)
    with TestingCursor(postgresql) as cursor:
        create_pd.create_participant_details_table(cursor)
        create_pd.create_view_all_participants_all_experiments(cursor)


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
