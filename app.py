import os
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from models import db, User, ContactLead, AuditLog
from security_utils import (
    generate_csrf_token,
    validate_csrf_token,
    check_rate_limit,
    registrar_auditoria,
    seed_admin_user,
)

app = Flask(__name__)

# Configuración de Seguridad y Persistencia
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "ggsolutions-secret-key-cordoba-2026-secure")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///ggsolutions.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Sesiones seguras
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Inicializar BD y Login Manager
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin_login"
login_manager.login_message = "Debes iniciar sesión para acceder al panel."


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Inicialización de tablas y seed de administrador
with app.app_context():
    db.create_all()
    seed_admin_user(app)


# Context Processor para inyectar token CSRF en Jinja2
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf_token())


# ==============================================================================
# RUTA PÚBLICA (LANDING PAGE)
# ==============================================================================
@app.route("/")
def home():
    context = {
        "company_name": "GG Solutions",
        "tagline": "Estudio de Software & Consultoría Técnica",
        "description": "Diseñamos y desarrollamos software a medida para empresas que buscan claridad, arquitectura sólida y precisión técnica.",
        "badge_text": "Estudio & Consultoría de Software",
        
        "hero_title": "Software pensado para resolver problemas reales.",
        "hero_subtitle": "Nos sentemos a tomar un café, te escucho, vemos qué necesitás y encontramos la solución. Sin sobreingeniería, sin ruido y con arquitectura de alto rendimiento.",
        
        "manifesto_title": "Tu negocio no necesita más ruido. Necesita una solución bien pensada.",
        "manifesto_text": "El software de calidad nace de la claridad conceptual y la escucha atenta. En GG Solutions eliminamos las capas innecesarias de gestión y las tecnologías de moda no justificadas.\n\nTrabajamos de forma directa para transformar requerimientos complejos en aplicaciones web limpias, seguras y escalables.",
        
        "services": [
            {
                "num": "01",
                "title": "Desarrollo Web a Medida",
                "desc": "Construcción de aplicaciones y plataformas web desde cero, optimizadas para velocidad, seguridad y mantenibilidad a largo plazo."
            },
            {
                "num": "02",
                "title": "Sistemas Internos & Dashboards",
                "desc": "Diseño de paneles de control y software de gestión interna adaptados a la dinámica y los flujos de trabajo específicos de tu empresa."
            },
            {
                "num": "03",
                "title": "Automatización & Arquitectura API",
                "desc": "Conexión de sistemas, integración de servicios de terceros y automatización de procesos para maximizar la eficiencia operacional."
            },
            {
                "num": "04",
                "title": "Consultoría Técnica & MVPs",
                "desc": "Diagnóstico de arquitectura, evaluación de código y desarrollo rápido de productos mínimos viables orientados al mercado."
            }
        ],
        
        "differentials": [
            {
                "title": "Trato Directo con Ingenieros",
                "desc": "Diálogo fluido sin intermediarios comerciales. Hablás directamente con quienes diseñan y construyen la arquitectura de tu software."
            },
            {
                "title": "Foco en la Mantenibilidad",
                "desc": "Escribimos código estructurado y legible. Elegimos la tecnología por su solidez y costo de mantenimiento, no por tendencias pasajeras."
            },
            {
                "title": "Transparencia & Iteración",
                "desc": "Visibilidad total del avance del proyecto con entregas semanales y canales de comunicación abiertos en todo momento."
            },
            {
                "title": "Criterio de Negocio",
                "desc": "Cada decisión técnica está alineada con tus objetivos comerciales, priorizando el impacto real sobre el volumen de código."
            }
        ],
        
        "built_cases": [
            {
                "id": "ecommerce",
                "title": "E-Commerce & Plataforma Comercial",
                "subtitle": "Conversión y producto",
                "desc": "Arquitectura comercial orientada a catálogo dinámico, velocidad instantánea de respuesta y experiencia fluida diseñada para maximizar la conversión.",
                "video": "content/ecommerce.mov",
                "badge": "Conversión & Producto",
                "focus": "Capacidad Técnica: Conversión"
            },
            {
                "id": "telemetria",
                "title": "Telemetría & Monitoreo en Tiempo Real",
                "subtitle": "Datos en tiempo real y visualización",
                "desc": "Paneles de monitoreo continuo con procesamiento en vivo de métricas críticas, diagnóstico operativo y visualización clara para entornos de alta demanda.",
                "video": "content/telemetria.mov",
                "badge": "Datos en Tiempo Real & Visualización",
                "focus": "Capacidad Técnica: Visualización"
            },
            {
                "id": "agente_decisiones",
                "title": "Agente de Decisiones & Automatización",
                "subtitle": "Automatización y estrategia",
                "desc": "Sistemas de lógica algorítmica y motores de reglas para la automatización de procesos clave, recomendación táctica y soporte operacional en tiempo real.",
                "video": "content/agente_decisiones.mov",
                "badge": "Automatización & Estrategia",
                "focus": "Capacidad Técnica: Automatización"
            }
        ]
    }
    return render_template("index.html", **context)


# ==============================================================================
# ENDPOINT PÚBLICO DE RECEPCIÓN DE MENSAJES (RECEPCIÓN Y PERSISTENCIA)
# ==============================================================================
@app.route("/api/contacto", methods=["POST"])
def api_contacto():
    # Rate Limiting: Máximo 5 peticiones por minuto por IP
    if not check_rate_limit("contact_api", limit=5, window_seconds=60):
        return jsonify({
            "status": "error",
            "message": "Demasiadas peticiones. Por favor aguardá un minuto antes de volver a enviar."
        }), 429

    try:
        data = request.get_json(force=True, silent=True) or request.form.to_dict()
        
        nombre = (data.get("nombre") or "").strip()
        email = (data.get("email") or "").strip().lower()
        telefono = (data.get("telefono") or "").strip()
        mensaje = (data.get("mensaje") or "").strip()

        # Validaciones de servidor estrictas
        if not nombre or len(nombre) < 2:
            return jsonify({"status": "error", "message": "Por favor ingresá un nombre válido."}), 400

        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not email or not re.match(email_regex, email):
            return jsonify({"status": "error", "message": "Por favor ingresá un correo electrónico válido."}), 400

        if not telefono or len(telefono) < 6:
            return jsonify({"status": "error", "message": "Por favor ingresá un número de teléfono con característica válido."}), 400

        if not mensaje or len(mensaje) < 5:
            return jsonify({"status": "error", "message": "El mensaje debe tener al menos 5 caracteres."}), 400

        # Persistir en la base de datos
        lead = ContactLead(
            nombre=nombre,
            email=email,
            telefono=telefono,
            mensaje=mensaje,
            estado="NUEVO",
            ip_origen=request.remote_addr or "127.0.0.1",
            user_agent=request.headers.get("User-Agent", "")[:250],
            fecha_creacion=datetime.utcnow()
        )
        db.session.add(lead)
        db.session.commit()

        # Registrar auditoría de nuevo lead
        registrar_auditoria("NUEVO_LEAD", f"Nuevo mensaje recibido de {email} ({nombre})")

        return jsonify({
            "status": "ok",
            "message": "¡Gracias por tu mensaje! Nos pondremos en contacto a la brevedad."
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR CONTACTO API] {e}")
        return jsonify({"status": "error", "message": "Error interno del servidor. Por favor reintenta."}), 500


# ==============================================================================
# RUTAS PRIVADAS DEL PANEL DE ADMINISTRACIÓN (/admin)
# ==============================================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for("admin_dashboard"))

    error = None

    if request.method == "POST":
        # Rate Limiting: Máximo 5 intentos por minuto
        if not check_rate_limit("login_admin", limit=5, window_seconds=60):
            error = "Demasiados intentos fallidos. Por favor aguardá un minuto."
            return render_template("admin/login.html", error=error), 429

        # Validar token CSRF
        token = request.form.get("csrf_token")
        if not validate_csrf_token(token):
            error = "Sesión o token CSRF inválido. Por favor recargá e intentalo de nuevo."
            return render_template("admin/login.html", error=error), 400

        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        user = User.query.filter_by(email=email, activo=True).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=False)
            registrar_auditoria("LOGIN_EXITOSO", f"Inicio de sesión exitoso para {email}", user_id=user.id)
            return redirect(url_for("admin_dashboard"))
        else:
            registrar_auditoria("LOGIN_FALLIDO", f"Intento de inicio de sesión fallido para {email}")
            error = "Credenciales incorrectas o usuario inactivo."

    return render_template("admin/login.html", error=error)


@app.route("/admin")
@login_required
def admin_dashboard():
    estado_filtro = request.args.get("estado", "").upper().strip()

    query = ContactLead.query

    if estado_filtro in ["NUEVO", "LEIDO", "RESPONDIDO", "ARCHIVADO"]:
        query = query.filter_by(estado=estado_filtro)

    leads = query.order_by(ContactLead.fecha_creacion.desc()).all()

    # Métricas consolidadas
    total_leads = ContactLead.query.count()
    nuevos_leads = ContactLead.query.filter_by(estado="NUEVO").count()
    respondidos_leads = ContactLead.query.filter_by(estado="RESPONDIDO").count()
    archivados_leads = ContactLead.query.filter_by(estado="ARCHIVADO").count()

    # Auditorías recientes (últimas 10)
    audit_logs = AuditLog.query.order_by(AuditLog.fecha.desc()).limit(10).all()

    return render_template(
        "admin/dashboard.html",
        leads=leads,
        total_leads=total_leads,
        nuevos_leads=nuevos_leads,
        respondidos_leads=respondidos_leads,
        archivados_leads=archivados_leads,
        estado_filtro=estado_filtro,
        audit_logs=audit_logs,
    )


@app.route("/admin/leads/<int:lead_id>/estado", methods=["POST"])
@login_required
def admin_cambiar_estado_lead(lead_id):
    token = request.form.get("csrf_token")
    if not validate_csrf_token(token):
        abort(400, description="Token CSRF inválido.")

    nuevo_estado = (request.form.get("nuevo_estado") or "").upper().strip()
    if nuevo_estado not in ["NUEVO", "LEIDO", "RESPONDIDO", "ARCHIVADO"]:
        abort(400, description="Estado no válido.")

    lead = ContactLead.query.get_or_404(lead_id)
    estado_anterior = lead.estado
    lead.estado = nuevo_estado
    db.session.commit()

    registrar_auditoria(
        "CAMBIO_ESTADO",
        f"Lead ID {lead_id} ({lead.email}): {estado_anterior} -> {nuevo_estado}",
        user_id=current_user.id
    )

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/leads/<int:lead_id>/eliminar", methods=["POST"])
@login_required
def admin_eliminar_lead(lead_id):
    token = request.form.get("csrf_token")
    if not validate_csrf_token(token):
        abort(400, description="Token CSRF inválido.")

    lead = ContactLead.query.get_or_404(lead_id)
    email_lead = lead.email
    db.session.delete(lead)
    db.session.commit()

    registrar_auditoria(
        "ELIMINACION_LEAD",
        f"Lead ID {lead_id} de {email_lead} fue eliminado por {current_user.email}",
        user_id=current_user.id
    )

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/logout")
@login_required
def admin_logout():
    registrar_auditoria("LOGOUT", f"Cierre de sesión de {current_user.email}", user_id=current_user.id)
    logout_user()
    return redirect(url_for("admin_login"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=True)
