from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Optional, List
import json

app = FastAPI()

class Cast(BaseModel):
    actor: Annotated[str, Field(..., description="abc")]
    role: Annotated[str, Field(..., description="abc")]

class Available(BaseModel):
    platform: Annotated[str, Field(..., description="abc")]
    subscription_required: Annotated[bool, Field(..., description="abc")]

class Movie(BaseModel):
    title: Annotated[str, Field(..., description="abc")]
    director: Annotated[str, Field(..., description="abc")]
    release_year: Annotated[int, Field(..., gt=1900, lt=2100, description="abc")]
    genres: Annotated[List[str], Field(..., description="abc")]
    rating: Annotated[Optional[float], Field(None, description="abc")]
    cast: Annotated[Optional[List[Cast]], Field(None, description="abc")]
    available_on: Annotated[Optional[List[Available]], Field(None, description="abc")]

    @computed_field
    @property
    def is_classic(self) -> bool:
        return self.release_year <= 2000

def load_data():
    try:
        with open('movie.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open('movie.json', 'w') as f:
        json.dump(data, f, indent=4, default=str)

@app.post('/create_movie/{movie_id}')
def create_movie(movie_id: str, movie: Movie):
    data = load_data()
    if movie_id in data:
        raise HTTPException(status_code=400, detail="already found")

    movie_data = movie.model_dump()
    movie_data['is_classic'] = movie.is_classic
    data[movie_id] = movie_data
    save_data(data)
    return {"message": "Movie added", "movie": movie_data}

@app.get('/movies')
def all_movies():
    data = load_data()
    return data  # বা শুধু return [m["title"] for m in data.values()]
