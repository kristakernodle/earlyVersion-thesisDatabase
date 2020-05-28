from models.cursors import TestingCursor, Cursor
import utilities as util


def list_all_experiments(cursor):
    cursor.execute("SELECT experiment_name FROM experiments;")
    return list(item for tup in cursor.fetchall() for item in tup)


class Experiments:
    def __init__(self, experiment_name, experiment_dir, experiment_id=None):
        self.experiment_name = util.prep_string_for_db(experiment_name)
        self.experiment_dir = experiment_dir
        self.experiment_id = experiment_id

    def __str__(self):
        return f"< Experiment {self.experiment_name} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Experiments):
            return NotImplemented
        return self.experiment_id == compare_to.experiment_id

    @classmethod
    def __from_db(cls, cursor, experiment_name):
        cursor.execute("SELECT * FROM experiments WHERE experiment_name = %s;", (experiment_name,))
        exp = cursor.fetchone()
        return cls(experiment_name=exp[2], experiment_dir=exp[1],
                   experiment_id=exp[0])

    @classmethod
    def from_db(cls, experiment_name, testing=False, postgresql=None):
        experiment_name = util.prep_string_for_db(experiment_name)
        if testing:
            with TestingCursor(postgresql) as cursor:
                return cls.__from_db(cursor, experiment_name)
        else:
            with Cursor() as cursor:
                return cls.__from_db(cursor)

    def __save_to_db(self, cursor):
        cursor.execute("INSERT INTO experiments(experiment_dir, experiment_name) VALUES(%s, %s);",
                       (self.experiment_dir, self.experiment_name))

    def save_to_db(self, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                if self.experiment_name not in list_all_experiments(cursor):
                    self.__save_to_db(cursor)
                return self.__from_db(cursor, self.experiment_name)
        else:
            with Cursor() as cursor:
                if self.experiment_name not in list_all_experiments(cursor):
                    self.__save_to_db(cursor)
                return self.__from_db(cursor, self.experiment_name)

    def __delete_from_db(self, cursor):
        cursor.execute("DELETE FROM experiments WHERE experiment_id = %s", (self.experiment_id,))

    def delete_from_db(self, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                self.__delete_from_db(cursor)
        else:
            with Cursor() as cursor:
                self.__delete_from_db(cursor)

    # @classmethod
    # def list_participants(cls, experiment_name=None):
    #     if experiment_name is not None:
    #         experiment_name = util.prep_string_for_db(experiment_name)
    #         with Cursor() as cursor:
    #             cursor.execute("SELECT eartag FROM all_participants_all_experiments WHERE experiment_name = %s;",
    #                            (experiment_name,))
    #             participants = cursor.fetchall()
    #     else:
    #         with Cursor() as cursor:
    #             cursor.execute("SELECT eartag FROM all_participants_all_experiments;")
    #             participants = cursor.fetchall()
    #     participants = [Mouse.from_db(eartag) for eartag in participants]
    #     return participants
    #
    # def add_participant(self, eartag, start_date=None, end_date=None):
    #     return ParticipantDetails(eartag, self.experiment_name, start_date=start_date, end_date=end_date).save_to_db()
    #
    # @classmethod
    # def is_member_db(cls, experiment_dir):
    #     if type(experiment_dir) == str:
    #         experiment_dir = pathlib.PurePath(experiment_dir)
    #     else:
    #         experiment_dir = experiment_dir
    #     with Cursor() as cursor:
    #         cursor.execute("SELECT * FROM experiments WHERE experiment_dir = %s", (experiment_dir.name,))
    #         if cursor.fetchone() is None:
    #             return False
    #     return True
