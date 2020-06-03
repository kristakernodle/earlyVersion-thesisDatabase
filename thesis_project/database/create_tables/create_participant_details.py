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


def create_view_all_participants_all_experiments(a_cursor):
    a_cursor.execute(
        "CREATE VIEW all_participants_all_experiments "
        "   (mouse_id, experiment_id, detail_id, eartag, experiment_name, start_date, end_date) AS "
        "SELECT mouse.mouse_id, experiments.experiment_id, participant_details.detail_id, mouse.eartag, "
        "   experiments.experiment_name, participant_details.start_date, participant_details.end_date "
        "FROM participant_details "
        "JOIN mouse ON mouse.mouse_id = participant_details.mouse_id "
        "JOIN experiments ON experiments.experiment_id = participant_details.experiment_id;")
