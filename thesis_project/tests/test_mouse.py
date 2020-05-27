import unittest
import testing.postgresql as tpg

import utilities as util
import tests.setup_DB_for_testing as testdb
from models.cursors import TestingCursor
from models.mouse import Mouse, list_all_mice

mice_seed = set(testdb.test_mouse_table_seed)
Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True, on_initialized=testdb.handler_create_all_empty_tables)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewMouse(unittest.TestCase):
    birthdate = 20200527

    def setUp(self):
        self.postgresql = Postgresql()
        Mouse(1111, self.birthdate, 'wild type', 'female').save_to_db(testing=True, postgresql=self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_mouse(self):
        test_mouse = Mouse(1111, self.birthdate, 'wild type', 'female').save_to_db(testing=True,
                                                                                   postgresql=self.postgresql)
        self.assertEqual(1111, test_mouse.eartag)
        self.assertEqual(util.convert_date_int_yyyymmdd(self.birthdate), test_mouse.birthdate)
        self.assertEqual('wild type', test_mouse.genotype)
        self.assertEqual('female', test_mouse.sex)
        self.assertFalse(test_mouse.mouse_id is None)

    def test_duplicate_mouse(self):
        test_mouse = Mouse(1111, self.birthdate, 'wild type', 'female').save_to_db(testing=True,
                                                                                   postgresql=self.postgresql)
        test_mouse = test_mouse.save_to_db(testing=True, postgresql=self.postgresql)
        self.assertEqual(1111, test_mouse.eartag)
        self.assertEqual(util.convert_date_int_yyyymmdd(self.birthdate), test_mouse.birthdate)
        self.assertEqual('wild type', test_mouse.genotype)
        self.assertEqual('female', test_mouse.sex)
        self.assertFalse(test_mouse.mouse_id is None)


class TestLoadMouse(unittest.TestCase):
    seed_tup = mice_seed.pop()

    def setUp(self):
        self.postgresql = Postgresql()
        testdb.handler_seed_mouse(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_from_db(self):
        self.load_mouse = Mouse.from_db(self.seed_tup[0], testing=True, postgresql=self.postgresql)
        self.assertEqual(self.seed_tup[0], self.load_mouse.eartag)
        self.assertEqual(self.seed_tup[1], self.load_mouse.birthdate)
        self.assertEqual(self.seed_tup[2], self.load_mouse.genotype)
        self.assertEqual(self.seed_tup[3], self.load_mouse.sex)
        self.assertFalse(self.load_mouse.mouse_id is None)


class TestDeleteMouse(unittest.TestCase):
    seed_tup = mice_seed.pop()

    def setUp(self):
        self.postgresql = Postgresql()
        testdb.handler_seed_mouse(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_delete_mouse(self):
        mouse_to_delete = Mouse.from_db(self.seed_tup[0], testing=True, postgresql=self.postgresql)
        mouse_to_delete.delete_from_db(testing=True, postgresql=self.postgresql)
        with TestingCursor(self.postgresql) as cursor:
            all_mice = list_all_mice(cursor)
        self.assertFalse(self.seed_tup[0] in all_mice)


# TODO: TestAddParticipant - I think this needs to be in a different test document, some kind of integration testing
#       rather than the current set up
# class TestAddParticipant(unittest.TestCase):
#
#     def setUp(self):
#         self.postgresql = tpg.PostgresqlFactory(cache_initialized_db=True, on_initialized=testdb.handler_seed_mouse_experiments)
#
#     def tearDown(self):
#         self.postgresql.stop()
#
#     def test_add_participant(self):
#         self.test_mouse_details = []
#         for mouse in self.test_mouse_table_seed:
#             if util.prep_string_for_db(mouse[5]) == util.prep_string_for_db(self.test_experiment_one.experiment_name):
#                 self.test_mouse_details.append(Mouse.from_db(mouse[0])
#                                                .add_participant(util.prep_string_for_db(self
#                                                                                         .test_experiment_one
#                                                                                         .experiment_name)))
#             elif util.prep_string_for_db(mouse[5]) == util.prep_string_for_db(self.test_experiment_two.experiment_name):
#                 self.test_mouse_details.append(Mouse.from_db(mouse[0])
#                                                .add_participant(util
#                                                                 .prep_string_for_db(self
#                                                                                     .test_experiment_two.experiment_name)))
#         self.assertListEqual(sorted(self.test_participants_list, key=lambda m: m.eartag),
#                              sorted(Experiments.list_participants(), key=lambda m: m.eartag))


if __name__ == '__main__':
    unittest.main()
