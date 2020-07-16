import utilities as utils
from models.mouse import Mouse
from models.experiments import Experiments
from database.cursors import TestingCursor, Cursor


def list_all_trial_dirs(cursor):
    cursor.execute("SELECT trial_dir FROM trials;")
    return list(item for tup in cursor.fetchall() for item in tup)


class Trial:

    def __init__(self, experiment_id, folder_id, trial_dir, trial_date, trial_id=None):
        self.experiment_id = experiment_id
        self.folder_id = folder_id
        self.trial_dir = trial_dir
        self.trial_date = utils.convert_date_int_yyyymmdd(trial_date)
        self.trial_id = trial_id

    def __str__(self):
        return f"< Trial {self.trial_dir} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Trial):
            return NotImplemented
        return self.trial_id == compare_to.trial_id

    @classmethod
    def __from_db(cls, cursor, trial_dir):
        cursor.execute("SELECT * FROM trials WHERE trial_dir = %s", (trial_dir,))
        trial_data = cursor.fetchone()
        if trial_data is None:
            print(f"No trial in the database with directory {trial_dir}")
            return None
        return cls(experiment_id=trial_data[1], folder_id=trial_data[2], trial_dir=trial_data[3],
                   trial_date=trial_data[4], trial_id=trial_data[0])

    @classmethod
    def from_db(cls, trial_dir, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                return cls.__from_db(cursor, trial_dir)
        else:
            with Cursor() as cursor:
                return cls.__from_db(cursor, trial_dir)

    def save_to_db(self, testing=False, postgresql=None):

        def main(a_cursor, trial_dir):
            cursor.execute(
                "INSERT INTO trials (experiment_id, folder_id, trial_dir, trial_date) VALUES (%s, %s, %s, %s);",
                (self.experiment_id, self.folder_id, self.trial_dir,
                 utils.convert_date_int_yyyymmdd(self.trial_date)))
            return self.__from_db(a_cursor, trial_dir)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main(cursor, self.trial_dir)
        else:
            with Cursor() as cursor:
                return main(cursor, self.trial_dir)

    @classmethod
    def list_participants(cls, experiment_name, testing=False, postgresql=None):

        def main(a_cursor, experiment_id):
            a_cursor.execute("SELECT eartag FROM all_participants_all_trials "
                             "WHERE experiment_id = %s;", (experiment_id,))
            no_dups = sorted(set(utils.list_from_cursor(cursor.fetchall())), key=int)
            return no_dups

        experiment = Experiments.from_db(experiment_name, testing, postgresql)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main(cursor, experiment.experiment_id)
        else:
            with Cursor() as cursor:
                return main(cursor, experiment.experiment_id)

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
