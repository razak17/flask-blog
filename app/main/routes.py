from flask import request, render_template, current_app
from flask_login import login_required
from app.models import User, Post
from config import Config
from app.main import bp
from app import db



@bp.route("/home")
@bp.route("/")
@login_required
def index():
    posts = Post.query.all()
    page =request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'])
    return render_template("main/index.html", posts=posts)


@bp.route("/about")
def about():
    return render_template("main/about.html", title="About")


