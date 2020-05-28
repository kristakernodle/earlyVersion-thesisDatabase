import unittest
import testing.postgresql as tpg

import setup_DB_for_testing as testdb
from models.mouse import Mouse
from models.experiments import Experiments
from models.participant_details import ParticipantDetails

mice_seed = set(testdb.test_mouse_table_seed)
experiment_seed = {testdb.exp_one, testdb.exp_two}
Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True, on_initialized=testdb.handler_create_all_empty_tables)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewParticipantDetails(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        testdb.handler_seed_mouse_experiments(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_participant_details(self):
        test_mouse = Mouse.from_db(9999, testing=True, postgresql=self.postgresql)
        test_exp = Experiments.from_db('test experiment two', testing=True, postgresql=self.postgresql)
        test_details = ParticipantDetails(test_mouse, test_exp, 20200515, 20200615).save_to_db(testing=True,
                                                                                               postgresql=self.postgresql)
        self.assertTrue(test_mouse == test_details.mouse)
        self.assertTrue(test_exp == test_details.experiment)
        self.assertFalse(test_details.detail_id is None)


if __name__ == '__main__':
    unittest.main()
