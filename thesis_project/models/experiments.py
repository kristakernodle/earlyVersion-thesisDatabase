from database import Cursor


class Experiments:
    def __init__(self, experiment_name, experiment_dir, experiment_id = None):
        self.experiment_name = experiment_name
        self.experiment_dir = experiment_dir
        self.experiment_id = experiment_id

    def __str__(self):
        return f"< Experiment {self.experiment_name} >"

    @classmethod
    def from_db(cls, experiment_name):
        with Cursor() as cursor:
            cursor.execute("SELECT * FROM experiments WHERE experiment_name = %s;", (experiment_name,))
            exp = cursor.fetchone()
            return cls(experiment_dir=exp[1], experiment_id=exp[0])

    def save_to_db(self):
        with Cursor() as cursor:
            cursor.execute("INSERT INTO experiments(experiment_dir, experiment_name) VALUES(%s, %s);", (self.experiment_dir,self.experiment_name))
