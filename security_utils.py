"""
Utilidades de Seguridad y Auditoría para GG Solutions.
Incluye protección CSRF, Rate Limiting básico por IP y Registro de Auditoría.
"""

from datetime import datetime, timedelta
import secrets
from flask import request, session, abort
from werkzeug.security import generate_password_hash
from models import db, User, AuditLog

# Almacenamiento en memoria para Rate Limiting (IP -> list of timestamps)
_rate_limit_store = {}


def generate_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]


def validate_csrf_token(token):
    session_token = session.get("csrf_token")
    if not session_token or not token or not secrets.compare_digest(session_token, token):
        return False
    return True


def check_rate_limit(key_prefix: str, limit: int = 5, window_seconds: int = 60) -> bool:
    """
    Verifica si la IP actual ha superado el límite de peticiones en la ventana de tiempo.
    Retorna True si la petición es permitida, False si superó el límite.
    """
    ip = request.remote_addr or "127.0.0.1"
    key = f"{key_prefix}:{ip}"
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=window_seconds)

    timestamps = _rate_limit_store.get(key, [])
    # Filtrar timestamps dentro de la ventana
    timestamps = [ts for ts in timestamps if ts > cutoff]

    if len(timestamps) >= limit:
        _rate_limit_store[key] = timestamps
        return False

    timestamps.append(now)
    _rate_limit_store[key] = timestamps
    return True


def registrar_auditoria(accion: str, detalle: str, user_id: int = None):
    """
    Registra un evento de auditoría en la base de datos.
    """
    try:
        ip = request.remote_addr or "127.0.0.1"
        log = AuditLog(
            user_id=user_id,
            accion=accion,
            detalle=detalle,
            ip_origen=ip,
            fecha=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR AUDITORIA] {e}")


def seed_admin_user(app):
    """
    Crea el usuario administrador inicial leyendo variables de entorno.
    """
    import os
    with app.app_context():
        admin_email = os.environ.get("ADMIN_EMAIL", "contacto@ggsolutions.com.ar").lower().strip()
        admin_password = os.environ.get("ADMIN_PASSWORD", "ggsolutions2026")
        
        user = User.query.filter_by(email=admin_email).first()
        if not user:
            new_admin = User(
                email=admin_email,
                password_hash=generate_password_hash(admin_password, method="pbkdf2:sha256"),
                nombre="GG Admin",
                rol="admin",
                activo=True
            )
            db.session.add(new_admin)
            db.session.commit()
            print(f"[SECURITY] Usuario Administrador inicial creado ({admin_email}).")
