from flask import Flask, render_template, url_for, current_app
from app.main import bp


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@bp.route("/home")
@bp.route("/")
def index():
    return render_template("main/index.html", posts=posts)


@bp.route("/about")
def about():
    return render_template("main/about.html", title="About")



