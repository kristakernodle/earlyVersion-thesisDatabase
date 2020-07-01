def create_mouse_table(a_cursor):
    a_cursor.execute("CREATE TABLE mouse("
                     "mouse_id  uuid default uuid_generate_v4() not null constraint mouse_pkey primary key,"
                     "scored_dir    smallint                        not null,"
                     "birthdate date                            not null,"
                     "genotype  boolean                         not null,"
                     "sex       varchar(6)                      not null);")
    a_cursor.execute("create unique index mouse_eartag_index on mouse (scored_dir);")


def create_experiments_table(a_cursor):
    a_cursor.execute("CREATE TABLE experiments( "
                     "experiment_id   uuid default uuid_generate_v4() not null constraint experiments_pkey primary key,"
                     "experiment_dir  varchar(255)                    not null,"
                     "experiment_name varchar(50)                     not null);")
    a_cursor.execute("create unique index experiments_experiment_dir_uindex on experiments (experiment_dir);")
    a_cursor.execute("create unique index experiments_experiment_name_uindex on experiments (experiment_name);")


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
                     "exp_spec_details json,"
                     "participant_dir varchar(255));")
    a_cursor.execute("create unique index participant_dir_index on participant_details (participant_dir);")


def create_reviewers_table(a_cursor):
    a_cursor.execute("CREATE TABLE reviewers("
                     "reviewer_id  uuid default uuid_generate_v4() not null constraint reviewers_pkey primary key,"
                     "first_name varchar(10) not null,"
                     "last_name varchar(10) not null,"
                     "toScore_dir varchar(255) not null,"
                     "scored_dir varchar(255) not null);")
    a_cursor.execute("create unique index reviewers_toScore_dir_index on reviewers (toScore_dir);")
    a_cursor.execute("create unique index reviewers_scored_dir_index on reviewers (scored_dir);")


def create_sessions_table(a_cursor):
    a_cursor.execute("CREATE TABLE sessions( "
                     "session_id uuid default uuid_generate_v4() not null "
                     "  constraint sessions_pkey primary key, "
                     "mouse_id uuid not null"
                     "  constraint sessions_mouse_id_fkey references mouse, "
                     "experiment_id uuid not null "
                     "  constraint sessions_experiment_id_fkey references experiments, "
                     "session_date date not null, "
                     "session_dir varchar(255) not null);")


def create_folders_table(a_cursor):
    a_cursor.execute("CREATE TABLE folders( "
                     "folder_id uuid default uuid_generate_v4() not null "
                     "  constraint folders_pkey primary key, "
                     "session_id uuid not null "
                     "  constraint folders_session_id_fkey references sessions, "
                     "folder_dir varchar(255) not null);")


def create_blind_folders_table(a_cursor):
    a_cursor.execute("CREATE TABLE blind_folders( "
                     "blind_folder_id uuid default uuid_generate_v4() not null "
                     "  constraint blind_folders_pkey primary key, "
                     "folder_id uuid not null "
                     "  constraint blind_folders_folder_id_fkey references folders, "
                     "reviewer_id uuid not null "
                     "  constraint blind_folders_reviewer_id_fkey references reviewers, "
                     "blind_name varchar(255) not null);")
    a_cursor.execute("create unique index blind_name_index on blind_folders (blind_name);")


def create_trials_table(a_cursor):
    a_cursor.execute("CREATE TABLE trials( "
                     "trial_id   uuid default uuid_generate_v4()     not null "
                     "    constraint trials_pkey primary key,"
                     "experiment_id uuid                                   not null "
                     "    constraint participant_details_experiments_id_fkey references experiments,"
                     "folder_id uuid                              not null"
                     "    constraint participant_details_folder_id_fkey references folders,"
                     "trial_dir varchar(255),"
                     "trial_date date);")
    a_cursor.execute("create unique index trial_dir_index on trials (trial_dir);")


def create_blind_trials_table(a_cursor):
    a_cursor.execute("CREATE TABLE blind_folders( "
                     "blind_trial_id   uuid default uuid_generate_v4() not null "
                     "  constraint trial_pkey primary key, "
                     "trial_id uuid references trials not null, "
                     "folder_id  uuid references folders not null, "
                     "full_path varchar(15) not null);")
    a_cursor.execute("create unique index blind_folders_full_path_uindex on blind_folders (full_path);")
