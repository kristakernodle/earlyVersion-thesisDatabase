import unittest
from models.experiments import Experiments
from database import Database
from data.constants import dbConnection_Krista
import os


class TestNewExperiment(unittest.TestCase):

    def setUp(self):
        self.test_exp = Experiments('test experiment', '/Volumes/SharedX/Neuro-Leventhal/data/')
        Database.initialize(**dbConnection_Krista)
        self.test_exp.save_to_db()

    def tearDown(self):
        self.load_exp.delete_from_db()

    def test_from_db_name(self):
        self.load_exp = Experiments.from_db('test experiment')
        self.assertEqual(self.test_exp.experiment_name, self.load_exp.experiment_name)

    def test_from_db_directory(self):
        self.load_exp = Experiments.from_db('test experiment')
        self.assertEqual(self.test_exp.experiment_dir, self.load_exp.experiment_dir)

    def test_from_db_exp_id(self):
        self.load_exp = Experiments.from_db('test experiment')
        self.assertFalse(self.load_exp.experiment_id is None)


if __name__ == '__main__':
    unittest.main()
