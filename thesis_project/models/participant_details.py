import json

import utilities as utils
from models.mouse import Mouse
from models.experiments import Experiments
from models.cursors import TestingCursor, Cursor


class ParticipantDetails:
    def __init__(self, mouse, experiment, start_date=None, end_date=None,
                 exp_spec_details=None, detail_id=None):
        self.mouse = mouse
        self.experiment = experiment
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
        if len(participant_details) == 3:
            return cls(mouse, experiment)
        elif len(participant_details) == 4:
            if  # TODO Finish this bit...

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
