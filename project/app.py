import os

from flask import Flask, flash, redirect, render_template, request, session,jsonify
import requests
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from db import Database
import sqlite3
# Initialize the database
db = Database("project.db")


# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  # Store sessions in the file system
Session(app)  

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

geocoding_api_endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", 
            (request.form.get("username"),), 
            fetch_all=True
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]


        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/apply", methods=["GET", "POST"])
def apply():
    if request.method == "POST":
        return render_template("ngo_options.html")
    return render_template("apply.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'GET':
        return render_template("register.html")
    else:
        number = request.form.get("number")  # Accessing Phone number
        email = request.form.get("email")  # Accessing Email
        username = request.form.get("username")  # Accessing Username
        password = request.form.get("password")  # Accessing Password
        confirm = request.form.get("confirm")  # Accessing Confirm password

        # All fields should be validated
        if not number or not email or not username or not password or not confirm:
            return apology("no empty fields")

        # Check if passwords matches with confirm password
        if password != confirm:
            return apology("Password do not match")
        # check the email format
        if '@' not in email or '.' not in email:
            return apology("Invalid email format")

        # Hash the password using library
        hashed_password = generate_password_hash(password)

        # Check if the username already exists in the database

        newuser = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        if newuser:
            return apology("Username already exits")

        # inserting the data in database
        db.execute("INSERT INTO users(username,password,email,phone_number) VALUES(?,?,?,?)", (username,hashed_password,email,number))

        flash("Registration successful! Please log in.", "success") # flashing the message for success
        return redirect("/login") # redirecting to login page

@app.route("/", methods = ["GET", "POST"])
@login_required
def index():
    return render_template("index.html")

# For debugging the error this command is used which shows in terminal window which values are passing to it
if __name__ == "__main__":
    app.run(debug=True)
