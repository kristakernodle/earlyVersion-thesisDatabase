import utilities as utils
from models.mouse import Mouse
from models.experiments import Experiments
from database.cursors import TestingCursor, Cursor


class Trials:

    def __init__(self, mouse, experiment, trial_dir, trial_date, trial_id=None):
        self.mouse = mouse
        self.experiment = experiment
        self.trial_dir = trial_dir
        self.trial_date = trial_date
        self.trial_id = trial_id

    def __str__(self):
        return f"< Trial {self.trial_dir} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Trials):
            return NotImplemented
        return self.trial_id == compare_to.trial_id

    @classmethod
    def __from_db(cls, cursor, trial_dir, testing, postgresql):
        cursor.execute("SELECT * FROM trials WHERE trial_dir = %s", (trial_dir,))
        trial_data = cursor.fetchone()
        if trial_data is None:
            print(f"No trial in the database with directory {trial_dir}")
            return None
        return cls(mouse=Mouse.from_db_by_id(trial_data[2], testing, postgresql),
                   experiment=Experiments.from_db_by_id(trial_data[1], testing, postgresql),
                   trial_dir=trial_data[3], trial_date=trial_data[4], trial_id=trial_data[0])

    @classmethod
    def from_db(cls, trial_dir, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                return cls.__from_db(cursor, trial_dir, testing, postgresql)
        else:
            with Cursor() as cursor:
                return cls.__from_db(cursor, trial_dir, testing, postgresql)

    def __save_to_db(self, cursor):
        cursor.execute("INSERT INTO trials (experiment_id, mouse_id, trial_dir, trial_date) VALUES (%s, %s, %s, %s);",
                       (self.experiment.experiment_id, self.mouse.mouse_id, self.trial_dir,
                        utils.convert_date_int_yyyymmdd(self.trial_date)))

    def save_to_db(self, testing=False, postgresql=None):

        def main(a_cursor, trial_dir):
            self.__save_to_db(a_cursor)
            return self.__from_db(a_cursor, trial_dir, testing, postgresql)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main(cursor, self.trial_dir)
        else:
            with Cursor() as cursor:
                return main(cursor, self.trial_dir)

    # def __delete_from_db(self, cursor):
    #     cursor.execute("DELETE FROM mouse WHERE mouse_id = %s", (self.mouse_id,))
    #
    # def delete_from_db(self, testing=False, postgresql=None):
    #     if testing:
    #         with TestingCursor(postgresql) as cursor:
    #             self.__delete_from_db(cursor)
    #     else:
    #         with Cursor() as cursor:
    #             self.__delete_from_db(cursor)
