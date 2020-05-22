import unittest
from data.constants import dbConnection_Krista
from database import Database
from models.experiments import Experiments
from models.mouse import Mouse
from models.participant_details import ParticipantDetails
import datetime


class TestNewParticipantDetails(unittest.TestCase):
    eartag = 9999
    experiment_name = 'test experiment'

    def setUp(self):
        Database.initialize(**dbConnection_Krista)
        self.test_mouse = Mouse(self.eartag, 20200521, 'knock out', 'female').save_to_db()
        self.test_exp = Experiments(self.experiment_name, '/Volumes/SharedX/Neuro-Leventhal/data/').save_to_db()
        self.test_participant_details = ParticipantDetails(self.test_mouse.eartag, self.test_exp.experiment_name, 20200501, 20200521).save_to_db()

    def tearDown(self):
        self.test_participant_details.delete_from_db()
        self.test_mouse.delete_from_db()
        self.test_exp.delete_from_db()

    def test_from_db_mouse(self):
        self.load_participant_details = ParticipantDetails.from_db(self.eartag, self.experiment_name)
        self.assertEqual(self.test_mouse.mouse_id, self.load_participant_details.mouse.mouse_id)

    def test_from_db_experiment(self):
        self.load_participant_details = ParticipantDetails.from_db(self.eartag, self.experiment_name)
        self.assertEqual(self.test_exp.experiment_id, self.load_participant_details.experiment.experiment_id)

    def test_from_db_start_date(self):
        self.load_participant_details = ParticipantDetails.from_db(self.eartag, self.experiment_name)
        self.assertIsInstance(self.load_participant_details.start_date, datetime.date)

    def test_from_db_end_date(self):
        self.load_participant_details = ParticipantDetails.from_db(self.eartag, self.experiment_name)
        self.assertIsInstance(self.load_participant_details.end_date, datetime.date)

    def test_from_db_mouse_id(self):
        self.load_participant_details = ParticipantDetails.from_db(self.eartag, self.experiment_name)
        self.assertFalse(self.load_participant_details.detail_id is None)


if __name__ == '__main__':
    unittest.main()
