from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import traceback
from typing import Dict, List, Tuple
from schema import PaymentVoucher
from datetime import datetime

class ArchivaDB:
    def __init__(self):
        uri = "mongodb://10.12.29.68:27017/?directConnection=true"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.DhuvasDatabase = self.client["365"]
        self.RacksDatabase = self.client["racks"]
        self.BandeyriDatabase = self.client["bandeyri"]

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

    def get_records(self) -> List[Tuple[str, str]]:
        """
        Get the name of all the records in the database.\n
        Returns a list of tuples. Each tuple contains the record name and the rack.\n
        Eg: ``[("record_name", "rack_number")]``
        """
        results: List[Tuple[str, str]] = []
        for rack in self.get_racks():
            if rack["records"]:
                results += [(record, rack["rack"]) for record in rack["records"]]
            else:
                for num, item in rack["sections"].items():
                    results += [(record, rack["rack"]) for record in item["records"]]
        
        return results
    
    def get_pvs(self) -> List[Dict]:
        """Get all the PVs in the database."""
        pvCollection: List[Dict] = self.BandeyriDatabase["pv"].find({})
        results: List[Dict] = []
        for pv in pvCollection:
            # pv["_id"] = str(pv["_id"])
            pv.pop("_id")
            results.append(pv)
        
        return results

    def get_pv(self, pvNum: str):
        """Get a PV from the database using the PV number"""
        pv: Dict = self.BandeyriDatabase["pv"].find_one({"pvNum": pvNum})
        pv.pop("_id")
        return pv
        
    def add_pv(self, PV: PaymentVoucher):
        """Adds the PV to the database"""
        pvCollection = self.BandeyriDatabase["pv"]

        
        for invoice in PV.invoiceDetails:
            # Change the invoice date to a datetime object in each invoice
            invoice["invoiceDate"] = datetime.fromisoformat(invoice["invoiceDate"].replace("Z", "+00:00"))

            # Rounding off the invoice total to 2 decimal
            invoice["invoiceTotal"] = round(float(invoice["invoiceTotal"]), 2)
            
            # Rounding off GL amounts to 2 decimal 
            glDetails = invoice["glDetails"]
            for gl in glDetails:
                gl["amount"] = round(float(gl["amount"]), 2)
            invoice["glDetails"] = glDetails

        pvCollection.insert_one({
            "pvNum": PV.pvNum,
            "businessArea": PV.businessArea,
            "agency": PV.agency, 
            "vendor": PV.vendor,
            "date": PV.date,
            "notes": PV.notes,
            "currency": PV.currency,
            "exchangeRate": PV.exchangeRate,
            "numOfInvoice": len(PV.invoiceDetails),
            "invoiceDetails": PV.invoiceDetails,
            "preparedBy": PV.preparedBy,
            "verifiedBy": PV.verifiedBy,
            "authorisedByOne": PV.authorisedByOne,
            "authorisedByTwo": PV.authorisedByTwo,

            "poNum": PV.poNum,
            "paymentMethod": PV.paymentMethod,
            "parkedDate": PV.parkedDate,
            "postingDate": PV.postingDate,
            "clearingDoc": PV.clearingDoc,
            "transferNum": PV.transferNum
        })

    def update_pv(self, PV: PaymentVoucher) -> Dict:
        """Updates an already existing PV in the DB. Returns the updated PV document."""
        pvCollection = self.BandeyriDatabase["pv"]

        updated_pv = pvCollection.find_one_and_update({"pvNum": PV.pvNum}, { "$set": {
            "businessArea": PV.businessArea,
            "agency": PV.agency, 
            "vendor": PV.vendor,
            "date": PV.date,
            "notes": PV.notes,
            "currency": PV.currency,
            "exchangeRate": PV.exchangeRate,
            "numOfInvoice": len(PV.invoiceDetails),
            "invoiceDetails": PV.invoiceDetails,
            "preparedBy": PV.preparedBy,
            "verifiedBy": PV.verifiedBy,
            "authorisedByOne": PV.authorisedByOne,
            "authorisedByTwo": PV.authorisedByTwo,

            "poNum": PV.poNum,
            "paymentMethod": PV.paymentMethod,
            "parkedDate": PV.parkedDate,
            "postingDate": PV.postingDate,
            "clearingDoc": PV.clearingDoc,
            "transferNum": PV.transferNum 
        }}, return_document=True)

        del updated_pv["_id"]
        
        return updated_pv

    def delete_pv(self, pvNum: str):
        """Deletes the PV with the PV number from the database."""
        pvCollection = self.BandeyriDatabase["pv"]

        pvCollection.delete_one({"pvNum": pvNum})
    
    def get_staff(self):
        """Get the exisitng staff of NAM from the DB."""
        staffCollection: List[Dict] = self.BandeyriDatabase["staff"].find({})

        return [ {
            "_id": str(staff["_id"]),
            "name": staff["name"],
            "designation": staff["designation"]
        } for staff in staffCollection]

    def add_staff(self, name: str, designation: str):
        """Add a new staff with their ``name`` and ``designation``."""
        staffCollection = self.BandeyriDatabase["staff"]
        staffCollection.insert_one({
            "name": name,
            "designation": designation
        })

    def delete_staff(self, staffId: str):
        staffCollection = self.BandeyriDatabase["staff"]
        try:
            staffCollection.delete_one({"_id": ObjectId(staffId)})
            return True
        except Exception:
            print(traceback.print_exc())
            return False

if __name__ == "__main__":
    db = ArchivaDB()