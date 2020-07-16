import database.create_database.create_tables as create_tables
import database.create_database.create_views as create_views
from database.cursors import Cursor
from database.database import Database
from data.constants import dbDetails, dbUser_Krista

Database.initialize(**dbDetails, **dbUser_Krista)

with Cursor() as cursor:
    cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    create_tables.create_mouse_table(cursor)
    create_tables.create_experiments_table(cursor)
    create_tables.create_participant_details_table(cursor)
    create_tables.create_sessions_table(cursor)
    create_tables.create_folders_table(cursor)
    create_tables.create_trials_table(cursor)
    create_tables.create_reviewers_table(cursor)
    create_tables.create_blind_folders_table(cursor)
    create_tables.create_blind_trials_table(cursor)
    create_views.create_view_all_participants_all_experiments(cursor)
    create_views.create_view_folders_all_upstream_ids(cursor)
    create_views.create_view_trials_all_upstream_ids(cursor)
