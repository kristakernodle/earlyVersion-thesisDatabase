import unittest
from models.mouse import Mouse
from models.experiments import Experiments
from database import Database
from data.constants import dbConnection_Krista
import utilities as util


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

    test_mouse_table_seed = [(9990, 20200102, 'wild type', 'male', True, 'test experiment one', 20200501, 20200601),
                             (9991, 20200101, 'wild type', 'male', False, 'test experiment two', 20200515, 20200615),
                             (9992, 20200101, 'wild type', 'male', True, 'test experiment one', 20200501, 20200601),
                             (9993, 20200101, 'wild type', 'male', False, 'test experiment two', 20200515, 20200615),
                             (9994, 20200101, 'wild type', 'female', True, 'test experiment one', 20200501, 20200601),
                             (9995, 20200101, 'wild type', 'female', False, 'test experiment two', 20200515, 20200615),
                             (9996, 20200101, 'knock out', 'female', True, 'test experiment one', 20200501, 20200601),
                             (9997, 20200101, 'knock out', 'female', False, 'test experiment two', 20200515, 20200615),
                             (9998, 20200101, 'knock out', 'female', True, 'test experiment one', 20200501, 20200601),
                             (9999, 20200102, 'knock out', 'female', False, 'test experiment two', 20200515, 20200615)]
    experiment_name_one = 'test experiment one'
    experiment_name_two = 'test experiment two'
    experiment_dir_one = '/test/directory/experiment/one'
    experiment_dir_two = '/test/directory/experiment/two'

    def setUp(self):
        Database.initialize(**dbConnection_Krista)
        self.test_experiment_one = Experiments(self.experiment_name_one, self.experiment_dir_one).save_to_db()
        self.test_experiment_two = Experiments(self.experiment_name_two, self.experiment_dir_two).save_to_db()
        self.test_participants_list = []
        for mouse in self.test_mouse_table_seed:
            self.test_participants_list.append(Mouse(eartag=mouse[0], birthdate=mouse[1],
                                                     genotype=mouse[2], sex=mouse[3]).save_to_db())

    def tearDown(self):
        for mouse_detail in self.test_mouse_details:
            mouse_detail.delete_from_db()
        for mouse in self.test_participants_list:
            mouse.delete_from_db()
        self.test_experiment_one.delete_from_db()
        self.test_experiment_two.delete_from_db()

    def test_add_participant(self):
        self.test_mouse_details = []
        for mouse in self.test_mouse_table_seed:
            if util.prep_string_for_db(mouse[5]) == util.prep_string_for_db(self.test_experiment_one.experiment_name):
                self.test_mouse_details.append(Mouse.from_db(mouse[0])
                                               .add_participant(util.prep_string_for_db(self
                                                                                        .test_experiment_one
                                                                                        .experiment_name)))
            elif util.prep_string_for_db(mouse[5]) == util.prep_string_for_db(self.test_experiment_two.experiment_name):
                self.test_mouse_details\
                    .append(Mouse.from_db(mouse[0])
                            .add_participant(util
                                             .prep_string_for_db(self
                                                                 .test_experiment_two.experiment_name)))
        self.assertListEqual(sorted(self.test_participants_list, key=lambda m: m.eartag),
                             sorted(Experiments.list_participants(), key=lambda m: m.eartag))


if __name__ == '__main__':
    unittest.main()
