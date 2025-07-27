from fastapi import FastAPI, Path
import json 
app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data['patients']


@app.get('/')
def hello():
    return {'message':'hello world hiii'}


@app.get('/about')
def about():
    return {'message':'aasif is a idle boy'}

@app.get('/view')

def view():
    data=load_data()
    return data


@app.get('/patients/{list_index}')

def patients(list_index : int =Path(..., title="Put Patients Index",description="there are only 5 patients.",ge=0,le=len(load_data())-1,example="2")):
    data=load_data()
    # return data[list_index]['contact']
    if list_index>len(data):
        return {"Error":"There are only % patients.Give 0-5 index"}
    for i in range(len(data)):
        if i==list_index:
            return data[i]




