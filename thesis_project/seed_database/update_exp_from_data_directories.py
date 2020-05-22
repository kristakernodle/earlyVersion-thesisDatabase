from database import Database
from data.constants import dbConnection_Krista
from models.experiments import Experiments
from models.mouse import Mouse
import pathlib


Database.initialize(**dbConnection_Krista)

experiment = 'skilled-reaching'
sr_exp = Experiments.from_db(experiment)

