from database.database import Database
import data.constants as constants
from models.mouse import Mouse


Database.initialize(database=constants.database, user=constants.user, password=constants.password, host=constants.host)
this_mouse = Mouse.from_db(704)

print(this_mouse)

