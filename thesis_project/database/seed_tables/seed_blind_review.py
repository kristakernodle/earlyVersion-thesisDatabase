def seed_blind_trials(cursor, trial_id, reviewer_id, blind_name):
    cursor.execute("INSERT INTO blind_trials (trial_id, reviewer_id, blind_name) "
                   "VALUES (%s, %s, %s);", (trial_id, reviewer_id, blind_name))


def seed_reviewers_table(cursor, first_name, last_name, toScore_dir, scored_dir):
    cursor.execute("INSERT INTO reviewers (first_name, last_name, toScore_dir, scored_dir) "
                   "VALUES (%s, %s, %s, %s);", (first_name, last_name, toScore_dir, scored_dir))
