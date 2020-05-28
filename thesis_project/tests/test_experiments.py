import unittest
import testing.postgresql as tpg

import utilities as util
import tests.setup_DB_for_testing as testdb
from models.cursors import TestingCursor
from models.experiments import Experiments, list_all_experiments

mice_seed = set(testdb.test_mouse_table_seed)
experiment_seed = {testdb.exp_one, testdb.exp_two}
Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True, on_initialized=testdb.handler_create_all_empty_tables)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewExperiment(unittest.TestCase):
    seed_exp = ('experiment-name', '/Volumes/SharedX/experiment/directory/')

    def setUp(self):
        self.postgresql = Postgresql()

    def tearDown(self):
        self.postgresql.stop()

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
        testdb.handler_seed_experiments(self.postgresql)

    def tearDwon(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)
        with TestingCursor(self.postgresql) as cursor:
            print(list_all_experiments(cursor))

    def test_from_db(self):
        self.load_exp = Experiments.from_db(self.seed_tup[0], testing=True, postgresql=self.postgresql)
        self.assertEqual(util.prep_string_for_db(self.seed_tup[0]), self.load_exp.experiment_name)
        self.assertEqual(self.seed_tup[1], self.load_exp.experiment_dir)
        self.assertFalse(self.load_exp.experiment_name is None)


# class TestListExperimentParticipants(unittest.TestCase):
#
#     def setUp(self):
#         Database.initialize(**dbConnection_Krista)
#         self.test_experiment_one = Experiments(self.experiment_name_one, self.experiment_dir_one).save_to_db()
#         self.test_experiment_two = Experiments(self.experiment_name_two, self.experiment_dir_two).save_to_db()
#         self.test_participants_list = []
#         self.test_mouse_detail_list = []
#         for mouse in self.test_mouse_table_seed:
#             if mouse[4]:
#                 exp_x = self.experiment_name_one
#                 start_x = 20200501
#                 end_x = 20200601
#             else:
#                 exp_x = self.experiment_name_two
#                 start_x = 20200515
#                 end_x = 20200615
#
#             self.test_participants_list.append(ms.Mouse(eartag=mouse[0], birthdate=mouse[1],
#                                                         genotype=mouse[2], sex=mouse[3]).save_to_db())
#             self.test_mouse_detail_list.append(ParticipantDetails(mouse[0], exp_x, start_x, end_x).save_to_db())
#
#     def tearDown(self):
#         for mouse_detail in self.test_mouse_detail_list:
#             mouse_detail.delete_from_db()
#         self.test_experiment_one.delete_from_db()
#         self.test_experiment_two.delete_from_db()
#         for mouse in self.test_mouse_detail_list:
#             mouse.delete_from_db()
#         for mouse in self.test_participants_list:
#             mouse.delete_from_db()
#
#     def test_list_participants(self):
#         load_participants_list = Experiments.list_participants()  # should return a list of Mouse objects
#         self.assertListEqual(self.test_participants_list, load_participants_list)
#
#     def test_list_participants_by_experiment(self):
#         load_participants_list_exp_1 = Experiments.list_participants("Test Experiment One")
#         load_participants_list_exp_2 = Experiments.list_participants("Test Experiment Two")
#         exp1 = []
#         exp2 = []
#         for mouse_detail in self.test_mouse_detail_list:
#             if mouse_detail.experiment.experiment_name == 'test-experiment-one':
#                 exp1.append(mouse_detail.mouse)
#             elif mouse_detail.experiment.experiment_name == 'test-experiment-two':
#                 exp2.append(mouse_detail.mouse)
#         self.assertListEqual(exp1, load_participants_list_exp_1)
#         self.assertListEqual(exp2, load_participants_list_exp_2)
#
#
# class TestAddParticipant(unittest.TestCase):
#
#     test_mouse_table_seed = [(9990, 20200102, 'wild type', 'male', True, 'test experiment one', 20200501, 20200601),
#                              (9991, 20200101, 'wild type', 'male', False, 'test experiment two', 20200515, 20200615),
#                              (9992, 20200101, 'wild type', 'male', True, 'test experiment one', 20200501, 20200601),
#                              (9993, 20200101, 'wild type', 'male', False, 'test experiment two', 20200515, 20200615),
#                              (9994, 20200101, 'wild type', 'female', True, 'test experiment one', 20200501, 20200601),
#                              (9995, 20200101, 'wild type', 'female', False, 'test experiment two', 20200515, 20200615),
#                              (9996, 20200101, 'knock out', 'female', True, 'test experiment one', 20200501, 20200601),
#                              (9997, 20200101, 'knock out', 'female', False, 'test experiment two', 20200515, 20200615),
#                              (9998, 20200101, 'knock out', 'female', True, 'test experiment one', 20200501, 20200601),
#                              (9999, 20200102, 'knock out', 'female', False, 'test experiment two', 20200515, 20200615)]
#     experiment_name_one = 'test experiment one'
#     experiment_name_two = 'test experiment two'
#     experiment_dir_one = '/test/directory/experiment/one'
#     experiment_dir_two = '/test/directory/experiment/two'
#
#     def setUp(self):
#         Database.initialize(**dbConnection_Krista)
#         self.test_experiment_one = Experiments(self.experiment_name_one, self.experiment_dir_one).save_to_db()
#         self.test_experiment_two = Experiments(self.experiment_name_two, self.experiment_dir_two).save_to_db()
#         self.test_participants_list = []
#         for mouse in self.test_mouse_table_seed:
#             self.test_participants_list.append(ms.Mouse(eartag=mouse[0], birthdate=mouse[1],
#                                                         genotype=mouse[2], sex=mouse[3]).save_to_db())
#
#     def tearDown(self):
#         for mouse_detail in self.test_mouse_details:
#             mouse_detail.delete_from_db()
#         for mouse in self.test_participants_list:
#             mouse.delete_from_db()
#         self.test_experiment_one.delete_from_db()
#         self.test_experiment_two.delete_from_db()
#
#     def test_add_participant(self):
#         self.test_mouse_details = []
#         for mouse in self.test_mouse_table_seed:
#             if util.prep_string_for_db(mouse[5]) == util.prep_string_for_db(self.test_experiment_one.experiment_name):
#                 self.test_mouse_details.append(self.test_experiment_one.add_participant(mouse[0]))
#             elif util.prep_string_for_db(mouse[5]) == util.prep_string_for_db(self.test_experiment_two.experiment_name):
#                 self.test_mouse_details.append(self.test_experiment_two.add_participant(mouse[0]))
#         self.assertListEqual(sorted(self.test_participants_list, key=lambda m: m.eartag),
#                              sorted(Experiments.list_participants(), key=lambda m: m.eartag))


if __name__ == '__main__':
    unittest.main()
