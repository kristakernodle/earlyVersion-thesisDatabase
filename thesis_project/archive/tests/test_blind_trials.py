import unittest

import testing.postgresql as tpg

from archive import models
from archive.database import TestingCursor
from archive.models import Folder
from archive.models import Trial
from archive.models import BlindFolder
from archive.models import Reviewer
from archive.models import BlindTrial

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=archive.database.handlers.handlers.handler_create_blind_trials_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewBlindTrial(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        archive.database.handlers.handlers.handler_seed_trials_table(self.postgresql)
        archive.database.handlers.handlers.handler_seed_reviewers_table(self.postgresql)
        with TestingCursor(self.postgresql) as cursor:
            archive.database.handlers.handlers.handler_seed_blind_folders_table_only(cursor)
            blind_name = models.blind_folders.list_all_blind_names(cursor).pop()
        trial = 'trial_1.txt'
        self.blind_folder = BlindFolder.from_db(blind_name=blind_name, testing=True, postgresql=self.postgresql)
        self.folder = Folder.from_db(folder_id=self.blind_folder.folder_id, testing=True, postgresql=self.postgresql)
        self.reviewer = Reviewer.from_db(reviewer_id=self.blind_folder.reviewer_id,
                                         testing=True, postgresql=self.postgresql)
        self.trial = Trial.from_db(trial_dir='/'.join([self.folder.folder_dir, trial]),
                                   testing=True, postgresql=self.postgresql)
        self.full_path = '/'.join([self.reviewer.toScore_dir, self.blind_folder.blind_name,
                                   self.blind_folder.blind_name + '_1.txt'])

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_blind_trial(self):
        test_blind_trial = BlindTrial(self.trial.trial_id, self.folder.folder_id,
                                      self.full_path).save_to_db(testing=True, postgresql=self.postgresql)
        self.assertFalse(test_blind_trial.blind_trial_id is None)


class TestLoadBlindTrial(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        archive.database.handlers.handlers.handler_seed_trials_table(self.postgresql)
        archive.database.handlers.handlers.handler_seed_reviewers_table(self.postgresql)
        archive.database.handlers.handlers.handler_seed_blind_trials(self.postgresql)

        with TestingCursor(self.postgresql) as cursor:
            all_blind_names = models.blind_folders.list_all_blind_names(cursor)
        blind_name = all_blind_names.pop()
        trial_file = 'trial_1.txt'
        self.blind_folder = BlindFolder.from_db(blind_name=blind_name, testing=True, postgresql=self.postgresql)
        self.folder = Folder.from_db(folder_id=self.blind_folder.folder_id, testing=True, postgresql=self.postgresql)
        self.reviewer = Reviewer.from_db(reviewer_id=self.blind_folder.reviewer_id,
                                         testing=True, postgresql=self.postgresql)
        self.trial = Trial.from_db(trial_dir='/'.join([self.folder.folder_dir, trial_file]),
                                   testing=True, postgresql=self.postgresql)
        self.full_path = '/'.join([self.reviewer.toScore_dir, self.blind_folder.blind_name,
                                   self.blind_folder.blind_name + trial_file])

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_from_db(self):
        test_blind_trial = BlindTrial.from_db(full_path=self.full_path, testing=True, postgresql=self.postgresql)
        self.assertIsNotNone(test_blind_trial)
