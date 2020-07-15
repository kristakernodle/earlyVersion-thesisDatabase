import random
import unittest

import testing.postgresql as tpg

import database.handlers.handlers
import database.seed_tables.seeds as seeds
import utilities as utils
from models.experiments import Experiments
from models.mouse import Mouse
from models.trials import Trials

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=database.handlers.handlers.handler_create_trials_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewTrial(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        database.handlers.handlers.handler_create_trials_table(self.postgresql)
        database.handlers.handlers.handler_seed_folders_table(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_trial(self):
        test_folder_dir = '/exp/two/dir/9993/20200516_S1/Reaches01'
        test_trial = 'trial_2.txt'

        trial_dir = '/'.join([test_folder_dir, test_trial])

        test_folder = Folder.from_db(folder_dir=test_folder_dir)
        test_session = Session.from_db(test_folder.session_id)
        test_trial = Trial(test_session.experiment_id, test_folder.folder_id, trial_dir, test_session.session_date)

        self.assertEqual(test_session.experiment_id, test_trial.experiment_id)
        self.assertEqual(test_folder.folder_id, test_trial.folder_id)
        self.assertEqual(trial_dir, test_trial.trial_dir)
        self.assertEqual(test_session.session_date, test_trial.trial_date)
        self.assertFalse(test_trial.trial_id is None)
#
# class TestLoadTrial(unittest.TestCase):
#
#     def setUp(self):
#         self.postgresql = Postgresql()
#         database.handlers.handlers.handler_seed_trials(self.postgresql)
#
#         self.trial_key = random.choice(list(seeds.test_trial_table_seed.keys()))
#         self.eartag, self.experiment_name = self.trial_key
#         self.trial_date, self.trial_dir = random.choice(seeds.test_trial_table_seed[self.trial_key])
#
#     def tearDown(self):
#         self.postgresql.stop()
#
#     @unittest.skip("Not currently testing")
#     def test_setUp_tearDown(self):
#         self.assertTrue(1)
#
#     def test_from_db(self):
#         test_trial = Trials.from_db(self.trial_dir, testing=True, postgresql=self.postgresql)
#         self.assertFalse(test_trial.trial_id is None)
#         self.assertFalse(utils.convert_date_int_yyyymmdd(self.trial_date) != test_trial.trial_date)
#         self.assertTrue(Experiments.from_db(self.experiment_name,
#                                             testing=True, postgresql=self.postgresql) == test_trial.experiment)
#         self.assertTrue(Mouse.from_db(self.eartag, testing=True, postgresql=self.postgresql) == test_trial.mouse)
#
#
# class TestListTrials(unittest.TestCase):
#
#     def setUp(self):
#         self.postgresql = Postgresql()
#         database.handlers.handlers.handler_seed_trials(self.postgresql)
#
#         self.trial_key = random.choice(list(seeds.test_trial_table_seed.keys()))
#         self.eartag, self.experiment_name = self.trial_key
#         self.trials_mouse_exp = seeds.test_trial_table_seed[self.trial_key]
#
#     def tearDown(self):
#         self.postgresql.stop()
#
#     @unittest.skip("Not currently testing")
#     def test_setUp_tearDown(self):
#         self.assertTrue(1)
#
#     def test_list_participants(self):
#         all_participants = Trials.list_participants(self.experiment_name, testing=True, postgresql=self.postgresql)
#         self.assertTrue(len(all_participants) == 5)
#         if 'one' in self.experiment_name:
#             for eartag in all_participants:
#                 self.assertTrue((eartag % 2) == 0)
#         else:
#             for eartag in all_participants:
#                 self.assertTrue((eartag % 2) != 0)
