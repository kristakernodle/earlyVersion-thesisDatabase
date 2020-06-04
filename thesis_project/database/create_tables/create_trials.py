def create_trials_table(a_cursor):
    a_cursor.execute("CREATE TABLE trials( "
                     "trial_id   uuid default uuid_generate_v4()     not null "
                     "    constraint trials_pkey primary key,"
                     "experiment_id uuid                                   not null "
                     "    constraint participant_details_experiments_id_fkey references experiments,"
                     "mouse_id uuid                              not null"
                     "    constraint participant_details_mouse_id_fkey references mouse,"
                     "trial_dir varchar(255),"
                     "trial_date date);")
    a_cursor.execute("create unique index trial_dir_index on trials (trial_dir);")
