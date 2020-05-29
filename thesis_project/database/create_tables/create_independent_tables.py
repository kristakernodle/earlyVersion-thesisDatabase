def create_mouse_table(a_cursor):
    a_cursor.execute("CREATE TABLE mouse("
                     "mouse_id  uuid default uuid_generate_v4() not null constraint mouse_pkey primary key,"
                     "eartag    smallint                        not null,"
                     "birthdate date                            not null,"
                     "genotype  boolean                         not null,"
                     "sex       varchar(6)                      not null);")
    a_cursor.execute("create unique index mouse_eartag_index on mouse (eartag);")


def create_experiments_table(a_cursor):
    a_cursor.execute("CREATE TABLE experiments( "
                     "experiment_id   uuid default uuid_generate_v4() not null constraint experiments_pkey primary key,"
                     "experiment_dir  varchar(255)                    not null,"
                     "experiment_name varchar(50)                     not null);")
    a_cursor.execute("create unique index experiments_experiment_dir_uindex on experiments (experiment_dir);")
    a_cursor.execute("create unique index experiments_experiment_name_uindex on experiments (experiment_name);")
