from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, EmailStr
from typing import Annotated, Literal, Optional, List, Dict
import json
from datetime import date

app=FastAPI()


class Medication(BaseModel):
    name: str
    dose: str
    frequency: str

class Bloodwork(BaseModel):
    glucose: float
    hdl: float
    ldl: float
    triglycerides: float
    date: date

class Insurance(BaseModel):
    provider: str
    policy_number: str

class EmergencyContact(BaseModel):
    name: str
    relation: str
    phone: str

class Patient(BaseModel):
    name: str
    city: str
    state: str
    age: int
    
    gender: str
    contact: str
    email: EmailStr
    height: float
    weight: float
    blood_pressure: str
    blood_group: str
    pulse_rate: int
    oxygen_level: int
    temperature: float
    allergies: List[str]
    chronic_conditions: List[str]
    medications: List[Medication]
    last_bloodwork: Bloodwork
    last_visit: date
    next_appointment: date
    insurance: Insurance
    emergency_contact: EmergencyContact

    @computed_field
    @property
    def BMI(self) -> float:
        bmi= self.weight/(self.height**2)
        return bmi


def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data


def save_data(data):
    with open('patients1.json', 'w') as f:
        json.dump(data, f, indent=4, default=str)

@app.get('/saved')
def home():
    dataa=load_data()
    data: Dict[str,Patient]={}
    for i,j in dataa.items():
        val=Patient(**j)
        x=val.model_dump()
        x["BMI"]=val.BMI
        data[i]=x

    # with open("saved_data.json","w") as f:
    #     json.dump(data,f,indent=4,default=str)
    # return {"message": "Saved succesfully"}
    save_data(data)
    return{"kicchu na":"bc"}


@app.get('/patient/{index}')

def view(index : str):
    data=load_data()
    if index not in data:
        raise HTTPException(status_code=404,detail="patient not found")
    else:
        return data[index]



