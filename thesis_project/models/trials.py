from database import Cursor


class Trials:
    def __init__(self, experiment_id, mouse_id, trial_dir, trial_id=None):
        self.trial_id = trial_id
        self.experiment_id = experiment_id
        self.mouse_id = mouse_id
        self.trial_dir = trial_dir

    def __str__(self):
        return f"< Trial {self.trial_dir} >"

    @classmethod
    def from_db(cls, trial_dir):
        with Cursor() as cursor:
            cursor.execute("SELECT * FROM trials WHERE trial_dir = %s;", (trial_dir,))
            trial = cursor.fetchone()
            return cls(experiment_id=trial[1], mouse_id=trial[2], trial_dir=trial[3], trial_id=trial[0])

    def save_to_db(self):
        with Cursor() as cursor:
            cursor.execute("INSERT INTO trials(experiment_id, mouse_id, trial_dir) VALUES(%s, %s, %s);",
                           (self.experiment_id, self.mouse_id, self.trial_dir))

    def delete_from_db(self):
        with Cursor() as cursor:
            cursor.execute("DELETE FROM trials WHERE trial_id = %s", (self.trial_id,))