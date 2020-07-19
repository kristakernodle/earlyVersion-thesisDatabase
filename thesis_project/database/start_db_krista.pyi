from database.database import Database
from data.constants import dbDetails, dbUser_Krista

Database.initialize(**dbDetails, **dbUser_Krista)
