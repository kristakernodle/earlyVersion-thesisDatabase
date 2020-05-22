from database import Database, Cursor
import utilities as util
from models.mouse import Mouse
import pathlib
from data.constants import sharedx_prefix


class Experiments:
    def __init__(self, experiment_name, experiment_dir, experiment_id=None):
        self.experiment_name = util.prep_string_for_db(experiment_name)
        if type(experiment_name) == str:
            self.experiment_dir = pathlib.PurePath(experiment_dir)
        else:
            self.experiment_dir = experiment_dir
        self.experiment_id = experiment_id

    def __str__(self):
        return f"< Experiment {self.experiment_name} >"

    @classmethod
    def from_db(cls, experiment_name):
        experiment_name = util.prep_string_for_db(experiment_name)
        with Cursor() as cursor:
            cursor.execute("SELECT * FROM experiments WHERE experiment_name = %s;", (experiment_name,))
            exp = cursor.fetchone()
            return cls(experiment_name=exp[2], experiment_dir=pathlib.PurePath(sharedx_prefix, exp[1]), experiment_id=exp[0])

    def save_to_db(self):
        experiment_name = util.prep_string_for_db(self.experiment_name)
        with Cursor() as cursor:
            cursor.execute("INSERT INTO experiments(experiment_dir, experiment_name) VALUES(%s, %s);",
                           (self.experiment_dir.name, experiment_name))
        return self.from_db(experiment_name)

    def delete_from_db(self):
        with Cursor() as cursor:
            cursor.execute("DELETE FROM experiments WHERE experiment_id = %s", (self.experiment_id,))

    @classmethod
    def list_participants(cls, experiment_name=None):
        if experiment_name is not None:
            experiment_name = util.prep_string_for_db(experiment_name)
            with Cursor() as cursor:
                cursor.execute("SELECT eartag FROM all_participants_all_experiments WHERE experiment_name = %s;",
                               (experiment_name,))
                participants = cursor.fetchall()
        else:
            with Cursor() as cursor:
                cursor.execute("SELECT eartag FROM all_participants_all_experiments;")
                participants = cursor.fetchall()
        participants = [Mouse.from_db(eartag) for eartag in participants]
        return participants




