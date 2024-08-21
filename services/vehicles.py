from models.vehicles import Vehicles as VehiclesModel
class VehiclesService():
    def __init__(self, db) -> None:
        self.db = db

    def get_vehicles(self):
        result = self.db.query(VehiclesModel).all
        return result