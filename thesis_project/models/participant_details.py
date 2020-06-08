from psycopg2._json import Json

import utilities as utils
from models.mouse import Mouse
from models.experiments import Experiments
from database.cursors import TestingCursor, Cursor


def list_all_detail_ids(cursor):
    cursor.execute("SELECT detail_id FROM participant_details;")
    return utils.list_from_cursor(cursor.fetchall())


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
                mouse = Mouse.from_db(eartag, testing=testing, postgresql=postgresql)
                experiment = Experiments.from_db(experiment_name, testing=testing, postgresql=postgresql)
                return cls.__from_db(cursor, mouse, experiment)
        else:
            with Cursor() as cursor:
                mouse = Mouse.from_db(eartag)
                experiment = Experiments.from_db(experiment_name)
                return cls.__from_db(cursor, mouse, experiment)

    def save_to_db(self, testing=False, postgresql=None):

        def save_to_db(a_cursor, mouse_id, experiment_id, start_date, end_date, exp_spec_details):
            a_cursor.execute("INSERT INTO participant_details "
                             "(mouse_id, experiment_id, start_date, end_date, exp_spec_details) "
                             "VALUES (%s, %s, %s, %s, %s);",
                             (mouse_id, experiment_id, start_date, end_date, Json(exp_spec_details)))

        def update_details(a_cursor, start_date, end_date, exp_spec_details, participant_dir, detail_id):
            a_cursor.execute("UPDATE participant_details "
                             "SET (start_date, end_date, exp_spec_details, participant_dir) = (%s, %s, %s, %s) "
                             "WHERE detail_id = %s;",
                             (start_date, end_date, Json(exp_spec_details), participant_dir, detail_id))

        def save_to_db_main(a_cursor):
            if self.detail_id not in list_all_detail_ids(a_cursor):
                save_to_db(a_cursor, self.mouse.mouse_id, self.experiment.experiment_id,
                           self.start_date, self.end_date, self.exp_spec_details)
            else:
                update_details(a_cursor, self.start_date, self.end_date, self.exp_spec_details,
                               self.participant_dir, self.detail_id)
            return self.__from_db(a_cursor, self.mouse, self.experiment)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(cursor)

    @classmethod
    def __list_participants(cls, cursor, experiment_id):
        cursor.execute("SELECT eartag FROM all_participants_all_experiments WHERE experiment_id = %s;",
                       (experiment_id,))
        return utils.list_from_cursor(cursor.fetchall())

    @classmethod
    def list_participants(cls, experiment_name, testing=False, postgresql=None):

        experiment_id = Experiments.get_id(experiment_name, testing, postgresql)
        if len(experiment_id) == 1:
            experiment_id = experiment_id[0]

        if testing:
            with TestingCursor(postgresql) as cursor:
                return cls.__list_participants(cursor, experiment_id)
        else:
            with Cursor() as cursor:
                return cls.__list_participants(cursor, experiment_id)
