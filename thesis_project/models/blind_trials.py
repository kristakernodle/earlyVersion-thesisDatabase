from database.cursors import TestingCursor, Cursor


class BlindTrial:
    def __init__(self, trial_id, folder_id, full_path, blind_trial_id=None):
        self.trial_id = trial_id
        self.folder_id = folder_id
        self.full_path = full_path
        self.blind_trial_id = blind_trial_id

    def __str__(self):
        return f"< Blind Trial {self.full_path} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, BlindTrial):
            return NotImplemented
        return self.blind_trial_id == compare_to.blind_trial_id

    @classmethod
    def __from_db(cls, cursor, full_path):
        cursor.execute("SELECT * FROM blind_trials WHERE full_path = %s", (full_path,))
        blind_trial_data = cursor.fetchone()
        if blind_trial_data is None:
            print(f"No blind trial in the database with full path {full_path}")
            return None
        return cls(trial_id=blind_trial_data[1], folder_id=blind_trial_data[2],
                   full_path=blind_trial_data[3], blind_trial_id=blind_trial_data[0])

    @classmethod
    def from_db(cls, full_path, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                return cls.__from_db(cursor, full_path)
        else:
            with Cursor() as cursor:
                return cls.__from_db(cursor, full_path)

    def save_to_db(self, testing=False, postgresql=None):

        def main(a_cursor, full_path):
            cursor.execute(
                "INSERT INTO blind_trials (trial_id, folder_id, full_path) VALUES (%s, %s, %s);",
                (self.trial_id, self.folder_id, self.full_path))
            return self.__from_db(a_cursor, full_path)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main(cursor, self.full_path)
        else:
            with Cursor() as cursor:
                return main(cursor, self.full_path)
