from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from pytesseract import image_to_string
from telegram import Bot

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://username:password@localhost/db_name"
db = SQLAlchemy(app)

fake = Faker()

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    coins = db.Column(db.Integer, nullable=False, default=0)
    referrals = db.Column(db.Integer, nullable=False, default=0)

# Define the Referral model
class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    referral_link = db.Column(db.String(255), nullable=False)
    referral_type = db.Column(db.String(255), nullable=False)

# Define the PromoCode model
class PromoCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), nullable=False)
    coins = db.Column(db.Integer, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

# Define the Telegram bot
bot = Bot(token="YOUR_TELEGRAM_BOT_TOKEN")

# Define the routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    user = User.query.filter_by(username=session["username"]).first()
    referrals = Referral.query.filter_by(user_id=user.id).all()
    return render_template("dashboard.html", referrals=referrals)

@app.route("/referral", methods=["GET", "POST"])
def referral():
    if request.method == "POST":
        referral_link = request.form["referral_link"]
        referral_type = request.form["referral_type"]
        user = User.query.filter_by(username=session["username"]).first()
        referral = Referral(user_id=user.id, referral_link=referral_link, referral_type=referral_type)
        db.session.add(referral)
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("referral.html")

@app.route("/promo_code", methods=["GET", "POST"])
def promo_code():
    if request.method == "POST":
        code = request.form["code"]
        promo_code = PromoCode.query.filter_by(code=code).first()
        if promo_code:
            user = User.query.filter_by(username=session["username"]).first()
            user.coins += promo_code.coins
            db.session.commit()
            return redirect(url_for("dashboard"))
    return render_template("promo_code.html")

if __name__ == "__main__":
    app.run(debug=True)
