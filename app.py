import os
import re
import json
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from models import db, User, ContactLead, AuditLog, DemoSolution, DemoViewLog
from security_utils import (
    generate_csrf_token,
    validate_csrf_token,
    check_rate_limit,
    registrar_auditoria,
    seed_admin_user,
    asegurar_esquema_bd,
)
from services.google_places import (
    obtener_datos_lugar_google,
    extrae_ciudad_de_direccion,
    validar_y_formatear_whatsapp,
    obtener_api_keys,
)
from services.demo_engine import preparar_contexto_demo


app = Flask(__name__)

# Configuración de Seguridad y Persistencia
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "ggsolutions-secret-key-cordoba-2026-secure")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///ggsolutions.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuración de carpeta para uploads (logos)
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads", "logos")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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
    return db.session.get(User, int(user_id))



# Inicialización de tablas, migración automática de columnas y seed de administrador
with app.app_context():
    asegurar_esquema_bd(app)
    seed_admin_user(app)


# Context Processor para inyectar token CSRF en Jinja2
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf_token())


def solo_superadmin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("admin_login"))
        rol_usuario = (getattr(current_user, "rol", "") or "").strip().lower()
        if rol_usuario not in ["superadmin", "admin"]:
            return redirect(url_for("admin_demos_list", error="Acceso restringido: Se requieren permisos de Superadministrador."))
        return f(*args, **kwargs)
    return decorated_function


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

        search_email = "admin@ggsolutions.com.ar" if email == "admin" else email
        user = User.query.filter_by(email=search_email, activo=True).first()


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


def generar_slug(nombre: str) -> str:
    s = (nombre or "demo").lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s).strip("-")
    token = uuid.uuid4().hex[:6]
    return f"{s}-{token}"


# ==============================================================================
# RUTAS DE GESTIÓN Y CREACIÓN DE DEMOS (/admin/demos)
# ==============================================================================

@app.route("/admin/demos", methods=["GET"])
@login_required
def admin_demos_list():
    try:
        demos = DemoSolution.query.order_by(DemoSolution.fecha_creacion.desc()).all()
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR ADMIN DEMOS QUERY] {e}")
        try:
            asegurar_esquema_bd(app)
            demos = DemoSolution.query.order_by(DemoSolution.fecha_creacion.desc()).all()
        except Exception as err:
            print(f"[ERROR ADMIN DEMOS RECOVERY FAILED] {err}")
            demos = []

    error = request.args.get("error")
    mensaje = request.args.get("mensaje")
    keys = obtener_api_keys()
    google_maps_api_key = keys[0] if (keys and len(keys) > 0) else os.environ.get("GOOGLE_MAPS_API_KEY", "")
    return render_template(
        "admin/demos.html",
        demos=demos,
        error=error,
        mensaje=mensaje,
        google_maps_api_key=google_maps_api_key,
        google_maps_api_keys=keys
    )


@app.route("/admin/demos/nueva", methods=["POST"])
@login_required
def admin_crear_demo():
    token = request.form.get("csrf_token")
    if not validate_csrf_token(token):
        return redirect(url_for("admin_demos_list", error="Token CSRF inválido. Reintentá."))

    maps_input = (request.form.get("google_maps_input") or "").strip()
    rubro = (request.form.get("rubro") or "general").strip().lower()
    rubro_secundario_raw = (request.form.get("rubro_secundario") or "").strip().lower()
    rubro_secundario = rubro_secundario_raw if (rubro_secundario_raw and rubro_secundario_raw != "ninguno" and rubro_secundario_raw != rubro) else None
    enfoque = (request.form.get("enfoque") or "Conversión High-Ticket").strip()

    # Procesar múltiples módulos seleccionados
    modulos_seleccionados = request.form.getlist("modulos_solucion")
    rubro_ingresado = (request.form.get("rubro") or "").strip().lower()
    if not modulos_seleccionados:
        modulos_seleccionados = [ (request.form.get("modulo_solucion") or ("hostel" if rubro_ingresado in ["hostel", "hoteleria", "turismo"] else "agenda")).strip().lower() ]

    # Si es rubro hostel/hoteleria y hostel está en los seleccionados, garantizar que hostel sea el módulo principal
    if (rubro_ingresado in ["hostel", "hoteleria", "turismo"] or "hostel" in rubro_ingresado) and "hostel" in modulos_seleccionados:
        modulos_seleccionados.remove("hostel")
        modulos_seleccionados.insert(0, "hostel")

    modulo_solucion_principal = modulos_seleccionados[0]
    modulos_json = json.dumps(modulos_seleccionados, ensure_ascii=False)

    tipo_software = (request.form.get("tipo_software") or "ambas").strip().lower()
    dolor_principal = (request.form.get("dolor_principal") or "").strip()
    objetivo = (request.form.get("objetivo") or "").strip()

    # Personalización de marca, colores y plantilla de diseño
    color_primario = (request.form.get("color_primario") or "").strip()
    color_header = (request.form.get("color_header") or "").strip()
    logo_url = (request.form.get("logo_url") or "").strip()
    diseno_template = (request.form.get("diseno_template") or "classic").strip().lower()
    mostrar_novedades = True if request.form.get("mostrar_novedades") in ["1", "true", "on"] else False

    # Manejar subida de archivo de logo si se adjuntó
    if "logo_file" in request.files:
        file = request.files["logo_file"]
        if file and file.filename != "":
            ext = os.path.splitext(file.filename)[1].lower()
            if ext in [".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif"]:
                filename = f"{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                logo_url = f"/static/uploads/logos/{filename}"

    # Campos de override desde Autocomplete / Map JS
    nombre_override = (request.form.get("nombre_negocio_override") or "").strip()
    place_id_override = (request.form.get("google_place_id") or "").strip()
    direccion_override = (request.form.get("direccion_override") or "").strip()
    ciudad_override = (request.form.get("ciudad_override") or "").strip()
    telefono_override = (request.form.get("telefono_override") or "").strip()
    whatsapp_override = (request.form.get("whatsapp_override") or "").strip()
    rating_override = request.form.get("rating_override")
    reviews_count_override = request.form.get("reviews_count_override")

    if not maps_input and not nombre_override:
        return redirect(url_for("admin_demos_list", error="Por favor buscá y seleccioná un comercio en el mapa o ingresá su nombre."))

    # Consultar API de Google Places si hay Place ID o búsqueda
    query_target = place_id_override if (place_id_override and place_id_override.startswith("ChIJ")) else (maps_input or nombre_override)
    datos_lugar = obtener_datos_lugar_google(query_target)

    # Sobrescribir con las ediciones personalizadas del usuario si existen
    if nombre_override:
        datos_lugar["nombre_negocio"] = nombre_override

    if direccion_override:
        datos_lugar["direccion"] = direccion_override
        datos_lugar["ciudad"] = extrae_ciudad_de_direccion(direccion_override)

    if whatsapp_override:
        phone_meta = validar_y_formatear_whatsapp(whatsapp_override)
        datos_lugar["whatsapp"] = phone_meta["whatsapp_digits"]
        if telefono_override:
            datos_lugar["telefono"] = telefono_override
        else:
            datos_lugar["telefono"] = phone_meta["telefono_display"]

    if rating_override:
        try:
            datos_lugar["rating"] = float(rating_override)
        except ValueError:
            pass

    if reviews_count_override:
        try:
            datos_lugar["reviews_count"] = int(reviews_count_override)
        except ValueError:
            pass

    nombre_negocio = datos_lugar.get("nombre_negocio") or "Comercio Prospectado"
    slug = generar_slug(nombre_negocio)

    try:
        demo = DemoSolution(
            slug=slug,
            nombre_negocio=nombre_negocio,
            rubro=rubro,
            rubro_secundario=rubro_secundario,
            enfoque=enfoque,
            dolor_principal=dolor_principal,
            objetivo=objetivo,
            modulo_solucion=modulo_solucion_principal,
            tipo_software=tipo_software,
            logo_url=logo_url,
            color_primario=color_primario,
            color_header=color_header,
            modulos_json=modulos_json,
            diseno_template=diseno_template,
            mostrar_novedades=mostrar_novedades,
            google_place_id=datos_lugar.get("google_place_id"),

            direccion=datos_lugar.get("direccion"),
            ciudad=datos_lugar.get("ciudad"),
            telefono=datos_lugar.get("telefono"),
            whatsapp=datos_lugar.get("whatsapp"),
            rating=datos_lugar.get("rating", 4.9),
            reviews_count=datos_lugar.get("reviews_count", 24),
            reviews_json=json.dumps(datos_lugar.get("reviews", []), ensure_ascii=False),
            fotos_json=json.dumps(datos_lugar.get("fotos", []), ensure_ascii=False),
            sitio_web_original=datos_lugar.get("sitio_web_original", ""),
            creado_por_id=current_user.id
        )
        db.session.add(demo)
        db.session.commit()

        registrar_auditoria("CREACION_DEMO", f"Demo creada para {nombre_negocio} (slug: {slug})", user_id=current_user.id)

        return redirect(url_for("admin_demos_list", mensaje=f"¡Demo creada exitosamente para '{nombre_negocio}'! Link: /demo/{slug}"))


    except Exception as e:
        db.session.rollback()
        print(f"[ERROR CREAR DEMO] {e}")
        return redirect(url_for("admin_demos_list", error="Ocurrió un error interno al guardar la demo."))


@app.route("/admin/demos/<int:demo_id>/eliminar", methods=["POST"])
@login_required
def admin_eliminar_demo(demo_id):
    token = request.form.get("csrf_token")
    if not validate_csrf_token(token):
        abort(400, description="Token CSRF inválido.")

    demo = DemoSolution.query.get_or_404(demo_id)
    nombre = demo.nombre_negocio
    db.session.delete(demo)
    db.session.commit()

    registrar_auditoria("ELIMINACION_DEMO", f"Demo ID {demo_id} ({nombre}) eliminada", user_id=current_user.id)
    return redirect(url_for("admin_demos_list", mensaje=f"La demo de '{nombre}' fue eliminada."))


# ==============================================================================
# RUTAS DE ADMINISTRACIÓN Y ABM DE USUARIOS
# ==============================================================================

@app.route("/admin/usuarios")
@login_required
@solo_superadmin
def admin_usuarios_list():
    usuarios = User.query.order_by(User.fecha_creacion.desc()).all()
    cant_superadmins = sum(1 for u in usuarios if u.rol in ["superadmin", "admin"])
    cant_comerciales = sum(1 for u in usuarios if u.rol == "comercial")
    cant_activos = sum(1 for u in usuarios if u.activo)
    
    mensaje = request.args.get("mensaje")
    error = request.args.get("error")
    
    return render_template(
        "admin/usuarios.html",
        usuarios=usuarios,
        cant_superadmins=cant_superadmins,
        cant_comerciales=cant_comerciales,
        cant_activos=cant_activos,
        mensaje=mensaje,
        error=error,
    )


@app.route("/admin/usuarios/nuevo", methods=["POST"])
@login_required
@solo_superadmin
def admin_crear_usuario():
    token = request.form.get("csrf_token")
    if not validate_csrf_token(token):
        return redirect(url_for("admin_usuarios_list", error="Token CSRF inválido. Reintentá."))

    nombre = (request.form.get("nombre") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    rol = (request.form.get("rol") or "comercial").strip().lower()
    activo = bool(request.form.get("activo"))

    if not nombre or not email or not password:
        return redirect(url_for("admin_usuarios_list", error="Todos los campos marcados con (*) son obligatorios."))

    if User.query.filter_by(email=email).first():
        return redirect(url_for("admin_usuarios_list", error=f"El correo '{email}' ya se encuentra registrado."))

    try:
        nuevo_user = User(
            nombre=nombre,
            email=email,
            password_hash=generate_password_hash(password, method="pbkdf2:sha256"),
            rol=rol,
            activo=activo,
        )
        db.session.add(nuevo_user)
        db.session.commit()

        registrar_auditoria("CREACION_USUARIO", f"Creado usuario {email} con rol {rol}", user_id=current_user.id)
        return redirect(url_for("admin_usuarios_list", mensaje=f"¡Usuario '{nombre}' ({email}) creado exitosamente!"))

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR CREAR USUARIO] {e}")
        return redirect(url_for("admin_usuarios_list", error="Ocurrió un error al intentar crear el usuario."))


@app.route("/admin/usuarios/<int:user_id>/editar", methods=["POST"])
@login_required
@solo_superadmin
def admin_editar_usuario(user_id):
    token = request.form.get("csrf_token")
    if not validate_csrf_token(token):
        return redirect(url_for("admin_usuarios_list", error="Token CSRF inválido. Reintentá."))

    user = User.query.get_or_404(user_id)

    nombre = (request.form.get("nombre") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    rol = (request.form.get("rol") or "comercial").strip().lower()
    activo = bool(request.form.get("activo"))

    if not nombre or not email:
        return redirect(url_for("admin_usuarios_list", error="Nombre y Correo son obligatorios."))

    existente = User.query.filter_by(email=email).first()
    if existente and existente.id != user.id:
        return redirect(url_for("admin_usuarios_list", error=f"El correo '{email}' ya pertenece a otro usuario."))

    try:
        user.nombre = nombre
        user.email = email
        user.rol = rol
        
        if user.id == current_user.id:
            user.activo = True
        else:
            user.activo = activo

        if password and len(password.strip()) >= 6:
            user.password_hash = generate_password_hash(password.strip(), method="pbkdf2:sha256")

        db.session.commit()
        registrar_auditoria("EDICION_USUARIO", f"Actualizados datos de usuario ID {user.id} ({user.email})", user_id=current_user.id)
        return redirect(url_for("admin_usuarios_list", mensaje=f"¡Usuario '{user.nombre}' actualizado correctamente!"))

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR EDITAR USUARIO] {e}")
        return redirect(url_for("admin_usuarios_list", error="Error al actualizar los datos del usuario."))


@app.route("/admin/usuarios/<int:user_id>/estado", methods=["POST"])
@login_required
@solo_superadmin
def admin_cambiar_estado_usuario(user_id):
    token = request.form.get("csrf_token")
    if not validate_csrf_token(token):
        return redirect(url_for("admin_usuarios_list", error="Token CSRF inválido. Reintentá."))

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return redirect(url_for("admin_usuarios_list", error="No podés desactivar tu propia cuenta actual."))

    user.activo = not user.activo
    db.session.commit()
    
    estado_str = "activado" if user.activo else "desactivado"
    registrar_auditoria("CAMBIO_ESTADO_USUARIO", f"Usuario ID {user.id} ({user.email}) {estado_str}", user_id=current_user.id)
    return redirect(url_for("admin_usuarios_list", mensaje=f"Usuario '{user.nombre}' fue {estado_str}."))


@app.route("/admin/usuarios/<int:user_id>/eliminar", methods=["POST"])
@login_required
@solo_superadmin
def admin_eliminar_usuario(user_id):
    token = request.form.get("csrf_token")
    if not validate_csrf_token(token):
        return redirect(url_for("admin_usuarios_list", error="Token CSRF inválido. Reintentá."))

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return redirect(url_for("admin_usuarios_list", error="No podés eliminar tu propia cuenta de usuario."))

    nombre = user.nombre
    email = user.email
    db.session.delete(user)
    db.session.commit()

    registrar_auditoria("ELIMINACION_USUARIO", f"Usuario {email} (ID {user_id}) eliminado", user_id=current_user.id)
    return redirect(url_for("admin_usuarios_list", mensaje=f"El usuario '{nombre}' ({email}) fue eliminado."))


# ==============================================================================
# RUTA PÚBLICA DE LA DEMO CON TRACKING (/demo/<slug>)
# ==============================================================================

@app.route("/demo/<slug>")
def ver_demo_publica(slug):
    demo = DemoSolution.query.filter_by(slug=slug).first_or_404()
    template_override = request.args.get("template")
    modo_param = (request.args.get("modo") or "").lower().strip()
    vista_param = (request.args.get("vista") or "").lower().strip()

    es_admin_logueado = current_user.is_authenticated if current_user else False
    es_vista_interna = (vista_param == "interna" or modo_param == "admin")

    if modo_param == "cliente":
        modo_cliente = True
    else:
        modo_cliente = not (es_admin_logueado or es_vista_interna)

    # Registrar visualización
    try:
        now = datetime.utcnow()
        demo.vistas_count = (demo.vistas_count or 0) + 1
        demo.ultima_vista = now

        log_vista = DemoViewLog(
            demo_id=demo.id,
            ip_origen=request.remote_addr or "127.0.0.1",
            user_agent=request.headers.get("User-Agent", "")[:250],
            fecha_vista=now
        )
        db.session.add(log_vista)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"[WARN TRACKING DEMO] {e}")

    lang = (request.args.get("lang") or request.cookies.get("demo_lang") or "es").lower().strip()
    context = preparar_contexto_demo(demo, template_override=template_override, modo_cliente=modo_cliente, lang=lang)
    return render_template("demos/preview.html", **context)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=True)

