from models.mouse import Mouse
import models.experiments as exp
from database import Cursor
import utilities as utils


class ParticipantDetails:
    def __init__(self, eartag, experiment_name, start_date, end_date,
                 exp_spec_details=None, detail_id=None):
        self.mouse = Mouse.from_db(eartag)
        self.experiment = exp.Experiments.from_db(experiment_name)
        self.start_date = utils.convert_date_int_yyyymmdd(start_date)
        self.end_date = utils.convert_date_int_yyyymmdd(end_date)
        self.exp_spec_details = exp_spec_details
        self.detail_id = detail_id

    def __str__(self):
        return f"< Participant {self.mouse.eartag} in {self.experiment.experiment_name} >"

    @classmethod
    def from_db(cls, eartag, experiment_name):
        mouse = Mouse.from_db(eartag)
        experiment = exp.Experiments.from_db(experiment_name)
        with Cursor() as cursor:
            cursor.execute("SELECT * FROM participant_details WHERE mouse_id = %s AND experiment_id = %s;",
                           (mouse.mouse_id, experiment.experiment_id))
            participant = cursor.fetchone()
            mouse.mouse_id = participant[0]
        return mouse

    def save_to_db(self):
        with Cursor() as cursor:
            cursor.execute("INSERT INTO participant_details "
                           "    (mouse_id, experiment_id, start_date, end_date, exp_spec_details) "
                           "VALUES "
                           "    (%s, %s, %s, %s, %s);",
                           (self.mouse.mouse_id, self.experiment.experiment_id,
                            self.start_date, self.end_date, self.exp_spec_details))
        return self.from_db(self.mouse.eartag, self.experiment.experiment_name)

    def delete_from_db(self):
        with Cursor() as cursor:
            cursor.execute("DELETE FROM participant_details WHERE detail_id = %s", (self.detail_id,))

