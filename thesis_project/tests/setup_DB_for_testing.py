import testing.postgresql as tpg
import psycopg2
import unittest

test_mouse_table_seed = [(9990, 20200102, 'wild type', 'male', True, 'test experiment one', 20200501, 20200601),
                         (9991, 20200101, 'wild type', 'male', False, 'test experiment two', 20200515, 20200615),
                         (9992, 20200101, 'wild type', 'male', True, 'test experiment one', 20200501, 20200601),
                         (9993, 20200101, 'wild type', 'male', False, 'test experiment two', 20200515, 20200615),
                         (9994, 20200101, 'wild type', 'female', True, 'test experiment one', 20200501, 20200601),
                         (9995, 20200101, 'wild type', 'female', False, 'test experiment two', 20200515, 20200615),
                         (9996, 20200101, 'knock out', 'female', True, 'test experiment one', 20200501, 20200601),
                         (9997, 20200101, 'knock out', 'female', False, 'test experiment two', 20200515, 20200615),
                         (9998, 20200101, 'knock out', 'female', True, 'test experiment one', 20200501, 20200601),
                         (9999, 20200102, 'knock out', 'female', False, 'test experiment two', 20200515, 20200615)]

exp_one = ('/test/directory/experiment/one', 'test experiment one')
exp_two = ('/test/directory/experiment/two', 'test experiment two')


def create_mouse_table(a_cursor, seed=False):
    a_cursor.execute("CREATE TABLE mouse("
                     "mouse_id  uuid default uuid_generate_v4() not null constraint mouse_pkey primary key,"
                     "eartag    smallint                        not null,"
                     "birthdate date                            not null,"
                     "genotype  boolean                         not null,"
                     "sex       varchar(6)                      not null);")
    a_cursor.execute("create unique index mouse_eartag_index on mouse (eartag);")
    if seed:
        a_cursor.execute("CREATE TABLE mouse("
                         "mouse_id  uuid default uuid_generate_v4() not null constraint mouse_pkey primary key,"
                         "eartag    smallint                        not null,"
                         "birthdate date                            not null,"
                         "genotype  boolean                         not null,"
                         "sex       varchar(6)                      not null);")
        a_cursor.execute("create unique index mouse_eartag_index on mouse (eartag);")
        for mouse in test_mouse_table_seed:
            a_cursor.execute("INSERT INTO mouse"
                             "    (eartag, birthdate, genotype, sex) "
                             "VALUES"
                             "    (%s, %s, %s, %s);", mouse)


def create_experiments_table(a_cursor, seed=False):
    a_cursor.execute("CREATE TABLE experiments( "
                     "experiment_id   uuid default uuid_generate_v4() not null constraint experiments_pkey primary key,"
                     "experiment_dir  varchar(255)                    not null,"
                     "experiment_name varchar(50)                     not null);")
    a_cursor.execute("create unique index experiments_experiment_dir_uindex on experiments (experiment_dir);")
    a_cursor.execute("create unique index experiments_experiment_name_uindex on experiments (experiment_name);")
    if seed:
        a_cursor.execute("INSERT INTO experiments"
                         "    (experiment_dir, experiment_name)"
                         "VALUES"
                         "    (%s, %s);",
                         exp_one)
        a_cursor.execute("INSERT INTO experiments"
                         "    (experiment_dir, experiment_name)"
                         "VALUES"
                         "    (%s, %s);",
                         exp_two)

def create_participant_details_table(a_cursor):
    a_cursor.execute("CREATE TABLE participant_details( "
                     "detail_id   uuid default uuid_generate_v4()     not null "
                     "    constraint participant_details_pkey primary key,"
                     "mouse_id uuid                                   not null "
                     "    constraint participant_details_mouse_id_fkey references mouse,"
                     "experiment_id uuid                              not null"
                     "    constraint participant_details_experiment_id_fkey references experiments,"
                     "start_date date,"
                     "end_date date,"
                     "exp_spec_details json);")


# create initial data on create as fixtures into the database
def handler(postgresql, tables_to_seed):

    """

    :param postgresql:
    :param tables_to_seed: List of table names that need to be seeded
    :return:
    """

    conn = psycopg2.connect(**postgresql.dsn())
    cursor = conn.cursor()

    if 'mouse' in tables_to_seed:
        mouse_seed = True
    else:
        mouse_seed = False

    if 'experiments' in tables_to_seed:
        exp_seed = True
    else:
        exp_seed = False

    # TODO: participant details seed
    # if 'participant_details' in tables_to_seed:
    #     participant_deets_seed = True
    # else:
    #     participant_deets_seed = True

    create_mouse_table(cursor, seed=mouse_seed)
    create_experiments_table(cursor, seed=exp_seed)
    create_participant_details_table(cursor)

    cursor.close()
    conn.commit()
    conn.close()


# Use `handler()` on initialize database
Postgresql = tpg.PostgresqlFactory(cache_initialized_db=True, on_initialized=handler)


def tearDownModule():
    # clear cached database at end of tests
    Postgresql.clear_cache()


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Use the generated Postgresql class instead of testing.postgresql.Postgresql
        self.postgresql = Postgresql()

    def tearDown(self):
        self.postgresql.stop()

    def test_hello(self):
        self.assertFalse(False)
