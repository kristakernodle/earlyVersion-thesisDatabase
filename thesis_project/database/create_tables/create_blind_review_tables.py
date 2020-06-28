def create_reviewers_table(a_cursor):
    a_cursor.execute("CREATE TABLE reviewers("
                     "reviewer_id  uuid default uuid_generate_v4() not null constraint reviewers_pkey primary key,"
                     "first_name varchar(10) not null,"
                     "last_name varchar(10) not null,"
                     "toScore_dir varchar(255) not null,"
                     "scored_dir varchar(255) not null);")
    a_cursor.execute("create unique index reviewers_toScore_dir_index on reviewers (toScore_dir);")
    a_cursor.execute("create unique index reviewers_scored_dir_index on reviewers (scored_dir);")


def create_blind_trials_table(a_cursor):
    a_cursor.execute("CREATE TABLE blind_trials( "
                     "blind_trial_id   uuid default uuid_generate_v4() not null constraint trial_pkey primary key,"
                     "trial_id uuid references trials not null,"
                     "reviewer_id  varchar(255)                    not null,"
                     "blind_name varchar(15)                     not null);")
    a_cursor.execute("create unique index trials_blind_name_uindex on blind_trials (blind_name);")
