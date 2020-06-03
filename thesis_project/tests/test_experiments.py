import unittest
import testing.postgresql as tpg

import utilities as util
from models.experiments import Experiments, list_all_experiments

from database.cursors import TestingCursor
import database.handlers.handlers_independent_tables as handlers_id

import database.seed_tables.seeds as seeds

mice_seed = set(seeds.test_mouse_table_seed)
experiment_seed = {seeds.exp_one, seeds.exp_two}
Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=handlers_id.handler_create_experiments_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewExperiment(unittest.TestCase):
    seed_exp = ('experiment-name', '/Volumes/SharedX/experiment/directory/')

    def setUp(self):
        self.postgresql = Postgresql()

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_experiment(self):
        test_exp = Experiments(self.seed_exp[0], self.seed_exp[1]).save_to_db(testing=True,
                                                                              postgresql=self.postgresql)
        self.assertEqual(util.prep_string_for_db(self.seed_exp[0]), test_exp.experiment_name)
        self.assertEqual(self.seed_exp[1], test_exp.experiment_dir)
        self.assertFalse(test_exp.experiment_id is None)

    def test_duplicate_experiment(self):
        test_exp = Experiments(self.seed_exp[0], self.seed_exp[1]).save_to_db(testing=True,
                                                                              postgresql=self.postgresql)
        dup_exp = test_exp.save_to_db(testing=True, postgresql=self.postgresql)
        self.assertFalse(dup_exp.experiment_id is None)


class TestLoadExperiment(unittest.TestCase):
    seed_tup = experiment_seed.pop()

    def setUp(self):
        self.postgresql = Postgresql()
        handlers_id.handler_seed_experiments(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_from_db(self):
        self.load_exp = Experiments.from_db(self.seed_tup[0], testing=True, postgresql=self.postgresql)
        self.assertEqual(util.prep_string_for_db(self.seed_tup[0]), self.load_exp.experiment_name)
        self.assertEqual(self.seed_tup[1], self.load_exp.experiment_dir)
        self.assertFalse(self.load_exp.experiment_name is None)


class TestDeleteExperiment(unittest.TestCase):
    seed_tup = experiment_seed.pop()

    def setUp(self):
        self.postgresql = Postgresql()
        handlers_id.handler_seed_experiments(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_delete_experiment(self):
        experiment_to_delete = Experiments.from_db(self.seed_tup[0], testing=True, postgresql=self.postgresql)
        experiment_to_delete.delete_from_db(testing=True, postgresql=self.postgresql)
        with TestingCursor(self.postgresql) as cursor:
            all_experiments = list_all_experiments(cursor)
            self.assertFalse(util.prep_string_for_db(self.seed_tup[0]) in all_experiments)


class TestUpdateExperiment(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        handlers_id.handler_seed_experiments(self.postgresql)
        self.seed_tup = {seeds.exp_one, seeds.exp_two}.pop()

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_update_existing_experiment(self):
        new_name = "New Experiment Name"
        load_exp = Experiments.from_db(self.seed_tup[0], testing=True, postgresql=self.postgresql)
        update_exp = load_exp
        update_exp.experiment_name = new_name
        saved_exp = update_exp.save_to_db(testing=True, postgresql=self.postgresql)
        self.assertEqual(util.prep_string_for_db(new_name), saved_exp.experiment_name)
        self.assertTrue(load_exp.experiment_id == saved_exp.experiment_id)
        self.assertTrue(load_exp.experiment_dir == saved_exp.experiment_dir)


if __name__ == '__main__':
    unittest.main()
