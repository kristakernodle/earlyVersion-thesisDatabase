import utilities as util
from database import Cursor


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
    def from_db(cls, eartag):
        with Cursor() as cursor:
            cursor.execute("SELECT * FROM mouse WHERE eartag = %s", (eartag,))
            mouse_data = cursor.fetchone()
            if mouse_data is None:
                print(f"No mouse in the database with mouse number {eartag}")
                return None
            return cls(eartag=mouse_data[1], birthdate=mouse_data[2],
                       genotype=util.decode_genotype(mouse_data[3]), sex=mouse_data[4], mouse_id=mouse_data[0])

    def save_to_db(self):
        try:
            with Cursor() as cursor:
                cursor.execute("INSERT INTO mouse"
                               "    (eartag, birthdate, genotype, sex) "
                               "VALUES"
                               "    (%s, %s, %s, %s);",
                               (self.eartag, self.birthdate, util.encode_genotype(self.genotype), self.sex))
        finally:
            return self.from_db(self.eartag)


    def delete_from_db(self):
        with Cursor() as cursor:
            cursor.execute("DELETE FROM mouse WHERE mouse_id = %s", (self.mouse_id,))

    def add_participant(self, experiment_name, start_date=None, end_date=None):
        return "ParticipantDetails(self.mouse, util.prep_string_for_db(experiment_name), start_date=start_date, " \
               "end_date=end_date).save_to_db() "
