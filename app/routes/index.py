from fastapi import APIRouter
from fastapi import File, UploadFile

import requests
from starlette.requests import Request
from starlette.responses import JSONResponse

from pydantic import BaseModel
import json

#from inspect import currentframe as frame
from datetime import datetime
from dataclasses import asdict
from typing import Optional

router = APIRouter()

db = []

class City(BaseModel):
    name:str
    timezone:str

@router.get("/")
async def root(req: Request):
    """
    `ELB 상태 체크용 API` \n
    :return:
    """
    return JSONResponse( {'hello':'sixxx'} )

@router.get("/cities")
def get_cities():
    results = []
    for aCity in db:
        strs = f"http://worldtimeapi.org/api/timezone/{aCity['timezone']}"
        r = requests.get(strs)
        cur_time = r.json()['datetime']
        results.append(
            {'name':aCity['name'],
                'timezone':aCity['timezone'],
                'current_time':cur_time}
        )
    return results

@router.get("/cities/{city_id}")
async def get_city(city_id:int):
    #db[]
    aCity = db[city_id-1]
    strs = f"http://worldtimeapi.org/api/timezone/{aCity['timezone']}"
    r = requests.get(strs)
    cur_time = r.json()['datetime']
    return(
        {'name':aCity['name'],
            'timezone':aCity['timezone'],
            'current_time':cur_time}
    )

@router.post("/uploadfile/")
async def create_upload_file(myFile: UploadFile = File(...)):
    contents = await myFile.read()
    con_dict = json.loads(contents)
    for i in con_dict:
        db.append(i)
    print(db)
    return {"filename": myFile.filename}

@router.post("/cities")
async def create_city(city: City):
    db.append(city.dict())
    return db[-1]

@router.delete("/cities/{city_id}")
def delete_city(city_id:int):
    db.pop(city_id-1) 
    return {}