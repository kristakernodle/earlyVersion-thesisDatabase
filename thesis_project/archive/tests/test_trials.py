import unittest

import testing.postgresql as tpg

from archive.database import TestingCursor
from archive.models import Session
from archive.models import Folder
from archive.models import Trial

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=archive.database.handlers.handlers.handler_create_trials_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewTrial(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        archive.database.handlers.handlers.handler_seed_folders_table(self.postgresql)

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_trial(self):
        test_folder_dir = '/exp/two/dir/9993/20200516_S1/Reaches01'
        test_trial = 'trial_2.txt'

        trial_dir = '/'.join([test_folder_dir, test_trial])

        test_folder = Folder.from_db(folder_dir=test_folder_dir, testing=True, postgresql=self.postgresql)
        test_session = Session.from_db(test_folder.session_id, testing=True, postgresql=self.postgresql)
        test_trial = Trial(test_session.experiment_id, test_folder.folder_id, trial_dir,
                           test_session.session_date).save_to_db(testing=True, postgresql=self.postgresql)

        self.assertEqual(test_session.experiment_id, test_trial.experiment_id)
        self.assertEqual(test_folder.folder_id, test_trial.folder_id)
        self.assertEqual(trial_dir, test_trial.trial_dir)
        self.assertEqual(test_session.session_date, test_trial.trial_date)
        self.assertFalse(test_trial.trial_id is None)


class TestLoadTrial(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        archive.database.handlers.handlers.handler_seed_trials_table(self.postgresql)
        with TestingCursor(self.postgresql) as cursor:
            cursor.execute("SELECT session_dir from sessions;")
            all_session_dir = cursor.fetchall()
        session_dir = all_session_dir.pop()
        self.session = Session.from_db(session_dir=session_dir, testing=True, postgresql=self.postgresql)
        folder_dir = '/'.join([self.session.session_dir, 'Reaches02'])
        self.folder = Folder.from_db(folder_dir, testing=True, postgresql=self.postgresql)
        self.trial_dir = '/'.join([self.folder.folder_dir, 'trial_1.txt'])

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_from_db(self):
        test_trial = Trial.from_db(trial_dir=self.trial_dir, testing=True, postgresql=self.postgresql)

        self.assertFalse(test_trial.trial_id is None)
        self.assertTrue(self.session.experiment_id == test_trial.experiment_id)
        self.assertTrue(self.folder.folder_id == test_trial.folder_id)
        self.assertTrue(self.trial_dir == test_trial.trial_dir)
        self.assertFalse(self.session.session_date != test_trial.trial_date)
