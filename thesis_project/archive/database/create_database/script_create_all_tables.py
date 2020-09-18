from archive import database as create_tables, database as create_views
from archive.database import Cursor
from archive.database import Database
from archive.data.constants import dbDetails, dbUser_Krista

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
