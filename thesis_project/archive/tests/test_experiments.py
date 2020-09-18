import unittest

import testing.postgresql as tpg

from archive import database as seeds, utilities as util
from archive.database import TestingCursor
from archive.models import Experiment, list_all_experiments

mice_seed = set(seeds.test_mouse_table_seed)
experiment_seed = {seeds.exp_one, seeds.exp_two}
Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=archive.database.handlers.handlers.handler_create_experiments_table)


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
        test_exp = Experiment(self.seed_exp[0], self.seed_exp[1]).save_to_db(testing=True,
                                                                             postgresql=self.postgresql)
        self.assertEqual(util.prep_string_for_db(self.seed_exp[0]), test_exp.experiment_name)
        self.assertEqual(self.seed_exp[1], test_exp.experiment_dir)
        self.assertFalse(test_exp.experiment_id is None)

    def test_duplicate_experiment(self):
        test_exp = Experiment(self.seed_exp[0], self.seed_exp[1]).save_to_db(testing=True,
                                                                             postgresql=self.postgresql)
        dup_exp = test_exp.save_to_db(testing=True, postgresql=self.postgresql)
        self.assertFalse(dup_exp.experiment_id is None)


class TestLoadExperiment(unittest.TestCase):
    seed_tup = experiment_seed.pop()

    def setUp(self):
        self.postgresql = Postgresql()
        archive.database.handlers.handlers.handler_seed_experiments(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_from_db(self):
        load_exp = Experiment.from_db(self.seed_tup[0], testing=True, postgresql=self.postgresql)
        self.assertEqual(util.prep_string_for_db(self.seed_tup[0]), load_exp.experiment_name)
        self.assertEqual(self.seed_tup[1], load_exp.experiment_dir)
        self.assertFalse(load_exp.experiment_name is None)

    def test_get_id(self):
        load_exp_id = Experiment.get_id(self.seed_tup[0], testing=True, postgresql=self.postgresql)
        load_fake_id = Experiment.get_id('Experiment Not Here', testing=True, postgresql=self.postgresql)
        self.assertTrue(len(load_exp_id) == 1)
        self.assertTrue(len(load_fake_id) == 0)


class TestDeleteExperiment(unittest.TestCase):
    seed_tup = experiment_seed.pop()

    def setUp(self):
        self.postgresql = Postgresql()
        archive.database.handlers.handlers.handler_seed_experiments(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_delete_experiment(self):
        experiment_to_delete = Experiment.from_db(self.seed_tup[0], testing=True, postgresql=self.postgresql)
        experiment_to_delete.delete_from_db(testing=True, postgresql=self.postgresql)
        with TestingCursor(self.postgresql) as cursor:
            all_experiments = list_all_experiments(cursor)
            self.assertFalse(util.prep_string_for_db(self.seed_tup[0]) in all_experiments)


class TestUpdateExperiment(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        archive.database.handlers.handlers.handler_seed_experiments(self.postgresql)
        self.seed_tup = {seeds.exp_one, seeds.exp_two}.pop()

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_update_existing_experiment(self):
        new_name = "New Experiment Name"
        load_exp = Experiment.from_db(self.seed_tup[0], testing=True, postgresql=self.postgresql)
        update_exp = load_exp
        update_exp.experiment_name = new_name
        saved_exp = update_exp.save_to_db(testing=True, postgresql=self.postgresql)
        self.assertEqual(util.prep_string_for_db(new_name), saved_exp.experiment_name)
        self.assertTrue(load_exp.experiment_id == saved_exp.experiment_id)
        self.assertTrue(load_exp.experiment_dir == saved_exp.experiment_dir)


if __name__ == '__main__':
    unittest.main()
