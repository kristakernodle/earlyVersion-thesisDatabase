from models.cursors import Cursor


class NetworkDetails:
    def __init__(self, paw_preference, view, network_config, network_id):
        self.paw_preference = paw_preference
        self.view = view
        self.network_config = network_config
        self.network_id = network_id

    def __str__(self):
        return f"< Network {self.network_config} >"

    @classmethod
    def from_db(cls, paw_preference, view):
        with Cursor() as cursor:
            cursor.execute("SELECT * FROM network_details WHERE paw_preference = %s AND view = %s;",
                           (paw_preference, view))
            network_details = cursor.fetchone()
        return cls(paw_preference=network_details[2], view=network_details[3],
                   network_config=network_details[1], network_id=network_details[0])

    def save_to_db(self):
        with Cursor() as cursor:
            cursor.execute("INSERT INTO network_details(network_config, paw_preference, view) VALUES(%s, %s, %s);",
                           (self.network_config, self.paw_preference, self.view))

