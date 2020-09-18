import unittest
import testing.postgresql as tpg

from archive.models import Session
from archive.models import Folder

from archive.database import test_session_table_seed

Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True,
                                   on_initialized=archive.database.handlers.handlers.handler_create_folders_table)


def tearDownModule():
    Postgresql.clear_cache()


class TestNewFolder(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        archive.database.handlers.handlers.handler_seed_sessions_table(self.postgresql)
        self.session = Session.from_db(session_dir='/exp/one/dir/9990/20200503_S2', testing=True,
                                       postgresql=self.postgresql)
        self.folder_dir = '/exp/one/dir/9990/20200503_S2/Reaches02'

    def tearDown(self):
        self.postgresql.stop()

    # @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_add_new_session(self):
        test_folder = Folder(self.session.session_id, self.folder_dir).save_to_db(testing=True,
                                                                                  postgresql=self.postgresql)
        self.assertFalse(test_folder.folder_id is None)

    def test_duplicate_session(self):
        test_folder = Folder(self.session.session_id, self.folder_dir).save_to_db(testing=True,
                                                                                  postgresql=self.postgresql)
        dup_folder = test_folder.save_to_db(testing=True, postgresql=self.postgresql)
        self.assertFalse(dup_folder.folder_id is None)


class TestLoadFolder(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        archive.database.handlers.handlers.handler_seed_folders_table(self.postgresql)
        seed_sessions = list(test_session_table_seed.keys())
        seed_eartag, seed_experiment = seed_sessions.pop()
        all_sessions = test_session_table_seed[seed_eartag, seed_experiment]
        session_date, session_dir = all_sessions.pop()
        self.session = Session.from_db(session_dir=session_dir, testing=True, postgresql=self.postgresql)
        self.folder_dir = '/'.join([session_dir, 'Reaches01'])

    def tearDown(self):
        self.postgresql.stop()

    # @unittest.skip("Not currently testing")
    def test_setUp_tearDown(self):
        self.assertTrue(1)

    def test_from_db(self):
        load_folder = Folder.from_db(folder_dir=self.folder_dir, testing=True, postgresql=self.postgresql)
        self.assertEqual(self.session.session_id, load_folder.session_id)
        self.assertEqual(self.folder_dir, load_folder.folder_dir)
        self.assertFalse(load_folder.folder_id is None)


if __name__ == '__main__':
    unittest.main()
