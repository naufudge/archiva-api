from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from AssetRegisterReader import AssetRegister
from DB import ArchivaDB
from schema import Dhuvas, PaymentVoucher
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
    "http://10.12.29.207:3000",
    "http://10.12.29.207:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

asset_register = AssetRegister()

@app.get("/", tags=["root"])
async def root():
    return {"start": "Welcome to Archiva API", "last_updated": "23/09/2024"}

@app.get("/assets", tags=["assets"])
async def assets():
    _assets = asset_register.read_assets_json_file()
    return _assets

@app.get("/asset/{asset_num}", tags=["assets"])
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

@app.get("/update_assets", tags=["assets"])
async def update_assets():
    try:
        asset_register.export_to_json()
        return {"success": True, "message": "Successfully updated assets data"}
    except Exception:
        return {"success": False, "message": traceback.print_exc()}
    
@app.get("/dhuvas", tags=["dhuvas"])
async def dhuvas():
    try:
        result = DB.get_dhuvas()
        return {"success": True, "result": result}
    except Exception:
        return {"success": False, "result": traceback.print_exc()}
    

@app.post("/dhuvas/add/", tags=["dhuvas"])
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

@app.post("/dhuvas/remove/", tags=["dhuvas"])
async def remove_dhuvas(dhuvas: Dhuvas):
    try:
        DB.remove_dhuvas(dhuvasId = dhuvas.id)
        return {"success": True, "message": "Successfully removed dhuvas!"}
    except Exception:
        return {"success": False, "message": traceback.print_exc()}

@app.get("/racks/", tags=["records"])
async def racks():
    """Used to get the details of all the racks in the records room."""
    return DB.get_racks()

@app.get("/racks/{rackRoute}", tags=["records"])
async def get_rack(rackRoute: str):
    """Used to get the details of a specifc rack in the records room."""
    return DB.get_rack(rackRoute.lower())

@app.get("/records/all", tags=["records"])
async def get_all_records():
    """Used to get all the records in the database."""
    # results = DB.get_records()
    results = [{"name": record, "rack": rack} for record, rack in DB.get_records()]
    return results

@app.get("/records/search/{query}", tags=["records"])
async def searchRecords(query: str):
    """
    Used to search for records in the database.\n 
    Returns a list of tuples, each tuple containing the name of the record and the rack number.
    """
    records = DB.get_records()
    results = [(record, rack) for record, rack in records if query in record]
    return results

@app.post("/pvs", tags=["pvs"])
async def add_PV(pv: PaymentVoucher):
    try:
        DB.add_pv(pv)
        return {"success": True, "message": "Successfully added PV!"}
    except Exception:
        return {"success": False, "message": traceback.print_exc()}


@app.get("/pvs", tags=["pvs"])
async def get_PVs():
    try:
        result = DB.get_pvs()
        return {"success": True, "result": result}
    except Exception:
        return {"success": False, "result": traceback.print_exc()}


@app.put("/pvs", tags=["pvs"])
async def update_PV(pv: PaymentVoucher):
    """Updates a PV"""
    try:
        result = DB.update_pv(pv)
        return {"success": True, "result": result}
    except:
        return {"success": False, "result": traceback.print_exc()}


@app.get("/pvs/{pvNum}", tags=["pvs"])
async def get_PV(pvNum: str):
    try:
        result = DB.get_pv(pvNum)
        return {"success": True, "result": result}
    except:
        return {"success": False, "result": traceback.print_exc()}

@app.delete("/pvs/{pvNum}", tags=["pvs"])
async def delete_PV(pvNum: str):
    try:
        result = DB.delete_pv(pvNum)
        return {"success": True, "result": result}
    except:
        return {"success": False, "result": traceback.print_exc()}
