from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, EmailStr
from typing import Annotated, Literal, Optional, List, Dict, Annotated, Optional
import json
from datetime import date

app=FastAPI()


# class Medication(BaseModel):
#     name: str
#     dose: str
#     frequency: str

# class Bloodwork(BaseModel):
#     glucose: float
#     hdl: float
#     ldl: float
#     triglycerides: float
#     date: date

# class Insurance(BaseModel):
#     provider: str
#     policy_number: str

# class EmergencyContact(BaseModel):
#     name: str
#     relation: str
#     phone: str

# class Patient(BaseModel):
#     name: str
#     city: str
#     state: str
#     age: int
    
#     gender: str
#     contact: str
#     email: EmailStr
#     height: float
#     weight: float
#     blood_pressure: str
#     blood_group: str
#     pulse_rate: int
#     oxygen_level: int
#     temperature: float
#     allergies: List[str]
#     chronic_conditions: List[str]
#     medications: List[Medication]
#     last_bloodwork: Bloodwork
#     last_visit: date
#     next_appointment: date
#     insurance: Insurance
#     emergency_contact: EmergencyContact

#     @computed_field
#     @property
#     def bmi(self) -> float:
#         bmi= self.weight/(self.height**2)
#         return bmi
    
#     @computed_field
#     @property
#     def verdict(self) -> str:
#         # bmi= self.weight/(self.height**2)

#         if self.bmi < 18.5:
#             return 'Underweight'
#         elif self.bmi < 25:
#             return 'Normal'
#         elif self.bmi < 30:
#             return 'Normal'
#         else:
#             return 'Obese'
# from typing import List, Literal, Annotated, Optional
# from pydantic import BaseModel, Field, computed_field, EmailStr
# from datetime import date
# from typing import List, Literal, Annotated, Optional
# from pydantic import BaseModel, Field, computed_field, EmailStr
# from datetime import date

class Medication(BaseModel):
    name: Annotated[str, Field(..., description='Medication name')]
    dose: Annotated[str, Field(..., description='Dosage of the medication')]
    frequency: Annotated[str, Field(..., description='How often the medication is taken')]

class Bloodwork(BaseModel):
    glucose: Annotated[float, Field(..., description='Glucose level')]
    hdl: Annotated[float, Field(..., description='HDL cholesterol')]
    ldl: Annotated[float, Field(..., description='LDL cholesterol')]
    triglycerides: Annotated[float, Field(..., description='Triglyceride level')]
    date: Annotated[date, Field(..., description='Date of bloodwork')]

class Insurance(BaseModel):
    provider: Annotated[str, Field(..., description='Insurance provider name')]
    policy_number: Annotated[str, Field(..., description='Policy number')]

class EmergencyContact(BaseModel):
    name: Annotated[str, Field(..., description='Emergency contact name')]
    relation: Annotated[str, Field(..., description='Relation to patient')]
    phone: Annotated[str, Field(..., description='Contact phone number')]

class Patient(BaseModel):
    name: Annotated[str, Field(..., description='Full name of the patient')]
    city: Annotated[str, Field(..., description='City of residence')]
    state: Annotated[str, Field(..., description='State of residence')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age in years')]
    
    gender: Annotated[str, Field(..., description='Gender of the patient')]
    contact: Optional[str] = Field(None, description='Phone number')
    email: Optional[EmailStr] = Field(None, description='Email address')

    height: Annotated[float, Field(..., gt=0, description='Height in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight in kilograms')]

    blood_pressure: Optional[str] = Field(None, description='Blood pressure')
    blood_group: Optional[str] = Field(None, description='Blood group')
    pulse_rate: Optional[int] = Field(None, description='Pulse rate')
    oxygen_level: Optional[int] = Field(None, description='Oxygen saturation level')
    temperature: Optional[float] = Field(None, description='Body temperature')
    
    allergies: Optional[List[str]] = Field(default_factory=list, description='Known allergies')
    chronic_conditions: Optional[List[str]] = Field(default_factory=list, description='Chronic health conditions')
    medications: Optional[List[Medication]] = Field(default_factory=list, description='Current medications')
    last_bloodwork: Optional[Bloodwork] = Field(None, description='Most recent bloodwork results')
    last_visit: Optional[date] = Field(None, description='Last visit date')
    next_appointment: Optional[date] = Field(None, description='Next appointment date')
    
    insurance: Optional[Insurance] = Field(None, description='Insurance information')
    emergency_contact: Optional[EmergencyContact] = Field(None, description='Emergency contact person')

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'



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
        x["bmi"]=val.bmi
        x["verdict"]=val.verdict
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



@app.post('/create/{patient_id}')
def create(patient_id : str, patient:Patient):
    data=load_data()
    if patient_id in data:
        raise HTTPException(status_code=404, detail="Already added")
    daaata=patient.model_dump()
    daaata['bmi']=patient.bmi
    daaata['verdict']=patient.verdict
    data[patient_id]=daaata
    save_data(data)
    return {"message": "Patient created successfully", "id": patient_id}