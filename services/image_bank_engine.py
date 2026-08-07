"""
Motor de Banco de Imágenes Semánticas HD para GG Solutions Studio.
Garantiza imágenes de altísima definición (Unsplash HD 1600px+ curadas) mapeadas,
etiquetadas y catalogadas por rubro para encabezados Hero, pilares 16:9 y novedades del sector.
"""

import os

HERO_BANK_POR_RUBRO = {
    "gastronomia": [
        {
            "tag": "smash_burger",
            "label": "Hamburguesería & Fast Food Premium",
            "url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "gourmet",
            "label": "Restaurante Gourmet & Salón de Autor",
            "url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "bakery_cafe",
            "label": "Cafetería de Especialidad & Pastelería",
            "url": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=1600&q=90"
        }
    ],
    "automotriz": [
        {
            "tag": "mecanica_general",
            "label": "Taller Mecánico & Elevadores",
            "url": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "lubricentro",
            "label": "Service & Escaneo Computarizado OBD2",
            "url": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=1600&q=90"
        }
    ],
    "herramientas": [
        {
            "tag": "herramientas_electricas",
            "label": "Herramientas Inalámbricas & Taller",
            "url": "https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "ferreteria_industrial",
            "label": "Insumos Industriales & Obras",
            "url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1600&q=90"
        }
    ],
    "opticas": [
        {
            "tag": "optica_boutique",
            "label": "Armazones de Diseño & Colección",
            "url": "https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "examen_optometrico",
            "label": "Gabinete de Examen & Salud Visual",
            "url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "lentes_sol",
            "label": "Colección Lentes de Sol UV400",
            "url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=1600&q=90"
        }
    ],
    "kiosco": [
        {
            "tag": "minimarket_express",
            "label": "Minimarket 24hs & Góndolas",
            "url": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "bebidas_combos",
            "label": "Bebidas Frías & Combos para Previas",
            "url": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "almacen_cercania",
            "label": "Almacén de Cercanía & Productos Frescos",
            "url": "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "golosinas_snacks",
            "label": "Snacks, Chocolates & Golosinas XL",
            "url": "https://images.unsplash.com/photo-1588964895597-cfccd6e2dbf9?auto=format&fit=crop&w=1600&q=90"
        }
    ],
    "deportes": [
        {
            "tag": "canchas_tenis",
            "label": "Complejo de Tenis & Canchas Polvo de Ladrillo",
            "url": "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "academia_tenis",
            "label": "Academia de Tenis & Clases Particulares",
            "url": "https://images.unsplash.com/photo-1554068865-24cecd4e34b8?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "canchas_nocturnas",
            "label": "Canchas de Tenis Iluminadas & Club",
            "url": "https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?auto=format&fit=crop&w=1600&q=90"
        }
    ],
    "salud": [
        {
            "tag": "clinica_medica",
            "label": "Centro Médico & Consultorios",
            "url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "odontologia",
            "label": "Centro Odontológico & Estética",
            "url": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "diagnostico_lab",
            "label": "Laboratorio & Diagnóstico",
            "url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1600&q=90"
        }
    ],
    "retail": [
        {
            "tag": "boutique_moda",
            "label": "Boutique de Ropa & Indumentaria",
            "url": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "showroom_decoracion",
            "label": "Showroom de Muebles & Decoración",
            "url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "tecnologia_gadgets",
            "label": "Tecnología, Celulares & Gadgets",
            "url": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1600&q=90"
        }
    ],
    "inmobiliaria": [
        {
            "tag": "casas_modernas",
            "label": "Casas de Arquitectura Moderna",
            "url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "departamentos_lujo",
            "label": "Torres & Departamentos de Lujo",
            "url": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1600&q=90"
        }
    ],
    "servicios": [
        {
            "tag": "oficina_moderna",
            "label": "Oficina & Estudio Profesional",
            "url": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "tag": "asesoramiento_tecnico",
            "label": "Consultoría & Desarrollo Técnico",
            "url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1600&q=90"
        }
    ],
    "general": [
        {
            "tag": "equipo_profesional",
            "label": "Equipo Profesional & Instalaciones",
            "url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1600&q=90"
        }
    ]
}


IMAGE_BANK_POR_RUBRO = {
    "salud": {
        "hero": HERO_BANK_POR_RUBRO["salud"][0]["url"],
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
    "deportes": {
        "hero": HERO_BANK_POR_RUBRO["deportes"][0]["url"],
        "pilares": [
            "/static/img/bank/deportes/pilar_1.jpg",
            "/static/img/bank/deportes/pilar_2.jpg",
            "/static/img/bank/deportes/pilar_3.jpg",
            "/static/img/bank/deportes/pilar_4.jpg"
        ],
        "news": [
            {
                "title": "Técnicas de Saque & Control de Tensión en Raquetas",
                "date": "Tenis & Rendimiento",
                "snippet": "Optimizá tu potencia y precisión ajustando el encordado y la tensión a tu estilo de juego.",
                "read_time": "3 min",
                "image": "/static/img/bank/deportes/pilar_2.jpg"
            },
            {
                "title": "Mantenimiento de Canchas de Polvo de Ladrillo",
                "date": "Infraestructura Club",
                "snippet": "Riego, cepillado y nivelación diaria para garantizar el mejor pique de la pelota.",
                "read_time": "4 min",
                "image": "/static/img/bank/deportes/pilar_1.jpg"
            },
            {
                "title": "Torneos Internos & Ranking de Socios 2026",
                "date": "Competencias",
                "snippet": "Inscripciones abiertas para el Torneo Abierto de Singles y Dobles de Otoño.",
                "read_time": "2 min",
                "image": "/static/img/bank/deportes/pilar_3.jpg"
            }
        ]
    },
    "automotriz": {
        "hero": HERO_BANK_POR_RUBRO["automotriz"][0]["url"],
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
        "hero": HERO_BANK_POR_RUBRO["gastronomia"][0]["url"],
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
    "herramientas": {
        "hero": HERO_BANK_POR_RUBRO["herramientas"][0]["url"],
        "pilares": [
            "https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1581092335397-9583fe92d232?auto=format&fit=crop&w=800&q=80"
        ],
        "news": [
            {
                "title": "Nuevas Herramientas Inalámbricas Brushless para Profesionales",
                "date": "Lanzamiento",
                "snippet": "Mayor autonomía y potencia en trabajos de obra e industria pesada.",
                "read_time": "3 min",
                "image": "https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Presupuestos de Materiales para Gremios & Obras",
                "date": "Venta B2B",
                "snippet": "Cotizá listas de insumos con descuentos especiales por volumen en el día.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Guía de Seguridad & Mantenimiento de Maquinaria",
                "date": "Capacitación",
                "snippet": "Recomendaciones para prolongar la vida útil de tus equipos de corte y perforación.",
                "read_time": "4 min",
                "image": "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "opticas": {
        "hero": HERO_BANK_POR_RUBRO["opticas"][0]["url"],
        "pilares": [
            "https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1577803645773-f96470509666?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=800&q=80"
        ],
        "news": [
            {
                "title": "Protección de Filtro Azul (Blue Block) para Pantallas",
                "date": "Salud Visual",
                "snippet": "Evitá la fatiga ocular y dolores de cabeza protegiendo tu vista frente a monitores.",
                "read_time": "3 min",
                "image": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Nuevas Colecciones de Sol & Armazones de Diseño",
                "date": "Tendencias",
                "snippet": "Conocé las últimas novedades en materiales livianos y protección UV400.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Agendamiento Online de Examen Optométrico",
                "date": "Turnos",
                "snippet": "Reservá tu control visual con nuestros optómetras matriculados sin esperas.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1577803645773-f96470509666?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "kiosco": {
        "hero": HERO_BANK_POR_RUBRO["kiosco"][0]["url"],
        "pilares": [
            "https://images.unsplash.com/photo-1578916171728-46686eac8d58?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1588964895597-cfccd6e2dbf9?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?auto=format&fit=crop&w=800&q=80"
        ],
        "news": [
            {
                "title": "Combos para Previas & Promociones de Bebidas",
                "date": "Ofertas Express",
                "snippet": "Llevate tus bebidas frías y snacks con descuentos especiales de fin de semana.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Pedidos por WhatsApp & Retiro Inmediato Sin Filas",
                "date": "Servicios",
                "snippet": "Armá tu pedido desde el celular y pasá a buscarlo listo por el mostrador.",
                "read_time": "1 min",
                "image": "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Stock Permanente de Golosinas, Almacén y Varios",
                "date": "Cercanía",
                "snippet": "Encontrá tus marcas favoritas con la atención rápida y amigable de siempre.",
                "read_time": "2 min",
                "image": "https://images.unsplash.com/photo-1588964895597-cfccd6e2dbf9?auto=format&fit=crop&w=800&q=80"
            }
        ]
    },
    "retail": {
        "hero": HERO_BANK_POR_RUBRO["retail"][0]["url"],
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
        "hero": HERO_BANK_POR_RUBRO["inmobiliaria"][0]["url"],
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
        "hero": HERO_BANK_POR_RUBRO["servicios"][0]["url"],
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
        "hero": HERO_BANK_POR_RUBRO["general"][0]["url"],
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


def resolver_url_imagen(local_rel_path: str, remote_url: str) -> str:
    """
    Comprueba si existe el archivo estático local en /static/img/bank/...
    Si existe, devuelve la ruta local /static/img/bank/... para carga ultra-rápida.
    Si no existe, devuelve la URL remota de alta definición de Unsplash.
    """
    abs_path = os.path.join(os.path.dirname(__file__), "..", local_rel_path.lstrip("/"))
    if os.path.exists(abs_path):
        return local_rel_path
    return remote_url


def obtener_imagenes_rubro(rubro_key: str) -> dict:
    """Devuelve las imágenes semánticas correspondientes al rubro con resolución local/remota."""
    key = (rubro_key or "general").lower()
    raw_data = IMAGE_BANK_POR_RUBRO.get(key, IMAGE_BANK_POR_RUBRO["general"])
    
    # Resolver rutas de pilares locales si están presentes
    pilares_resueltos = []
    for idx, p_url in enumerate(raw_data.get("pilares", [])):
        local_path = f"/static/img/bank/{key}/pilar_{idx + 1}.jpg"
        pilares_resueltos.append(resolver_url_imagen(local_path, p_url))

    hero_local = f"/static/img/bank/{key}/hero_1.jpg"
    hero_resuelto = resolver_url_imagen(hero_local, raw_data.get("hero", ""))

    res_data = dict(raw_data)
    res_data["hero"] = hero_resuelto
    res_data["pilares"] = pilares_resueltos
    return res_data


def seleccionar_hero_inteligente(rubro_key: str, nombre_negocio: str = "") -> dict:
    """
    Selecciona la imagen Hero de alta definición (1600px+) más precisa según las palabras
    clave del nombre del negocio y su rubro.
    """
    key = (rubro_key or "general").lower()
    heroes = HERO_BANK_POR_RUBRO.get(key, HERO_BANK_POR_RUBRO["general"])
    nombre_lower = (nombre_negocio or "").lower()

    selected_hero = heroes[0]

    # Búsqueda semántica por palabras clave en el nombre del negocio
    if "burger" in nombre_lower or "hamburgues" in nombre_lower or "smash" in nombre_lower:
        for h in heroes:
            if h["tag"] == "smash_burger":
                selected_hero = h
                break
    elif "caf" in nombre_lower or "pasteler" in nombre_lower or "bakery" in nombre_lower:
        for h in heroes:
            if h["tag"] == "bakery_cafe":
                selected_hero = h
                break
    elif "bar" in nombre_lower or "birra" in nombre_lower or "coctel" in nombre_lower:
        for h in heroes:
            if h["tag"] == "bar_cocktails":
                selected_hero = h
                break
    elif "lubri" in nombre_lower or "aceite" in nombre_lower or "service" in nombre_lower:
        for h in heroes:
            if h["tag"] == "lubricentro":
                selected_hero = h
                break
    elif "repuesto" in nombre_lower or "freno" in nombre_lower:
        for h in heroes:
            if h["tag"] == "repuestos":
                selected_hero = h
                break
    elif "detail" in nombre_lower or "lavad" in nombre_lower:
        for h in heroes:
            if h["tag"] == "detailing":
                selected_hero = h
                break
    elif "corralon" in nombre_lower or "material" in nombre_lower:
        for h in heroes:
            if h["tag"] == "corralon_materiales":
                selected_hero = h
                break
    elif "lente" in nombre_lower or "sol" in nombre_lower:
        for h in heroes:
            if h["tag"] == "lentes_sol":
                selected_hero = h
                break
    elif "kiosc" in nombre_lower or "combo" in nombre_lower or "previa" in nombre_lower:
        for h in heroes:
            if h["tag"] == "bebidas_combos":
                selected_hero = h
                break

    # Resolver URL local o remota
    h_res = dict(selected_hero)
    local_hero_file = f"/static/img/bank/{key}/hero_1.jpg"
    h_res["url"] = resolver_url_imagen(local_hero_file, selected_hero["url"])
    return h_res
