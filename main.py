from fastapi import FastAPI
import json 
app=FastAPI()

def load_data():
    with open('patient.json','/r') as f:
        data=json.load(f)
    return data
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


