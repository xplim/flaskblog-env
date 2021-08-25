import os
import secrets
from flask import url_for
from flask_mail import Message
from PIL import Image

from application import app, mail


def get_image_path(image_file):
    return os.path.join(app.root_path, "static/profile_pics", image_file)


def remove_image(image_file):
    os.remove(get_image_path(image_file))


def save_image(form_image):
    _, f_ext = os.path.splitext(form_image.filename)
    image_file = f"{secrets.token_hex(8)}{f_ext}"
    image_resized = Image.open(form_image)
    image_resized.thumbnail((125, 125))
    image_resized.save(get_image_path(image_file))
    return image_file


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request",
        sender="noreply@flaskblog.com",
        recipients=[user.email],
    )
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email and no changes will be made.
"""
    mail.send(msg)


def url_for_author_image(post):
    return url_for("static", filename=f"profile_pics/{post.author.image_file}")
