import os
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from models import db, User
from auth_forms import RegisterForm, LoginForm, AdminCreateUserForm, AdminResetPasswordForm

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///site.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))

def ensure_admin_user():
    admin_email = "admin@gymkong.it"
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(username="admin", email=admin_email, is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

# Flask 3 workaround: init DB once
_db_initialized = False
@app.before_request
def _init_db_once():
    global _db_initialized
    if not _db_initialized:
        db.create_all()
        ensure_admin_user()
        _db_initialized = True

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        if not getattr(current_user, "is_admin", False):
            abort(403)
        return fn(*args, **kwargs)
    return wrapper

# ------------------ WEBSITE PAGES ------------------
@app.get("/")
def index():
    return render_template("index.html", active_page="home")

@app.get("/corsi")
def corsi():
    return render_template("corsi.html", active_page="corsi")

@app.get("/planning")
def planning():
    return render_template("planning.html", active_page="planning")

@app.get("/centro")
def centro():
    return render_template("centro.html", active_page="centro")

@app.get("/tribu")
def tribu():
    return render_template("tribu.html", active_page="tribu")

@app.get("/evidenza")
def evidenza():
    return render_template("evidenza.html", active_page="evidenza")

@app.get("/contatti")
def contatti():
    return render_template("contatti.html", active_page="contatti")

# ------------------ AUTH ------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        username = form.username.data.strip()

        if User.query.filter_by(email=email).first():
            flash("Email già registrata.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Username già usato.", "danger")
            return redirect(url_for("register"))

        user = User(username=username, email=email, is_admin=False)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Account creato!", "success")
        return redirect(url_for("index"))

    return render_template("auth_register.html", form=form, active_page="")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in.", "success")
            return redirect(url_for("index"))

        flash("Credenziali non valide.", "danger")

    return render_template("auth_login.html", form=form, active_page="")

@app.get("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("index"))

# ------------------ ADMIN ------------------
@app.route("/admin/users", methods=["GET", "POST"])
@login_required
@admin_required
def admin_users():
    create_form = AdminCreateUserForm()
    reset_form = AdminResetPasswordForm()

    # CREATE USER
    if request.method == "POST" and request.form.get("action") == "create_user":
        if create_form.validate_on_submit():
            email = create_form.email.data.lower().strip()
            username = create_form.username.data.strip()

            if User.query.filter_by(email=email).first():
                flash("Email già esistente.", "danger")
                return redirect(url_for("admin_users"))

            if User.query.filter_by(username=username).first():
                flash("Username già esistente.", "danger")
                return redirect(url_for("admin_users"))

            u = User(
                username=username,
                email=email,
                is_admin=bool(create_form.is_admin.data),
            )
            u.set_password(create_form.password.data)
            db.session.add(u)
            db.session.commit()

            flash("Utente creato.", "success")
            return redirect(url_for("admin_users"))
        else:
            flash("Errore nel form crea utente.", "danger")

    users = User.query.order_by(User.id.desc()).all()
    return render_template(
        "admin_users.html",
        active_page="",
        users=users,
        create_form=create_form,
        reset_form=reset_form,
    )

@app.post("/admin/users/<int:user_id>/delete")
@login_required
@admin_required
def admin_delete_user(user_id: int):
    if current_user.id == user_id:
        flash("Non puoi eliminare te stesso.", "danger")
        return redirect(url_for("admin_users"))

    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    flash("Utente eliminato.", "success")
    return redirect(url_for("admin_users"))

@app.post("/admin/users/<int:user_id>/reset-password")
@login_required
@admin_required
def admin_reset_password(user_id: int):
    form = AdminResetPasswordForm()
    if not form.validate_on_submit():
        flash("Password non valida.", "danger")
        return redirect(url_for("admin_users"))

    u = User.query.get_or_404(user_id)
    u.set_password(form.new_password.data)
    db.session.commit()

    flash("Password resettata.", "success")
    return redirect(url_for("admin_users"))

if __name__ == "__main__":
    app.run(debug=True)
