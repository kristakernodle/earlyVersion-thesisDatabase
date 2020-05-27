import utilities as util
from models.cursors import Cursor, TestingCursor


class Mouse:
    def __init__(self, eartag, birthdate, genotype, sex, mouse_id=None):
        self.eartag = int(eartag)
        self.birthdate = util.convert_date_int_yyyymmdd(birthdate)
        self.genotype = genotype
        self.sex = sex
        self.mouse_id = mouse_id

    def __str__(self):
        return f"< Mouse {self.eartag} >"

    def __repr__(self):
        return f"< Mouse {self.eartag} >"

    def __eq__(self, compare_to):
        if not isinstance(compare_to, Mouse):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.mouse_id == compare_to.mouse_id

    @classmethod
    def __from_db(cls, cursor, eartag):
        cursor.execute("SELECT * FROM mouse WHERE eartag = %s", (eartag,))
        mouse_data = cursor.fetchone()
        if mouse_data is None:
            print(f"No mouse in the database with mouse number {eartag}")
            return None
        return cls(eartag=mouse_data[1], birthdate=mouse_data[2],
                   genotype=util.decode_genotype(mouse_data[3]), sex=mouse_data[4], mouse_id=mouse_data[0])

    @classmethod
    def from_db(cls, eartag, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                return cls.__from_db(cursor, eartag)
        else:
            with Cursor() as cursor:
                return cls.__from_db(cursor, eartag)

    def __save_to_db(self, cursor):
        cursor.execute("INSERT INTO mouse (eartag, birthdate, genotype, sex) VALUES (%s, %s, %s, %s);",
                       (self.eartag, self.birthdate, util.encode_genotype(self.genotype), self.sex))

    def save_to_db(self, testing=False, postgresql=None):
        # TODO Check if mouse is in database
        cursor.execute("SELECT eartag FROM all_participants_all_experiments WHERE experiment_name = %s;",
                       (experiment_name,))

    def __delete_from_db(self, cursor):
        cursor.execute("DELETE FROM mouse WHERE mouse_id = %s", (self.mouse_id,))

    def delete_from_db(self, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                self.__delete_from_db(cursor)
        else:
            with Cursor() as cursor:
                self.__delete_from_db(cursor)

    def add_participant(self, experiment_name, start_date=None, end_date=None):
        return "ParticipantDetails(self.mouse, util.prep_string_for_db(experiment_name), start_date=start_date, " \
               "end_date=end_date).save_to_db() "
