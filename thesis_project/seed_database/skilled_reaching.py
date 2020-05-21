from database import Database
import data.constants as constants
from models.experiments import Experiments
from models.mouse import Mouse


Database.initialize(database=constants.database, user=constants.user, password=constants.password, host=constants.host)

experiment = 'skilled-reaching'
sr_exp = Experiments.from_db(experiment)
