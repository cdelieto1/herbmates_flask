"""Automate the db creation and population"""

import os, json, crud, model, server
from datetime import datetime


os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

# with open('data/movies.json') as f:
#     movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings
movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = (movie['title'],
                                    movie['overview'],
                                    movie['poster_path'])
    release_date = datetime.strptime(movie['release_date'], '%Y-%m-%d')

    db_movie = crud.create_movie(title,
                                 overview,
                                 release_date,
                                 poster_path)
    movies_in_db.append(db_movie)

# Create 4 users; each user will have 1 apt complex. We need 2 users per complex.
# 1 for pickup, one for delivery. 
for n in range(4):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'
    complex_id = 1

    user = crud.create_user(email, password, complex_id)

    for _ in range(4):
        random_herb = choice(movies_in_db)
        score = randint(1, 5)

        crud.create_rating(user, random_movie, score)
    