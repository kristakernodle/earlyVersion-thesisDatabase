from models.cursors import Cursor


class DLCNetworks:
    def __init__(self, network_name, network_dir, experiment_id, network_id=None):
        self.network_name = network_name
        self.network_dir = network_dir
        self.experiment_id = experiment_id
        self.network_id = network_id

    def __str__(self):
        return f"< Network {self.network_dir} >"

    @classmethod
    def from_db(cls, network_name):
        with Cursor() as cursor:
            cursor.execute("SELECT * FROM dlc_networks WHERE network_name = %s;", (network_name,))
            network = cursor.fetchone()
            return cls(network_name=network[3], network_dir=network[2], experiment_id=network[1], network_id=network[0])

    def save_to_db(self):
        with Cursor() as cursor:
            cursor.execute("INSERT INTO dlc_networks(experiment_id, network_dir, network_name) VALUES(%s, %s, %s);",
                           (self.experiment_id, self.network_dir, self.network_name))
