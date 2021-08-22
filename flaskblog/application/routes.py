import os
import secrets
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image

from application import app, bcrypt, db
from application.forms import LoginForm, RegistrationForm, UpdateAccountForm
from application.models import User


posts = [
    {
        "author": "Corey Schafer",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "April 20, 2018",
    },
    {
        "author": "Jane Doe",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "April 21, 2018",
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(
            "Your account has been created! You can log in now.",
            "success",
        )
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (
            user
            and bcrypt.check_password_hash(user.password, form.password.data)
        ):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page) if next_page
                else redirect(url_for("home"))
            )
        else:
            flash(
                "Login unsuccessful. Please check email and password.",
                "danger",
            )
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def save_image(form_image):
    _, f_ext = os.path.splitext(form_image.filename)
    image_file = f"{secrets.token_hex(8)}{f_ext}"
    image_path = os.path.join(
        app.root_path, "static/profile_pics", image_file
    )
    image_resized = Image.open(form_image)
    image_resized.thumbnail((125, 125))
    image_resized.save(image_path)
    return image_file


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_image(form.image.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        "static", filename=f"profile_pics/{current_user.image_file}"
    )
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )
