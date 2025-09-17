from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, EmailStr
from typing import Annotated, Literal, Optional, List, Dict, Annotated, Optional
import json
from datetime import date

app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data
@app.get('/')
def home():
    data=load_data()
    return data
