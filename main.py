from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from AssetRegisterReader import AssetRegister
from DB import ArchivaDB
from schema import Dhuvas
from typing import List, Dict
import traceback

app = FastAPI(
    title="ArchivaAPI",
    version="0.1.2"
)

DB = ArchivaDB()

origins = [
    "http://localhost:3000",
    "https://10.12.29.68:3001",
    "http://10.12.29.68:3001",
    "https://10.12.29.68:3000",
    "http://10.12.29.68:3000",
    "http://10.12.29.70:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

asset_register = AssetRegister()

@app.get("/")
async def root():
    return {"start": "Welcome to Archiva API", "last_updated": "23/09/2024"}

@app.get("/assets")
async def assets():
    _assets = asset_register.read_assets_json_file()
    return _assets

@app.get("/asset/{asset_num}")
async def asset(asset_num: str):
    _assets = asset_register.read_assets_json_file()
    for each_asset in _assets:
        if asset_num == each_asset["asset_number"]:
            return each_asset
    return {
                "asset_number": "",
                "sap_number": "",
                "name": "",
                "present_location": "",
                "condition": ""
            }

@app.get("/update_assets")
async def update_assets():
    try:
        asset_register.export_to_json()
        return {"success": True, "message": "Successfully updated assets data"}
    except Exception:
        return {"success": False, "message": traceback.print_exc()}
    
@app.get("/dhuvas")
async def dhuvas():
    try:
        result = DB.get_dhuvas()
        return {"success": True, "result": result}
    except Exception:
        return {"success": False, "result": traceback.print_exc()}
    

@app.post("/dhuvas/add/")
async def add_dhuvas(dhuvas: Dhuvas):
    try:
        DB.add_dhuvas(
            day=dhuvas.day,
            month=dhuvas.month,
            year=dhuvas.year,
            detail=dhuvas.detail,
            source=dhuvas.source
        )
        return {"success": True, "message": "Successfully added dhuvas!"}
    except Exception:
        return {"success": False, "message": traceback.print_exc()}

@app.post("/dhuvas/remove/")
async def remove_dhuvas(dhuvas: Dhuvas):
    try:
        DB.remove_dhuvas(dhuvasId = dhuvas.id)
        return {"success": True, "message": "Successfully removed dhuvas!"}
    except Exception:
        return {"success": False, "message": traceback.print_exc()}

@app.get("/racks/")
async def racks():
    """Used to get the details of all the racks in the records room."""
    return DB.get_racks()

@app.get("/racks/{rackRoute}")
async def get_rack(rackRoute: str):
    """Used to get the details of a specifc rack in the records room."""
    return DB.get_rack(rackRoute.lower())

@app.get("/records/all")
async def get_all_records():
    """Used to get all the records in the database."""
    # results = DB.get_records()
    results = [{"name": record, "rack": rack} for record, rack in DB.get_records()]
    return results

@app.get("/records/search/{query}")
async def searchRecords(query: str):
    """
    Used to search for records in the database.\n 
    Returns a list of tuples, each tuple containing the name of the record and the rack number.
    """
    records = DB.get_records()
    results = [(record, rack) for record, rack in records if query in record]
    return results