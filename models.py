from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    coins = db.Column(db.Integer, nullable=False, default=0)
    referrals = db.Column(db.Integer, nullable=False, default=0)

class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    referral_link = db.Column(db.String(255), nullable=False)
    referral_type = db.Column(db.String(255), nullable=False)

class PromoCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), nullable=False)
    coins = db.Column(db.Integer, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
