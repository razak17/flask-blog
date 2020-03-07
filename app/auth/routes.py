from flask import Flask, render_template, flash, redirect, url_for, current_app
from app.auth import bp
from app.auth.forms import RegistrationForm, LoginForm


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "1234":
            flash("Login successful", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Login unsuccessful. Incorrect email or password!", "danger")

    return render_template("auth/login.html", title="Login", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Accounted created for {form.username.data}!", "success")
        return redirect(url_for('main.index'))
    
    return render_template("auth/register.html", title="Register", form=form)