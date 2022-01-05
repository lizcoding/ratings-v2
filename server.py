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
    return render_template("all_movies.html", all_movies=all_movies)


@app.route("/movies/<movie_id>")
def movie_details(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)


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
    all_users = crud.get_users()
    return render_template("all_users.html", all_users=all_users)


@app.route("/users/<user_id>")
def user_profile(user_id):
    user = crud.get_user_by_id(user_id)
    return render_template("user_profile.html", user=user)


@app.route("/login", methods=['POST'])
def handle_login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user.email == email and user.password == password:
        session["user_id"] = user.user_id
        flash("Logged in!")
    else:
        flash("Invalid login credentials.")
    return redirect("/")

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
