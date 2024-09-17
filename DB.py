from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import traceback
from typing import Dict, List


class ArchivaDB:
    def __init__(self):
        uri = "mongodb://10.12.29.68:27017/?directConnection=true"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.DhuvasDatabase = self.client["365"]
        self.RacksDatabase = self.client["racks"]

        self.racksCollection = self.RacksDatabase["racks"]
    
    def get_dhuvas(self):
        """Get all the items in 365 Dhuvas collection."""
        dhuvas = self.DhuvasDatabase["dhuvas"].find({})
        return [
            {
                "id": str(day["_id"]),
                "day" : day["day"],
                "month": day["month"],
                "year": day["year"],
                "detail": day["detail"],
                "source": day["source"] 
            } for day in dhuvas
        ]
    
    def add_dhuvas(self, day: int, month: int, year: int, detail: str, source: str):
        """Add an item (dhuvas) to 365 Dhuvas collection."""
        dhuvasCollection = self.DhuvasDatabase["dhuvas"]
        dhuvasCollection.insert_one({
            "day": day,
            "month": month,
            "year": year,
            "detail": detail,
            "source": source
        })
    
    def remove_dhuvas(self, dhuvasId: str):
        dhuvasCollection = self.DhuvasDatabase["dhuvas"]
        try:
            dhuvasCollection.delete_one({"_id": ObjectId(dhuvasId)})
            return True
        except Exception:
            print(traceback.print_exc())
            return False

    def get_racks(self) -> List[Dict[str, int | str | List[str] | Dict[str, Dict[str, str | List[str]]]]]:
        """Get the list of the records room racks."""
        return [rack for rack in self.racksCollection.find({})]

    def get_rack(self, rackRoute: str) -> Dict[str, int | str | List[str] | Dict[str, Dict[str, str | List[str]]]] | None:
        """Get rack details using the rack route."""
        return self.racksCollection.find_one({"rack_route": rackRoute})
    
    def update_rack_sections(self, rackRoute: str, section: Dict[str, Dict[str, str | List[str]]]):
        """Use this function to update the sections details of a rack"""
        if type(section) != dict:
            return False
        else:
            self.racksCollection.find_one_and_update({"rack_route": rackRoute}, {"$set": {"sections": section}})
            return True


if __name__ == "__main__":
    db = ArchivaDB()
