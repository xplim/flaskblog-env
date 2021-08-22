import os
import secrets
from PIL import Image

from application import app


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
