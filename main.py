from fastapi import FastAPI
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

def patients(list_index : int):
    data=load_data()
    return data[list_index]['contact']

    


