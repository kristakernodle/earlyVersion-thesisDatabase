from models.cursors import TestingCursor
import utilities as util


birthdate1 = util.convert_date_int_yyyymmdd(20200101)
birthdate2 = util.convert_date_int_yyyymmdd(20200102)
start1 = util.convert_date_int_yyyymmdd(20200501)
end1 = util.convert_date_int_yyyymmdd(20200601)
start2 = util.convert_date_int_yyyymmdd(20200515)
end2 = util.convert_date_int_yyyymmdd(20200615)
test_mouse_table_seed = [(9990, birthdate2, 'wild type', 'male', True, 'test experiment one', start1, end1),
                         (9991, birthdate1, 'wild type', 'male', False, 'test experiment two', start2, end2),
                         (9992, birthdate1, 'wild type', 'male', True, 'test experiment one', start1, end1),
                         (9993, birthdate1, 'wild type', 'male', False, 'test experiment two', start2, end2),
                         (9994, birthdate1, 'wild type', 'female', True, 'test experiment one', start1, end1),
                         (9995, birthdate1, 'wild type', 'female', False, 'test experiment two', start2, end2),
                         (9996, birthdate1, 'knock out', 'female', True, 'test experiment one', start1, end1),
                         (9997, birthdate1, 'knock out', 'female', False, 'test experiment two', start2, end2),
                         (9998, birthdate1, 'knock out', 'female', True, 'test experiment one', start1, end1),
                         (9999, birthdate2, 'knock out', 'female', False, 'test experiment two', start2, end2)]

exp_one = ('test experiment one', '/test/directory/experiment/one')
exp_two = ('test experiment two', '/test/directory/experiment/two')


def create_mouse_table(a_cursor):
    a_cursor.execute("CREATE TABLE mouse("
                     "mouse_id  uuid default uuid_generate_v4() not null constraint mouse_pkey primary key,"
                     "eartag    smallint                        not null,"
                     "birthdate date                            not null,"
                     "genotype  boolean                         not null,"
                     "sex       varchar(6)                      not null);")
    a_cursor.execute("create unique index mouse_eartag_index on mouse (eartag);")


def seed_mouse_table(a_cursor):
    for mouse in test_mouse_table_seed:
        genotype = util.encode_genotype(mouse[2])
        sex = util.prep_string_for_db(mouse[3])

        a_cursor.execute("INSERT INTO mouse"
                         "    (eartag, birthdate, genotype, sex) "
                         "VALUES"
                         "    (%s, %s, %s, %s);", (mouse[0], mouse[1], genotype, sex))


def create_experiments_table(a_cursor):
    a_cursor.execute("CREATE TABLE experiments( "
                     "experiment_id   uuid default uuid_generate_v4() not null constraint experiments_pkey primary key,"
                     "experiment_dir  varchar(255)                    not null,"
                     "experiment_name varchar(50)                     not null);")
    a_cursor.execute("create unique index experiments_experiment_dir_uindex on experiments (experiment_dir);")
    a_cursor.execute("create unique index experiments_experiment_name_uindex on experiments (experiment_name);")


def seed_experiments_table(a_cursor):
    a_cursor.execute("INSERT INTO experiments (experiment_dir, experiment_name) VALUES (%s, %s);", exp_one)
    a_cursor.execute("INSERT INTO experiments (experiment_dir, experiment_name) VALUES (%s, %s);", exp_two)


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

    # TODO: participant details seed
    # if 'participant_details' in tables_to_seed:
    #     participant_deets_seed = True
    # else:
    #     participant_deets_seed = True


def handler_create_all_empty_tables(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_mouse_table(cursor)
        create_experiments_table(cursor)
        create_participant_details_table(cursor)


def handler_seed_mouse(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        seed_mouse_table(cursor)


def handler_seed_mouse_experiments(postgresql):
    handler_create_all_empty_tables(postgresql)
    with TestingCursor(postgresql) as cursor:
        seed_mouse_table(cursor)
        seed_experiments_table(cursor)


def create_view_all_participants_all_experiments(postgresql):
    with TestingCursor(postgresql) as cursor:
        cursor.execute(
            "CREATE VIEW all_participants_all_experiments "
            "   (mouse_id, experiment_id, detail_id, eartag, experiment_name, start_date, end_date) AS "
            "SELECT mouse.mouse_id, experiments.experiment_id, participant_details.detail_id, mouse.eartag, "
            "   experiments.experiment_name, participant_details.start_date, participant_details.end_date "
            "FROM participant_details "
            "JOIN mouse ON mouse.mouse_id = participant_details.mouse_id "
            "JOIN experiments ON experiments.experiment_id = participant_details.experiment_id;")
