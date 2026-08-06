"""
Motor de Banco de Imágenes Semánticas HD para GG Solutions.
Garantiza imágenes de altísima definición (Unsplash HD curadas) mapeadas semánticamente
por rubro para tarjetería 16:9, héroes y novedades del sector.
"""

IMAGE_BANK_POR_RUBRO = {
    "salud": {
        "hero": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1400&q=85",
        "pilares": [
            "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=800&q=80"
        ],
        "news": [
            {
                "title": "Nuevas Tecnologías en Diagnóstico de Alta Precisión",
                "date": "Última Actualización",
                "snippet": "Incorporamos escáneres e imagenología avanzada para diagnósticos sin esperas.",
                "read_time": "3 min",
                "image": "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Protocolo de Atención Segura & Turnos Digitales",
                "date": "Guía Médica",
                "snippet": "Descubrí cómo el agendamiento online agiliza tu consulta médica.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Cuidado Preventivo & Recomendaciones de Salud",
                "date": "Prevención",
                "snippet": "Chequeos anuales y hábitos clave recomendados por nuestro cuerpo médico.",
                "read_time": "4 min",
                "image": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "automotriz": {
        "hero": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=1400&q=85",
        "pilares": [
            "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1530046339160-ce3e530c7d2f?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1517524008697-84bbe3c3fd98?auto=format&fit=crop&w=800&q=80"
        ],
        "news": [
            {
                "title": "Importancia del Diagnóstico Escaneado Preventivo",
                "date": "Mecánica Avanzada",
                "snippet": "Prevenir fallas complejas escaneando los módulos electrónicos de tu vehículo a tiempo.",
                "read_time": "3 min",
                "image": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Guía de Mantenimiento de Frenos & Tren Delantero",
                "date": "Seguridad Vial",
                "snippet": "Signos de desgaste que indican la necesidad de reemplazar pastillas y amortiguadores.",
                "read_time": "4 min",
                "image": "https://images.unsplash.com/photo-1530046339160-ce3e530c7d2f?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Equipamiento Computarizado de Última Generación",
                "date": "Innovación",
                "snippet": "Taller equipado con tecnología multimarca para un diagnóstico certero.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "gastronomia": {
        "hero": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1400&q=85",
        "pilares": [
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1526367790999-0150786686a2?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80"
        ],
        "news": [
            {
                "title": "Lanzamiento de nuestra Carta de Autor de Estación",
                "date": "Gastronomía",
                "snippet": "Nuevas preparaciones exclusivas y maridaje sugerido por nuestro chef ejecutivo.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Selección de Ingredientes de Productores Locales",
                "date": "Calidad Certificada",
                "snippet": "Conocé nuestro estándar de frescura e insumos orgánicos de primera calidad.",
                "read_time": "3 min",
                "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Experiencia de Reservas Online & Menú Digital",
                "date": "Servicios",
                "snippet": "Agendá tu mesa o realizá tu pedido directamente por WhatsApp en 3 simples pasos.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "retail": {
        "hero": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1400&q=85",
        "pilares": [
            "https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1556742049-0a674718036d?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1534452203293-494d7ddbf7e0?auto=format&fit=crop&w=800&q=80"
        ],
        "news": [
            {
                "title": "Novedades en Catálogo & Tendencias de Temporada",
                "date": "Colección Exclusiva",
                "snippet": "Descubrí los últimos lanzamientos con disponibilidad inmediata y promociones.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Envíos Express & Compras Digitales en el Día",
                "date": "Logística",
                "snippet": "Despachos rápidos y atención directa por WhatsApp para coordinar la entrega.",
                "read_time": "3 min",
                "image": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Beneficios Exclusivos & Opciones de Pago",
                "date": "Promociones",
                "snippet": "Cuotas sin interés, transferencias directas y atención personalizada.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1556742049-0a674718036d?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "inmobiliaria": {
        "hero": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1400&q=85",
        "pilares": [
            "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80"
        ],
        "news": [
            {
                "title": "Oportunidades de Inversión Inmobiliaria en la Zona",
                "date": "Mercado Inmobiliario",
                "snippet": "Propiedades seleccionadas con alto retorno de inversión y documentación al día.",
                "read_time": "3 min",
                "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Tours Virtuales HD & Asesoramiento Legal",
                "date": "Servicios",
                "snippet": "Explorá cada propiedad con fotos en alta resolución antes de coordinar tu visita.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Guía para Comprar o Alquilar tu Próximo Hogar",
                "date": "Consejos",
                "snippet": "Paso a paso para concretar tu operación con máxima transparencia y rapidez.",
                "read_time": "4 min",
                "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "servicios": {
        "hero": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1400&q=85",
        "pilares": [
            "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80"
        ],
        "news": [
            {
                "title": "Optimizá tus Procesos Operativos con Soluciones a Medida",
                "date": "Eficiencia",
                "snippet": "Estandarización de servicios y garantía de calidad en cada entregable.",
                "read_time": "3 min",
                "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Cotizaciones Digitales & Presupuestos al Instante",
                "date": "Innovación",
                "snippet": "Consultá los costos estimados de tu requerimiento sin demoras.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Atención Directa & Seguimiento de Proyectos",
                "date": "Calidad",
                "snippet": "Canales abiertos de comunicación para resolver consultas en tiempo real.",
                "read_time": "3 min",
                "image": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "general": {
        "hero": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1400&q=85",
        "pilares": [
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80"
        ],
        "news": [
            {
                "title": "Compromiso de Satisfacción & Atención de Excelencia",
                "date": "Calidad",
                "snippet": "Procesos diseñados para brindar la mejor experiencia en cada consulta.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Respuestas Inmediatas por WhatsApp y Canales Digitales",
                "date": "Atención 24/7",
                "snippet": "Coordiná tu servicio de forma rápida y sin complicaciones.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Equipo Capacitado & Soluciones Profesionales",
                "date": "Garantía",
                "snippet": "Respaldo directo en cada trabajo contratado por nuestros clientes.",
                "read_time": "3 min",
                "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80"
            }
        ]
    }
}

def obtener_imagenes_rubro(rubro_key: str) -> dict:
    """Devuelve las imágenes semánticas correspondientes al rubro."""
    key = (rubro_key or "general").lower()
    return IMAGE_BANK_POR_RUBRO.get(key, IMAGE_BANK_POR_RUBRO["general"])
