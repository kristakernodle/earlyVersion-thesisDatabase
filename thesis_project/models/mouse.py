import utilities as util
from database.cursors import Cursor, TestingCursor

from models.experiments import Experiments


def list_all_mice(cursor):
    cursor.execute("SELECT eartag FROM mouse;")
    return list(item for tup in cursor.fetchall() for item in tup)


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

        # TODO: apply this format to all public methods
        #   def save_to_db_main(eartag, a_cursor):
        #       if eartag not in list_all_mice(a_cursor):
        #           self.__save_to_db(a_cursor)
        #       return self.__from_db(a_cursor, eartag)
        def save_to_db_main(eartag, a_cursor):
            if eartag not in list_all_mice(a_cursor):
                self.__save_to_db(a_cursor)
            return self.__from_db(a_cursor, eartag)

        if testing:
            with TestingCursor(postgresql) as cursor:
                return save_to_db_main(self.eartag, cursor)
        else:
            with Cursor() as cursor:
                return save_to_db_main(self.eartag, cursor)

    def __delete_from_db(self, cursor):
        cursor.execute("DELETE FROM mouse WHERE mouse_id = %s", (self.mouse_id,))

    def delete_from_db(self, testing=False, postgresql=None):
        if testing:
            with TestingCursor(postgresql) as cursor:
                self.__delete_from_db(cursor)
        else:
            with Cursor() as cursor:
                self.__delete_from_db(cursor)
