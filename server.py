"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/movies")
def all_movies():
    all_movies = crud.get_movies()

    if session.get("user_id"):
        return render_template("all_movies.html", all_movies=all_movies)
    else:
        return redirect("/")
    

@app.route("/movies/<movie_id>")
def movie_details(movie_id):    
    if session.get("user_id") is None:
        return redirect("/")
    else:
        movie = crud.get_movie_by_id(movie_id)
        if movie.ratings:
            avg_rating = sum([r.score for r in movie.ratings]) / len([r.score for r in movie.ratings])
            rating = ("{:.2f}".format(avg_rating))
        else:
            rating = ""
        return render_template("movie_details.html", movie=movie, rating=rating)


@app.route("/users", methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)

    if user:
        flash("That email is already associated with an account.")
    else:
        crud.create_user(email, password)
        flash("Account created!")
    
    return redirect("/")


@app.route("/show_users")
def all_users():
    if session.get("user_id"): 
        all_users = crud.get_users()
        return render_template("all_users.html", all_users=all_users)
    else:
        return redirect("/")


@app.route("/users/<user_id>")
def user_profile(user_id):
    if session.get("user_id"): 
        user = crud.get_user_by_id(user_id)
        return render_template("user_profile.html", user=user)
    else:
        return redirect("/")


@app.route("/login", methods=['POST'])
def handle_login():
    email = request.form.get("email")
    password = request.form.get("password")
    if session.get("user_id"): 
        user = crud.get_user_by_email(email)
        if user.email == email and user.password == password:
            session["user_id"] = user.user_id
            flash("Logged in!")
        else:
            flash("Invalid login credentials.")
    else:
        flash("No user associated with this account.")
    return redirect("/")


@app.route("/movies/<movie_id>/rating", methods = ["POST"])
def rate_movie(movie_id):
    new_rating = int(request.form.get("rating"))
    movie = crud.get_movie_by_id(movie_id)
    user = crud.get_user_by_id(session["user_id"])

    crud.create_rating(user, movie, new_rating)
    avg_rating = sum([r.score for r in movie.ratings]) / len([r.score for r in movie.ratings])
    rounded_avg_rating = ("{:.2f}".format(avg_rating))
    return render_template("movie_details.html", movie=movie, rating=rounded_avg_rating)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
