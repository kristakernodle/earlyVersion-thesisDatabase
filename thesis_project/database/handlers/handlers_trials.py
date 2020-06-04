from database.cursors import TestingCursor
import database.create_tables.create_independent_tables as create_id
import database.create_tables.create_trials as create_tr


def handler_create_trials_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_id.create_mouse_table(cursor)
        create_id.create_experiments_table(cursor)
        create_tr.create_trials_table(cursor)
