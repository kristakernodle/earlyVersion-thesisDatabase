from database.database import Database
from data.constants import dbConnection_Krista
from models.experiments import Experiments
import pathlib
from pathlib import Path

Database.initialize(**dbConnection_Krista)

experiment = 'skilled reaching'
sr_exp = Experiments.from_db(experiment)
sr_exp.experiment_dir = '/'.join(['/Volumes/SharedX', sr_exp.experiment_dir])
sr_exp.save_to_db()

experiment_dir = pathlib.PosixPath(sr_exp.experiment_dir)
