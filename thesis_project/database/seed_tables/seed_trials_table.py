def seed_trials(cursor, mouse_id, experiment_id, trial_date, trial_dir):
    cursor.execute("INSERT INTO trials (experiment_id, mouse_id, trial_dir, trial_date) "
                   "VALUES (%s, %s, %s, %s);", (experiment_id, mouse_id, trial_dir, trial_date))
