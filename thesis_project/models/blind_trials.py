from blind_review.blinded.common.auxiliary_functions import random_string_generator

from database.cursors import TestingCursor, Cursor


class BlindTrial:

    def __init__(self, trial_id, reviewer_id, blind_name=random_string_generator(10), blind_trial_id=None):
        self.trial_id = trial_id
        self.reviewer_id = reviewer_id
        self.blind_name = blind_name
        self.blind_trial_id = blind_trial_id

    def __str__(self):
        return f"< Blind Trial {self.blind_name} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, BlindTrial):
            return NotImplemented
        return self.blind_trial_id == compare_to.blind_trial_id

    @classmethod
    def __from_db(cls, cursor, blind_name):
        cursor.execute("SELECT * FROM blind_trials WHERE blind_name = %s", (blind_name,))
        blind_trial_data = cursor.fetchone()
        if blind_trial_data is None:
            print(f"No blind trial in the database with blind name {blind_name}")
            return None
        return cls(trial_id=blind_trial_data[1], reviewer_id=blind_trial_data[2],
                   blind_name=blind_trial_data[3], blind_trial_id=blind_trial_data[0])

    @classmethod
    def from_db(cls, blind_name, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                return cls.__from_db(cursor, blind_name)
        else:
            with Cursor() as cursor:
                return cls.__from_db(cursor, blind_name)

    def save_to_db(self, testing=False, postgresql=None):

        def main(a_cursor, blind_name):
            cursor.execute(
                "INSERT INTO blind_trials (trial_id, reviewer_id, blind_name) VALUES (%s, %s, %s);",
                (self.trial_id, self.reviewer_id, self.blind_name))
            return self.__from_db(a_cursor, blind_name)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return main(cursor, self.blind_name)
        else:
            with Cursor() as cursor:
                return main(cursor, self.blind_name)
