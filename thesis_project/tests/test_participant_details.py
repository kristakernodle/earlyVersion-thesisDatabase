import unittest

import testing.postgresql as tpg

import database.handlers.handlers
import database.seed_tables.seeds as seeds
from models.experiments import Experiments
from models.mouse import Mouse
from models.participant_details import ParticipantDetails

mice_seed = set(seeds.test_mouse_table_seed)
experiment_seed = {seeds.exp_one, seeds.exp_two}
Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=database.handlers.handlers.handler_create_participant_details)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewParticipantDetails(unittest.TestCase):
    mouse_seed = mice_seed.pop()

    def setUp(self):
        self.postgresql = Postgresql()
        database.handlers.handlers.handler_seed_mouse_experiments(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
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
        database.handlers.handlers.handler_seed_participant_details(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
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
        database.handlers.handlers.handler_seed_participant_details(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_list_participants(self):
        all_participants = ParticipantDetails.list_participants(self.exp_seed[0],
                                                                testing=True, postgresql=self.postgresql)
        self.assertTrue(len(all_participants) == 5)
        if 'one' in self.exp_seed[0]:
            for eartag in all_participants:
                self.assertTrue((eartag % 2) == 0)
        else:
            for eartag in all_participants:
                self.assertTrue((eartag % 2) != 0)


class TestUpdateParticipant(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        database.handlers.handlers.handler_seed_participant_details(self.postgresql)
        self.seed_mouse = mice_seed.pop()

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_update_participant(self):
        new_participant_dir = "/this/is/a/new/directory/"
        load_details = ParticipantDetails.from_db(self.seed_mouse[0], self.seed_mouse[5],
                                                  testing=True, postgresql=self.postgresql)
        update_details = load_details
        update_details.participant_dir = new_participant_dir
        saved_details = update_details.save_to_db(testing=True, postgresql=self.postgresql)
        self.assertEqual(new_participant_dir, saved_details.participant_dir)
        self.assertTrue(load_details.detail_id == saved_details.detail_id)


if __name__ == '__main__':
    unittest.main()
