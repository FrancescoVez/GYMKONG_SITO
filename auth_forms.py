from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=72)])
    submit = SubmitField("Crea account")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=72)])
    submit = SubmitField("Accedi")

# ---------- ADMIN ----------
class AdminCreateUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=72)])
    is_admin = BooleanField("Admin?")
    submit = SubmitField("Crea utente")

class AdminResetPasswordForm(FlaskForm):
    new_password = PasswordField("Nuova password", validators=[DataRequired(), Length(min=6, max=72)])
    submit = SubmitField("Reset password")
