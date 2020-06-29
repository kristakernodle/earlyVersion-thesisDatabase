from database.cursors import Cursor, TestingCursor

import utilities as utils
from models.experiments import Experiments
from models.mouse import Mouse


class Session:

    def __init__(self, mouse, experiment, session_date, session_dir, session_id=None):
        self.mouse = mouse
        self.experiment = experiment
        self.session_date = utils.convert_date_int_yyyymmdd(session_date)
        self.session_dir = session_dir
        self.session_id = session_id

    def __str__(self):
        return f"< Session {self.session_dir} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Session):
            return NotImplemented
        return self.session_id == compare_to.session_id

    @classmethod
    def __from_db(cls, cursor, session_dir, testing, postgresql):
        cursor.execute("SELECT * FROM sessions WHERE session_dir = %s", (session_dir,))
        session_data = cursor.fetchone()
        if session_data is None:
            print(f"No session in the database with directory {session_dir}")
            return None
        return cls(mouse=Mouse.from_db_by_id(session_data[1], testing, postgresql),
                   experiment=Experiments.from_db_by_id(session_data[2], testing, postgresql),
                   session_date=session_data[3], session_dir=session_data[4], session_id=session_data[0])

    @classmethod
    def from_db(cls, trial_dir, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                return cls.__from_db(cursor, trial_dir, testing, postgresql)
        else:
            with Cursor() as cursor:
                return cls.__from_db(cursor, trial_dir, testing, postgresql)

    def save_to_db(self, testing=False, postgresql=None):

        def main(a_cursor, session_dir):
            cursor.execute(
                "INSERT INTO sessions (mouse_id,  experiment_id, session_date, session_dir) VALUES (%s, %s, %s, %s);",
                (self.mouse.mouse_id, self.experiment.experiment_id, utils.convert_date_int_yyyymmdd(self.session_date),
                 self.session_dir))
            return self.__from_db(a_cursor, session_dir, testing, postgresql)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main(cursor, self.session_dir)
        else:
            with Cursor() as cursor:
                return main(cursor, self.session_dir)
