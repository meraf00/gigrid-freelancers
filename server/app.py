import os
from datetime import datetime
from dotenv import load_dotenv

from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from model import User, UserType, db
from chat import chat_bp, socketio
from docs.doc import doc_bp
from auth import AuthenticationManager

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

socketio.init_app(app)

app.register_blueprint(chat_bp, url_prefix='/messages')
app.register_blueprint(doc_bp, url_prefix='/docs')

auth_manager = AuthenticationManager(os.getenv('FLASK_SECRET_KEY'))


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        redirect_url = request.form.get('redirect', url_for('home'))

        if auth_manager.verify_credentials(email, password):
            user = User.get_by_email(email)
            user.token = auth_manager.generate_auth_token(user.id)
            db.session.commit()

            login_user(user)
            return redirect(redirect_url)
        else:
            return render_template("login.html", message="Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    user = User.get(current_user.id)
    user.token = None
    db.session.commit()
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
                        email=email, password=generate_password_hash(password),
                        date_of_birth=datetime.now(), user_type=UserType.FREELANCER)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html")


if __name__ == "__main__":
    socketio.run(app, debug=True)
