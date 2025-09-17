from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, EmailStr
from typing import Annotated, Literal, Optional, List, Dict, Annotated, Optional
import json
from datetime import date

app=FastAPI()

class Cast(BaseModel):
    actor : Annotated[str, Field(..., description="abc")]
    role: Annotated[str, Field(...,description="abc")]

class Available(BaseModel):
    platform: Annotated[str, Field(...,description="abc")]
    subscription_required: Annotated[bool, Field(..., description="abc")]
class Movie(BaseModel):
    title : Annotated[str, Field(..., description="abc")]
    director: Annotated[str, Field(..., description="abc")]
    release_year: Annotated[int, Field(..., gt=1900,lt=2100, description="abc")]
    genres : Annotated[List[str],Field(..., description="abc")]
    rating : Annotated[Optional[float], Field(None, description="abc")]
    cast : Annotated[Optional[List[Cast]], Field(None, description="abc")]
    available_on: Annotated[Optional[List[Available]], Field(None, description="abc")]
    @computed_field
    @property
    def is_classis(self) -> bool:
        if self.release_year<=2000:
            return True
        else:
            return False


def load_data():
    with open('movie.json', 'r') as f:
        data=json.load(f)
    return data


def save_data(data):
    with open('movie.json', 'w') as f:
        json.dump(data, f, indent=4, default=str)


@app.post('/create_movie/{movie_id}')
def create_movie(movie_id:str, movie: Movie):
    data=load_data()
    if movie_id in data:
        raise HTTPException(status_code=404, detail="already found")
    
    dataa=movie.model_dump()
    dataa['is_classic']=movie.is_classis
    data[movie_id]=dataa
    save_data(data)
    return data


@app.get('/movies')
def all_movies():
    data=load_data()
    return data
