import unittest
import testing.postgresql as tpg
from archive.database import TestingCursor

from archive.models import Folder
from archive.models import BlindFolder
import archive.models.reviewers
import archive.models.blind_folders

from archive import models, utilities as utils

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=archive.database.handlers.handlers.handler_create_blind_folders_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewBlindFolder(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        archive.database.handlers.handlers.handler_seed_blind_folders_table(self.postgresql)
        with TestingCursor(self.postgresql) as cursor:
            all_folder_dir = archive.models.folders.list_all_folder_dir(cursor)
            all_reviewer_ids = archive.models.reviewers.list_all_reviewer_ids(cursor)
        self.folder = Folder.from_db(folder_dir=all_folder_dir.pop(), testing=True, postgresql=self.postgresql)
        self.reviewer_id = all_reviewer_ids.pop()
        self.blind_name = utils.random_string_generator(10)

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_blind_folder(self):
        test_blind_folder = BlindFolder(self.folder.folder_id, self.reviewer_id,
                                        self.blind_name).save_to_db(testing=True, postgresql=self.postgresql)
        self.assertFalse(test_blind_folder.blind_folder_id is None)

    def test_duplicate_session(self):
        test_folder = BlindFolder(self.folder.folder_id, self.reviewer_id,
                                  self.blind_name).save_to_db(testing=True, postgresql=self.postgresql)
        dup_folder = test_folder.save_to_db(testing=True, postgresql=self.postgresql)
        self.assertFalse(dup_folder.folder_id is None)


class TestLoadBlindFolder(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        archive.database.handlers.handlers.handler_seed_blind_folders_table(self.postgresql)
        with TestingCursor(self.postgresql) as cursor:
            # noinspection PyUnresolvedReferences
            all_blind_names = models.blind_folders.list_all_blind_names(cursor)
        self.blind_name = all_blind_names.pop()

    def tearDown(self):
        self.postgresql.stop()

    @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertIsNotNone(self.blind_name)
        self.assertTrue(1)

    def test_from_db(self):
        load_blind_folder = BlindFolder.from_db(blind_name=self.blind_name, testing=True, postgresql=self.postgresql)
        self.assertFalse(load_blind_folder is None)


if __name__ == '__main__':
    unittest.main()
