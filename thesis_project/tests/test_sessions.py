import unittest
import testing.postgresql as tpg

import utilities as utils
from models.mouse import Mouse
from models.experiments import Experiments
from models.sessions import Session

import database.handlers.handlers
import database.seed_tables.seed_tables
from database.seed_tables.seeds import test_mouse_table_seed, test_session_table_seed

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=database.handlers.handlers.handler_create_sessions_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewSession(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        database.handlers.handlers.handler_seed_mouse(self.postgresql)
        database.handlers.handlers.handler_seed_experiments(self.postgresql)
        self.mouse = Mouse.from_db(9990, testing=True, postgresql=self.postgresql)
        self.experiment = Experiments.from_db('test-experiment-one', testing=True, postgresql=self.postgresql)
        self.session_date = 20200503
        self.session_dir = '/exp/one/dir/9990/20200503_S2'

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_session(self):
        test_session = Session(self.mouse.mouse_id, self.experiment.experiment_id,
                               self.session_dir, self.session_date).save_to_db(testing=True, postgresql=self.postgresql)
        self.assertFalse(test_session.session_id is None)

    def test_duplicate_session(self):
        test_session = Session(self.mouse.mouse_id, self.experiment.experiment_id,
                               self.session_dir, self.session_date).save_to_db(testing=True, postgresql=self.postgresql)
        dup_session = test_session.save_to_db(testing=True, postgresql=self.postgresql)
        self.assertFalse(dup_session.session_id is None)


class TestLoadSession(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        database.handlers.handlers.handler_seed_sessions_table(self.postgresql)
        [eartag, _, _, _, _, experiment_name, _, _] = test_mouse_table_seed.pop()
        self.mouse = Mouse.from_db(eartag, testing=True, postgresql=self.postgresql)
        self.experiment = Experiments.from_db(experiment_name, testing=True, postgresql=self.postgresql)
        possible_sessions = test_session_table_seed[eartag, utils.prep_string_for_db(experiment_name)]
        self.session_date, self.session_dir = possible_sessions.pop()

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_from_db(self):
        load_session = Session.from_db(session_dir=self.session_dir, testing=True, postgresql=self.postgresql)
        self.assertEqual(self.mouse.mouse_id, load_session.mouse_id)
        self.assertEqual(self.experiment.experiment_id, load_session.experiment_id)
        self.assertEqual(utils.convert_date_int_yyyymmdd(self.session_date), load_session.session_date)
        self.assertEqual(self.session_dir, load_session.session_dir)
        self.assertFalse(load_session.session_id is None)


if __name__ == '__main__':
    unittest.main()
