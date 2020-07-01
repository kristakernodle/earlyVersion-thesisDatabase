import unittest
import testing.postgresql as tpg
import random

import database.handlers.handlers
import database.seed_tables.seeds as seeds

from models.mouse import Mouse
from models.experiments import Experiments
from models.sessions import Session

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=database.handlers.handlers.handler_create_sessions_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewSession(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        database.handlers.handlers.handler_seed_sessions_table(self.postgresql)
        self.test_session_key = random.choice(list(seeds.test_trial_table_seed.keys()))
        self.test_session_date, self.test_session_dir = random.choice(
            seeds.test_trial_table_seed[self.test_session_key])

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_session(self):
        mouse = Mouse.from_db(self.test_session_key[0], testing=True, postgresql=self.postgresql)
        experiment = Experiments.from_db(self.test_session_key[1], testing=True, postgresql=self.postgresql)
        saved_session = Session(mouse, experiment, self.test_session_date,
                                self.test_session_dir).save_to_db(testing=True, postgresql=self.postgresql)
        self.assertFalse(saved_session.session_id is None)
        self.assertTrue(mouse == saved_session.mouse)
        self.assertTrue(experiment == saved_session.experiment)


if __name__ == '__main__':
    unittest.main()
