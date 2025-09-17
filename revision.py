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
    return data["P001"]
