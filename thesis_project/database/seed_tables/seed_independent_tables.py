import utilities as util
from database.seed_tables.seeds import test_mouse_table_seed, exp_one, exp_two


def seed_mouse_table(a_cursor):
    for mouse in test_mouse_table_seed:
        genotype = util.encode_genotype(mouse[2])
        sex = util.prep_string_for_db(mouse[3])

        a_cursor.execute("INSERT INTO mouse"
                         "    (eartag, birthdate, genotype, sex) "
                         "VALUES"
                         "    (%s, %s, %s, %s);", (mouse[0], mouse[1], genotype, sex))


def seed_experiments_table(a_cursor):
    prepped_exp_one = (util.prep_string_for_db(exp_one[0]), exp_one[1])
    prepped_exp_two = (util.prep_string_for_db(exp_two[0]), exp_two[1])
    a_cursor.execute("INSERT INTO experiments (experiment_name, experiment_dir) VALUES (%s, %s);", prepped_exp_one)
    a_cursor.execute("INSERT INTO experiments (experiment_name, experiment_dir) VALUES (%s, %s);", prepped_exp_two)
