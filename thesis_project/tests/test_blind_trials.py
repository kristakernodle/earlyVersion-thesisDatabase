import unittest
import random
import testing.postgresql as tpg

from utilities import random_string_generator

from models.blind_trials import BlindTrial
from models.reviewer import Reviewer
from models.trials import Trials

import database.handlers.handlers_blind_review as handlers_bt

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=handlers_bt.handler_create_blind_trials_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewBlindTrial(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        handlers_bt.handler_seed_blind_trials(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_blind_trial(self):
        trial_dir = '/exp/two/trial/dir/9997/3'
        trial = Trials.from_db(trial_dir, testing=True, postgresql=self.postgresql)

        reviewer_scored_dir = '/blind/review/reviewer_one/Scored'
        reviewer = Reviewer.from_db(reviewer_scored_dir, testing=True, postgresql=self.postgresql)

        len_string = 10
        blind_name = random_string_generator(len_string)

        saved_blind_trial = BlindTrial(trial.trial_id,
                                       reviewer.reviewer_id,
                                       blind_name).save_to_db(testing=True, postgresql=self.postgresql)
        print(trial)
        print(saved_blind_trial)
        self.assertEqual(trial.trial_id, saved_blind_trial.trial_id)
        self.assertEqual(reviewer.reviewer_id, saved_blind_trial.reviewer_id)
        self.assertEqual(blind_name, saved_blind_trial.blind_name)
        self.assertFalse(saved_blind_trial.blind_trial_id is None)


class TestLoadBlindTrial(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        all_blind_names = handlers_bt.handler_seed_blind_trials(self.postgresql)
        self.trial_id, self.reviewer_id, self.blind_name = random.choice(all_blind_names)

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_from_db(self):
        test_blind_trial = BlindTrial.from_db(self.blind_name, testing=True, postgresql=self.postgresql)
        self.assertEqual(self.trial_id, test_blind_trial.trial_id)
        self.assertEqual(self.reviewer_id, test_blind_trial.reviewer_id)
        self.assertFalse(test_blind_trial.blind_trial_id is None)


if __name__ == '__main__':
    unittest.main()
