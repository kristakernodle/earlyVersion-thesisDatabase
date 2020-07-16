import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from data.constants import dbDetails, dbUser_superUser, dbUser_Krista

# Connect to PostgreSQL DBMS
con = psycopg2.connect(**dbUser_superUser)
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Obtain a DB Cursor
cursor = con.cursor()

# Create Database
sqlCreateDatabase = f"CREATE DATABASE {dbDetails['database']};"
cursor.execute(sqlCreateDatabase)
