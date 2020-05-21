import unittest
from models.mouse import Mouse
from models.experiments import Experiments
from models.trials import Trials
from database import Database
from data.constants import dbConnection_Krista


class TestNewTrial(unittest.TestCase):
    trial_dir = '/Volumes/SharedX/Neuro-Leventhal/data/experiment/subject/session_type/session/trial/'

    def setUp(self):
        self.test_mouse = Mouse(9999, 20200521, 'knock out', 'female')
        self.test_exp = Experiments('test experiment', '/Volumes/SharedX/Neuro-Leventhal/data/')
        self.test_trial = Trials(self.test_exp.experiment_id, self.test_mouse.mouse_id, self.trial_dir)

        Database.initialize(**dbConnection_Krista)
        self.__test_trial = self.test_trial.save_to_db()

    def tearDown(self):
        self.__test_trial.delete_from_db()

    def test_from_db_experiment_id(self):
        self.load_trial = Trials.from_db(self.trial_dir)
        self.assertEqual(self.test_trial.experiment_id, self.load_trial.experiment_id)

    def test_from_db_mouse_id(self):
        self.load_trial = Trials.from_db(self.trial_dir)
        self.assertEqual(self.test_trial.mouse_id, self.load_trial.mouse_id)

    def test_from_db_trial_id(self):
        self.load_trial = Trials.from_db(self.trial_dir)
        self.assertFalse(self.load_trial.trial_id is None)


if __name__ == '__main__':
    unittest.main()
