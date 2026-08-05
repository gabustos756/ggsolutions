"""
Modelos de Datos para GG Solutions (SQLAlchemy).
Persistencia de Usuarios Administradores, Leads de Contacto y Auditoría de Cambios.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    nombre = db.Column(db.String(100), nullable=False, default="Administrador")
    rol = db.Column(db.String(20), nullable=False, default="admin")  # "admin", "editor"
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User {self.email} ({self.rol})>"


class ContactLead(db.Model):
    __tablename__ = "contact_leads"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    telefono = db.Column(db.String(40), nullable=True)
    mensaje = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="NUEVO")  # NUEVO, LEIDO, RESPONDIDO, ARCHIVADO
    ip_origen = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono or "",
            "mensaje": self.mensaje,
            "estado": self.estado,
            "fecha_creacion_iso": self.fecha_creacion.isoformat() if self.fecha_creacion else "",
            "fecha_formateada": self.fecha_creacion.strftime("%d/%m/%Y %H:%M hs") if self.fecha_creacion else "",
        }

    def __repr__(self):
        return f"<ContactLead {self.id} - {self.email} ({self.estado})>"


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    accion = db.Column(db.String(50), nullable=False)
    detalle = db.Column(db.String(255), nullable=False)
    ip_origen = db.Column(db.String(50), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    usuario = db.relationship("User", backref="auditorias")

    def __repr__(self):
        return f"<AuditLog {self.accion}: {self.detalle}>"
