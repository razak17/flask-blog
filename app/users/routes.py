from flask import request, render_template, flash, redirect, url_for, current_app
from app.users.forms import UpdateAccountForm
from flask_login import login_required, current_user
from app.users.utils import save_picture
from app.models import User, Post
from config import Config
from app.users import bp
from app import db



@bp.route("/account", methods=["GET", "POST"])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
    
    return render_template('users/account.html', title='Account', image_file=image_file, form=form)


@bp.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page, current_app.config['POSTS_PER_PAGE'])
    return render_template('users/user_posts.html', posts=posts, user=user)