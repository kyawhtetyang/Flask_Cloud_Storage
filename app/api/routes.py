from flask import jsonify
from ..models import File
from . import api_bp

@api_bp.route("/files")
def list_files():
    files = File.query.all()
    return jsonify([{
        "id": f.id,
        "filename": f.filename,
        "username": f.username,
        "category": f.category,
        "tags": f.tags,
        "description": f.description,
        "size": f.size,
        "version": f.version,
        "uploaded_at": f.uploaded_at.isoformat()
    } for f in files])


