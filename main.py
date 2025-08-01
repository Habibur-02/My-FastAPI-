from fastapi import FastAPI, Path, HTTPException, Query
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

def patients(list_index : int =Path(..., title="Put Patients Index",description="there are only 5 patients.")): #,ge=0,le=len(load_data())-1,example="2") we can add this also,there are some benifits
    data=load_data()
    # x=len(data)
    # return data[list_index]['contact']
    if list_index>len(data):
        # return {"Error":"There are only % patients.Give 0-5 index. {list_index} is not appropiate"}
        raise HTTPException(status_code=404, detail=" ID not found.")
    for i in range(len(data)):
        if i==list_index:
            return data[i]



# @app.get('/sort')
# def sort_patients(sort_by : str =Query(..., description="based on age, hight, bmi"), order: str =Query('asc',description="sort in ascending or decending")):
#     valid_fields=['age']
#     if sort_by not in valid_fields:
#         raise HTTPException(status_code=404, detail=f"Invalid field. keep input on {valid_fields}")
#     if order not in ['asc','desc']:
#         raise HTTPException(status_code=404,detail=f"Invalid order,keep it in {'asc','desc'}")
    
#     data=load_data()
#     sorted_data = sorted(data, key=lambda x: x.get(sort_by, 0), reverse=sort_order)


@app.get('/sort')
def sort_patients(
    sort_by: str = Query(default="age", description="Sort by field (currently only 'age' supported)"),
    order: str = Query(default="asc", description="Sort order: 'asc' or 'desc'")
):
    data = load_data()
    
    valid_fields = ['age']
    
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field. Only these fields are supported: {valid_fields}"
        )
    
    if order not in ['asc', 'desc']:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Must be either 'asc' or 'desc'"
        )
    
    
    reverse_order = (order == 'desc')
    try:
        sorted_data = sorted(data, key=lambda x: x[sort_by], reverse=reverse_order)
        return sorted_data
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail=f"Field '{sort_by}' not found in patient records"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while sorting: {str(e)}"
        )
    


    