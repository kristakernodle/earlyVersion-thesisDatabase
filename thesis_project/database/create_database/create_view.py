def create_view_all_participants_all_trials(a_cursor):
    a_cursor.execute(
        "CREATE VIEW all_participants_all_trials "
        "   (trial_id, experiment_id, mouse_id, trial_dir, trial_date, scored_dir, experiment_name) AS "
        "SELECT trial_id, trials.experiment_id, trials.mouse_id, trial_dir, trial_date, mouse.scored_dir, "
        "   experiments.experiment_name "
        "FROM trials "
        "JOIN mouse on mouse.mouse_id = trials.mouse_id "
        "JOIN experiments on experiments.experiment_id = trials.experiment_id;")
