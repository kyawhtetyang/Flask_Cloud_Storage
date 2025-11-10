from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, File
from ..extensions import db
from . import admin_bp

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role!="admin":
            flash("Admin access required","danger")
            return redirect(url_for("storage.index"))
        return func(*args, **kwargs)
    return wrapper

@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    files = File.query.all()
    return render_template("admin_dashboard.html", users=users, files=files)


