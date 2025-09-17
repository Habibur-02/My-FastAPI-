from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, EmailStr
from typing import Annotated, Literal, Optional, List, Dict, Annotated, Optional
import json
from datetime import date

app=FastAPI()

def load_data():
    with open('new_patients.json','r') as f:
        data=json.load(f)
    return data
def save_data():
    with open('patients1.json', 'w') as f:
        json.dump(data, f, indent=4, default=str)

@app.get('/')
def home():
    data=load_data()
    return data["P001"]["last_bloodwork"]
@app.get('/about')
def about():
    return {"abc":"Aasif is idle boy"}
@app.get('/patient/{p_id}')
def see_patient(p_id: str=Path(..., title = "Put Patient ID", description= " Give id of patient")):
    data=load_data()
    if p_id not in data:
        raise HTTPException(status_code=404,detail="Id not found")
    else:
        return data[p_id]

@app.get('/city')
def city(city: str=Query(None, description="input city name")):
    data=load_data()
    list_p={}
    for i in data:
        # if city in j:
        #     list_p.append(data[i]["name"])
        if city==data[i]["city"]:
            list_p.append(data[i]["name"])

        
    return list_p



    

