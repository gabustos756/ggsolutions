"""
Motor de Ensamblado de Demos Personalizadas para GG Solutions.
Genera sitios web y landings 100% enfocados en vender el negocio del cliente a sus usuarios finales
con diseño ultra-premium, tipografías legibles e imágenes de alta definición.
"""

import json
import re
import urllib.parse


DOLORES_POR_RUBRO = {
    "salud": [
        "Ausentismo constante en turnos agendados sin aviso previo",
        "Recepción con líneas de teléfono saturadas durante horas pico",
        "Falta de fichas médicas e historias clínicas digitalizadas"
    ],
    "automotriz": [
        "Presupuestos informales enviados sin detalle claro al cliente",
        "Mano de obra frenada por falta de repuestos en stock al reparar",
        "Clientes consultando reiteradamente el estado de su vehículo"
    ],
    "gastronomia": [
        "Desperdicio de insumos por falta de control de inventario",
        "Comandas manuales lentas que demoran el servicio en mesa",
        "Falta de catálogo digital interactivo con pedidos directos a cocina/WA"
    ],
    "retail": [
        "Stock desincronizado entre el local físico y la venta online",
        "Pérdida de carritos de compra por procesos de checkout lentos",
        "Consultas repetitivas por disponibilidad de talles/colores"
    ],
    "servicios": [
        "Lógica de cotización manual lenta que retrasa la firma de contratos",
        "Desorden en el seguimiento de tareas, archivos y entregables",
        "Falta de un portal privado para que el cliente consulte sus avances"
    ],
    "inmobiliaria": [
        "Consultas masivas sobre propiedades que ya fueron alquiladas o vendidas",
        "Dificultad para coordinar visitas presenciales con interesados",
        "Falta de un buscador con mapa e imágenes HD por presupuesto"
    ],
    "general": [
        "Falta de automatización en la captación y filtro de prospectos",
        "Procesos operativos en hojas de cálculo desactualizadas",
        "Pérdida de tiempo en respuestas repetitivas por canales de atención"
    ]
}


THEMES_MAP = {
    "salud": {
        "bg": "#070d17",
        "card_bg": "rgba(15, 23, 42, 0.75)",
        "accent": "#00f2fe",
        "gradient": "from-cyan-400 via-teal-300 to-emerald-400",
        "badge_bg": "bg-cyan-500/15 text-cyan-300 border-cyan-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Plus Jakarta Sans', sans-serif",
        "hero_bg_image": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-user-doctor", "title": "Médicos Especialistas", "desc": "Cuerpo profesional de excelencia"},
            {"icon": "fa-stethoscope", "title": "Tecnología Médica", "desc": "Diagnóstico de alta precisión"},
            {"icon": "fa-calendar-check", "title": "Turnos en Línea", "desc": "Reserva ágil sin esperas"},
            {"icon": "fa-shield-heart", "title": "Atención Humanizada", "desc": "Seguimiento médico continuo"}
        ]
    },
    "automotriz": {
        "bg": "#0c0a09",
        "card_bg": "rgba(28, 25, 23, 0.75)",
        "accent": "#f97316",
        "gradient": "from-amber-400 via-orange-500 to-red-500",
        "badge_bg": "bg-orange-500/15 text-orange-300 border-orange-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Outfit', sans-serif",
        "hero_bg_image": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-screwdriver-wrench", "title": "Diagnóstico Computarizado", "desc": "Escaneo de módulos multimarca"},
            {"icon": "fa-shield-halved", "title": "Garantía Escrita", "desc": "Respaldo en cada reparación"},
            {"icon": "fa-gears", "title": "Repuestos Originales", "desc": "Componentes de fábrica"},
            {"icon": "fa-clock", "title": "Entrega Puntual", "desc": "Cumplimiento estricto de plazos"}
        ]
    },
    "gastronomia": {
        "bg": "#0f0b08",
        "card_bg": "rgba(28, 19, 14, 0.75)",
        "accent": "#f59e0b",
        "gradient": "from-amber-300 via-orange-400 to-amber-500",
        "badge_bg": "bg-amber-500/15 text-amber-300 border-amber-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Outfit', sans-serif",
        "hero_bg_image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-utensils", "title": "Ingredientes Frescos", "desc": "Selección diaria de temporada"},
            {"icon": "fa-wine-glass", "title": "Carta de Autor", "desc": "Recetas exclusivas y maridaje"},
            {"icon": "fa-motorcycle", "title": "Delivery Express", "desc": "Empaquetado térmico especial"},
            {"icon": "fa-chair", "title": "Reservas Online", "desc": "Mesa garantizada en segundos"}
        ]
    },
    "retail": {
        "bg": "#0a0814",
        "card_bg": "rgba(22, 17, 38, 0.75)",
        "accent": "#ec4899",
        "gradient": "from-pink-400 via-rose-400 to-purple-400",
        "badge_bg": "bg-pink-500/15 text-pink-300 border-pink-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Outfit', sans-serif",
        "hero_bg_image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-tags", "title": "Precios Directos", "desc": "La mejor relación costo-beneficio"},
            {"icon": "fa-truck-fast", "title": "Envíos en el Día", "desc": "Entregas express a domicilio"},
            {"icon": "fa-credit-card", "title": "Pagos Flexibles", "desc": "Todas las tarjetas y transferencias"},
            {"icon": "fa-headset", "title": "Asesoramiento Experto", "desc": "Atención directa por WhatsApp"}
        ]
    },
    "servicios": {
        "bg": "#080c18",
        "card_bg": "rgba(15, 23, 42, 0.75)",
        "accent": "#3b82f6",
        "gradient": "from-blue-400 via-sky-400 to-indigo-400",
        "badge_bg": "bg-blue-500/15 text-blue-300 border-blue-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Plus Jakarta Sans', sans-serif",
        "hero_bg_image": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-award", "title": "Calidad Garantizada", "desc": "Procesos estandarizados de precisión"},
            {"icon": "fa-lightbulb", "title": "Soluciones a Medida", "desc": "Diseño adaptado a tu necesidad"},
            {"icon": "fa-handshake", "title": "Trato Directo", "desc": "Comunicación clara sin intermediarios"},
            {"icon": "fa-chart-line", "title": "Resultados Medibles", "desc": "Cumplimiento estricto de metas"}
        ]
    },
    "inmobiliaria": {
        "bg": "#070f0c",
        "card_bg": "rgba(16, 28, 22, 0.75)",
        "accent": "#10b981",
        "gradient": "from-emerald-400 via-teal-300 to-emerald-500",
        "badge_bg": "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Plus Jakarta Sans', sans-serif",
        "hero_bg_image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-house-circle-check", "title": "Propiedades Verificadas", "desc": "Catálogo auditado de inmuebles"},
            {"icon": "fa-scale-balanced", "title": "Asesoramiento Legal", "desc": "Acompañamiento en todo el proceso"},
            {"icon": "fa-camera-retro", "title": "Fotos & Tours HD", "desc": "Visualización completa del inmueble"},
            {"icon": "fa-handshake-angle", "title": "Atención Personalizada", "desc": "Agentes especializados de zona"}
        ]
    },
    "general": {
        "bg": "#080a14",
        "card_bg": "rgba(16, 21, 35, 0.75)",
        "accent": "#6366f1",
        "gradient": "from-indigo-400 via-purple-400 to-cyan-400",
        "badge_bg": "bg-indigo-500/15 text-indigo-300 border-indigo-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Plus Jakarta Sans', sans-serif",
        "hero_bg_image": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-star", "title": "Servicio de Excelencia", "desc": "Máxima atención al cliente"},
            {"icon": "fa-shield-check", "title": "Garantía de Satisfacción", "desc": "Compromiso total en cada trabajo"},
            {"icon": "fa-bolt", "title": "Respuesta Inmediata", "desc": "Atención rápida por WhatsApp"},
            {"icon": "fa-users", "title": "Equipo Especializado", "desc": "Profesionales capacitados"}
        ]
    }
}

MODULOS_TITULOS = {
    "agenda": {
        "badge": "AGENDA & TURNO DIGITAL 24/7",
        "titulo": "Reservá tu Cita o Turno en Línea en 3 Pasos",
        "subtitulo": "Elegí el servicio, el profesional y la fecha que mejor se adapte a tus horarios sin demoras ni llamadas.",
    },
    "stock": {
        "badge": "CATÁLOGO & DISPONIBILIDAD EN VIVO",
        "titulo": "Explorá Nuestro Catálogo & Consultá Disponibilidad",
        "subtitulo": "Productos seleccionados con la mejor garantía, precios competitivos y atención personalizada.",
    },
    "logistica": {
        "badge": "ENVÍOS RÁPIDOS A DOMICILIO",
        "titulo": "Cotizá el Envío & Seguimiento de Tu Pedido",
        "subtitulo": "Calculá el valor del flete según tu zona y monitoreá el estado de tu pedido en tiempo real.",
    },
    "decisiones": {
        "badge": "ATENCIÓN INTELIGENTE EN LÍNEA",
        "titulo": "Asesoramiento Digital & Respuestas Inmediatas",
        "subtitulo": "Seleccioná el tipo de consulta que necesitás para recibir asistencia personalizada al instante.",
    },
    "metricas": {
        "badge": "COMPROMISO DE CALIDAD & EFICIENCIA",
        "titulo": "Indicadores de Atención & Satisfacción del Cliente",
        "subtitulo": "Nuestras métricas en vivo respaldadas por las calificaciones verificadas de nuestros clientes.",
    },
    "ecommerce": {
        "badge": "CATÁLOGO & COMPRAS AL INSTANTE",
        "titulo": "Catálogo Dinámico & Pedidos por WhatsApp",
        "subtitulo": "Explorá nuestros productos, agregá al carrito y enviá tu pedido directamente por WhatsApp.",
    },
    "cotizador": {
        "badge": "SIMULADOR DE PRESUPUESTOS",
        "titulo": "Cotizá Tu Requerimiento al Instante",
        "subtitulo": "Seleccioná las características de tu servicio o proyecto y obtené una estimación transparente.",
    }
}


def generar_copy_negocio(nombre_negocio, rubro_key):
    """
    Genera titulares y propuestas de valor 100% enfocadas en vender el negocio del cliente
    a sus propios clientes finales.
    """
    nombre = nombre_negocio.strip()
    
    if rubro_key == "salud":
        headline = f"Atención Médica Integral & Cuidado de Confianza en {nombre}"
        subheadline = f"En {nombre} combinamos profesionales de excelencia, equipamiento moderno y atención personalizada. Reservá tu turno online de forma rápida."
    elif rubro_key == "automotriz":
        headline = f"Servicio Técnico, Mecánica & Diagnóstico Computarizado en {nombre}"
        subheadline = f"En {nombre} cuidamos tu vehículo con repuestos de máxima calidad, diagnóstico preciso y garantía escrita. Agendá tu turno o cotizá tu servicio."
    elif rubro_key == "gastronomia":
        headline = f"Sabores Auténticos, Calidad & Atención Exclusiva en {nombre}"
        subheadline = f"En {nombre} elaboramos cada propuesta con ingredientes frescos seleccionados. Disfrutá de una experiencia única, reservá tu mesa o hacé tu pedido online."
    elif rubro_key == "retail":
        headline = f"Catálogo Completo, Asesoramiento Experto & Envíos en {nombre}"
        subheadline = f"En {nombre} encontrás todo lo que necesitás con la mejor relación precio-calidad, stock garantizado y entregas a domicilio."
    elif rubro_key == "inmobiliaria":
        headline = f"Propiedades Exclusivas & Asesoramiento Inmobiliario en {nombre}"
        subheadline = f"Encontrá tu próximo hogar o la inversión ideal en {nombre} con el respaldo y la transparencia de nuestro equipo de profesionales."
    elif rubro_key == "servicios":
        headline = f"Soluciones Profesionales a Medida & Asesoramiento Técnico en {nombre}"
        subheadline = f"En {nombre} transformamos tus requerimientos en resultados concretos con la máxima precisión, calidad y cumplimiento de plazos."
    else:
        headline = f"Calidad, Compromiso & Atención de Excelencia en {nombre}"
        subheadline = f"En {nombre} brindamos soluciones integrales adaptadas a cada cliente, garantizando la máxima eficiencia y satisfacción."

    return headline, subheadline


def preparar_contexto_demo(demo_obj) -> dict:
    """
    Toma una instancia de DemoSolution de la BD y genera el diccionario de contexto
    completo para renderizar `templates/demos/preview.html`.
    """
    rubro_key = (demo_obj.rubro or "general").lower()
    if rubro_key not in THEMES_MAP:
        rubro_key = "general"

    theme = THEMES_MAP[rubro_key]
    modulo_key = (demo_obj.modulo_solucion or "agenda").lower()
    modulo_info = MODULOS_TITULOS.get(modulo_key, MODULOS_TITULOS["agenda"])

    # Generar titulares enfocados 100% en el negocio del cliente
    hero_headline, hero_subheadline = generar_copy_negocio(demo_obj.nombre_negocio, rubro_key)

    # Parsear reseñas de JSON
    reviews = []
    if demo_obj.reviews_json:
        try:
            reviews = json.loads(demo_obj.reviews_json)
        except Exception:
            reviews = []

    if not reviews:
        reviews = [
            {
                "author_name": "Gabriel M.",
                "rating": 5,
                "text": f"La mejor atención en {demo_obj.nombre_negocio}. Muy satisfecho con el servicio y la rapidez.",
                "relative_time": "hace 1 semana"
            },
            {
                "author_name": "Ana Clara S.",
                "rating": 5,
                "text": f"Rápidos, prolijos y súper recomendables. Excelente experiencia en {demo_obj.nombre_negocio}.",
                "relative_time": "hace un mes"
            }
        ]

    # Parsear fotos reales de Google Places si existen
    fotos = []
    if demo_obj.fotos_json:
        try:
            fotos = json.loads(demo_obj.fotos_json)
        except Exception:
            fotos = []

    # Formatear WhatsApp
    wa_clean = re.sub(r"\D", "", demo_obj.whatsapp or demo_obj.telefono or "5493515550199")

    # Mensaje predeterminado de consulta para el botón de la demo (del cliente final al negocio)
    msg_wa = f"Hola {demo_obj.nombre_negocio}, quisiera consultar por sus productos y servicios."
    wa_link = f"https://wa.me/{wa_clean}?text={urllib.parse.quote(msg_wa)}"

    # Link directo de WhatsApp para el equipo de GG Solutions (en el Dock Superior)
    msg_gg = f"Hola GG Solutions, estuve revisando la demo creada para {demo_obj.nombre_negocio} y quisiera consultar para implementar nuestro sistema."
    wa_ggsolutions = f"https://wa.me/5493513360533?text={urllib.parse.quote(msg_gg)}"

    return {
        "demo": demo_obj,
        "theme": theme,
        "modulo_info": modulo_info,
        "hero_headline": hero_headline,
        "hero_subheadline": hero_subheadline,
        "reviews": reviews,
        "fotos": fotos,
        "wa_link": wa_link,
        "wa_ggsolutions": wa_ggsolutions,
        "maps_embed_query": urllib.parse.quote(f"{demo_obj.nombre_negocio}, {demo_obj.direccion or demo_obj.ciudad or 'Córdoba'}")
    }
