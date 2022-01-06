"""CRUD operations."""

from flask.templating import _default_template_ctx_processor
from flask_sqlalchemy import _record_queries
from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    
    return user

def get_users():
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


def create_movie(title, overview, release_date, poster_path):
    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)
    db.session.add(movie)
    db.session.commit()
    
    return movie


def get_movies():
    return Movie.query.all()


def get_movie_by_id(movie_id):
    return Movie.query.get(movie_id)


def get_movie_rating_by_user(user_id, movie_id):
    return Rating.query.filter(Rating.user_id == user_id and Rating.movie_id == movie_id).all()


def create_rating(user, movie, score):
    db_user = User.query.get(user)
    all_ratings = db_user.ratings
    movie_ratings = []
    for obj in all_ratings:
        if obj.movie_id == movie.movie_id:
            movie_ratings.append(obj)

    if movie_ratings:
        movie_ratings.clear()
        db.session.commit()
    
    new_rating = Rating(user=db_user, movie=movie, score=score)
    db.session.add(new_rating)
    db.session.commit()
    
    return new_rating


if __name__ == '__main__':
    from server import app
    connect_to_db(app)