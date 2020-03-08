from flask import Flask, request, render_template, flash, redirect, url_for, current_app, abort
from app.main.forms import UpdateAccountForm, PostForm
from flask_login import login_required, current_user
from app.main.save_picture import save_picture
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
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
    
    return render_template('main/account.html', title='Account', image_file=image_file, form=form)


@bp.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("You post has been created successfully", "success")
        return redirect(url_for("main.index"))

    return render_template("main/create_post.html", title="New Post", form=form, legend="New Post")


@bp.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('main/post.html', title=post.title, post=post)


@bp.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('main/create_post.html', title='Update Post', form=form, legend='Update Post')


@bp.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))


@bp.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page, current_app.config['POSTS_PER_PAGE'])
    return render_template('main/user_posts.html', posts=posts, user=user)