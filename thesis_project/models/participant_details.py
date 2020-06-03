import utilities as utils
from models.mouse import Mouse
from models.experiments import Experiments
from database.cursors import TestingCursor, Cursor


class ParticipantDetails:
    def __init__(self, mouse, experiment, participant_dir=None, start_date=None, end_date=None,
                 exp_spec_details=None, detail_id=None):
        self.mouse = mouse
        self.experiment = experiment
        self.participant_dir = participant_dir
        self.start_date = utils.convert_date_int_yyyymmdd(start_date)
        self.end_date = utils.convert_date_int_yyyymmdd(end_date)
        self.exp_spec_details = exp_spec_details
        self.detail_id = detail_id

    def __str__(self):
        return f"< Participant {self.mouse.eartag} in {self.experiment.experiment_name} >"

    @classmethod
    def __from_db(cls, cursor, mouse, experiment):
        cursor.execute("SELECT * FROM participant_details WHERE mouse_id = %s AND experiment_id = %s;",
                       (mouse.mouse_id, experiment.experiment_id))
        participant_details = cursor.fetchone()
        return cls(mouse, experiment, participant_dir=participant_details[6], start_date=participant_details[3],
                   end_date=participant_details[4],
                   exp_spec_details=participant_details[5], detail_id=participant_details[0])

    @classmethod
    def from_db(cls, eartag, experiment_name, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                mouse = Mouse.from_db(eartag, testing=True, postgresql=postgresql)
                experiment = Experiments.from_db(experiment_name, testing=True, postgresql=postgresql)
                return cls.__from_db(cursor, mouse, experiment)
        else:
            with Cursor() as cursor:
                mouse = Mouse.from_db(eartag, testing=True, postgresql=postgresql)
                experiment = Experiments.from_db(experiment_name, testing=True, postgresql=postgresql)
                return cls.__from_db(cursor, mouse, experiment)

    def __save_to_db(self, cursor):
        cursor.execute("INSERT INTO participant_details "
                       "(mouse_id, experiment_id, start_date, end_date, exp_spec_details) "
                       "VALUES (%s, %s, %s, %s, %s);",
                       (self.mouse.mouse_id, self.experiment.experiment_id,
                        self.start_date, self.end_date, self.exp_spec_details))

    def save_to_db(self, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                self.__save_to_db(cursor)
                return self.__from_db(cursor, self.mouse, self.experiment)
        else:
            with Cursor() as cursor:
                self.__save_to_db(cursor)
                return self.__from_db(cursor, self.mouse, self.experiment)

    @classmethod
    def __list_participants(cls, cursor, experiment_id):
        cursor.execute("SELECT eartag FROM all_participants_all_experiments WHERE experiment_id = %s;",
                       (experiment_id,))
        return utils.list_from_cursor(cursor.fetchall())

    @classmethod
    def list_participants(cls, experiment_name, testing=False, postgresql=None):
        # First: Get the experiment_id
        experiment = Experiments.from_db(experiment_name, testing, postgresql)
        # Second: Define the cursor
        if testing:
            with TestingCursor(postgresql) as cursor:
                return cls.__list_participants(cursor, experiment.experiment_id)
        else:
            with Cursor() as cursor:
                return cls.__list_participants(cursor, experiment.experiment_id)
