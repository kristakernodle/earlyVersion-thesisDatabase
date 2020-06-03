import unittest
import testing.postgresql as tpg

import database.handlers.handlers_independent_tables as create_independent_tables
import database.seed_tables.seed_independent_tables as seed_independent_tables
from database.handler_seed_participant_details import handler_seed_participant_details
from models.mouse import Mouse
from models.experiments import Experiments
from models.participant_details import ParticipantDetails
from database.seed_tables.seeds import test_mouse_table_seed, exp_one, exp_two

mice_seed = set(test_mouse_table_seed)
experiment_seed = {exp_one, exp_two}
Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=create_independent_tables.handler_create_all_empty_tables)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewParticipantDetails(unittest.TestCase):
    mouse_seed = mice_seed.pop()

    def setUp(self):
        self.postgresql = Postgresql()
        seed_independent_tables.handler_seed_mouse_experiments(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_participant_details(self):
        test_mouse = Mouse.from_db(self.mouse_seed[0], testing=True, postgresql=self.postgresql)
        test_exp = Experiments.from_db(self.mouse_seed[5], testing=True, postgresql=self.postgresql)
        test_details = ParticipantDetails(test_mouse, test_exp, self.mouse_seed[6], self.mouse_seed[7]).save_to_db(
            testing=True, postgresql=self.postgresql)
        self.assertTrue(test_mouse == test_details.mouse)
        self.assertTrue(test_exp == test_details.experiment)
        self.assertFalse(test_details.detail_id is None)


class TestLoadParticipantDetails(unittest.TestCase):
    mouse_seed = mice_seed.pop()

    def setUp(self):
        self.postgresql = Postgresql()
        handler_seed_participant_details(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_from_db(self):
        test_details = ParticipantDetails.from_db(self.mouse_seed[0], self.mouse_seed[5],
                                                  testing=True, postgresql=self.postgresql)
        self.assertTrue(Mouse.from_db(self.mouse_seed[0],
                                      testing=True, postgresql=self.postgresql) == test_details.mouse)
        self.assertTrue(Experiments.from_db(self.mouse_seed[5],
                                            testing=True, postgresql=self.postgresql) == test_details.experiment)
        self.assertFalse(test_details.detail_id is None)


class TestListParticipants(unittest.TestCase):
    exp_seed = experiment_seed.pop()

    def setUp(self):
        self.postgresql = Postgresql()
        handler_seed_participant_details(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_list_participants(self):
        all_participants = ParticipantDetails.list_participants(self.exp_seed[0])
        if 'one' in self.exp_seed[0]:
            for eartag in all_participants:
                self.assertTrue((eartag % 2) == 0)
        else:
            for eartag in all_participants:
                self.assertTrue((eartag % 2) != 0)


if __name__ == '__main__':
    unittest.main()
