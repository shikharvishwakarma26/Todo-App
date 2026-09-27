# validation on Movies

from fastapi import FastAPI,Body,Path,Query,HTTPException
from pydantic import BaseModel,Field
from typing import Optional
import uvicorn
from starlette import status

app=FastAPI()

class Movie():
    id:int
    name:str 
    director:str 
    rating:int 

def __init__(self,id,name,director,rating):
    self.id=id
    self.name=name
    self.director=director
    self.rating=rating


class MovieRequest(BaseModel):
    id:int
    name:str=Field(min_length=3)
    director:str=Field(min_length=1)
    rating:int=Field(gt=0,lt=5)

    model_config={
"json_schema_extra":{
    "name":"movie name",
    "director":"directors name",
    "rating":"movie rating by viwers"
}
    }

Movies = [
    {"id": 1, "name": "top gun", "director": "tony scot", "rating": 2},
    {"id": 2, "name": "avatar", "director": "cameron", "rating": 4},
    {"id": 3, "name": "squid game", "director": "hwang", "rating": 3}
]   


@app.get("/movies")
async def watch_movies():
    return Movies


# fetch some movies
@app.get("/movies/{movie_id}")
async def watch_movie(movie_id:int):
    for movie in Movies:
        if movie.get('id')==movie_id:
            return movie




# pydentic post request
@app.post("/new_movie")
async def new_movie(movie_request:MovieRequest):
    new_movie=Movie(**movie_request.model_dump())
    Movies.append(new_movie)

def find_movie_id(Movie:Movie):
    Movie.id=1 if len(Movies) ==0 else Movies[-1].id+1
    return Movie


# validate with path parameter
@app.get("/movies/{movies_id}")
async def watch_all_movies (movies_id:int=Path(gt=0)):
    for movie in Movies:
        if movie.get('id')==movies_id:
            return Movie

# validation with query parameter
@app.get("/movies")
async def movie_rating(movie_rating:int=Query(gt=0,lt=5)):
    movie_to_return=[]
    for movie in Movies:
        if movie.get('rating')==movie_rating:
            movie_to_return.append(movie)
            return movie_to_return

        
# http exception and status expicit code
@app.get("/movie/{movie_id}",status_code=status.HTTP_204_NO_CONTENT)
async def watch_movie_id(movie_id:int=Path(gt=0)):
    for movie in Movies:
        if movie.get('id')==movie_id:
            return Movies
        raise HTTPException(status_code=404)
