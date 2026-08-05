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


class DemoSolution(db.Model):
    __tablename__ = "demo_solutions"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    nombre_negocio = db.Column(db.String(150), nullable=False)
    rubro = db.Column(db.String(50), nullable=False, default="general")
    enfoque = db.Column(db.String(100), nullable=False, default="conversion")
    dolor_principal = db.Column(db.Text, nullable=True)
    objetivo = db.Column(db.String(150), nullable=True)
    modulo_solucion = db.Column(db.String(50), nullable=False, default="agenda")
    tipo_software = db.Column(db.String(30), nullable=False, default="ambas")  # "exposicion", "gestion", "ambas"

    # Datos de Google Maps / Negocio

    google_place_id = db.Column(db.String(100), nullable=True)
    direccion = db.Column(db.String(250), nullable=True)
    ciudad = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    whatsapp = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.Float, nullable=True, default=4.8)
    reviews_count = db.Column(db.Integer, nullable=True, default=15)
    reviews_json = db.Column(db.Text, nullable=True)
    fotos_json = db.Column(db.Text, nullable=True)
    sitio_web_original = db.Column(db.String(250), nullable=True)

    # Métricas y relación
    vistas_count = db.Column(db.Integer, nullable=False, default=0)
    ultima_vista = db.Column(db.DateTime, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    creado_por_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("contact_leads.id"), nullable=True)

    creador = db.relationship("User", backref="demos_creadas")
    lead = db.relationship("ContactLead", backref="demos_asociadas")

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "nombre_negocio": self.nombre_negocio,
            "rubro": self.rubro,
            "enfoque": self.enfoque,
            "dolor_principal": self.dolor_principal or "",
            "objetivo": self.objetivo or "",
            "modulo_solucion": self.modulo_solucion,
            "tipo_software": self.tipo_software or "ambas",

            "direccion": self.direccion or "",
            "ciudad": self.ciudad or "",
            "telefono": self.telefono or "",
            "whatsapp": self.whatsapp or "",
            "rating": self.rating or 4.8,
            "reviews_count": self.reviews_count or 0,
            "vistas_count": self.vistas_count,
            "ultima_vista_iso": self.ultima_vista.isoformat() if self.ultima_vista else None,
            "fecha_creacion_iso": self.fecha_creacion.isoformat() if self.fecha_creacion else "",
            "fecha_formateada": self.fecha_creacion.strftime("%d/%m/%Y %H:%M hs") if self.fecha_creacion else "",
        }

    def __repr__(self):
        return f"<DemoSolution {self.slug} ({self.nombre_negocio})>"


class DemoViewLog(db.Model):
    __tablename__ = "demo_view_logs"

    id = db.Column(db.Integer, primary_key=True)
    demo_id = db.Column(db.Integer, db.ForeignKey("demo_solutions.id"), nullable=False, index=True)
    ip_origen = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    fecha_vista = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    demo = db.relationship("DemoSolution", backref=db.backref("logs_vistas", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<DemoViewLog Demo {self.demo_id} at {self.fecha_vista}>"

