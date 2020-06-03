def seed_participant_details(cursor, mouse_id, experiment_id, start_date, end_date):
    cursor.execute("INSERT INTO participant_details (mouse_id, experiment_id, start_date, end_date) "
                   "VALUES (%s, %s, %s, %s);", (mouse_id, experiment_id, start_date, end_date))
