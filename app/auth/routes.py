from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from ..extensions import db
from . import auth_bp

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u = request.form.get("username","").strip()
        p = request.form.get("password","")
        user = User.query.filter_by(username=u).first()
        if user and user.check_password(p):
            login_user(user)
            flash("Logged in successfully","success")
            return redirect(url_for("storage.index"))
        flash("Invalid credentials","danger")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        u = request.form.get("username","").strip()
        p = request.form.get("password","")
        e = request.form.get("email","").strip()
        if User.query.filter_by(username=u).first():
            flash("Username exists","warning")
            return redirect(url_for("auth.register"))
        new_user = User(username=u, email=e)
        new_user.set_password(p)
        db.session.add(new_user)
        db.session.commit()
        flash("User registered","success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out","info")
    return redirect(url_for("storage.index"))

@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


