"""
Motor de Ensamblado de Demos Personalizadas para GG Solutions.
Genera sitios web y landings 100% enfocados en vender el negocio del cliente a sus usuarios finales
con diseño ultra-premium, tipografías legibles e imágenes de alta definición.
"""

import json
import re
import urllib.parse
from services.i18n_engine import get_i18n_context, translate_pilares


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
    "indumentaria": [
        "Consultas repetitivas sobre disponibilidad de talles, colores y medidas por WhatsApp",
        "Dificultad para mostrar la caída, género y detalles de las prendas sin tienda física",
        "Pérdida de carritos de compra por falta de catálogo filtrable por categoría"
    ],
    "hostel": [
        "Elevadas comisiones pagadas a OTAs (Booking, Hostelworld, Airbnb) de hasta 18-20%",
        "Descontrol de camas disponibles y overbooking al gestionar reservas por WhatsApp",
        "Consultas tardías de precios y tipos de cama (mixta, femenina, privada)"
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
    "indumentaria": {
        "bg": "#0b0813",
        "card_bg": "rgba(22, 16, 35, 0.75)",
        "accent": "#d946ef",
        "gradient": "from-fuchsia-400 via-pink-500 to-purple-500",
        "badge_bg": "bg-fuchsia-500/15 text-fuchsia-300 border-fuchsia-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Outfit', sans-serif",
        "font_google": "https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-shirt", "title": "Diseño & Confección", "desc": "Prendas seleccionadas de calidad noble", "tag": "Lookbook"},
            {"icon": "fa-ruler-horizontal", "title": "Talles Reales", "desc": "Asesoramiento de calce e información de medidas", "tag": "Guía Talles"},
            {"icon": "fa-truck-fast", "title": "Envíos en el Día", "desc": "Entregas express a domicilio y todo el país", "tag": "Logística"},
            {"icon": "fa-rotate-left", "title": "Cambios Sin Cargo", "desc": "Garantía de satisfacción y cambio ágil", "tag": "Confianza"}
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
    "deportes": {
        "bg": "#06120e",
        "card_bg": "rgba(10, 26, 20, 0.75)",
        "accent": "#10b981",
        "gradient": "from-emerald-400 via-teal-300 to-lime-400",
        "badge_bg": "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Outfit', sans-serif",
        "font_google": "https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-table-tennis-paddle-ball", "title": "Canchas Polvo de Ladrillo", "desc": "Mantenimiento diario & luz LED nocturna", "tag": "Infraestructura"},
            {"icon": "fa-user-graduate", "title": "Academia de Tenis", "desc": "Clases individuales & grupales AAT", "tag": "Entrenamiento"},
            {"icon": "fa-screwdriver-wrench", "title": "Encordado Digital Express", "desc": "Calibración exacta de tensión en raquetas", "tag": "Pro Shop"},
            {"icon": "fa-trophy", "title": "Torneos & Rankings", "desc": "Competencias internas de socios todo el año", "tag": "Club Life"}
        ]
    },
    "pilates_wellness": {
        "bg": "#061310",
        "card_bg": "rgba(12, 30, 24, 0.75)",
        "accent": "#34d399",
        "gradient": "from-emerald-400 via-teal-300 to-cyan-400",
        "badge_bg": "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Outfit', sans-serif",
        "font_google": "https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-child-reaching", "title": "Pilates Reformer & Postura", "desc": "Alineación corporal, tono muscular y flexibilidad en máquinas de última generación", "tag": "Reformer Pro"},
            {"icon": "fa-spa", "title": "Yoga & Mindful Wellbeing", "desc": "Vinyasa, Hatha y meditación guiada para reducir el estrés y renovar energía", "tag": "Mente & Cuerpo"},
            {"icon": "fa-users-between-lines", "title": "Grupos Reducidos & Personalizado", "desc": "Atención enfocada en las necesidades de cada alumno", "tag": "Atención Exclusiva"},
            {"icon": "fa-heart-pulse", "title": "Rehabilitación & Salud Integral", "desc": "Prevención del dolor de espalda y mejora de la movilidad funcional", "tag": "Salud Activa"}
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
    },
    "hostel": {
        "bg": "#09131a",
        "card_bg": "rgba(15, 30, 42, 0.75)",
        "accent": "#2dd4bf",
        "gradient": "from-teal-300 via-emerald-400 to-cyan-500",
        "badge_bg": "bg-teal-500/15 text-teal-300 border-teal-500/30",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "title_font": "'Outfit', sans-serif",
        "font_google": "https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
        "hero_bg_image": "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=1200&q=80",
        "pilares": [
            {"icon": "fa-bed", "title": "Camas & Lockers", "desc": "Lockers individuales de alta seguridad y enchufes por cama", "tag": "Confort & Seguridad"},
            {"icon": "fa-location-dot", "title": "Ubicación Central", "desc": "En el corazón de la ciudad, cerca de transportes y tours", "tag": "Ubicación"},
            {"icon": "fa-people-group", "title": "Ambiente & Eventos", "desc": "Bar, zona social, cenas compartidas y tours grupales", "tag": "Social & Bar"},
            {"icon": "fa-wifi", "title": "High-Speed Wi-Fi", "desc": "Conexión estable y espacio de trabajo para nómadas digitales", "tag": "Co-Working"}
        ]
    }
}

MODULOS_TITULOS = {
    "hostel": {
        "badge": "RESERVA DE CAMAS & ESTADÍAS EN VIVO 24/7",
        "titulo": "Reserva tu Cama & Estadía en Vivo",
        "subtitulo": "Elegí las fechas de tu viaje, hora aproximada de llegada y el tipo de cama ideal con tarifa directa sin comisiones.",
    },
    "agenda": {
        "badge": "AGENDA & RESERVAS DIGITALES 24/7",
        "titulo": "Agendá tu Turno o Reserva en 3 Pasos",
        "subtitulo": "Elegí la modalidad, el horario y confirmá directamente por WhatsApp sin llamadas ni esperas.",
    },
    "stock": {
        "badge": "CATÁLOGO & DISPONIBILIDAD EN VIVO",
        "titulo": "Explorá Nuestro Catálogo & Consultá Disponibilidad",
        "subtitulo": "Productos seleccionados con la mejor garantía, precios competitivos y atención personalizada.",
    },
    "ecommerce": {
        "badge": "PEDIDOS & CARTA DIGITAL EN VIVO",
        "titulo": "Hacé tu Pedido Online con Envíos Directos",
        "subtitulo": "Armá tu carrito con nuestros productos estrella y enviá tu orden armada directamente a nuestro WhatsApp.",
    },
    "cotizador": {
        "badge": "PRESUPUESTADOR Y SIMULADOR B2B",
        "titulo": "Cotizá tus Insumos & Materiales en el Acto",
        "subtitulo": "Seleccioná las cantidades requeridas y calculá el costo estimado con precios actualizados.",
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
    },
    "hostel": {
        "badge": "RESERVA DE CAMAS & ESTADÍAS EN VIVO",
        "titulo": "Reserva tu Cama & Estadía en Vivo",
        "subtitulo": "Elegí las fechas de tu viaje, número de huéspedes y tipo de cama ideal con tarifa directa sin comisiones.",
    }
}

HOSTEL_CONFIG = {
    "titulo": "Reserva de Camas & Estadías",
    "subtitulo": "Ingresá tus fechas de entrada/salida y elegí la habitación que mejor se adapte a tu viaje.",
    "badge": "Disponibilidad Garantizada 100%",
    "paso1_label": "1. Fechas de Estadía & Huéspedes",
    "paso2_label": "2. Tipo de Habitación / Cama",
    "paso3_label": "3. Datos del Huésped & Confirmación",
    "opciones": [
        {
            "id": "dorm_mixto_4",
            "nombre": "Dormitorio Mixto (4 Camas)",
            "desc": "Con aire acondicionado, lockers individuales y baño compartido.",
            "precio_usd": 15,
            "precio_ars": 18000,
            "tag": "Más Popular",
            "badge_color": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
            "icon": "fa-bed"
        },
        {
            "id": "dorm_fem_6",
            "nombre": "Dormitorio Femenino (6 Camas)",
            "desc": "Exclusivo mujeres, secador de pelo, espejo amplio y lockers de seguridad.",
            "precio_usd": 14,
            "precio_ars": 16800,
            "tag": "Exclusivo Mujeres",
            "badge_color": "bg-purple-500/20 text-purple-300 border-purple-500/30",
            "icon": "fa-person-dress"
        },
        {
            "id": "dorm_masc_8",
            "nombre": "Dormitorio Masculino (8 Camas)",
            "desc": "Habitación espaciosa, enchufes y luz de lectura en cada cama.",
            "precio_usd": 12,
            "precio_ars": 14400,
            "tag": "Económico",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "icon": "fa-person"
        },
        {
            "id": "privada_doble",
            "nombre": "Habitación Privada Doble (Baño Privado)",
            "desc": "Cama Sommier Matrimonial, TV Smart, A/C y baño en suite.",
            "precio_usd": 35,
            "precio_ars": 42000,
            "tag": "Privada & Confort",
            "badge_color": "bg-amber-500/20 text-amber-300 border-amber-500/30",
            "icon": "fa-door-closed"
        }
    ]
}


AGENDA_CONFIG_POR_RUBRO = {
    "pilates_wellness": {
        "badge": "Reserva de Clases & Evaluación Postural 24/7",
        "titulo": "Reservá tu Clase de Pilates, Yoga o Evaluación Saludable",
        "subtitulo": "Elegí la modalidad de clase, la fecha y confirmá tu lugar directamente por WhatsApp.",
        "paso1_label": "1. Seleccioná el Tipo de Clase / Servicio",
        "opcion1": {
            "title": "Clase de Pilates Reformer",
            "desc": "Entrenamiento en máquinas Reformer | Máximo 5 alumnos por clase",
            "tag": "Más Solicitado",
            "icon": "fa-child-reaching"
        },
        "opcion2": {
            "title": "Yoga Vinyasa & Meditación",
            "desc": "Fluidez corporal, respiración guiada y relajación profunda",
            "tag": "Mindfulness",
            "icon": "fa-spa"
        },
        "opcion3": {
            "title": "Evaluación Postural & Salud",
            "desc": "Diagnóstico inicial de movilidad, columna y plan personalizado",
            "tag": "Diagnóstico",
            "icon": "fa-heart-pulse"
        },
        "paso2_label": "2. Fecha de Clase / Sesión",
        "paso3_label": "3. Horarios Disponibles en Estudio",
        "paso4_label": "4. Datos del Alumno / Paciente",
        "input_nombre_placeholder": "Tu Nombre Completo",
        "input_tel_placeholder": "Tu WhatsApp (ej: 3515551234)",
        "cta_text": "🧘 Confirmar Reserva de Clase por WhatsApp"
    },
    "deportes": {
        "badge": "Reserva de Canchas & Clases 24/7",
        "titulo": "Reservá tu Cancha de Tenis o Clase en Línea",
        "subtitulo": "Elegí la cancha, la fecha y el horario sin llamadas ni superposición de turnos.",
        "paso1_label": "1. Seleccioná el Tipo de Reserva / Servicio",
        "opcion1": {
            "title": "Cancha Polvo de Ladrillo (90 min)",
            "desc": "Turnos de singles o dobles | Iluminación LED",
            "tag": "Canchas",
            "icon": "fa-table-tennis-paddle-ball"
        },
        "opcion2": {
            "title": "Clase Particular / Academia",
            "desc": "Profesor matriculado AAT | Canasto de pelotas",
            "tag": "Recomendado",
            "icon": "fa-graduation-cap"
        },
        "opcion3": {
            "title": "Encordado & Servicio Pro Shop",
            "desc": "Calibración digital de tensión | Luxilon / Babolat",
            "tag": "Pro Shop",
            "icon": "fa-screwdriver-wrench"
        },
        "paso2_label": "2. Fecha de Juego / Clase",
        "paso3_label": "3. Horarios Disponibles en Grilla",
        "paso4_label": "4. Datos del Jugador / Socio",
        "input_nombre_placeholder": "Tu Nombre Completo (Socio / Jugador)",
        "input_tel_placeholder": "Tu WhatsApp de Contacto",
        "cta_text": "🎾 Confirmar Reserva de Cancha por WA"
    },
    "gastronomia": {
        "badge": "Reserva de Mesas & Take Away",
        "titulo": "Reservá tu Mesa o Encargá para Llevar",
        "subtitulo": "Garantizá tu lugar en el salón o programá tu pedido para retirar en el horario que prefieras.",
        "paso1_label": "1. Seleccioná el Tipo de Reserva / Servicio",
        "opcion1": {
            "title": "Reserva de Mesa Salón",
            "desc": "Capacidad de 2 a 8 comensales | Salón principal",
            "tag": "Recomendado",
            "icon": "fa-utensils"
        },
        "opcion2": {
            "title": "Pedido Take Away / Retiro",
            "desc": "Retiro express por mostrador | Sin esperas",
            "tag": "Express",
            "icon": "fa-bag-shopping"
        },
        "opcion3": {
            "title": "Mesa Especial / Evento",
            "desc": "Cumpleaños y reuniones de grupo | Reserva previa",
            "tag": "Grupos",
            "icon": "fa-wine-glass"
        },
        "paso2_label": "2. Fecha de Reserva",
        "paso3_label": "3. Horarios Disponibles",
        "paso4_label": "4. Datos de la Reserva",
        "input_nombre_placeholder": "Tu Nombre Completo",
        "input_tel_placeholder": "Tu WhatsApp (ej: 3515551234)",
        "cta_text": "🍷 Confirmar Reserva por WhatsApp"
    },
    "automotriz": {
        "badge": "Agendamiento de Taller Computarizado",
        "titulo": "Agendá un Turno de Mantenimiento o Escaneo",
        "subtitulo": "Elegí la fecha y hora para el diagnóstico computarizado, service de aceite o revisión de frenos de tu vehículo.",
        "paso1_label": "1. Seleccioná el Servicio Mecánico",
        "opcion1": {
            "title": "Service Completo & Aceite",
            "desc": "Cambio de lubricante, filtro de aire y fluidos",
            "tag": "Mantenimiento",
            "icon": "fa-oil-can"
        },
        "opcion2": {
            "title": "Diagnóstico Escaneado OBD2",
            "desc": "Escaneo computarizado de módulos y sensores",
            "tag": "Recomendado",
            "icon": "fa-laptop-code"
        },
        "opcion3": {
            "title": "Frenos & Tren Delantero",
            "desc": "Revisión de pastillas, discos y amortiguadores",
            "tag": "Seguridad",
            "icon": "fa-shield-halved"
        },
        "paso2_label": "2. Fecha de Ingreso",
        "paso3_label": "3. Horarios Disponibles en Taller",
        "paso4_label": "4. Datos del Vehículo & Propietario",
        "input_nombre_placeholder": "Tu Nombre y Modelo / Patente del Auto",
        "input_tel_placeholder": "Tu WhatsApp de Contacto",
        "cta_text": "🔧 Confirmar Turno de Taller por WhatsApp"
    },
    "herramientas": {
        "badge": "Cotización B2B & Asesoramiento",
        "titulo": "Solicitá Cotización de Insumos o Demostración",
        "subtitulo": "Agendá asesoramiento técnico en mostrador o enviá tu lista de materiales para cotizar con descuento gremial.",
        "paso1_label": "1. Seleccioná el Tipo de Requerimiento",
        "opcion1": {
            "title": "Cotización de Lista de Obras",
            "desc": "Presupuestos de volumen para contratistas y gremios",
            "tag": "Venta B2B",
            "icon": "fa-file-invoice-dollar"
        },
        "opcion2": {
            "title": "Asesoramiento de Maquinaria",
            "desc": "Demostración de herramientas inalámbricas e insumos",
            "tag": "Recomendado",
            "icon": "fa-toolbox"
        },
        "opcion3": {
            "title": "Alta de Cuenta Gremial",
            "desc": "Apertura de cuenta corriente y descuentos por gremio",
            "tag": "Beneficio",
            "icon": "fa-id-card"
        },
        "paso2_label": "2. Fecha Estimada",
        "paso3_label": "3. Horario Preferido de Atención",
        "paso4_label": "4. Datos de Empresa / Gremio",
        "input_nombre_placeholder": "Empresa / Nombre de Contratista",
        "input_tel_placeholder": "WhatsApp de Contacto",
        "cta_text": "🔨 Enviar Lista para Cotizar por WA"
    },
    "opticas": {
        "badge": "Gabinete Optométrico Registrado",
        "titulo": "Agendá tu Examen Optométrico o Prueba de Armazones",
        "subtitulo": "Reservá tu turno con nuestros optómetras matriculados para control de graduación y cristales Blue Block.",
        "paso1_label": "1. Seleccioná el Motivo de Consulta",
        "opcion1": {
            "title": "Examen Visual & Graduación",
            "desc": "Control de agudeza visual y prescripción médica",
            "tag": "Salud Visual",
            "icon": "fa-eye"
        },
        "opcion2": {
            "title": "Prueba de Armazones & Sol",
            "desc": "Asesoramiento de estéticas y marcas de tendencia",
            "tag": "Recomendado",
            "icon": "fa-glasses"
        },
        "opcion3": {
            "title": "Contactología & Cristales",
            "desc": "Adaptación de lentes de contacto y filtro Blue Block",
            "tag": "Especializado",
            "icon": "fa-circle-dot"
        },
        "paso2_label": "2. Fecha deseada de Atención",
        "paso3_label": "3. Horarios Disponibles en Gabinete",
        "paso4_label": "4. Datos del Paciente",
        "input_nombre_placeholder": "Nombre y Apellido del Paciente",
        "input_tel_placeholder": "Tu WhatsApp para Confirmación",
        "cta_text": "👓 Confirmar Turno Optométrico por WA"
    },
    "kiosco": {
        "badge": "Pedidos Express & Combos Previa",
        "titulo": "Encargá tu Combo de Bebidas o Pedido Express sin Filas",
        "subtitulo": "Armá tu pedido con bebidas frías y snacks listos para pasar a buscar por mostrador.",
        "paso1_label": "1. Seleccioná la Modalidad de Pedido",
        "opcion1": {
            "title": "Combo Previa & Eventos",
            "desc": "Bebidas congeladas + Fernet + Hielo + Snacks XL",
            "tag": "Oferta",
            "icon": "fa-wine-bottle"
        },
        "opcion2": {
            "title": "Pedido Express Mostrador",
            "desc": "Retiro inmediato sin hacer filas en horas pico",
            "tag": "Sin Filas",
            "icon": "fa-bolt"
        },
        "opcion3": {
            "title": "Caja Regalo & Chocolates",
            "desc": "Golosinas seleccionadas y regalería especial",
            "tag": "Regalos",
            "icon": "fa-gift"
        },
        "paso2_label": "2. Fecha de Retiro",
        "paso3_label": "3. Horario de Retiro por Mostrador",
        "paso4_label": "4. Datos para el Retiro",
        "input_nombre_placeholder": "Tu Nombre Completo",
        "input_tel_placeholder": "Tu WhatsApp",
        "cta_text": "🛍️ Confirmar Pedido Express por WA"
    },
    "indumentaria": {
        "badge": "Asesoramiento de Imagen & Showroom 24/7",
        "titulo": "Agendá tu Cita en Showroom o Consulta de Talles",
        "subtitulo": "Coordiná tu visita privada o consultá calce de prendas directamente por WhatsApp.",
        "paso1_label": "1. Seleccioná el Tipo de Atención",
        "opcion1": {
            "title": "Prueba de Colección en Showroom",
            "desc": "Cita privada para probar prendas y asesoramiento de imagen",
            "tag": "Exclusivo",
            "icon": "fa-shirt"
        },
        "opcion2": {
            "title": "Consulta de Talles & Envíos",
            "desc": "Asistencia por WhatsApp sobre medidas y despacho",
            "tag": "Recomendado",
            "icon": "fa-ruler-horizontal"
        },
        "opcion3": {
            "title": "Reserva de Prendas / Lookbook",
            "desc": "Apartado de artículos seleccionados de nueva temporada",
            "tag": "Tendencia",
            "icon": "fa-bag-shopping"
        },
        "paso2_label": "2. Fecha de Cita / Atención",
        "paso3_label": "3. Horarios Disponibles",
        "paso4_label": "4. Datos de Contacto",
        "input_nombre_placeholder": "Tu Nombre Completo",
        "input_tel_placeholder": "Tu WhatsApp para Confirmación",
        "cta_text": "🛍️ Confirmar Cita / Consulta por WA"
    },
    "salud": {
        "badge": "Turnos Médicos Digitales",
        "titulo": "Agendá tu Consulta Médica o Chequeo de Salud",
        "subtitulo": "Seleccioná la especialidad médica, fecha y horario de atención sin esperas.",
        "paso1_label": "1. Seleccioná el Servicio / Especialidad",
        "opcion1": {
            "title": "Consulta Clínica General",
            "desc": "Evaluación médica e historia clínica",
            "tag": "Atención Médica",
            "icon": "fa-user-doctor"
        },
        "opcion2": {
            "title": "Chequeo Preventivo Anual",
            "desc": "Análisis clínicos y electrocardiograma",
            "tag": "Recomendado",
            "icon": "fa-heart-pulse"
        },
        "opcion3": {
            "title": "Estudios & Diagnóstico",
            "desc": "Imagenología y laboratorio de análisis",
            "tag": "Diagnóstico",
            "icon": "fa-stethoscope"
        },
        "paso2_label": "2. Fecha Preferida",
        "paso3_label": "3. Horarios Disponibles",
        "paso4_label": "4. Datos del Paciente",
        "input_nombre_placeholder": "Nombre del Paciente",
        "input_tel_placeholder": "Tu WhatsApp de Contacto",
        "cta_text": "🩺 Confirmar Turno Médico por WA"
    },
    "general": {
        "badge": "Agendamiento en Línea 24/7",
        "titulo": "Reservá tu Turno o Asesoramiento Personalizado",
        "subtitulo": "Seleccioná la fecha y horario disponible para coordinar tu atención sin demoras.",
        "paso1_label": "1. Seleccioná el Tipo de Atención",
        "opcion1": {
            "title": "Asesoramiento Inicial",
            "desc": "Evaluación de requerimientos y consulta",
            "tag": "Consulta",
            "icon": "fa-comments"
        },
        "opcion2": {
            "title": "Servicio Especializado",
            "desc": "Atención directa con nuestro equipo",
            "tag": "Recomendado",
            "icon": "fa-star"
        },
        "opcion3": {
            "title": "Revisión & Seguimiento",
            "desc": "Control de avances y gestión",
            "tag": "Seguimiento",
            "icon": "fa-circle-check"
        },
        "paso2_label": "2. Fecha Preferida",
        "paso3_label": "3. Horario Disponible",
        "paso4_label": "4. Datos de Contacto",
        "input_nombre_placeholder": "Tu Nombre Completo",
        "input_tel_placeholder": "Tu WhatsApp",
        "cta_text": "📅 Confirmar Turno por WhatsApp"
    }
}


ADMIN_PANEL_POR_RUBRO = {
    "hostel": {
        "kpi1_label": "Ocupación Hoy",
        "kpi2_label": "Check-ins / Check-outs",
        "kpi3_label": "Alerta Blanco & Insumos",
        "kpi4_label": "Caja & Estadías Hoy",
        "kpi_capacidad": "87% Ocupación Camas",
        "kpi_pedidos": "6 Movimientos Hoy",
        "kpi_stock": "2 Insumos Bajo Stock",
        "kpi_facturacion": "$184.000 Caja Hoy",
        "tab1_label": "1. Check-ins & Check-outs del Día",
        "tab2_label": "2. Control de Insumos & Blanco",
        "tab3_label": "3. Mensajes & Voluntariados (CRM)",
        "tab4_label": "4. Proveedores & Carga de Facturas",
        "tabla1_titulo": "Control de Arribos, Check-outs & Movimientos de Huéspedes",
        "tabla2_titulo": "Inventario de Blancos, Toallas & Insumos de Desayuno",
        "col1_nombre": "Código / ID",
        "col2_nombre": "Huésped / Origen",
        "col3_nombre": "Habitación / Cama Asignada",
        "productos_stock": [
            {"sku": "BLAN-101", "nombre": "Juegos de Sábanas 1 Plaza (Algodón 200 Hilos)", "stock": 48, "unidad": "juegos libres", "alerta": "Disponible", "precio": "$4.500/juego"},
            {"sku": "BLAN-102", "nombre": "Toallas de Mano & Toallones de Baño", "stock": 12, "unidad": "unidades libres", "alerta": "Reposición Lavandería", "precio": "$2.800/u"},
            {"sku": "DESA-103", "nombre": "Café en Grano & Té Variedades (Desayuno)", "stock": 5, "unidad": "kg disponibles", "alerta": "Disponible", "precio": "$12.000/kg"},
            {"sku": "DESA-104", "nombre": "Leche Entera & Medialunas Mediodía", "stock": 8, "unidad": "litros libres", "alerta": "Bajo Stock", "precio": "$1.200/L"},
            {"sku": "LIMP-105", "nombre": "Kit de Sanitización & Lavandina Concentrada", "stock": 15, "unidad": "litros libres", "alerta": "Disponible", "precio": "$3.500/L"}
        ],
        "pedidos": [
            {"id": "#RES-801", "cliente": "afQEcqapV8uVD16d (Argentina 🇦🇷)", "detalle": "Reserva Dormitorio Mixto (2 Noches) — Arribo Estimado 16:00 hs", "monto": "$36.000", "hora": "Hoy 16:00 hs", "estado": "CHECK-IN PENDIENTE", "tipo_accion": "checkin", "btn_texto": "Registrar Check-in", "btn_icon": "fa-key", "btn_class": "bg-emerald-500 hover:bg-emerald-400 text-slate-950", "nuevo_estado": "EN ESTADÍA", "badge_class": "bg-amber-500/20 text-amber-300 border border-amber-500/30"},
            {"id": "#OUT-802", "cliente": "Sophie L. (Francia 🇫🇷)", "detalle": "Reserva Dormitorio Femenino (3 Noches) — Check-out y Salida", "monto": "$50.400", "hora": "Hoy 11:00 hs", "estado": "CHECK-OUT HOY", "tipo_accion": "checkout", "btn_texto": "Registrar Check-out", "btn_icon": "fa-door-open", "btn_class": "bg-cyan-500 hover:bg-cyan-400 text-slate-950", "nuevo_estado": "LIBERADO / LIMPIEZA", "badge_class": "bg-rose-500/20 text-rose-300 border border-rose-500/30"},
            {"id": "#RES-803", "cliente": "Mateo G. (Uruguay 🇺🇾)", "detalle": "Habitación Privada Doble Suite #204 (1 Noche) — En Estadía", "monto": "$42.000", "hora": "En Estadía", "estado": "EN ESTADÍA", "tipo_accion": "estadia", "btn_texto": "Ficha de Huésped", "btn_icon": "fa-id-card", "btn_class": "bg-slate-800 hover:bg-slate-700 text-white border border-white/10", "nuevo_estado": "ESTADÍA ACTIVA", "badge_class": "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"},
            {"id": "#VOL-804", "cliente": "Lucas P. (Brasil 🇧🇷)", "detalle": "Postulación Voluntariado Recepción — Disponibilidad 15 Sep / 15 Oct", "monto": "$0", "hora": "Hace 2 horas", "estado": "POSTULANTE VOLUNTARIO", "tipo_accion": "voluntario", "btn_texto": "Entrevista WhatsApp", "btn_icon": "fa-brands fa-whatsapp", "btn_class": "bg-emerald-600 hover:bg-emerald-500 text-white", "nuevo_estado": "ENTREVISTA COORDINADA", "badge_class": "bg-purple-500/20 text-purple-300 border border-purple-500/30"}
        ],
        "mensajes": [
            {"cliente": "Lucas P. (Brasil 🇧🇷)", "tel": "5511988776655", "consulta": "Olá! Gostaria de me candidatar para o voluntariado de recepção em setembro.", "hora": "14:20 hs", "estado": "PENDIENTE"},
            {"cliente": "Emma W. (EE.UU. 🇺🇸)", "tel": "12025550143", "consulta": "Hi! Can I store my luggage before 14:00 check-in time today?", "hora": "11:05 hs", "estado": "RESPONDIDO"}
        ],
        "proveedores": [
            {"nombre": "Lavandería & Blanco San Martín", "rubro": "Sabanas, Toallas & Lavandería", "deuda": "$45.000", "estado": "Al día"},
            {"nombre": "Distribuidora Bebidas & Desayunos", "rubro": "Insumos Desayuno & Bar", "deuda": "$32.000", "estado": "Al día"}
        ]
    },
    "pilates_wellness": {
        "kpi1_label": "Ocupación Reformers",
        "kpi2_label": "Alumnos / Turnos Hoy",
        "kpi3_label": "Pases / Bonos Activos",
        "kpi4_label": "Caja & Clases Hoy",
        "kpi_capacidad": "88% Ocupación Camas Reformer",
        "kpi_pedidos": "18 Alumnos / Reservas Hoy",
        "kpi_stock": "4 Bonos por Vencer",
        "kpi_facturacion": "$480.000 Caja Hoy",
        "tab1_label": "1. Reservas de Clases & Alumnos",
        "tab2_label": "2. Equipamiento & Insumos Wellness",
        "tab3_label": "3. Consultas & Inscripciones (CRM)",
        "tab4_label": "4. Proveedores & Carga de Facturas",
        "tabla1_titulo": "Control de Asistencia & Reservas de Clases",
        "tabla2_titulo": "Inventario de Mats, Bandas & Insumos de Sanitización",
        "col1_nombre": "ID Reserva",
        "col2_nombre": "Alumno / Cliente",
        "col3_nombre": "Clase / Horario Asignado",
        "productos_stock": [
            {"sku": "WELL-101", "nombre": "Pase Mensual Pilates Reformer (8 Clases)", "stock": 25, "unidad": "pases", "alerta": "Disponible", "precio": "$45.000"},
            {"sku": "WELL-102", "nombre": "Pase Libre Yoga & Meditación (Ilimitado)", "stock": 18, "unidad": "pases", "alerta": "Disponible", "precio": "$38.000"},
            {"sku": "WELL-103", "nombre": "Mat de Yoga Antideslizante Pro Eco-Friendly", "stock": 3, "unidad": "unidades", "alerta": "Bajo Stock", "precio": "$22.000"},
            {"sku": "WELL-104", "nombre": "Sanitizante de Reformer & Toallitas de Limpieza", "stock": 5, "unidad": "litros", "alerta": "Disponible", "precio": "$4.500"}
        ],
        "pedidos": [
            {"id": "#RES-401", "cliente": "Lucía P.", "detalle": "Reserva Clase Pilates Reformer (18:00 hs)", "monto": "$45.000", "hora": "Hoy 18:00 hs", "estado": "CONFIRMADO"},
            {"id": "#RES-402", "cliente": "Mariana V.", "detalle": "Evaluación Postural & Movilidad", "monto": "$18.000", "hora": "Hace 20 min", "estado": "EN ESTUDIO"}
        ],
        "mensajes": [
            {"cliente": "Carolina Rossi", "tel": "3516778899", "consulta": "Hola! Quisiera saber si tienen cupos disponibles en Pilates Reformer por la tarde.", "hora": "12:15 hs", "estado": "PENDIENTE"}
        ],
        "proveedores": [
            {"nombre": "Equipamientos Reformer Pro Argentina", "rubro": "Camas & Resortes Pilates", "deuda": "$120.000", "estado": "Al día"}
        ]
    },
    "deportes": {
        "kpi1_label": "Ocupación Canchas",
        "kpi2_label": "Turnos & Clases Hoy",
        "kpi3_label": "Encordados Pendientes",
        "kpi4_label": "Caja & Turnos Hoy",
        "kpi_capacidad": "94% Canchas Ocupadas",
        "kpi_pedidos": "28 Reservas / Turnos",
        "kpi_stock": "3 Encordados Faltantes",
        "kpi_facturacion": "$580.000 Caja Hoy",
        "tab1_label": "1. Turnos de Canchas & Clases",
        "tab2_label": "2. Insumos de Tenis, Pádel & Encordados",
        "tab3_label": "3. Consultas de Alumnos & Turnos (CRM)",
        "tab4_label": "4. Proveedores & Carga de Facturas",
        "tabla1_titulo": "Control de Turnos de Cancha & Encordados",
        "tabla2_titulo": "Inventario de Pelotas, Cuerdas & Grips de Pádel/Tenis",
        "col1_nombre": "Código Turno",
        "col2_nombre": "Jugadores / Alumno",
        "col3_nombre": "Cancha / Horario Reservado",
        "productos_stock": [
            {"sku": "TEN-101", "nombre": "Tubo de Pelotas Penn Tour Presurizadas (3u)", "stock": 36, "unidad": "tubos", "alerta": "Disponible", "precio": "$14.000"},
            {"sku": "TEN-102", "nombre": "Cuerda Luxilon Alu Power 1.25mm (Set)", "stock": 4, "unidad": "sets", "alerta": "Bajo Stock", "precio": "$16.500"},
            {"sku": "TEN-103", "nombre": "Overgrip Wilson Pro Comfort (Pack x3)", "stock": 25, "unidad": "packs", "alerta": "Disponible", "precio": "$6.800"},
            {"sku": "TEN-104", "nombre": "Raqueta Wilson Blade 98 V8 (Grip 3)", "stock": 2, "unidad": "unidades", "alerta": "Reposición", "precio": "$320.000"}
        ],
        "pedidos": [
            {"id": "#RES-101", "cliente": "Juan Cruz V. vs Matías S.", "detalle": "Reserva Cancha #1 Polvo de Ladrillo (90 min) + Luz LED", "monto": "$12.000", "hora": "Turno 19:30 hs", "estado": "CONFIRMADO"},
            {"id": "#RES-100", "cliente": "Federico B. (Alumno)", "detalle": "Clase Particular de Tenis 60 min con Prof. Nico M.", "monto": "$18.000", "hora": "Hace 20 min", "estado": "EN CURSO"},
            {"id": "#ENC-099", "cliente": "Gonzalo L.", "detalle": "Encordado Luxilon 52 lbs - Raqueta Babolat Pure Aero", "monto": "$16.500", "hora": "Hace 2 horas", "estado": "LISTO PARA RETIRAR"}
        ],
        "mensajes": [
            {"cliente": "Esteban R.", "tel": "3517654321", "consulta": "Hola! ¿Tienen cancha de polvo libre hoy a las 20:30hs para dobles?", "hora": "13:30 hs", "estado": "PENDIENTE"},
            {"cliente": "Facundo B.", "tel": "3512345678", "consulta": "Quería saber cuánto demora el encordado de una raqueta Wilson con Luxilon.", "hora": "11:15 hs", "estado": "RESPONDIDO"}
        ],
        "proveedores": [
            {"nombre": "Wilson Sporting Goods Argentina", "rubro": "Raquetas & Pelotas de Tenis", "deuda": "$240.000", "estado": "Al día"},
            {"nombre": "Babolat Argentina S.A.", "rubro": "Cuerdas, Encordadoras & Grips", "deuda": "$130.000", "estado": "Vence 20/08"}
        ]
    },
    "gastronomia": {
        "kpi1_label": "Ocupación Salón",
        "kpi2_label": "Comandas & Delivery",
        "kpi3_label": "Insumos de Cocina",
        "kpi4_label": "Caja & Ventas Hoy",
        "kpi_capacidad": "85% Salón Lleno",
        "kpi_pedidos": "18 Pedidos / Comandas",
        "kpi_stock": "4 Insumos Críticos",
        "kpi_facturacion": "$485.000 Caja Hoy",
        "tab1_label": "1. Comandas & Pedidos de Cocina",
        "tab2_label": "2. Insumos de Cocina, Carnes & Bebidas",
        "tab3_label": "3. Reservas de Mesas & WhatsApp CRM",
        "tab4_label": "4. Proveedores & Carga de Facturas",
        "tabla1_titulo": "Control de Comandas de Cocina & Pedidos Online",
        "tabla2_titulo": "Inventario de Materia Prima, Bebidas & Packaging",
        "col1_nombre": "Nº Comanda",
        "col2_nombre": "Cliente / Mesa",
        "col3_nombre": "Detalle del Pedido",
        "productos_stock": [
            {"sku": "GAST-101", "nombre": "Materia Prima Smash Burgers (Medallón 120g)", "stock": 42, "unidad": "kg", "alerta": "Disponible", "precio": "$8.500/kg"},
            {"sku": "GAST-102", "nombre": "Pan Brioche de Papa Artesanal", "stock": 8, "unidad": "docenas", "alerta": "Bajo Stock", "precio": "$4.200/doc"},
            {"sku": "GAST-103", "nombre": "Queso Cheddar Inglés Feteado & Huevos Fresh", "stock": 15, "unidad": "kg", "alerta": "Disponible", "precio": "$12.000/kg"},
            {"sku": "GAST-104", "nombre": "Cerveza IPA Tirada 50L (Barril)", "stock": 3, "unidad": "barriles", "alerta": "Reposición", "precio": "$45.000/u"}
        ],
        "pedidos": [
            {"id": "#CMD-1042", "cliente": "Juan Pablo M.", "detalle": "2x Double Bacon Smash + 2x Pintas IPA", "monto": "$24.500", "hora": "Hace 8 min", "estado": "EN COCINA"},
            {"id": "#CMD-1041", "cliente": "Carolina R.", "detalle": "1x Veggie Burger + Papas Rústicas + Gaseosa", "monto": "$14.200", "hora": "Hace 15 min", "estado": "LISTO PARA SERVIR"},
            {"id": "#CMD-1040", "cliente": "Lucas V.", "detalle": "Combo Familia: 4x Cheeseburger + 2x Papas XL", "monto": "$38.000", "hora": "Hace 28 min", "estado": "ENTREGADO"}
        ],
        "mensajes": [
            {"cliente": "Mariana Gómez", "tel": "3515123456", "consulta": "Hola, ¿tienen mesas disponibles para 6 personas hoy a las 21:30hs?", "hora": "12:45 hs", "estado": "PENDIENTE"},
            {"cliente": "Esteban F.", "tel": "3516987654", "consulta": "Quisiera consultar si hacen envíos a domicilio a Zona Norte.", "hora": "11:20 hs", "estado": "RESPONDIDO"}
        ],
        "proveedores": [
            {"nombre": "Frigorífico San Juan S.A.", "rubro": "Carnes & Medallones", "deuda": "$120.000", "estado": "Al día"},
            {"nombre": "Distribuidora Bebidas del Sur", "rubro": "Cervezas & Gaseosas", "deuda": "$85.000", "estado": "Vence 15/08"}
        ]
    },
    "automotriz": {
        "kpi1_label": "Ocupación Elevadores",
        "kpi2_label": "Turnos Taller Hoy",
        "kpi3_label": "Alertas de Aceite / Filtros",
        "kpi4_label": "Caja & Taller Hoy",
        "kpi_capacidad": "92% Elevadores Ocupados",
        "kpi_pedidos": "12 Turnos Taller",
        "kpi_stock": "3 Aceites / Filtros Bajos",
        "kpi_facturacion": "$890.000 Caja Hoy",
        "tab1_label": "1. Turnos de Taller & Vehículos",
        "tab2_label": "2. Repuestos, Lubricantes & Filtros",
        "tab3_label": "3. Consultas & Presupuestos (CRM)",
        "tab4_label": "4. Proveedores & Carga de Facturas",
        "tabla1_titulo": "Control de Órdenes de Trabajo & Vehículos en Taller",
        "tabla2_titulo": "Inventario de Aceites, Filtros & Pastillas de Freno",
        "col1_nombre": "Nº Orden",
        "col2_nombre": "Cliente / Vehículo",
        "col3_nombre": "Trabajo / Reparación Solicitada",
        "productos_stock": [
            {"sku": "AUTO-201", "nombre": "Aceite Sintético Shell Helix 5W30 (4L)", "stock": 14, "unidad": "bidones", "alerta": "Disponible", "precio": "$38.500"},
            {"sku": "AUTO-202", "nombre": "Filtro de Aceite Mann W712", "stock": 5, "unidad": "unidades", "alerta": "Bajo Stock", "precio": "$8.200"},
            {"sku": "AUTO-203", "nombre": "Pastillas de Freno Fras-le VW Gol/Polo", "stock": 8, "unidad": "juegos", "alerta": "Disponible", "precio": "$26.000"},
            {"sku": "AUTO-204", "nombre": "Líquido de Frenos DOT4 Bosch (500ml)", "stock": 2, "unidad": "unidades", "alerta": "Reposición", "precio": "$7.500"}
        ],
        "pedidos": [
            {"id": "#TRN-809", "cliente": "Martín G. (Toyota Hilux)", "detalle": "Service Completo 100.000km + Cambio de Pastillas", "monto": "$145.000", "hora": "En taller", "estado": "EN REPARACIÓN"},
            {"id": "#TRN-808", "cliente": "Gonzalo B. (Ford Ranger)", "detalle": "Escaneo Computarizado OBD2 + Check Engine", "monto": "$35.000", "hora": "Hace 30 min", "estado": "LISTO DENTRO DE 1H"},
            {"id": "#TRN-807", "cliente": "Sebastián L. (Peugeot 208)", "detalle": "Cambio de Aceite 5W30 + Filtros de Aire", "monto": "$52.000", "hora": "Hace 2 horas", "estado": "ENTREGADO"}
        ],
        "mensajes": [
            {"cliente": "Ricardo Méndez", "tel": "3514223344", "consulta": "Hola, ¿cuánto sale hacer el service de los 50 mil km a una Tracker 2021?", "hora": "13:10 hs", "estado": "PENDIENTE"},
            {"cliente": "Fabiana C.", "tel": "3516554433", "consulta": "Tengo turno para las 16hs para alineación y balanceo. ¿Están a término?", "hora": "12:05 hs", "estado": "RESPONDIDO"}
        ],
        "proveedores": [
            {"nombre": "Distribuidora Shell Argentina", "rubro": "Lubricantes & Fluidos", "deuda": "$340.000", "estado": "Al día"},
            {"nombre": "Bosch Autopartes S.R.L.", "rubro": "Frenos & Escáneres", "deuda": "$190.000", "estado": "Vence 20/08"}
        ]
    },
    "opticas": {
        "kpi_capacidad": "78% Turnos Gabinete",
        "kpi_pedidos": "15 Recetas / Cristales",
        "kpi_stock": "5 Armazones en Faltante",
        "kpi_facturacion": "$640.000 Caja Hoy",
        "productos_stock": [
            {"sku": "OPT-301", "nombre": "Cristal Monofocal Blue Block Antirreflex 1.56", "stock": 28, "unidad": "pares", "alerta": "Normal", "precio": "$32.000"},
            {"sku": "OPT-302", "nombre": "Armazón de Acetato Ray-Ban Wayfarer Classic", "stock": 3, "unidad": "unidades", "alerta": "Bajo Stock", "precio": "$89.000"},
            {"sku": "OPT-303", "nombre": "Lentes de Contacto Blandos Acuvue Oasys (Caja 6u)", "stock": 12, "unidad": "cajas", "alerta": "Normal", "precio": "$45.000"},
            {"sku": "OPT-304", "nombre": "Solución Multiuso para Lentes Renu 355ml", "stock": 4, "unidad": "unidades", "alerta": "Reposición", "precio": "$14.500"}
        ],
        "pedidos": [
            {"id": "#REC-504", "cliente": "Dr. Fernando M. (Paciente)", "detalle": "Multifocal Digital Antirreflex HD + Armazón Titanium", "monto": "$168.000", "hora": "En laboratorio", "estado": "EN LABORATORIO"},
            {"id": "#REC-503", "cliente": "Valeria K.", "detalle": "Lentes Monofocales Filtro Pantalla PC + Armazón Acetato", "monto": "$78.000", "hora": "Hace 40 min", "estado": "LISTO PARA RETIRAR"},
            {"id": "#REC-502", "cliente": "Ignacio B.", "detalle": "Anteojo de Sol Polarizado UV400 Oakley", "monto": "$92.000", "hora": "Hace 3 horas", "estado": "ENTREGADO"}
        ],
        "mensajes": [
            {"cliente": "Camila Soria", "tel": "3517889900", "consulta": "Hola! ¿Tienen convenio con OSDE o prevención salud para reembolso de receta?", "hora": "13:15 hs", "estado": "PENDIENTE"},
            {"cliente": "Gabriel R.", "tel": "3512334455", "consulta": "Quería saber si ya llegaron mis cristales multifocales encargados el martes.", "hora": "10:30 hs", "estado": "RESPONDIDO"}
        ],
        "proveedores": [
            {"nombre": "Laboratorio Óptico EssilorLuxottica", "rubro": "Cristales & Lentes Multifocales", "deuda": "$280.000", "estado": "Al día"},
            {"nombre": "Distribuidora Armazones Italia", "rubro": "Armazones & Gafas de Sol", "deuda": "$145.000", "estado": "Vence 18/08"}
        ]
    },
    "herramientas": {
        "kpi_capacidad": "89% Mostrador Gremial",
        "kpi_pedidos": "22 Presupuestos Obras",
        "kpi_stock": "6 Discos / Brocas Críticas",
        "kpi_facturacion": "$1.450.000 Caja Hoy",
        "productos_stock": [
            {"sku": "HERR-401", "nombre": "Taladro Percutor Inalámbrico Bosch GSB 18V-50 (2 Baterías)", "stock": 6, "unidad": "unidades", "alerta": "Normal", "precio": "$185.000"},
            {"sku": "HERR-402", "nombre": "Amoladora Angular DeWalt 4 1/2' 800W DWE4010", "stock": 2, "unidad": "unidades", "alerta": "Bajo Stock", "precio": "$78.000"},
            {"sku": "HERR-403", "nombre": "Disco de Corte Diamantado Continuo 115mm Bosch", "stock": 35, "unidad": "unidades", "alerta": "Normal", "precio": "$12.500"},
            {"sku": "HERR-404", "nombre": "Juego de Llaves Bocallave 108 Piezas Stanley", "stock": 1, "unidad": "caja", "alerta": "Reposición", "precio": "$120.000"}
        ],
        "pedidos": [
            {"id": "#COT-701", "cliente": "Constructora Edisur S.A.", "detalle": "5x Taladros 20V + 50x Discos Diamantados + 10x Antiparras", "monto": "$890.000", "hora": "Cotización B2B", "estado": "EN PREPARACIÓN"},
            {"id": "#COT-700", "cliente": "Plomería El Rayo", "detalle": "Termofusora 1500W + 20x Caños Termofusión 25mm", "monto": "$145.000", "hora": "Hace 20 min", "estado": "LISTO PARA DESPACHO"},
            {"id": "#COT-699", "cliente": "Electricidad Córdoba", "detalle": "Pinza Amperométrica Digital Fluke + Cable 2.5mm", "monto": "$230.000", "hora": "Hace 2 horas", "estado": "ENTREGADO"}
        ],
        "mensajes": [
            {"cliente": "Ing. Marcelo Torres", "tel": "3513445566", "consulta": "Hola, necesito cotizar 20 cajas de tornillos T2 autoperforantes y envío a obra en Manantiales.", "hora": "13:20 hs", "estado": "PENDIENTE"},
            {"cliente": "David M.", "tel": "3518776655", "consulta": "Tienen cuotas sin interés en herramientas inalámbricas DeWalt con Tarjeta Cordobesa?", "hora": "11:45 hs", "estado": "RESPONDIDO"}
        ],
        "proveedores": [
            {"nombre": "Robert Bosch Argentina S.A.", "rubro": "Herramientas Eléctricas", "deuda": "$620.000", "estado": "Al día"},
            {"nombre": "Stanley Black & Decker S.A.", "rubro": "Herramientas Manuales & Discos", "deuda": "$410.000", "estado": "Vence 25/08"}
        ]
    },
    "kiosco": {
        "kpi_capacidad": "95% Rotación Góndola",
        "kpi_pedidos": "34 Pedidos Express",
        "kpi_stock": "8 Snacks / Bebidas Bajas",
        "kpi_facturacion": "$390.000 Caja Hoy",
        "productos_stock": [
            {"sku": "KIOS-501", "nombre": "Fernet Branca 750ml (Caja x6)", "stock": 18, "unidad": "cajas", "alerta": "Normal", "precio": "$11.500/u"},
            {"sku": "KIOS-502", "nombre": "Coca-Cola Sabor Original 2.25L", "stock": 9, "unidad": "botellas", "alerta": "Bajo Stock", "precio": "$2.800/u"},
            {"sku": "KIOS-503", "nombre": "Papas Fritas Lay's Corte Americano 140g", "stock": 24, "unidad": "paquetes", "alerta": "Normal", "precio": "$2.400/u"},
            {"sku": "KIOS-504", "nombre": "Cerveza Stella Artois 710ml Retornable", "stock": 6, "unidad": "botellas", "alerta": "Reposición", "precio": "$3.200/u"}
        ],
        "pedidos": [
            {"id": "#EXP-309", "cliente": "Facundo T.", "detalle": "Combo Previa: 1x Fernet Branca + 2x Coca-Cola + Bolsa Hielo XL", "monto": "$18.500", "hora": "Hace 5 min", "estado": "EN MOSTRADOR"},
            {"id": "#EXP-308", "cliente": "Sonia M.", "detalle": "2x Chocolates Milka + 1x Alfajor Havanna + 1x Monster Energy", "monto": "$8.200", "hora": "Hace 18 min", "estado": "ENTREGADO"},
            {"id": "#EXP-307", "cliente": "Joaquín R.", "detalle": "1x Pack Cerveza Corona 6u + Lay's Stack", "monto": "$16.400", "hora": "Hace 40 min", "estado": "ENTREGADO"}
        ],
        "mensajes": [
            {"cliente": "Nicolás Peralta", "tel": "3519998877", "consulta": "Hola bro! Tienen hielo congelado y fernet frío para pasar a buscar ya?", "hora": "13:25 hs", "estado": "PENDIENTE"},
            {"cliente": "Romina G.", "tel": "3511112233", "consulta": "Quería encargar una caja de golosinas para un cumpleaños para retirar a las 18hs.", "hora": "12:10 hs", "estado": "RESPONDIDO"}
        ],
        "proveedores": [
            {"nombre": "Distribuidora Coca-Cola Andina", "rubro": "Gaseosas & Aguas", "deuda": "$190.000", "estado": "Al día"},
            {"nombre": "Fratelli Branca Destilerías", "rubro": "Aperitivos & Licores", "deuda": "$140.000", "estado": "Vence 22/08"}
        ]
    },
    "indumentaria": {
        "kpi_capacidad": "91% Rotación de Stock",
        "kpi_pedidos": "26 Ventas / Pedidos Hoy",
        "kpi_stock": "5 Talles Críticos en Faltante",
        "kpi_facturacion": "$680.000 Caja Hoy",
        "productos_stock": [
            {"sku": "IND-101", "nombre": "Campera Oversize Denim Premium (Talle M)", "stock": 5, "unidad": "unidades", "alerta": "Normal", "precio": "$68.000"},
            {"sku": "IND-102", "nombre": "Jean Straight Fit Urban Tailored (Talle 42)", "stock": 2, "unidad": "unidades", "alerta": "Bajo Stock", "precio": "$45.000"},
            {"sku": "IND-103", "nombre": "Remera Básica Organic Cotton Pack x2", "stock": 18, "unidad": "packs", "alerta": "Normal", "precio": "$24.000"},
            {"sku": "IND-104", "nombre": "Blazer Tailored Black Edition (Talle L)", "stock": 1, "unidad": "unidad", "alerta": "Reposición", "precio": "$75.000"}
        ],
        "pedidos": [
            {"id": "#PED-601", "cliente": "Sofía M.", "detalle": "1x Campera Denim M + 1x Jean Straight 40", "monto": "$113.000", "hora": "Hace 10 min", "estado": "EN EMPAQUE"},
            {"id": "#PED-600", "cliente": "Valentina G.", "detalle": "2x Remeras Orgánicas S + Envío Express", "monto": "$52.000", "hora": "Hace 35 min", "estado": "DESPACHADO"}
        ],
        "mensajes": [
            {"cliente": "Camila R.", "tel": "3516558899", "consulta": "Hola! Quisiera saber si la campera denim cede o si me conviene talle M o L.", "hora": "12:50 hs", "estado": "PENDIENTE"}
        ],
        "proveedores": [
            {"nombre": "Textil Denim Argentina S.A.", "rubro": "Tejidos & Confección", "deuda": "$190.000", "estado": "Al día"}
        ]
    },
    "general": {
        "kpi_capacidad": "88% Operativa",
        "kpi_pedidos": "14 Solicitudes",
        "kpi_stock": "2 Insumos Críticos",
        "kpi_facturacion": "$520.000 Caja Hoy",
        "productos_stock": [
            {"sku": "GEN-101", "nombre": "Insumo Principal de Servicio", "stock": 15, "unidad": "unidades", "alerta": "Normal", "precio": "$15.000"},
            {"sku": "GEN-102", "nombre": "Material de Reposición Directa", "stock": 4, "unidad": "unidades", "alerta": "Bajo Stock", "precio": "$8.500"}
        ],
        "pedidos": [
            {"id": "#ORD-9021", "cliente": "Clara M.", "detalle": "Solicitud de turno / presupuesto integral", "monto": "$45.000", "hora": "Hace 15 min", "estado": "EN PREPARACIÓN"}
        ],
        "mensajes": [
            {"cliente": "Roberto Gómez", "tel": "3515550199", "consulta": "Hola, quisiera consultar presupuesto de servicio.", "hora": "11:00 hs", "estado": "PENDIENTE"}
        ],
        "proveedores": [
            {"nombre": "Proveedor Central S.A.", "rubro": "Insumos Generales", "deuda": "$85.000", "estado": "Al día"}
        ]
    }
}


PRODUCTOS_POR_RUBRO = {
    "gastronomia": [
        {
            "id": 1,
            "nombre": "Double Bacon Smash Burger",
            "descripcion": "Doble medallón 120g de pella madurada, cheddar inglés, panceta crocante y salsa especial en pan brioche artesanal.",
            "precio": 18500,
            "precio_display": "$18.500",
            "badge": "MÁS VENDIDO",
            "badge_color": "bg-pink-500/20 text-pink-300 border-pink-500/30",
            "btn_color": "from-pink-500 to-rose-500 text-slate-950",
            "stock_count": 35,
            "imagen_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Combo Gourmet Salón & Papas XL",
            "descripcion": "Burger de Autor + Papas Rústicas con provolone frito y dip de alioli + Pinta Cerveza Tirada IPA.",
            "precio": 29900,
            "precio_display": "$29.900",
            "badge": "RECOMENDADO",
            "badge_color": "bg-amber-500/20 text-amber-300 border-amber-500/30",
            "btn_color": "from-amber-400 to-orange-400 text-slate-950",
            "stock_count": 20,
            "imagen_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Cerveza IPA de Autor (500ml)",
            "descripcion": "Elaboración artesanal de alta tomabilidad con notas cítricas y lupulado intenso.",
            "precio": 8500,
            "precio_display": "$8.500",
            "badge": "PROMO",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "btn_color": "from-emerald-400 to-teal-400 text-slate-950",
            "stock_count": 50,
            "imagen_url": "https://images.unsplash.com/photo-1535958636474-b021ee887b13?auto=format&fit=crop&w=800&q=80"
        }
    ],
    "indumentaria": [
        {
            "id": 1,
            "nombre": "Campera Oversize Denim Premium",
            "descripcion": "Confección en algodón 100% denim pesado con lavada vintage y botones grabado láser.",
            "precio": 68000,
            "precio_display": "$68.000",
            "badge": "NUEVA COLECCIÓN",
            "badge_color": "bg-purple-500/20 text-purple-300 border-purple-500/30",
            "btn_color": "from-purple-500 to-pink-500 text-white",
            "stock_count": 12,
            "imagen_url": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Jean Straight Fit Urban Tailored",
            "descripcion": "Calce recto de tendencia con elastano para máxima comodidad. Talles 38 al 48.",
            "precio": 45000,
            "precio_display": "$45.000",
            "badge": "MÁS VENDIDO",
            "badge_color": "bg-pink-500/20 text-pink-300 border-pink-500/30",
            "btn_color": "from-pink-500 to-rose-500 text-slate-950",
            "stock_count": 28,
            "imagen_url": "https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Remera Básica Organic Cotton (Pack x2)",
            "descripcion": "Tejido jersey 24/1 peinado super suave en colores neutros. Talles S al XL.",
            "precio": 24000,
            "precio_display": "$24.000",
            "badge": "BÁSICO",
            "badge_color": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
            "btn_color": "from-cyan-400 to-blue-500 text-slate-950",
            "stock_count": 40,
            "imagen_url": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?auto=format&fit=crop&w=800&q=80"
        }
    ],
    "automotriz": [
        {
            "id": 1,
            "nombre": "Aceite Sintético Shell Helix 5W30 (4L) + Filtro",
            "descripcion": "Bidón 4 litros lubricante 100% sintético para motores nafta y diesel + filtro de aceite Mann.",
            "precio": 46700,
            "precio_display": "$46.700",
            "badge": "MÁS VENDIDO",
            "badge_color": "bg-orange-500/20 text-orange-300 border-orange-500/30",
            "btn_color": "from-orange-500 to-red-500 text-white",
            "stock_count": 18,
            "imagen_url": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Diagnóstico Escaneado Computarizado OBD2",
            "descripcion": "Escaneo de módulos de inyección, ABS, Airbag y diagnóstico de sensores con informe impreso.",
            "precio": 35000,
            "precio_display": "$35.000",
            "badge": "RECOMENDADO",
            "badge_color": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
            "btn_color": "from-cyan-400 to-teal-400 text-slate-950",
            "stock_count": 15,
            "imagen_url": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Juego Pastillas de Freno Fras-le / Bosch",
            "descripcion": "Pastillas cerámicas de alto rendimiento con colocación y revisión de discos incluida.",
            "precio": 38500,
            "precio_display": "$38.500",
            "badge": "SEGURIDAD",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "btn_color": "from-emerald-400 to-teal-400 text-slate-950",
            "stock_count": 10,
            "imagen_url": "https://images.unsplash.com/photo-1530046339160-ce3e530c7d2f?auto=format&fit=crop&w=800&q=80"
        }
    ],
    "herramientas": [
        {
            "id": 1,
            "nombre": "Taladro Percutor Inalámbrico Bosch GSB 18V-50",
            "descripcion": "Motor Brushless sin carbones + 2 Baterías 2.0Ah + Cargador rápido en maletín rígido.",
            "precio": 185000,
            "precio_display": "$185.000",
            "badge": "GARANTÍA BOSCH",
            "badge_color": "bg-yellow-500/20 text-yellow-300 border-yellow-500/30",
            "btn_color": "from-yellow-400 to-amber-500 text-slate-950",
            "stock_count": 6,
            "imagen_url": "https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Amoladora Angular DeWalt 4 1/2' 800W",
            "descripcion": "Eje 5/8' reforzado, guarda sin llave y sistema de expulsión de polvo.",
            "precio": 78000,
            "precio_display": "$78.000",
            "badge": "OFERTA OBRA",
            "badge_color": "bg-amber-500/20 text-amber-300 border-amber-500/30",
            "btn_color": "from-amber-400 to-orange-400 text-slate-950",
            "stock_count": 12,
            "imagen_url": "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Juego de Bocallaves Stanley 108 Piezas Chrome Vanadium",
            "descripcion": "Crique 1/2' y 1/4' con tubos encastre milimétrico e insumos profesionales.",
            "precio": 120000,
            "precio_display": "$120.000",
            "badge": "PROFESIONAL",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "btn_color": "from-emerald-400 to-teal-400 text-slate-950",
            "stock_count": 4,
            "imagen_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80"
        }
    ],
    "opticas": [
        {
            "id": 1,
            "nombre": "Cristales Monofocales Blue Block Antirreflex",
            "descripcion": "Tratamiento de alta gama para protección contra luz azul de pantallas de PC y celulares.",
            "precio": 32000,
            "precio_display": "$32.000",
            "badge": "MÁS SOLICITADO",
            "badge_color": "bg-sky-500/20 text-sky-300 border-sky-500/30",
            "btn_color": "from-sky-400 to-blue-500 text-slate-950",
            "stock_count": 28,
            "imagen_url": "https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Armazón Acetato Ray-Ban Wayfarer Classic",
            "descripcion": "Diseño icónico con patillas flexibles y estuche rígido original.",
            "precio": 89000,
            "precio_display": "$89.000",
            "badge": "TENDENCIA",
            "badge_color": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
            "btn_color": "from-cyan-400 to-teal-400 text-slate-950",
            "stock_count": 5,
            "imagen_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Lentes de Contacto Acuvue Oasys (Caja 6u)",
            "descripcion": "Hidratación superior con tecnología Hydraclear Plus para uso prolongado.",
            "precio": 45000,
            "precio_display": "$45.000",
            "badge": "DISPONIBLE",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "btn_color": "from-emerald-400 to-teal-400 text-slate-950",
            "stock_count": 14,
            "imagen_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80"
        }
    ],
    "kiosco": [
        {
            "id": 1,
            "nombre": "Combo Previa XL: Fernet Branca + 2x Coca + Hielo",
            "descripcion": "Fernet 750ml helado + 2 Gaseosas 2.25L + Bolsa de hielo rolito 3kg.",
            "precio": 18500,
            "precio_display": "$18.500",
            "badge": "OFERTA PREVIA",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "btn_color": "from-emerald-400 to-teal-400 text-slate-950",
            "stock_count": 25,
            "imagen_url": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Pack Cerveza Corona 6u + Papas Lay's XL",
            "descripcion": "Porrón Corona 330ml congelado + Papas Fritas Corte Americano 140g.",
            "precio": 16400,
            "precio_display": "$16.400",
            "badge": "RECOMENDADO",
            "badge_color": "bg-amber-500/20 text-amber-300 border-amber-500/30",
            "btn_color": "from-amber-400 to-yellow-400 text-slate-950",
            "stock_count": 18,
            "imagen_url": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Caja Selección Chocolates Milka & Golosinas",
            "descripcion": "Mix de tabletas Milka, alfajores Havanna y gomitas premium.",
            "precio": 12500,
            "precio_display": "$12.500",
            "badge": "PROMO",
            "badge_color": "bg-pink-500/20 text-pink-300 border-pink-500/30",
            "btn_color": "from-pink-500 to-purple-400 text-white",
            "stock_count": 30,
            "imagen_url": "https://images.unsplash.com/photo-1588964895597-cfccd6e2dbf9?auto=format&fit=crop&w=800&q=80"
        }
    ],
    "deportes": [
        {
            "id": 1,
            "nombre": "Tubo de Pelotas Penn Tour Presurizadas (3u)",
            "descripcion": "Pelotas de fieltro sintético especial para máxima durabilidad en polvo de ladrillo.",
            "precio": 14000,
            "precio_display": "$14.000",
            "badge": "OFICIAL AAT",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "btn_color": "from-emerald-400 to-teal-400 text-slate-950",
            "stock_count": 36,
            "imagen_url": "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Encordado Luxilon Alu Power 1.25mm + Overgrip",
            "descripcion": "Calibración digital de tensión de acuerdo a tu estilo de juego + placement de overgrip Wilson.",
            "precio": 22500,
            "precio_display": "$22.500",
            "badge": "PRO SHOP",
            "badge_color": "bg-amber-500/20 text-amber-300 border-amber-500/30",
            "btn_color": "from-amber-400 to-orange-400 text-slate-950",
            "stock_count": 15,
            "imagen_url": "https://images.unsplash.com/photo-1554068865-24cecd4e34b8?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Raqueta Wilson Blade 98 V8 (Grip 3)",
            "descripcion": "Patrón de encordado 16x19 para jugadores competitivos buscando sensación y control absoluto.",
            "precio": 320000,
            "precio_display": "$320.000",
            "badge": "EDICIÓN PRO",
            "badge_color": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
            "btn_color": "from-cyan-400 to-blue-500 text-slate-950",
            "stock_count": 2,
            "imagen_url": "https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?auto=format&fit=crop&w=800&q=80"
        }
    ],
    "pilates_wellness": [
        {
            "id": 1,
            "nombre": "Pase Mensual Pilates Reformer (8 Clases)",
            "descripcion": "Entrenamiento en camas Reformer con atención personalizada en grupos reducidos.",
            "precio": 45000,
            "precio_display": "$45.000",
            "badge": "MÁS SOLICITADO",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "btn_color": "from-emerald-400 to-teal-400 text-slate-950",
            "stock_count": 25,
            "imagen_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Pase Libre Yoga Vinyasa & Meditación",
            "descripcion": "Acceso ilimitado a clases de postura, respiración consciente y bienestar integral.",
            "precio": 38000,
            "precio_display": "$38.000",
            "badge": "WELLNESS",
            "badge_color": "bg-teal-500/20 text-teal-300 border-teal-500/30",
            "btn_color": "from-teal-400 to-cyan-400 text-slate-950",
            "stock_count": 18,
            "imagen_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Mat de Yoga Eco-Friendly Antideslizante Pro",
            "descripcion": "Superficie de caucho natural 6mm con guías de alineación corporal lavables.",
            "precio": 22000,
            "precio_display": "$22.000",
            "badge": "ACCESORIO",
            "badge_color": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
            "btn_color": "from-cyan-400 to-blue-500 text-slate-950",
            "stock_count": 8,
            "imagen_url": "https://images.unsplash.com/photo-1545205597-3d9d02c29597?auto=format&fit=crop&w=800&q=80"
        }
    ],
    "salud": [
        {
            "id": 1,
            "nombre": "Consulta Médica General & Historia Clínica",
            "descripcion": "Evaluación clínica integral con seguimiento digital de historia de salud.",
            "precio": 25000,
            "precio_display": "$25.000",
            "badge": "ATENCIÓN MÉDICA",
            "badge_color": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
            "btn_color": "from-cyan-400 to-teal-400 text-slate-950",
            "stock_count": 30,
            "imagen_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Chequeo Preventivo Anual Salud Integral",
            "descripcion": "Análisis clínicos de laboratorio + Electrocardiograma de reposo e informe médico.",
            "precio": 48000,
            "precio_display": "$48.000",
            "badge": "PREVENCIÓN",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "btn_color": "from-emerald-400 to-teal-400 text-slate-950",
            "stock_count": 15,
            "imagen_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Estudio Diagnóstico por Imágenes HD",
            "descripcion": "Estudios de alta precisión con resultados digitales enviados a tu WhatsApp.",
            "precio": 38000,
            "precio_display": "$38.000",
            "badge": "DIAGNÓSTICO",
            "badge_color": "bg-blue-500/20 text-blue-300 border-blue-500/30",
            "btn_color": "from-blue-400 to-indigo-500 text-white",
            "stock_count": 20,
            "imagen_url": "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=800&q=80"
        }
    ],
    "retail": [
        {
            "id": 1,
            "nombre": "Producto Destacado Colección Premium",
            "descripcion": "Calidad garantizada directos de fábrica con entrega inmediata en el día.",
            "precio": 28500,
            "precio_display": "$28.500",
            "badge": "MÁS VENDIDO",
            "badge_color": "bg-pink-500/20 text-pink-300 border-pink-500/30",
            "btn_color": "from-pink-500 to-rose-500 text-slate-950",
            "stock_count": 42,
            "imagen_url": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Pack Solución Equipamiento Integral",
            "descripcion": "Combo completo diseñado para máxima eficiencia con envío gratis a domicilio.",
            "precio": 42000,
            "precio_display": "$42.000",
            "badge": "RECOMENDADO",
            "badge_color": "bg-purple-500/20 text-purple-300 border-purple-500/30",
            "btn_color": "from-purple-500 to-pink-500 text-white",
            "stock_count": 18,
            "imagen_url": "https://images.unsplash.com/photo-1556742049-0a674718036d?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Kit Accesorio & Mantenimiento Multiuso",
            "descripcion": "Componente esencial con garantía postventa extendida de 12 meses.",
            "precio": 19900,
            "precio_display": "$19.900",
            "badge": "PROMO",
            "badge_color": "bg-amber-500/20 text-amber-300 border-amber-500/30",
            "btn_color": "from-amber-400 to-orange-400 text-slate-950",
            "stock_count": 25,
            "imagen_url": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=800&q=80"
        }
    ],
    "inmobiliaria": [
        {
            "id": 1,
            "nombre": "Informe de Tasación Profesional & Mercado",
            "descripcion": "Valuación comercial auditada de inmuebles urbanos y comerciales.",
            "precio": 35000,
            "precio_display": "$35.000",
            "badge": "TASACIÓN",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "btn_color": "from-emerald-400 to-teal-400 text-slate-950",
            "stock_count": 10,
            "imagen_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Paquete Fotografía HD & Tour Virtual 360°",
            "descripcion": "Producción audiovisual profesional para potenciar la venta o alquiler de tu propiedad.",
            "precio": 65000,
            "precio_display": "$65.000",
            "badge": "RECOMENDADO",
            "badge_color": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
            "btn_color": "from-cyan-400 to-teal-400 text-slate-950",
            "stock_count": 15,
            "imagen_url": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Asesoramiento Jurídico & Gestión de Contratos",
            "descripcion": "Redacción de contratos de locación y revisión registral de títulos.",
            "precio": 40000,
            "precio_display": "$40.000",
            "badge": "SEGURIDAD",
            "badge_color": "bg-amber-500/20 text-amber-300 border-amber-500/30",
            "btn_color": "from-amber-400 to-orange-400 text-slate-950",
            "stock_count": 20,
            "imagen_url": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80"
        }
    ],
    "servicios": [
        {
            "id": 1,
            "nombre": "Servicio de Consultoría & Diagnóstico Operativo",
            "descripcion": "Revisión integral de procesos y plan de optimización comercial.",
            "precio": 85000,
            "precio_display": "$85.000",
            "badge": "MÁS SOLICITADO",
            "badge_color": "bg-blue-500/20 text-blue-300 border-blue-500/30",
            "btn_color": "from-blue-400 to-indigo-500 text-white",
            "stock_count": 10,
            "imagen_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Desarrollo & Implementación de Solución Técnica",
            "descripcion": "Ejecución a medida con cumplimiento estricto de metas y garantía de calidad.",
            "precio": 140000,
            "precio_display": "$140.000",
            "badge": "RECOMENDADO",
            "badge_color": "bg-purple-500/20 text-purple-300 border-purple-500/30",
            "btn_color": "from-purple-500 to-indigo-500 text-white",
            "stock_count": 8,
            "imagen_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Abono de Soporte & Mantenimiento Preventivo",
            "descripcion": "Asistencia continua de respuesta inmediata y supervisión periodica.",
            "precio": 45000,
            "precio_display": "$45.000",
            "badge": "MANTENIMIENTO",
            "badge_color": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
            "btn_color": "from-cyan-400 to-blue-400 text-slate-950",
            "stock_count": 15,
            "imagen_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80"
        }
    ],
    "general": [
        {
            "id": 1,
            "nombre": "Producto / Servicio Principal Destacado",
            "descripcion": "Solución de máxima calidad orientada a resolver las necesidades clave de tu negocio.",
            "precio": 25000,
            "precio_display": "$25.000",
            "badge": "DESTACADO",
            "badge_color": "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
            "btn_color": "from-indigo-500 to-purple-500 text-white",
            "stock_count": 30,
            "imagen_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "nombre": "Pack Solución Integral Personalizada",
            "descripcion": "Paquete estructurado con acompañamiento profesional y soporte directo.",
            "precio": 45000,
            "precio_display": "$45.000",
            "badge": "RECOMENDADO",
            "badge_color": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
            "btn_color": "from-cyan-400 to-teal-400 text-slate-950",
            "stock_count": 15,
            "imagen_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "nombre": "Servicio de Asesoría Directa & Diagnóstico",
            "descripcion": "Atención rápida por WhatsApp con respuesta en el día.",
            "precio": 18000,
            "precio_display": "$18.000",
            "badge": "CONSULTA",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "btn_color": "from-emerald-400 to-teal-400 text-slate-950",
            "stock_count": 25,
            "imagen_url": "https://images.unsplash.com/photo-1556742049-0a674718036d?auto=format&fit=crop&w=800&q=80"
        }
    ]
}


def generar_copy_negocio(nombre_negocio, rubro_key, dolor_principal=None, objetivo=None):
    """
    Genera titulares y propuestas de valor 100% enfocadas en vender el negocio del cliente
    a sus propios clientes finales, incorporando dolores u objetivos específicos si se proveen.
    """
    nombre = nombre_negocio.strip()
    
    if rubro_key == "pilates_wellness":
        headline = f"Pilates Reformer, Yoga & Cuidado Postural en {nombre}"
        subheadline = f"En {nombre} impulsamos tu crecimiento personal, salud y movilidad con clases en grupos reducidos, profesores certificados y equipamiento de última generación."
    elif rubro_key == "salud":
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
    elif rubro_key == "indumentaria":
        headline = f"Colecciones Exclusivas, Tendencia & Talles Reales en {nombre}"
        subheadline = f"En {nombre} combinamos diseño de autor, géneros seleccionados y envíos rápidos a todo el país. Conocé nuestro catálogo y consultá por WhatsApp."
    elif rubro_key in ["deportes", "tenis", "club"]:
        headline = f"Reserva de Canchas de Tenis, Clases & Pro Shop en {nombre}"
        subheadline = f"En {nombre} disfrutás del mejor tenis: canchas de polvo de ladrillo en excelente estado, clases con profesores matriculados y encordado profesional de raquetas."
    elif rubro_key in ["hostel", "hoteleria", "turismo"]:
        headline = f"Reserva de Camas, Habitaciones & Experiencias en {nombre}"
        subheadline = f"En {nombre} disfrutás del mejor ambiente viajero: instalaciones modernas, lockers individuales, zonas comunes de trabajo y la ubicación ideal para tu estadía."
    elif rubro_key == "servicios":
        headline = f"Soluciones Profesionales a Medida & Asesoramiento Técnico en {nombre}"
        subheadline = f"En {nombre} transformamos tus requerimientos en resultados concretos con la máxima precisión, calidad y cumplimiento de plazos."
    else:
        headline = f"Calidad, Compromiso & Atención de Excelencia en {nombre}"
        subheadline = f"En {nombre} brindamos soluciones integrales adaptadas a cada cliente, garantizando la máxima eficiencia y satisfacción."

    dolor_clean = (dolor_principal or "").strip()
    obj_clean = (objetivo or "").strip()

    if obj_clean:
        obj_fmt = obj_clean.rstrip(".")
        obj_title = obj_fmt[0].upper() + obj_fmt[1:] if len(obj_fmt) > 0 else obj_fmt
        headline = f"Solución Digital en {nombre}: {obj_title}"

    if dolor_clean:
        dolor_fmt = dolor_clean.rstrip(".")
        subheadline += f" Solucionamos de raíz: {dolor_fmt}."

    return headline, subheadline


def preparar_contexto_demo(demo_obj, template_override=None, modo_cliente=False, lang="es") -> dict:
    """
    Toma una instancia de DemoSolution de la BD y genera el diccionario de contexto
    completo para renderizar `templates/demos/preview.html`.
    """
    rubro_key = (demo_obj.rubro or "general").lower()
    if rubro_key not in THEMES_MAP:
        rubro_key = "general"

    # Obtener traducciones i18n según el idioma solicitado
    i18n_ctx = get_i18n_context(lang, rubro_key, demo_obj.nombre_negocio)

    # Determinar plantilla de diseño activa
    raw_template = template_override or getattr(demo_obj, "diseno_template", "classic") or "classic"
    diseno_template = str(raw_template).lower().strip()
    if diseno_template not in ["classic", "horizontal-scroll", "layered-reveal"]:
        diseno_template = "classic"

    templates_disponibles = [
        {"id": "classic", "nombre": "Classic Glassmorphism", "icon": "fa-gem", "badge": "Predeterminado"},
        {"id": "horizontal-scroll", "nombre": "Horizontal Scroll Editorial", "icon": "fa-newspaper", "badge": "Luxury Editorial"},
        {"id": "layered-reveal", "nombre": "Layered Reveal Narrative", "icon": "fa-layer-group", "badge": "Depth Parallax"}
    ]

    theme = THEMES_MAP[rubro_key]
    
    # Procesar lista de módulos activos (múltiples módulos)
    modulos_activos = []
    if demo_obj.modulos_json:
        try:
            modulos_activos = json.loads(demo_obj.modulos_json)
        except Exception:
            modulos_activos = []

    if not modulos_activos:
        modulos_activos = [(demo_obj.modulo_solucion or "agenda").lower()]

    # Garantizar que los módulos sean válidos y únicos manteniendo orden
    validos = ["agenda", "hostel", "stock", "ecommerce", "cotizador", "logistica", "decisiones", "metricas"]
    modulos_activos_filtrados = []
    for m in modulos_activos:
        m_lower = str(m).lower()
        if m_lower in validos and m_lower not in modulos_activos_filtrados:
            modulos_activos_filtrados.append(m_lower)
    # Forzar el módulo 'hostel' como principal si el rubro o slug es de hostel/hotelería
    es_rubro_hostel = rubro_key in ["hostel", "hoteleria", "turismo"] or "hostel" in (demo_obj.rubro or "").lower() or "hostel" in (demo_obj.slug or "").lower()
    if es_rubro_hostel:
        if "hostel" in modulos_activos_filtrados:
            modulos_activos_filtrados.remove("hostel")
        modulos_activos_filtrados.insert(0, "hostel")

    if not modulos_activos_filtrados:
        modulos_activos_filtrados = ["hostel" if es_rubro_hostel else "agenda"]

    print(f"[DEMO ENGINE DEBUG] Slug: {demo_obj.slug} | Rubro: {demo_obj.rubro} | Modulos Json: {demo_obj.modulos_json} | Modulo Solucion: {demo_obj.modulo_solucion} | Filtrados: {modulos_activos_filtrados}", flush=True)

    MODULOS_NOMBRES_ICONOS = {
        "agenda": {"nombre": "Agenda & Reservas", "icon": "fa-calendar-check"},
        "hostel": {"nombre": "Reserva de Camas & Estadías", "icon": "fa-bed"},
        "stock": {"nombre": "Catálogo & Stock", "icon": "fa-boxes-stacked"},
        "ecommerce": {"nombre": "E-Commerce / Carta", "icon": "fa-cart-shopping"},
        "cotizador": {"nombre": "Cotizador B2B", "icon": "fa-calculator"},
        "logistica": {"nombre": "Logística & Envíos", "icon": "fa-truck-fast"},
        "decisiones": {"nombre": "Agente de Decisiones", "icon": "fa-robot"},
        "metricas": {"nombre": "Métricas de Eficiencia", "icon": "fa-chart-line"}
    }

    modulos_info_list = []
    i18n_dic = i18n_ctx.get("i18n", {})
    lang_code = i18n_ctx.get("lang", "es")

    for m_key in modulos_activos_filtrados:
        info = dict(MODULOS_TITULOS.get(m_key, MODULOS_TITULOS["agenda"]))
        meta = MODULOS_NOMBRES_ICONOS.get(m_key, {"nombre": m_key.title(), "icon": "fa-cube"})
        info["key"] = m_key
        info["id"] = m_key
        info["nombre"] = meta["nombre"]
        info["icon"] = meta["icon"]
        info["template"] = f"demos/components/{m_key}.html"

        if lang_code != "es":
            if f"{m_key}_titulo" in i18n_dic:
                info["titulo"] = i18n_dic[f"{m_key}_titulo"]
            if f"{m_key}_subtitulo" in i18n_dic:
                info["subtitulo"] = i18n_dic[f"{m_key}_subtitulo"]
            if f"{m_key}_badge" in i18n_dic:
                info["badge"] = i18n_dic[f"{m_key}_badge"]

        modulos_info_list.append(info)

    modulo_key = modulos_activos_filtrados[0]
    modulo_info = dict(MODULOS_TITULOS.get(modulo_key, MODULOS_TITULOS["agenda"]))
    meta_main = MODULOS_NOMBRES_ICONOS.get(modulo_key, {"nombre": modulo_key.title(), "icon": "fa-cube"})
    modulo_info["key"] = modulo_key
    modulo_info["id"] = modulo_key
    modulo_info["nombre"] = meta_main["nombre"]
    modulo_info["icon"] = meta_main["icon"]
    modulo_info["template"] = f"demos/components/{modulo_key}.html"

    if lang_code != "es":
        if f"{modulo_key}_titulo" in i18n_dic:
            modulo_info["titulo"] = i18n_dic[f"{modulo_key}_titulo"]
        if f"{modulo_key}_subtitulo" in i18n_dic:
            modulo_info["subtitulo"] = i18n_dic[f"{modulo_key}_subtitulo"]
        if f"{modulo_key}_badge" in i18n_dic:
            modulo_info["badge"] = i18n_dic[f"{modulo_key}_badge"]

    # Generar titulares enfocados 100% en el negocio del cliente e incorporando dolores y objetivos
    dolor_principal = getattr(demo_obj, "dolor_principal", "") or ""
    objetivo = getattr(demo_obj, "objetivo", "") or ""
    hero_headline, hero_subheadline = generar_copy_negocio(
        demo_obj.nombre_negocio,
        rubro_key,
        dolor_principal=dolor_principal,
        objetivo=objetivo
    )

    if i18n_ctx.get("headline_tr") and not objetivo:
        hero_headline = i18n_ctx["headline_tr"]
    if i18n_ctx.get("subheadline_tr") and not dolor_principal:
        hero_subheadline = i18n_ctx["subheadline_tr"]

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

    # Traducir los pilares si el idioma es distinto a español
    pilares_enriquecidos = translate_pilares(pilares_enriquecidos, lang=lang_code, rubro=rubro_key)

    # Parsear reseñas de JSON y ordenar de mejor a peor (5★ a 1★)
    reviews = []
    if demo_obj.reviews_json:
        try:
            reviews = json.loads(demo_obj.reviews_json)
        except Exception:
            reviews = []

    if not reviews:
        if lang_code == "en":
            reviews = [
                {"author_name": "Gabriel M.", "rating": 5, "text": f"Best service at {demo_obj.nombre_negocio}. Highly satisfied with the quality and quick attention.", "relative_time": "1 week ago"},
                {"author_name": "Anna S.", "rating": 5, "text": f"Fast, neat and highly recommended. Excellent experience at {demo_obj.nombre_negocio}.", "relative_time": "1 month ago"},
                {"author_name": "Mark R.", "rating": 5, "text": f"Flawless service and instant response. Will definitely come back to {demo_obj.nombre_negocio}.", "relative_time": "2 weeks ago"}
            ]
        elif lang_code == "pt":
            reviews = [
                {"author_name": "Gabriel M.", "rating": 5, "text": f"O melhor atendimento em {demo_obj.nombre_negocio}. Muito satisfeito com a qualidade e rapidez.", "relative_time": "há 1 semana"},
                {"author_name": "Ana Clara S.", "rating": 5, "text": f"Rápidos, eficientes e super recomendáveis. Excelente experiência em {demo_obj.nombre_negocio}.", "relative_time": "há 1 mês"},
                {"author_name": "Marcos Rossi", "rating": 5, "text": f"Atendimento impecável e resposta imediata. Voltarei com certeza a {demo_obj.nombre_negocio}.", "relative_time": "há 2 semanas"}
            ]
        elif lang_code == "it":
            reviews = [
                {"author_name": "Gabriele M.", "rating": 5, "text": f"Il miglior servizio a {demo_obj.nombre_negocio}. Molto soddisfatto per la qualità e la velocità.", "relative_time": "1 settimana fa"},
                {"author_name": "Anna Chiara S.", "rating": 5, "text": f"Veloci, precisi e super consigliati. Eccellente esperienza a {demo_obj.nombre_negocio}.", "relative_time": "1 mese fa"},
                {"author_name": "Marco Rossi", "rating": 5, "text": f"Servizio impeccabile e risposta immediata. Tornerò sicuramente a {demo_obj.nombre_negocio}.", "relative_time": "2 settimane fa"}
            ]
        else:
            reviews = [
                {"author_name": "Gabriel M.", "rating": 5, "text": f"La mejor atención en {demo_obj.nombre_negocio}. Muy satisfecho con el servicio y la rapidez.", "relative_time": "hace 1 semana"},
                {"author_name": "Ana Clara S.", "rating": 5, "text": f"Rápidos, prolijos y súper recomendables. Excelente experiencia en {demo_obj.nombre_negocio}.", "relative_time": "hace un mes"},
                {"author_name": "Marcos Rossi", "rating": 5, "text": f"Atención impecable y respuesta inmediata. Volveré sin dudas a {demo_obj.nombre_negocio}.", "relative_time": "hace 2 semanas"}
            ]

    # Ordenar reseñas de mejor a peor (5 estrellas primero) y filtrar valoraciones bajas < 4
    reviews = [r for r in reviews if int(r.get("rating", 5)) >= 4]
    reviews.sort(key=lambda r: (int(r.get("rating", 5)), len(r.get("text", ""))), reverse=True)

    # Configuración adaptada de la Agenda por Rubro
    agenda_config = AGENDA_CONFIG_POR_RUBRO.get(rubro_key, AGENDA_CONFIG_POR_RUBRO["general"])

    # Parsear fotos reales de Google Places si existen
    fotos = []
    if demo_obj.fotos_json:
        try:
            fotos = json.loads(demo_obj.fotos_json)
        except Exception:
            fotos = []

    # Seleccionar la imagen Hero HD (Priorizando foto real de Google Places del negocio si existe)
    if fotos and len(fotos) > 0 and fotos[0]:
        hero_bg_url = fotos[0]
        hero_meta = {"url": fotos[0], "hd": True, "source": "Google Places Real Photo"}
    else:
        hero_meta = seleccionar_hero_inteligente(rubro_key, demo_obj.nombre_negocio)
        hero_bg_url = hero_meta["url"]

    # Asignar Hero HD y aplicar Overrides de Colores Personalizados al Tema
    theme_copy = dict(theme)
    theme_copy["hero_bg_image"] = hero_bg_url
    theme_copy["hero_meta"] = hero_meta

    if demo_obj.color_primario:
        theme_copy["accent"] = demo_obj.color_primario
    if demo_obj.color_header:
        theme_copy["header_bg"] = demo_obj.color_header

    # Formatear WhatsApp
    wa_clean = re.sub(r"\D", "", demo_obj.whatsapp or demo_obj.telefono or "5493515550199")

    # Mensaje predeterminado de consulta para el botón de la demo (del cliente final al negocio)
    msg_wa = f"Hola {demo_obj.nombre_negocio}, quisiera consultar por sus productos y servicios."
    wa_link = f"https://wa.me/{wa_clean}?text={urllib.parse.quote(msg_wa)}"

    # Link directo de WhatsApp para el equipo de GG Solutions (en el Dock Superior)
    msg_gg = f"Hola GG Solutions, estuve revisando la demo creada para {demo_obj.nombre_negocio} y quisiera consultar para implementar nuestro sistema."
    wa_ggsolutions = f"https://wa.me/5493513360533?text={urllib.parse.quote(msg_gg)}"

    # Configuración del Panel de Control Interno por Rubro
    admin_config = ADMIN_PANEL_POR_RUBRO.get(rubro_key, ADMIN_PANEL_POR_RUBRO["general"])

    # Construir banco de imágenes de capas (Layered Reveal & Sections) SIN REPETICIONES
    # Priorizando fotos reales subidas por clientes o el negocio en Google Places
    layer_images_unicas = []
    if fotos:
        for f_url in fotos:
            if f_url and f_url not in layer_images_unicas:
                layer_images_unicas.append(f_url)

    # Rellenar con imágenes HD únicas del banco de imágenes del rubro
    for img_candidate in img_data.get("layer_images", []):
        if len(layer_images_unicas) >= 5:
            break
        if img_candidate and img_candidate not in layer_images_unicas:
            layer_images_unicas.append(img_candidate)

    # Si por alguna razón faltan imágenes para llegar a 5 sin repetir, usar pool global diversificado
    pool_reserva = [
        "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1599447421416-3414500d18a5?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1545205597-3d9d02c29597?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=1200&q=80"
    ]
    for fb in pool_reserva:
        if len(layer_images_unicas) >= 5:
            break
        if fb not in layer_images_unicas:
            layer_images_unicas.append(fb)

    final_layer_images = layer_images_unicas[:5]

    # --- LÓGICA DE CATÁLOGO DE PRODUCTOS Y DOBLE RUBRO ---
    rubro_secundario_key = (getattr(demo_obj, "rubro_secundario", "") or "").lower().strip()
    if rubro_secundario_key and rubro_secundario_key not in THEMES_MAP:
        rubro_secundario_key = None

    # Obtener catálogo base del rubro principal
    prods_primario = [dict(p) for p in PRODUCTOS_POR_RUBRO.get(rubro_key, PRODUCTOS_POR_RUBRO["general"])]

    if rubro_secundario_key:
        prods_secundario = [dict(p) for p in PRODUCTOS_POR_RUBRO.get(rubro_secundario_key, [])]
        # Mezclar productos: 2 del primario + 1 o 2 del secundario
        productos_combinados = prods_primario[:2] + prods_secundario[:2]

        # Fusionar pilares visuales si hay rubro secundario
        theme_sec = THEMES_MAP[rubro_secundario_key]
        if len(pilares_enriquecidos) >= 4 and len(theme_sec["pilares"]) >= 2:
            p_sec_1 = dict(theme_sec["pilares"][0])
            p_sec_1["image"] = theme_sec["hero_bg_image"]
            p_sec_2 = dict(theme_sec["pilares"][1])
            p_sec_2["image"] = theme_sec["hero_bg_image"]
            pilares_enriquecidos[2] = p_sec_1
            pilares_enriquecidos[3] = p_sec_2
    else:
        productos_combinados = prods_primario

    productos_catalogo = productos_combinados

    return {
        "demo": demo_obj,
        "lang": i18n_ctx["lang"],
        "i18n": i18n_ctx["i18n"],
        "modo_cliente": modo_cliente,
        "mostrar_novedades": bool(getattr(demo_obj, "mostrar_novedades", False)),
        "theme": theme_copy,
        "diseno_template": diseno_template,
        "templates_disponibles": templates_disponibles,
        "pilares": pilares_enriquecidos,
        "news": img_data.get("news", []),
        "layer_images": final_layer_images,
        "modulo_info": modulo_info,
        "modulos_activos": modulos_activos_filtrados,
        "modulos_info_list": modulos_info_list,
        "agenda_config": agenda_config,
        "hostel_config": HOSTEL_CONFIG,
        "admin_config": admin_config,
        "hero_headline": hero_headline,
        "hero_subheadline": hero_subheadline,
        "hero_meta": hero_meta,
        "reviews": reviews,
        "fotos": fotos,
        "productos_catalogo": productos_catalogo,
        "rubro_secundario_key": rubro_secundario_key,
        "wa_link": wa_link,
        "wa_ggsolutions": wa_ggsolutions,
        "maps_embed_query": urllib.parse.quote(f"{demo_obj.nombre_negocio}, {demo_obj.direccion or demo_obj.ciudad or 'Córdoba'}")
    }

