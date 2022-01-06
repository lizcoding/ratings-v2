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


def create_rating(user, movie, score):
    new_rating = Rating(user=user, movie=movie, score=score)
    db.session.add(new_rating)
    db.session.commit()
    
    return new_rating


if __name__ == '__main__':
    from server import app
    connect_to_db(app)