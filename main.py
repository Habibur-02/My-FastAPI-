from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def hello():
    return {'message':'hello world hiii'}


@app.get('/about')
def about():
    return {'message':'aasif is a idle boy'}


