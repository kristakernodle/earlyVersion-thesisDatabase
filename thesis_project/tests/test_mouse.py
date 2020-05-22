import unittest
from models.mouse import Mouse
from database import Database
from data.constants import dbConnection_Krista


class TestNewMouse(unittest.TestCase):

    def setUp(self):
        self.test_mouse = Mouse(9999, 20200521, 'knock out', 'female')
        Database.initialize(**dbConnection_Krista)
        self.test_mouse.save_to_db()

    def tearDown(self):
        self.load_mouse.delete_from_db()

    def test_from_db_eartag(self):
        self.load_mouse = Mouse.from_db(9999)
        self.assertEqual(self.test_mouse.eartag, self.load_mouse.eartag)

    def test_from_db_birthdate(self):
        self.load_mouse = Mouse.from_db(9999)
        self.assertEqual(self.test_mouse.birthdate, self.load_mouse.birthdate)

    def test_from_db_genotype(self):
        self.load_mouse = Mouse.from_db(9999)
        self.assertEqual(self.test_mouse.genotype, self.load_mouse.genotype)

    def test_from_db_sex(self):
        self.load_mouse = Mouse.from_db(9999)
        self.assertEqual(self.test_mouse.sex, self.load_mouse.sex)

    def test_from_db_mouse_id(self):
        self.load_mouse = Mouse.from_db(9999)
        self.assertFalse(self.load_mouse.mouse_id is None)

class TestAddParticipant(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_participant(self):
        pass


if __name__ == '__main__':
    unittest.main()
