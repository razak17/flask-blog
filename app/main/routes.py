from flask import Flask, render_template, url_for, current_app
from flask_login import login_required
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
@login_required
def index():
    return render_template("main/index.html", posts=posts)


@bp.route("/about")
@login_required
def about():
    return render_template("main/about.html", title="About")


@bp.route("/account")
@login_required
def account():
    return render_template('main/account.html', title='Account')


