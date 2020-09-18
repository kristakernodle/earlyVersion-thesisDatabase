import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from archive.data.constants import dbDetails, dbUser_superUser, dbUser_Krista

# Connect to PostgreSQL DBMS
con = psycopg2.connect(**dbUser_superUser)
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Obtain a DB Cursor
cursor = con.cursor()

# Create Database and first user
sqlCreateDatabase = f"CREATE DATABASE {dbDetails['database']};"
sqlCreateUser = f"CREATE USER {dbUser_Krista['user']} WITH ENCRYPTED PASSWORD '{dbUser_Krista['password']}';"
sqlGrantPrivileges = f"GRANT ALL PRIVILEGES ON DATABASE {dbDetails['database']} TO {dbUser_Krista['user']};"

cursor.execute(sqlCreateDatabase)
cursor.execute(sqlCreateUser)
cursor.execute(sqlGrantPrivileges)
