import os, uuid
from flask import current_app, render_template, request, redirect, url_for, send_from_directory, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from ..extensions import db
from ..models import File
from . import storage_bp

def get_user():
    return getattr(current_user, "username", "guest")

@storage_bp.route("/")
@login_required
def index():
    files = File.query.order_by(File.uploaded_at.desc()).all()
    return render_template("index.html", files=files, username=get_user())

@storage_bp.route("/upload", methods=["POST"])
@login_required
def upload():
    files = request.files.getlist("file")
    username = get_user()
    category = request.form.get("category","general")
    tags = request.form.get("tags","")
    description = request.form.get("description","")
    for file in files:
        if not file or file.filename=="": continue
        filename = secure_filename(file.filename)
        user_folder = os.path.join(current_app.config['STORAGE_FOLDER'], username)
        os.makedirs(user_folder,exist_ok=True)
        filepath = os.path.join(user_folder, filename)
        if os.path.exists(filepath):
            base,ext = os.path.splitext(filename)
            filename = f"{base}_{uuid.uuid4().hex[:6]}{ext}"
            filepath = os.path.join(user_folder, filename)
        file.save(filepath)
        size = os.path.getsize(filepath)
        new_file = File(filename=filename, filepath=filepath, username=username, size=size, category=category, tags=tags, description=description)
        db.session.add(new_file)
        db.session.commit()
    flash("File(s) uploaded","success")
    return redirect(url_for("storage.index"))

@storage_bp.route("/download/<int:file_id>")
@login_required
def download(file_id):
    f = File.query.get_or_404(file_id)
    return send_from_directory(os.path.dirname(f.filepath), f.filename, as_attachment=True)

@storage_bp.route("/share/<int:file_id>")
@login_required
def share(file_id):
    f = File.query.get_or_404(file_id)
    f.generate_share()
    db.session.commit()
    flash("Share link generated","info")
    return redirect(url_for("storage.index"))

@storage_bp.route("/shared/<token>")
def shared(token):
    f = File.query.filter_by(shared_token=token).first_or_404()
    return send_from_directory(os.path.dirname(f.filepath), f.filename, as_attachment=True)

@storage_bp.route("/delete/<int:file_id>",methods=["POST"])
@login_required
def delete(file_id):
    f = File.query.get_or_404(file_id)
    try: os.remove(f.filepath)
    except Exception: pass
    db.session.delete(f)
    db.session.commit()
    flash("File deleted","danger")
    return redirect(url_for("storage.index"))

@storage_bp.route("/search")
@login_required
def search():
    q = request.args.get("q","").lower()
    files = File.query.filter(File.filename.ilike(f"%{q}%") | File.tags.ilike(f"%{q}%") | File.description.ilike(f"%{q}%")).order_by(File.uploaded_at.desc()).all()
    return render_template("index.html", files=files, username=get_user())


