from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app=FastAPI()



def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data



@app.get('/')
def home():
    dataa=load_data()
    return dataa




