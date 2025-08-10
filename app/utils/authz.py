from functools import wraps
from flask import session, redirect, url_for
from app.models import db
from app.models.admin import Admin

def is_admin(uid: str) -> bool:
    if not uid:
        return False
    return db.session.get(Admin, uid) is not None

def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        uid = session.get("uid")
        if not uid or not is_admin(uid):
            return redirect(url_for("home"))
        return view(*args, **kwargs)
    return wrapper
