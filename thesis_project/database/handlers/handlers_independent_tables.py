from database.create_tables.create_independent_tables import create_mouse_table, create_experiments_table
from database.cursors import TestingCursor
from database.handlers.handlers_participant_details import create_participant_details_table


def handler_create_all_empty_tables(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_mouse_table(cursor)
        create_experiments_table(cursor)
        create_participant_details_table(cursor)