import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (Only from page 2 onwards)
        if self._pageNumber > 1:
            self.drawString(54, 750, "GG SOLUTIONS — MANUAL DEL VENDEDOR B2B (GENERADOR DE DEMOS)")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Footer (All pages)
        self.setFont("Helvetica", 8)
        self.drawString(54, 36, "https://ggsolutions.com.ar/admin  |  Confidencial — Uso Exclusivo Comercial")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(558, 36, page_str)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        
        self.restoreState()


def build_pdf(filename="Manual_Vendedor_GG_Solutions.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Define custom palette & typography
    primary_color = colors.HexColor("#0f172a") # Slate 900
    accent_cyan = colors.HexColor("#0284c7")   # Sky 600
    emerald_color = colors.HexColor("#059669") # Emerald 600
    dark_bg = colors.HexColor("#1e293b")       # Slate 800
    light_bg = colors.HexColor("#f8fafc")      # Slate 50

    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=accent_cyan,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        "Body_Bold",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        "Code_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    story = []

    # ==================== PORTADA ====================
    story.append(Spacer(1, 10))
    story.append(Paragraph("GG SOLUTIONS", ParagraphStyle("BrandBadge", fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=accent_cyan, spaceAfter=4)))
    story.append(Paragraph("Manual Operativo del Vendedor B2B", title_style))
    story.append(Paragraph("Guía de Prospección, Generación de Demos Personalizadas y Cierre Comercial", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=accent_cyan, spaceBefore=0, spaceAfter=15))

    # Banner Informativo Portada
    meta_data = [
        [Paragraph("<b>Plataforma:</b> GG Solutions Admin", body_style), Paragraph("<b>Acceso:</b> ggsolutions.com.ar/admin", body_style)],
        [Paragraph("<b>Módulo:</b> Generador de Demos B2B", body_style), Paragraph("<b>Versión:</b> 2.5 (2026)", body_style)],
        [Paragraph("<b>Destinatarios:</b> Equipo Comercial & Socios", body_style), Paragraph("<b>Objetivo:</b> Cierre en &lt; 3 minutos", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0f9ff")),
        ('BORDER', (0,0), (-1,-1), 0.5, colors.HexColor("#bae6fd")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 15))

    # INTRODUCCIÓN
    story.append(Paragraph("1. Introducción y Propósito del Sistema", h1_style))
    story.append(Paragraph(
        "El <b>Generador de Demos B2B de GG Solutions</b> es una herramienta de ventas de alta conversión diseñada para armar sitios web y plataformas operativas interactivas adaptadas al negocio del prospecto en tiempo real.",
        body_style
    ))
    story.append(Paragraph(
        "Con este sistema, un vendedor puede prospeccionar un comercio en Google Maps, generar su prototipo funcional en menos de 2 minutos y enviarle un pitch por WhatsApp altamente personalizado según los dolores de su rubro.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # PASO 1: ACCESO
    story.append(Paragraph("2. Paso 1: Acceso al Panel de Administración", h1_style))
    story.append(Paragraph("<b>1.1 Ingreso a la Plataforma:</b>", h2_style))
    story.append(Paragraph("&bull; Abrí el navegador e ingresá a <b>https://ggsolutions.com.ar/admin</b>", bullet_style))
    story.append(Paragraph("&bull; Iniciá sesión con tus credenciales asignadas de socio o vendedor.", bullet_style))
    story.append(Paragraph("&bull; En el menú lateral o superior, seleccioná el módulo <b>Admin &rarr; Demos B2B</b>.", bullet_style))

    story.append(Spacer(1, 10))

    # PASO 2: BÚSQUEDA GOOGLE MAPS
    story.append(Paragraph("3. Paso 2: Búsqueda y Autocompletado del Comercio", h1_style))
    story.append(Paragraph(
        "El sistema cuenta con integración directa a <b>Google Places API</b>. Podés cargar un comercio de dos formas:",
        body_style
    ))
    story.append(Paragraph("<b>A) Buscador Inteligente (Recomendado):</b> Escribí el nombre del comercio y ciudad (ej: <i>'Pizzería Don Luis Córdoba'</i>) en el buscador del mapa y seleccioná el resultado desplegado.", bullet_style))
    story.append(Paragraph("<b>B) Carga Directa por Place ID:</b> Pegá el Place ID de Google Maps si lo tenés.", bullet_style))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>¿Qué datos extrae Google Maps automáticamente?</b>", body_style))
    story.append(Paragraph("&bull; Nombre exacto del negocio y dirección comercial.", bullet_style))
    story.append(Paragraph("&bull; Teléfono oficial y número de WhatsApp registrado.", bullet_style))
    story.append(Paragraph("&bull; Calificación (Rating 1-5 estrellas) y cantidad de reseñas reales.", bullet_style))
    story.append(Paragraph("&bull; Galería de fotos reales de la fachada e instalaciones del local.", bullet_style))

    story.append(Spacer(1, 10))

    # PASO 3: PASO A PASO EN EL FORMULARIO
    story.append(Paragraph("4. Paso 3: Configuración Paso a Paso de la Demo", h1_style))
    
    story.append(Paragraph("<b>Fase 1: Identificación y Rubro Comercial</b>", h2_style))
    story.append(Paragraph("Seleccioná el rubro que mejor coincida con el prospecto. El rubro define la paleta estética, los copys del Hero, los productos sugeridos y la grilla de servicios.", body_style))
    
    rubros_data = [
        [Paragraph("<b>Rubro</b>", body_bold), Paragraph("<b>Ejemplos de Comercio</b>", body_bold), Paragraph("<b>Módulo Sugerido</b>", body_bold)],
        [Paragraph("gastronomia", body_style), Paragraph("Restaurantes, Pizzerías, Bares, Cafés", body_style), Paragraph("E-Commerce / Carta Digital", body_style)],
        [Paragraph("hostel", body_style), Paragraph("Hostels, Hoteles, Posadas, Turismo", body_style), Paragraph("Reserva Camas / Estadía", body_style)],
        [Paragraph("pilates_wellness", body_style), Paragraph("Pilates, Yoga, Estética, Spas", body_style), Paragraph("Agenda &amp; Reservas", body_style)],
        [Paragraph("salud", body_style), Paragraph("Clínicas, Consultorios, Odontología", body_style), Paragraph("Agenda &amp; Reservas", body_style)],
        [Paragraph("automotriz", body_style), Paragraph("Talleres Mecánicos, Repuestos, Lavaderos", body_style), Paragraph("Cotizador / Stock", body_style)],
        [Paragraph("indumentaria", body_style), Paragraph("Locales de Ropa, Boutiques, Calzado", body_style), Paragraph("E-Commerce / Catálogo", body_style)],
        [Paragraph("retail", body_style), Paragraph("Tiendas, Bazares, Kioscos, Drugstores", body_style), Paragraph("Catálogo / Stock", body_style)],
        [Paragraph("herramientas", body_style), Paragraph("Ferreterías, Corralones, Insumos de Obra", body_style), Paragraph("Cotizador B2B", body_style)],
        [Paragraph("deportes", body_style), Paragraph("Complejos de Pádel, Canchas, Gimnasios", body_style), Paragraph("Agenda / Reserva Canchas", body_style)],
        [Paragraph("inmobiliaria", body_style), Paragraph("Inmobiliarias, Alquileres, Desarrollos", body_style), Paragraph("Catálogo Filtrable", body_style)],
        [Paragraph("opticas", body_style), Paragraph("Ópticas, Centros Oftalmológicos", body_style), Paragraph("Agenda &amp; Catálogo", body_style)],
        [Paragraph("servicios", body_style), Paragraph("Consultoría, Estudios, Empresas B2B", body_style), Paragraph("Cotizador / Soluciones", body_style)]
    ]
    t_rubros = Table(rubros_data, colWidths=[90, 260, 154])
    t_rubros.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), dark_bg),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_rubros)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Fase 2: Estrategia Comercial &amp; Dolores (Crucial para el Pitch)</b>", h2_style))
    story.append(Paragraph("&bull; <b>Dolores a Solucionar (subheadline):</b> Seleccioná de los chips prediseñados o escribí el dolor operativo del comercio. Ejemplo: <i>'Demoras en la toma de pedidos por WhatsApp'</i>. Se integrará automáticamente a la bajada del Hero.", body_style))
    story.append(Paragraph("&bull; <b>Objetivo Estratégico (headline H1):</b> Escribí la meta principal. Ejemplo: <i>'Reducir tiempos de atención en mesa y potenciar venta online'</i>. El H1 de la demo se personalizará como: <i>'Solución Digital en {Nombre}: {Objetivo}'</i>.", body_style))
    story.append(Paragraph("&bull; <b>Casilla 'Incluir sección Novedades / Blog':</b> Mantenela <b>desmarcada</b> por defecto a menos que el cliente explícitamente solicite un blog institucional de noticias.", body_style))

    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Fase 3: Personalización de Marca y Plantilla de Diseño</b>", h2_style))
    story.append(Paragraph("&bull; <b>Logo:</b> Subí el logo del cliente en PNG/SVG o dejá que el sistema use el avatar generado.", bullet_style))
    story.append(Paragraph("&bull; <b>Colores de Marca:</b> Ingresá los códigos HEX del cliente (ej: <code>#e11d48</code>) o usá la paleta sugerida por el rubro.", bullet_style))
    story.append(Paragraph("&bull; <b>Plantilla Visual Inicial:</b> Seleccioná entre <i>Classic Glassmorphism</i> (estándar), <i>Horizontal Scroll Editorial</i> (luxury) o <i>Layered Reveal Narrative</i> (parallax).", bullet_style))

    story.append(Spacer(1, 12))

    # PASO 4: MODO CLIENTE VS MODO INTERNO
    story.append(Paragraph("5. Paso 4: Presentación al Cliente (Modo Cliente vs. Modo Interno)", h1_style))
    story.append(Paragraph(
        "El sistema maneja automáticamente el comportamiento visual según quién abra la demo:",
        body_style
    ))
    
    modes_data = [
        [Paragraph("<b>Modo / Escenario</b>", body_bold), Paragraph("<b>Comportamiento Visual</b>", body_bold), Paragraph("<b>Uso Recomendado</b>", body_bold)],
        [
            Paragraph("<b>Modo Cliente (Default)</b><br/>URL limpia: <code>/demo/slug</code>", body_style),
            Paragraph("Dock superior <b>OCULTO</b> de forma 100% limpia. Muestra la landing comercial como un producto terminado real.", body_style),
            Paragraph("Para enviar al prospecto por WhatsApp o mostrar en reuniones sin distracciones de builder.", body_style)
        ],
        [
            Paragraph("<b>Modo Interno / Admin</b><br/>Sesión activa o <code>?vista=interna</code>", body_style),
            Paragraph("Dock superior <b>VISIBLE</b> con:<br/>&bull; Badge 'DEMO B2B'<br/>&bull; Selector en vivo de plantillas visuales<br/>&bull; Toggle 'Vista Pública / Panel Gestión'<br/>&bull; Botón Compartir", body_style),
            Paragraph("Para el equipo comercial durante la llamada o reunión en vivo para cambiar el estilo o mostrar el software interno.", body_style)
        ]
    ]
    t_modes = Table(modes_data, colWidths=[140, 220, 144])
    t_modes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), dark_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_modes)

    story.append(Spacer(1, 12))

    # PASO 5: MOTOR DE PROSPECCIÓN WHATSAPP
    story.append(Paragraph("6. Paso 5: Motor de Prospección Directa por WhatsApp", h1_style))
    story.append(Paragraph(
        "En la tabla de demos creadas del panel de administración, cada demo cuenta con un botón verde <b>'Prospectar WA'</b>.",
        body_style
    ))
    story.append(Paragraph(
        "Al presionar <b>'Prospectar WA'</b>, el sistema genera automáticamente un mensaje de prospección hiper-personalizado adaptado a las fortalezas y dolores del rubro del cliente, y abre el chat de WhatsApp listo para enviar.",
        body_style
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Ejemplo de Guión de Prospección Generado (Rubro Gastronomía):</b>", h2_style))
    story.append(Paragraph(
        "<i>\"Hola! Soy Gabi, de GG Solutions. Venimos trabajando con sistemas del rubro en la automatización de comandas, menú digital interactivo y pedidos por WhatsApp, y sabemos la cantidad de tiempo y plata que se ahorra al eliminar errores en mesa y filas en mostrador. Nos venimos perfeccionando cliente a cliente aprendiendo cada vez más del sector. Hoy me topé con {Nombre del Comercio} en Google Maps, me gustó mucho la propuesta y decidí hacer una pequeña demo basada en tus datos para que veas lo que hacemos: https://ggsolutions.com.ar/demo/{slug}<br/><br/>Si te interesa implementar alguna de las soluciones o quizás comentar algún otro dolor avísame, me mantengo atento. Gracias!!\"</i>",
        code_style
    ))

    story.append(Spacer(1, 10))

    # PASO 6: MANEJO DE OBJECIONES Y PREGUNTAS FRECUENTES
    story.append(Paragraph("7. Preguntas Frecuentes &amp; Manejo de Objeciones", h1_style))
    
    faq_data = [
        [
            Paragraph("<b>Pregunta / Objeción</b>", body_bold),
            Paragraph("<b>Respuesta &amp; Acción Sugerida para el Vendedor</b>", body_bold)
        ],
        [
            Paragraph("<b>¿Cómo le muestro el sistema de gestión interna al cliente?</b>", body_style),
            Paragraph("En el dock superior de la demo (en modo interno) usá el switch <b>'Vista Pública / Gestión'</b>. Esto alternará la pantalla para mostrarle el panel administrativo con pedidos, turnos y métricas en vivo.", body_style)
        ],
        [
            Paragraph("<b>'El cliente dice que no usa WhatsApp para tomar pedidos'</b>", body_style),
            Paragraph("Explicale que la demo es modular: se puede activar el <b>Cotizador B2B</b> o el <b>Módulo de Turnos</b> sin necesidad de carrito directo.", body_style)
        ],
        [
            Paragraph("<b>'El cliente no tiene fotos de calidad en Google Maps'</b>", body_style),
            Paragraph("No te preocupes. El motor de imágenes inyecta automáticamente fotografías HD 16:9 seleccionadas por rubro desde el banco de imágenes oficial.", body_style)
        ],
        [
            Paragraph("<b>¿Cómo cambio la plantilla si al cliente no le gusta el diseño?</b>", body_style),
            Paragraph("Tocá los botones <i>Classic</i>, <i>Horizontal Scroll</i> o <i>Layered Reveal</i> en el dock superior en vivo. La página cambiará al instante sin recargar.", body_style)
        ]
    ]
    t_faq = Table(faq_data, colWidths=[180, 324])
    t_faq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_faq)

    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>¡Éxitos en las ventas! Para soporte técnico o consultas operativas, contactar al equipo central de GG Solutions.</b>", ParagraphStyle("FinalNote", parent=body_style, fontName="Helvetica-Bold", textColor=colors.HexColor("#047857"), alignment=1)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado con éxito: {filename}")

if __name__ == "__main__":
    build_pdf()
