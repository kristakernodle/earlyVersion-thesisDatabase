from database import Cursor


class NetworkBodyParts:
    def __init__(self, bodypart, bodypart_id = None, network_id = None):
        self.bodypart = bodypart
        self.bodypart_id = bodypart_id
        self.network_id = network_id

    def __str__(self):
        return f"< Network Bodypart {self.bodypart} >"

    @classmethod
    def from_db(cls, bodypart_id, network_id):
        with Cursor() as cursor:
            cursor.execute("SELECT * FROM network_bodyparts WHERE bodypart_id = %s AND network_id = %s;",
                           (bodypart_id, network_id))
            bodypart_details = cursor.fetchone()
            return cls(bodypart=bodypart_details[2], network_id=bodypart_details[1], bodypart_id=network[0])

    def save_to_db(self):
        with Cursor() as cursor:
            cursor.execute("INSERT INTO network_bodyparts(bodypart_id, network_id, bodypart) VALUES(%s, %s, %s);",
                           (self.bodypart_id, self.network_id, self.bodypart))
