from flask import Blueprint, render_template, request

from application.models import Post
from application.posts.utils import url_for_author_image

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        per_page=5, page=page
    )
    return render_template(
        "home.html",
        posts=posts,
        url_for_author_image=url_for_author_image,
    )


@main.route("/about")
def about():
    return render_template("about.html", title="About")
