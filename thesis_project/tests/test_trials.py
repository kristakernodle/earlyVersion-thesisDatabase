import unittest
import testing.postgresql as tpg
import random

from models.mouse import Mouse
from models.experiments import Experiments
from models.trials import Trials

import database.handlers.handlers_trials as handlers_tr
import database.handlers.handlers_independent_tables as handlers_id
import database.seed_tables.seeds as seeds

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=handlers_tr.handler_create_trials_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestLoadTrial(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        handlers_tr.handler_seed_trials(self.postgresql)

        self.test_trial_key = random.choice(list(seeds.test_trial_table_seed.keys()))
        self.eartag, self.experiment_name = self.test_trial_key
        self.trial_date, self.trial_dir = random.choice(seeds.test_trial_table_seed[self.test_trial_key])

    def tearDown(self):
        self.postgresql.stop()

    # @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    # def test_from_db(self):
    #     test_details = Trials.from_db(self.trial_dir, testing=True, postgresql=self.postgresql)
    #     self.assertTrue(Mouse.from_db(self.mouse_seed[0],
    #                                   testing=True, postgresql=self.postgresql) == test_details.mouse)
    #     self.assertTrue(Experiments.from_db(self.mouse_seed[5],
    #                                         testing=True, postgresql=self.postgresql) == test_details.experiment)
    #     self.assertFalse(test_details.detail_id is None)


class TestNewTrial(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        handlers_id.handler_seed_mouse_experiments(self.postgresql)
        self.test_trial_key = random.choice(list(seeds.test_trial_table_seed.keys()))
        self.test_trial_one_date = random.choice(seeds.test_trial_table_seed[self.test_trial_key])

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_trial(self):
        mouse = Mouse.from_db(self.test_trial_key[0], testing=True, postgresql=self.postgresql)
        experiment = Experiments.from_db(self.test_trial_key[1], testing=True, postgresql=self.postgresql)
        saved_trial = Trials(mouse, experiment, self.test_trial_one_date[1], self.test_trial_one_date[0]).save_to_db(
            testing=True, postgresql=self.postgresql)
        self.assertFalse(saved_trial.trial_id is None)
        self.assertTrue(mouse == saved_trial.mouse)
        self.assertTrue(experiment == saved_trial.experiment)
