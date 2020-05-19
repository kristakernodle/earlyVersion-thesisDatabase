from database import Cursor


class ParticipantDetails:
    def __init__(self, eartag, experiment_name, start_date, end_date,
                 exp_spec_details=None, detail_id=None, mouse_id=None, experiment_id=None):
        self.eartag = eartag
        self.experiment_name = experiment_name
        self.start_date = start_date
        self.end_date = end_date
        self.exp_spec_details = exp_spec_details
        self.detail_id = detail_id
        self.mouse_id = mouse_id
        self.experiment_id = experiment_id

    def __str__(self):
        return f"< Participant {self.eartag} in {self.experiment_name} >"

    @classmethod
    def from_db(cls, eartag, experiment_name):
        with Cursor() as cursor:
            cursor.execute("SELECT * FROM participant_details WHERE eartag = %s AND experiment_name = %s;",
                           (eartag, experiment_name))
            participant = cursor.fetchone()
        return cls(eartag=participant[6], experiment_name=participant[7], start_date=participant[3],
                   end_date=participant[4], exp_spec_details=participant[5], detail_id=participant[0],
                   mouse_id=participant[1], experiment_id=participant[2])

    def save_to_db(self):
        with Cursor() as cursor:
            cursor.execute("INSERT INTO participant_details (detail_id, mouse_id, experiment_id, start_date, end_date, "
                           "exp_spec_details, eartag, experiment_name) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);",
                           (self.detail_id, self.mouse_id, self.experiment_id, self.start_date, self.end_date,
                            self.exp_spec_details, self.eartag, self.experiment_name))
