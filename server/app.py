import os
from dotenv import load_dotenv

from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from werkzeug.security import generate_password_hash

from model import User, db
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("home.html", current_user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if User.authenticate(email, password):
            user = User.get_by_email(email)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return "Invalid"
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname = request.form.get("firstname")
        lname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = User(firstname=fname, lastname=lname,
                        email=email, password=generate_password_hash(password), date_of_birth=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
