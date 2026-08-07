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
    "herramientas": [
        "Stock desincronizado y pérdida de tiempo respondiendo disponibilidad en mostrador",
        "Tardanza en armar cotizaciones y presupuestos complejos para gremios y obras",
        "Pérdida de ventas B2B por falta de catálogo digital filtrable por marcas"
    ],
    "opticas": [
        "Ausentismo en pruebas de visión y controles optométricos programados",
        "Complejidad para mostrar y explicar tratamientos de cristales (Blue Block, Antirreflex)",
        "Consultas repetitivas de pacientes sobre el estado de entrega de sus cristales"
    ],
    "kiosco": [
        "Pérdida de margen por mercadería congelada o golosinas sin rotación a tiempo",
        "Consultas repetitivas por WhatsApp sobre combos de bebidas y ofertas para eventos",
        "Filas lentas en mostrador durante horas pico buscando precios de artículos"
    ],
    "general": [
        "Falta de automatización en la captación y filtro de prospectos",
        "Procesos operativos en hojas de cálculo desactualizadas",
        "Pérdida de tiempo en respuestas repetitivas por canales de atención"
    ]
}


from services.image_bank_engine import obtener_imagenes_rubro, seleccionar_hero_inteligente

THEMES_MAP = {
    "salud": {
        "bg": "#070d17",
        "card_bg": "rgba(15, 23, 42, 0.75)",
        "accent": "#00f2fe",
        "gradient": "from-cyan-400 via-teal-300 to-emerald-400",
        "badge_bg": "bg-cyan-500/15 text-cyan-300 border-cyan-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Outfit', sans-serif",
        "font_google": "https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-user-doctor", "title": "Médicos Especialistas", "desc": "Cuerpo profesional de excelencia", "tag": "Atención Médica"},
            {"icon": "fa-stethoscope", "title": "Tecnología Médica", "desc": "Diagnóstico de alta precisión", "tag": "Equipamiento"},
            {"icon": "fa-calendar-check", "title": "Turnos en Línea", "desc": "Reserva ágil sin esperas", "tag": "Agendamiento"},
            {"icon": "fa-shield-heart", "title": "Atención Humanizada", "desc": "Seguimiento médico continuo", "tag": "Cuidado Integral"}
        ]
    },
    "automotriz": {
        "bg": "#0c0a09",
        "card_bg": "rgba(28, 25, 23, 0.75)",
        "accent": "#f97316",
        "gradient": "from-amber-400 via-orange-500 to-red-500",
        "badge_bg": "bg-orange-500/15 text-orange-300 border-orange-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Oswald', sans-serif",
        "font_google": "https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-screwdriver-wrench", "title": "Diagnóstico Computarizado", "desc": "Escaneo de módulos multimarca", "tag": "Tecnología"},
            {"icon": "fa-shield-halved", "title": "Garantía Escrita", "desc": "Respaldo en cada reparación", "tag": "Confianza"},
            {"icon": "fa-gears", "title": "Repuestos Originales", "desc": "Componentes de fábrica", "tag": "Calidad"},
            {"icon": "fa-clock", "title": "Entrega Puntual", "desc": "Cumplimiento estricto de plazos", "tag": "Eficiencia"}
        ]
    },
    "gastronomia": {
        "bg": "#0f0b08",
        "card_bg": "rgba(28, 19, 14, 0.75)",
        "accent": "#f59e0b",
        "gradient": "from-amber-300 via-orange-400 to-amber-500",
        "badge_bg": "bg-amber-500/15 text-amber-300 border-amber-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Playfair Display', serif",
        "font_google": "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-utensils", "title": "Ingredientes Frescos", "desc": "Selección diaria de temporada", "tag": "Gourmet"},
            {"icon": "fa-wine-glass", "title": "Carta de Autor", "desc": "Recetas exclusivas y maridaje", "tag": "Especialidad"},
            {"icon": "fa-motorcycle", "title": "Delivery Express", "desc": "Empaquetado térmico especial", "tag": "Pedidos Online"},
            {"icon": "fa-chair", "title": "Reservas Online", "desc": "Mesa garantizada en segundos", "tag": "Reservas"}
        ]
    },
    "herramientas": {
        "bg": "#0f0d0a",
        "card_bg": "rgba(28, 22, 16, 0.75)",
        "accent": "#eab308",
        "gradient": "from-amber-400 via-yellow-500 to-amber-600",
        "badge_bg": "bg-yellow-500/15 text-yellow-300 border-yellow-500/30",
        "font_family": "'Inter', sans-serif",
        "title_font": "'Outfit', sans-serif",
        "font_google": "https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-toolbox", "title": "Marcas Líderes", "desc": "Herramientas e insumos garantizados", "tag": "Industrial"},
            {"icon": "fa-truck-ramp-box", "title": "Venta por Volumen", "desc": "Descuentos directos para gremios", "tag": "B2B"},
            {"icon": "fa-calculator", "title": "Cotización de Obras", "desc": "Presupuestos rápidos en el día", "tag": "Cotización"},
            {"icon": "fa-shield-cat", "title": "Garantía Oficial", "desc": "Respaldo directo de fábrica", "tag": "Confianza"}
        ]
    },
    "opticas": {
        "bg": "#070c14",
        "card_bg": "rgba(14, 23, 38, 0.75)",
        "accent": "#38bdf8",
        "gradient": "from-sky-400 via-cyan-300 to-blue-500",
        "badge_bg": "bg-sky-500/15 text-sky-300 border-sky-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Plus Jakarta Sans', sans-serif",
        "font_google": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1591076482161-42ce6da69f67?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-glasses", "title": "Diseño & Estilo", "desc": "Armazones de tendencia internacional", "tag": "Colección"},
            {"icon": "fa-eye", "title": "Examen Optométrico", "desc": "Control de agudeza visual matriculado", "tag": "Salud Visual"},
            {"icon": "fa-laptop-medical", "title": "Filtro Blue Block", "desc": "Protección para trabajo con pantallas", "tag": "Tecnología"},
            {"icon": "fa-clock-rotate-left", "title": "Turnos en Línea", "desc": "Agendamiento ágil sin demoras", "tag": "Reserva"}
        ]
    },
    "kiosco": {
        "bg": "#060f14",
        "card_bg": "rgba(12, 28, 36, 0.75)",
        "accent": "#10b981",
        "gradient": "from-emerald-400 via-teal-400 to-cyan-500",
        "badge_bg": "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Outfit', sans-serif",
        "font_google": "https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-bottle-water", "title": "Bebidas Frías", "desc": "Stock permanente de primeras marcas", "tag": "Express"},
            {"icon": "fa-box-open", "title": "Combos & Ofertas", "desc": "Promociones exclusivas de fin de semana", "tag": "Ahorro"},
            {"icon": "fa-bolt-lightning", "title": "Retiro Inmediato", "desc": "Tu pedido listo por mostrador", "tag": "Sin Filas"},
            {"icon": "fa-basket-shopping", "title": "Almacén de Cercanía", "desc": "Todo lo que necesitás a metros", "tag": "Cercanía"}
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
        "font_google": "https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-tags", "title": "Precios Directos", "desc": "La mejor relación costo-beneficio", "tag": "Promociones"},
            {"icon": "fa-truck-fast", "title": "Envíos en el Día", "desc": "Entregas express a domicilio", "tag": "Logística"},
            {"icon": "fa-credit-card", "title": "Pagos Flexibles", "desc": "Todas las tarjetas y transferencias", "tag": "Facilidades"},
            {"icon": "fa-headset", "title": "Asesoramiento Experto", "desc": "Atención directa por WhatsApp", "tag": "Soporte"}
        ]
    },
    "servicios": {
        "bg": "#080c18",
        "card_bg": "rgba(15, 23, 42, 0.75)",
        "accent": "#3b82f6",
        "gradient": "from-blue-400 via-sky-400 to-indigo-400",
        "badge_bg": "bg-blue-500/15 text-blue-300 border-blue-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Outfit', sans-serif",
        "font_google": "https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-award", "title": "Calidad Garantizada", "desc": "Procesos estandarizados de precisión", "tag": "Estándar ISO"},
            {"icon": "fa-lightbulb", "title": "Soluciones a Medida", "desc": "Diseño adaptado a tu necesidad", "tag": "Personalizado"},
            {"icon": "fa-handshake", "title": "Trato Directo", "desc": "Comunicación clara sin intermediarios", "tag": "Transparencia"},
            {"icon": "fa-chart-line", "title": "Resultados Medibles", "desc": "Cumplimiento estricto de metas", "tag": "Eficiencia"}
        ]
    },
    "inmobiliaria": {
        "bg": "#070f0c",
        "card_bg": "rgba(16, 28, 22, 0.75)",
        "accent": "#10b981",
        "gradient": "from-emerald-400 via-teal-300 to-emerald-500",
        "badge_bg": "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Outfit', sans-serif",
        "font_google": "https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-house-circle-check", "title": "Propiedades Verificadas", "desc": "Catálogo auditado de inmuebles", "tag": "Catálogo"},
            {"icon": "fa-scale-balanced", "title": "Asesoramiento Legal", "desc": "Acompañamiento en todo el proceso", "tag": "Seguridad"},
            {"icon": "fa-camera-retro", "title": "Fotos & Tours HD", "desc": "Visualización completa del inmueble", "tag": "Experiencia"},
            {"icon": "fa-handshake-angle", "title": "Atención Personalizada", "desc": "Agentes especializados de zona", "tag": "Servicio"}
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
        "font_google": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-star", "title": "Servicio de Excelencia", "desc": "Máxima atención al cliente", "tag": "Calidad"},
            {"icon": "fa-shield-check", "title": "Garantía de Satisfacción", "desc": "Compromiso total en cada trabajo", "tag": "Garantía"},
            {"icon": "fa-bolt", "title": "Respuesta Inmediata", "desc": "Atención rápida por WhatsApp", "tag": "Rapidez"},
            {"icon": "fa-users", "title": "Equipo Especializado", "desc": "Profesionales capacitados", "tag": "Experiencia"}
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
    elif rubro_key == "herramientas":
        headline = f"Herramientas Profesionales, Insumos & Cotizador de Obras en {nombre}"
        subheadline = f"En {nombre} abastecemos a gremios y profesionales con las mejores marcas, asesoramiento técnico en mostrador y presupuestos rápidos por WhatsApp."
    elif rubro_key == "opticas":
        headline = f"Salud Visual, Armazones de Diseño & Examen Optométrico en {nombre}"
        subheadline = f"En {nombre} cuidamos tu visión con cristales de alta precisión, filtro Blue Block y atención personalizada por optómetras matriculados."
    elif rubro_key == "kiosco":
        headline = f"Tienda Express, Bebidas Frías & Combos en {nombre}"
        subheadline = f"En {nombre} encontrás todo lo que necesitás al instante: bebidas congeladas, combos para eventos y pedidos rápidos por WhatsApp sin hacer filas."
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

    # Inyección de Banco de Imágenes y Noticias
    img_data = obtener_imagenes_rubro(rubro_key)
    
    # Enriquecer los pilares con imágenes 16:9 del banco
    pilares_enriquecidos = []
    for idx, pilar in enumerate(theme["pilares"]):
        p_copy = dict(pilar)
        if "pilares" in img_data and idx < len(img_data["pilares"]):
            p_copy["image"] = img_data["pilares"][idx]
        else:
            p_copy["image"] = theme["hero_bg_image"]
        pilares_enriquecidos.append(p_copy)

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
            },
            {
                "author_name": "Marcos Rossi",
                "rating": 5,
                "text": f"Atención impecable y respuesta inmediata. Volveré sin dudas a {demo_obj.nombre_negocio}.",
                "relative_time": "hace 2 semanas"
            }
        ]

    # Parsear fotos reales de Google Places si existen
    fotos = []
    if demo_obj.fotos_json:
        try:
            fotos = json.loads(demo_obj.fotos_json)
        except Exception:
            fotos = []

    # Seleccionar la imagen Hero HD de más alta definición del banco etiquetado de la carpeta local
    hero_meta = seleccionar_hero_inteligente(rubro_key, demo_obj.nombre_negocio)
    hero_bg_url = hero_meta["url"]

    # Asignar Hero HD al tema visual
    theme_copy = dict(theme)
    theme_copy["hero_bg_image"] = hero_bg_url
    theme_copy["hero_meta"] = hero_meta

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
        "theme": theme_copy,
        "pilares": pilares_enriquecidos,
        "news": img_data.get("news", []),
        "modulo_info": modulo_info,
        "hero_headline": hero_headline,
        "hero_subheadline": hero_subheadline,
        "hero_meta": hero_meta,
        "reviews": reviews,
        "fotos": fotos,
        "wa_link": wa_link,
        "wa_ggsolutions": wa_ggsolutions,
        "maps_embed_query": urllib.parse.quote(f"{demo_obj.nombre_negocio}, {demo_obj.direccion or demo_obj.ciudad or 'Córdoba'}")
    }

