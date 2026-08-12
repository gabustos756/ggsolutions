"""
Utilidades de Seguridad y Auditoría para GG Solutions.
Incluye protección CSRF, Rate Limiting básico por IP y Registro de Auditoría.
"""

from datetime import datetime, timedelta
import secrets
from flask import request, session, abort
from werkzeug.security import generate_password_hash
from models import db, User, ContactLead, AuditLog, DemoSolution, DemoViewLog

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


def asegurar_esquema_bd(app):
    """
    Inspecciona las tablas de la base de datos SQLite y agrega automáticamente
    las tablas y columnas faltantes definidas en los modelos SQLAlchemy (ALTER TABLE).
    Garantiza compatibilidad sin pérdida de datos en entornos donde la BD ya existía.
    """
    from sqlalchemy import inspect, text
    with app.app_context():
        # 1. Crear tablas que no existan aún
        db.create_all()

        try:
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()

            def get_sqlite_type(column):
                col_type = str(column.type).lower()
                if "int" in col_type:
                    return "INTEGER"
                elif "float" in col_type or "numeric" in col_type:
                    return "REAL"
                elif "bool" in col_type:
                    return "BOOLEAN"
                elif "datetime" in col_type or "date" in col_type:
                    return "DATETIME"
                elif "text" in col_type:
                    return "TEXT"
                else:
                    return "VARCHAR(250)"

            for model_class in [User, ContactLead, AuditLog, DemoSolution, DemoViewLog]:
                table_name = model_class.__tablename__
                if table_name in existing_tables:
                    existing_columns = {col["name"] for col in inspector.get_columns(table_name)}
                    for column in model_class.__table__.columns:
                        if column.name not in existing_columns:
                            sq_type = get_sqlite_type(column)
                            alter_stmt = text(f'ALTER TABLE "{table_name}" ADD COLUMN "{column.name}" {sq_type}')
                            db.session.execute(alter_stmt)
                            print(f"[DB MIGRATION] Agregada columna faltante '{column.name}' ({sq_type}) a la tabla '{table_name}'.")
                    db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"[WARN DB MIGRATION] Error al verificar/migrar esquema: {e}")


def seed_admin_user(app):
    """
    Crea o actualiza el usuario administrador inicial con la nueva contraseña.
    """
    import os
    with app.app_context():
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@ggsolutions.com.ar").lower().strip()
        admin_password = os.environ.get("ADMIN_PASSWORD", "abl0420-")
        
        user = User.query.filter_by(email=admin_email).first()
        if not user:
            user = User.query.filter((User.email == "contacto@ggsolutions.com.ar") | (User.email == "admin")).first()

        if not user:
            new_admin = User(
                email=admin_email,
                password_hash=generate_password_hash(admin_password, method="pbkdf2:sha256"),
                nombre="GG Superadmin",
                rol="superadmin",
                activo=True
            )
            db.session.add(new_admin)
            db.session.commit()
            print(f"[SECURITY] Usuario Superadministrador creado ({admin_email}).")
        else:
            user.email = admin_email
            user.password_hash = generate_password_hash(admin_password, method="pbkdf2:sha256")
            user.rol = "superadmin"
            user.activo = True
            db.session.commit()
            print(f"[SECURITY] Contraseña y rol de usuario administrador actualizada ({admin_email}).")


