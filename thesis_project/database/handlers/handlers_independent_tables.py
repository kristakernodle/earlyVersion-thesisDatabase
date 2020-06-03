import database.create_tables.create_independent_tables as create_id
import database.seed_tables.seed_independent_tables as seed_id
from database.cursors import TestingCursor


def handler_create_mouse_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_id.create_mouse_table(cursor)


def handler_create_experiments_table(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_id.create_experiments_table(cursor)


def handler_create_all_independent_tables(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_id.create_mouse_table(cursor)
        create_id.create_experiments_table(cursor)


def handler_seed_mouse(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        seed_id.seed_mouse_table(cursor)


def handler_seed_experiments(postgresql):
    with TestingCursor(postgresql) as cursor:
        seed_id.seed_experiments_table(cursor)


def handler_seed_mouse_experiments(postgresql):
    with TestingCursor(postgresql) as cursor:
        seed_id.seed_mouse_table(cursor)
        seed_id.seed_experiments_table(cursor)
