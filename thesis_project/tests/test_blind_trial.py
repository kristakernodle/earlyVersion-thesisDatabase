import unittest
import testing.postgresql as tpg

from models.blind_trials import BlindTrials

import database.handlers.handlers_blind_review as handlers_bt

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=handlers_bt.handler_create_blind_trials_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewTrial(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)


if __name__ == '__main__':
    unittest.main()
