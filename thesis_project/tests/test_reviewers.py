import unittest
import testing.postgresql as tpg

import database.handlers.handlers_blind_review as handlers_br
from database.cursors import TestingCursor

from database.seed_tables.seeds import test_blind_review_reviewers_seed as reviewer_seed
from models.reviewer import Reviewer, list_all_scored_dirs

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=handlers_br.handler_create_reviewers_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewReviewer(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_reviewer(self):
        test_reviewer = Reviewer('tester', 'reviewer', 'toScore_dir', 'scored_dir').save_to_db(testing=True,
                                                                                               postgresql=self.postgresql)
        self.assertEqual('tester', test_reviewer.first_name)
        self.assertEqual('reviewer', test_reviewer.last_name)
        self.assertEqual('toScore_dir', test_reviewer.toScore_dir)
        self.assertEqual('scored_dir', test_reviewer.scored_dir)
        self.assertFalse(test_reviewer.reviewer_id is None)

    def test_duplicate_reviewer(self):
        test_reviewer = Reviewer('tester', 'reviewer', 'toScore_dir', 'scored_dir').save_to_db(testing=True,
                                                                                               postgresql=self.postgresql)
        dup_reviewer = test_reviewer.save_to_db(testing=True, postgresql=self.postgresql)
        self.assertFalse(dup_reviewer.reviewer_id is None)


class TestLoadDeleteReviewer(unittest.TestCase):
    seed_tup = reviewer_seed[0]

    def setUp(self):
        self.postgresql = Postgresql()
        handlers_br.handler_seed_reviewers(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_from_db(self):
        load_reviewer = Reviewer.from_db(self.seed_tup[-1], testing=True, postgresql=self.postgresql)
        self.assertEqual(self.seed_tup[0], load_reviewer.first_name)
        self.assertEqual(self.seed_tup[1], load_reviewer.last_name)
        self.assertEqual(self.seed_tup[2], load_reviewer.toScore_dir)
        self.assertEqual(self.seed_tup[3], load_reviewer.scored_dir)
        self.assertFalse(load_reviewer.reviewer_id is None)

    def test_delete_reviewer(self):
        reviewer_to_delete = Reviewer.from_db(self.seed_tup[-1], testing=True, postgresql=self.postgresql)
        reviewer_to_delete.delete_from_db(testing=True, postgresql=self.postgresql)
        with TestingCursor(self.postgresql) as cursor:
            all_scored_dirs = list_all_scored_dirs(cursor)
        self.assertFalse(self.seed_tup[-1] in all_scored_dirs)


if __name__ == '__main__':
    unittest.main()