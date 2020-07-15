def create_view_all_participants_all_experiments(a_cursor):
    a_cursor.execute(
        "CREATE VIEW all_participants_all_experiments "
        "   (mouse_id, experiment_id, detail_id, scored_dir, experiment_name, start_date, end_date) AS "
        "SELECT mouse.mouse_id, experiments.experiment_id, participant_details.detail_id, mouse.scored_dir, "
        "   experiments.experiment_name, participant_details.start_date, participant_details.end_date "
        "FROM participant_details "
        "JOIN mouse ON mouse.mouse_id = participant_details.mouse_id "
        "JOIN experiments ON experiments.experiment_id = participant_details.experiment_id;")


def create_view_all_participants_all_trials(a_cursor):
    a_cursor.execute(
        "CREATE VIEW all_participants_all_trials "
        "   (trial_id, experiment_id, mouse_id, trial_dir, trial_date, scored_dir, experiment_name) AS "
        "SELECT trial_id, trials.experiment_id, trials.mouse_id, trial_dir, trial_date, mouse.scored_dir, "
        "   experiments.experiment_name "
        "FROM trials "
        "JOIN mouse on mouse.mouse_id = trials.mouse_id "
        "JOIN experiments on experiments.experiment_id = trials.experiment_id;")


def create_view_folders_all_upstream_ids(a_cursor):
    a_cursor.execute(
        "CREATE VIEW folders_all_upstream_ids "
        "   (mouse_id, experiment_id, session_id, folder_id) AS "
        "SELECT mouse_id, experiment_id, sessoion_id, folder_id "
        "FROM folders "
        "JOIN sessions on sessions.mouse_id, sessions.experiment_id, sessions.session_id;")


def create_view_trials_all_upstream_ids(a_cursor):
    a_cursor.execute(
        "CREATE VIEW trials_all_upstream_ids "
        "   (mouse_id, experiment_id, session_id, folder_id, trial_id) AS "
        "SELECT mouse_id, experiment_id, sessoion_id, folder_id, trial_id "
        "FROM folders "
        "JOIN sessions on sessions.mouse_id, sessions.experiment_id, sessions.session_id "
        "JOIN trials on trials.trial_id;")
