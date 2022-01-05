import crud, model, server, os, json
from random import choice, randint
from datetime import datetime

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

movies_in_db = []
for movie in movie_data:
    title = movie["title"]
    overview = movie["overview"]
    poster_path = movie["poster_path"]
    release_date = datetime.strptime(movie["release_date"], '%Y-%m-%d')
    
    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"

    user = crud.create_user(email, password)

    for _ in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1, 5)

        crud.create_rating(user, random_movie, score)
