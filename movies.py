from fastapi import FastAPI,Body

app=FastAPI()

movies = [
    {
        "movie_name": "Avatar",
        "director_name": "James Cameron",
        "released_year": 2009,
        "genre": "Science Fiction, Adventure",
        "cost_year": "$237 million",
        "worldwide_box_office": "$2.92 billion"
    },
    {
        "movie_name": "Avengers: Endgame",
        "director_name": "Anthony Russo, Joe Russo",
        "released_year": 2019,
        "genre": "Action, Science Fiction",
        "cost_year": "$356 million",
        "worldwide_box_office": "$2.80 billion"
    },
    {
        "movie_name": "Avatar: The Way of Water",
        "director_name": "James Cameron",
        "released_year": 2022,
        "genre": "Science Fiction, Adventure",
        "cost_year": "$250 million",
        "worldwide_box_office": "$2.32 billion"
    },
    {
        "movie_name": "Titanic",
        "director_name": "James Cameron",
        "released_year": 1997,
        "genre": "Romance, Drama",
        "cost_year": "$210 million",
        "worldwide_box_office": "$2.26 billion"
    },
    {
        "movie_name": "Star Wars: The Force Awakens",
        "director_name": "J. J. Abrams",
        "released_year": 2015,
        "genre": "Science Fiction, Adventure",
        "cost_year": "$447 million",
        "worldwide_box_office": "$2.07 billion"
    },
    {
        "movie_name": "Avengers: Infinity War",
        "director_name": "Anthony Russo, Joe Russo",
        "released_year": 2018,
        "genre": "Action, Science Fiction",
        "cost_year": "$316 million",
        "worldwide_box_office": "$2.05 billion"
    },
    {
        "movie_name": "Spider-Man: No Way Home",
        "director_name": "Jon Watts",
        "released_year": 2021,
        "genre": "Action, Superhero",
        "cost_year": "$200 million",
        "worldwide_box_office": "$1.92 billion"
    },
    {
        "movie_name": "Jurassic World",
        "director_name": "Colin Trevorrow",
        "released_year": 2015,
        "genre": "Science Fiction, Adventure",
        "cost_year": "$150 million",
        "worldwide_box_office": "$1.67 billion"
    },
    {
        "movie_name": "The Lion King",
        "director_name": "Jon Favreau",
        "released_year": 2019,
        "genre": "Animation, Adventure",
        "cost_year": "$260 million",
        "worldwide_box_office": "$1.65 billion"
    },
    {
        "movie_name": "Top Gun: Maverick",
        "director_name": "Joseph Kosinski",
        "released_year": 2022,
        "genre": "Action, Drama",
        "cost_year": "$170 million",
        "worldwide_box_office": "$1.50 billion"
    }
]

@app.get("/all_movies/")
async def watch_all():
    return movies

@app.get("/movie/{movie_name}/")
async def watch_movie(movie_name:str):
    movie_to_return=[]
    for movie in movies:
        if movie.get('movie_name').casefold()==movie_name.casefold():
            movie_to_return.append(movie)
    return movie_to_return

@app.post("/movies/new")
async def add_movie(new_movie=Body()):
    movies.append(new_movie)

@app.put("/movies/update_movie")
async def update_movie(update_movie=Body()):
    for i in range (len(movies)):
        if movies[i].get('movie_name').casefold()==update_movie.get('movie_name').casefold():
            movies[i]=update_movie
 

@app.delete("/movies/delete_movies/{_name}")
async def delete_movie(movie_name:str):
    for i in range (len(movies)):
        if movies[i].get('movie_name').casefold()==movie_name.casefold():
            movies.pop(i)
            break
        