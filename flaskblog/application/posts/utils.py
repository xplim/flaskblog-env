from flask import url_for


def url_for_author_image(post):
    return url_for("static", filename=f"profile_pics/{post.author.image_file}")
