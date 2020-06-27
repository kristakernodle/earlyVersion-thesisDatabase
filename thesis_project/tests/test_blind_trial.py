import unittest
import testing.postgresql as tpg

from models.blind_trials import BlindTrials

import database.handlers.handlers_blind_review as handlers_bt

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=handlers_bt.handler_create_blind_trials_table)


def tearDownModule():
    Postgresql.clear_cache()


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
