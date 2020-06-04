import unittest
import testing.postgresql as tpg

import database.handlers.handlers_trials as handlers_tr

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=handlers_tr.handler_create_trials_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewTrial(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)

    # def test_add_new_mouse(self):
    #     test_mouse = Mouse(1111, self.birthdate, 'wild type', 'female').save_to_db(testing=True,
    #                                                                                postgresql=self.postgresql)
    #     self.assertEqual(1111, test_mouse.eartag)
    #     self.assertEqual(util.convert_date_int_yyyymmdd(self.birthdate), test_mouse.birthdate)
    #     self.assertEqual('wild type', test_mouse.genotype)
    #     self.assertEqual('female', test_mouse.sex)
    #     self.assertFalse(test_mouse.mouse_id is None)
