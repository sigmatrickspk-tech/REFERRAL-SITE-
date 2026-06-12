from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class ReferralForm(FlaskForm):
    referral_link = StringField("Referral Link", validators=[DataRequired()])
    referral_type = StringField("Referral Type", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PromoCodeForm(FlaskForm):
    code = StringField("Promo Code", validators=[DataRequired()])
    submit = SubmitField("Submit")
