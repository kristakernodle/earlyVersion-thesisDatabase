from database.create_tables.create_independent_tables import create_mouse_table, create_experiments_table
from database.cursors import TestingCursor
from database.seed_tables.seed_independent_tables import seed_mouse_table, seed_experiments_table


def handler_create_mouse_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_mouse_table(cursor)


def handler_create_experiments_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_experiments_table(cursor)


def handler_create_all_independent_tables(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_mouse_table(cursor)
        create_experiments_table(cursor)


def handler_seed_mouse(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        seed_mouse_table(cursor)


def handler_seed_experiments(postgresql):
    with TestingCursor(postgresql) as cursor:
        seed_experiments_table(cursor)


def handler_seed_mouse_experiments(postgresql):
    with TestingCursor(postgresql) as cursor:
        seed_mouse_table(cursor)
        seed_experiments_table(cursor)
