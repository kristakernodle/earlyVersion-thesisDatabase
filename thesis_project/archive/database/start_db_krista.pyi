from archive.database import Database
from archive.data.constants import dbDetails, dbUser_Krista

Database.initialize(**dbDetails, **dbUser_Krista)
