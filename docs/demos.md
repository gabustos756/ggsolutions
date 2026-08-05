# Documentación Técnica: Pipeline de Creación de Demos Comerciales B2B

Este documento explica de forma exhaustiva la arquitectura, recopilación de datos, motor de temas visuales, estructura HTML y flujo de ejecución para la generación automática de Landing Pages de alta conversión en **Nicho Landing Factory & CRM Engine**.

---

## 1. Visión General del Proceso de Generación

El objetivo del generador de demos es crear, en tiempo real y sin intervención manual, una **Landing Page estática personalizada de nivel Enterprise** para cualquier PYME prospectada. 

La demo no solo presenta el sitio web oficial de la PYME (con su estética, servicios, horarios y mapa real), sino que integra de forma fluida una **sección de venta B2B** (Canvas estilo Apple) que le permite a la agencia (*Emayon Forge*) vender la suscripción del sitio web y servicios digitales al cliente prospectado.

```
┌─────────────────────────┐
│   Prospecto ID (SQLite) │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐     ┌─────────────────────────────────────────────┐
│ Prospección & Scrape:   │ ──► │  DuckDuckGo, OSM Nominatim, Google Reviews, │
│  Enriquecimiento Datos │     │  Overpass GIS & Phone Enricher (+54 9...)   │
└────────────┬────────────┘     └─────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────┐     ┌─────────────────────────────────────────────┐
│ Motor Inferencia Rubro  │ ──► │  Categorización semántica (10 rubros) +     │
│ & Theme Engine          │     │  Paletas HSL/Glows, Fonts, Servicios, Hero  │
└────────────┬────────────┘     └─────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────┐     ┌─────────────────────────────────────────────┐
│ Ensamblado de HTML      │ ──► │  Landing Pública PYME + Canvas Enterprise   │
│ & Template Generator    │     │  SaaS Blanco + Checkout dLocal GO + WhatsApp│
└────────────┬────────────┘     └─────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────┐
│ Output: `demos/{id}.html`│ ──► Serving en `/static/demos/{place_id}.html`
└─────────────────────────┘
```

---

## 2. Ingesta y Enriquecimiento de Datos en Tiempo Real

El sistema garantiza que cada demo esté alimentada con datos fidedignos extraídos en tiempo real. Los servicios involucrados son:

### 2.1. Búsqueda y Extracción Web (`backend/services/agent_reach_service.py` & `web_scraper.py`)
* **DuckDuckGo Live Scraping**: Realiza búsquedas geolocalizadas (`"{rubro} en {ciudad}, Argentina"`) para extraer sitios web oficiales, redes sociales y menciones.
* **Desempaquetado de Enlaces**: Resuelve redirecciones internas (`uddg=`) de buscadores para obtener las URLs reales.
* **Filtros Anti-Ruido (Poka-Yoke)**: Descarta agregadores, directorios genéricos (Wikipedia, Top 10) y términos específicos de España (ej. *gastrotaberna*, *madrid*), garantizando prospección 100% latinoamericana/argentina.
* **Fallback Autocomplete**: Si el buscador principal limita peticiones por IP, recurre a la API de sugerencias JSON para mantener el flujo operativo.

### 2.2. Validaciones Telefónicas y WhatsApp (`backend/services/phone_enricher.py`)
* **Regex de Extracción**: Detecta teléfonos en snippets web o busca enlaces directos de WhatsApp (`wa.me/549...`, `api.whatsapp.com`).
* **Validación Geográfica por Ciudad**: Utiliza la matriz `PREFIJOS_AREA` (ej. `11` CABA/GBA, `341` Rosario, `351` Córdoba, `261` Mendoza) para verificar la validez del número.
* **Normalización E.164**: Formatea los teléfonos a estándar internacional (`+54 9 AAAA BBBBBB`). Si no posee celular verificado, genera una opción de contacto genérica sin romper la interfaz.

### 2.3. Geolocalización y GIS (`backend/services/real_gis_scraper.py`)
* **Nominatim OpenStreetMap (OSM)**: Obtiene las coordenadas latitud/longitud precisas de la ciudad del prospecto.
* **Overpass API**: Ejecuta consultas espaciales con filtros de etiquetas semánticas (`["shop"="bakery"]`, `["amenity"~"cafe|restaurant|bar"]`, `["shop"="car_repair"]`, etc.) sobre la red OSM.

### 2.4. Prueba Social y Reseñas Reales (`backend/services/google_reviews_service.py`)
* **Integración Oficial Google Places API**: Si se provee la API Key, consulta opiniones verificadas directamente del Place ID.
* **Scraping Defensivo de Reseñas**: En ausencia de API Key, extrae opiniones y comentarios reales de Google Maps/DuckDuckGo.
* **Regla Poka-Yoke de Testimonios**: Si la empresa **no posee opiniones verificables**, la sección de reseñas **no se renderiza en la demo**, evitando generar testimonios ficticios o fraudulentos.

### 2.5. Resumen Web Inteligente (`obtener_contexto_web_empresa` en `landing_theme_engine.py`)
* Escanea snippets reales de la empresa en la web para resumir en 1 o 2 oraciones la propuesta de valor comercial de la PYME en el Hero Section. En caso de no hallar referencias específicas, aplica una síntesis profesional basada en la ciudad.

---

## 3. Motor de Inferencia Visual & Taste DNA (`landing_theme_engine.py` & `generator.py`)

Para evitar landings genéricas o repetitivas, el sistema cuenta con un motor de diseño basado en **10 universos estéticos (Categorías Visuales)**:

1. `gastronomia` (Restaurantes, Cafés, Bares, Pizzerías)
2. `motos` (Talleres de motos, Repuestos, Mecánica)
3. `automotriz` (Talleres mecánicos, Lubricentros, Concesionarias)
4. `salud_belleza` (Clínicas, Odontología, Spas, Peluquerías)
5. `inmobiliaria` (Bienes Raíces, Tasaciones, Propiedades)
6. `tecnologia` (Software, Ciberseguridad, Soporte IT, Cloud)
7. `retail` (Tiendas de ropa, Boutiques, Comercios)
8. `logistica` (Fletes, Mudanzas, Envíos, Transporte)
9. `servicios_hogar` (Plomería, Electricidad, Refrigeración, Reformas)
10. `educacion` (Academia, Cursos, Instituto, Capacitación)
11. `corporativo` (Fallback para servicios profesionales y empresas generales)

### 3.1. Inferidor por Palabras Clave
La función `inferir_categoria_por_rubro()` analiza mediante expresiones regulares con límites de palabra (`\bkw\b`) el nombre comercial y tipo de búsqueda, mapeándolo a su categoría óptima.

### 3.2. Configuración Estética (Theme Config Map)
Cada categoría visual define un conjunto de tokens de diseño:
* **Esquema de Colores Oscuros Ultra-Premium**: `bg` (#0c0908, #070a12, #060f14, etc.), `card_bg` (glassmorphism con backdrop-blur 16px), `border`, `border_hover`, `glow` y `accent`.
* **Gradientes de Acento**: Aplicados a los títulos principales (`from-amber-300 via-orange-400 to-amber-500`, `from-blue-400 via-sky-400 to-indigo-400`, etc.).
* **Tipografías Temáticas via Google Fonts**:
  * *Playfair Display* para Gastronomía.
  * *Oswald* para Motos y Automotriz.
  * *Outfit* para Salud, Belleza, Educación y Retail.
  * *Cormorant Garamond* para Inmobiliaria.
  * *Space Grotesk* para Tecnología y Logística.
  * *Plus Jakarta Sans* para Servicios del Hogar y Corporativo.
* **Imágenes de Portada Fotorrealistas**: Rotación determinista mediante hashing del ID del prospecto (`idx = sum(ord(c) for c in seed) % len(image_pool)`), garantizando variedad visual sin cambios aleatorios en recargas.
* **Grilla de 6 Servicios Temáticos**: Cada servicio cuenta con icono FontAwesome, tag semántico y asignación de imagen 16:9 (`/static/img/services/{key}.jpg`).
* **Sección de Novedades del Sector**: 3 artículos con tiempo de lectura y síntesis redactada para el rubro.

---

## 4. Estructura HTML & Arquitectura del Template

El archivo final generado es un documento estático optimizado (`HTML5 + TailwindCSS CDN + FontAwesome 6`) estructurado en **dos bloques conceptuales principales**: la *Landing Pública del Cliente* y la *Propuesta Comercial Enterprise B2B*.

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. DOCK COMERCIAL B2B SUPERIOR (Emayon Forge Commercial Bar)          │
├────────────────────────────────────────────────────────────────────────┤
│ 2. STICKY NAVBAR PÚBLICO DE LA PYME (Logo + Nav Links + WA CTA)        │
├────────────────────────────────────────────────────────────────────────┤
│ 3. HERO BANNER FULL SPLIT 2-COLUMNS                                    │
│    - Izq: Badge Ciudad + Star Rating Google + Título Gradiente + Resumen│
│    - Der: Card Flotante Glassmorphic (Horarios + Calidad + WA Button)  │
├────────────────────────────────────────────────────────────────────────┤
│ 4. CONTENIDO PÚBLICO DEL NEGOCIO                                       │
│    - Servicios & Especialidades (Grilla Enterprise 3x2 Glass Cards)    │
│    - Novedades del Sector (Carrusel Interactivo Scroll-Snap + JS)      │
│    - Opiniones Reales de Google Maps (Condicional)                     │
│    - Ubicación & Horarios (Google Maps Iframe con Filtro Dark + Pin)    │
├────────────────────────────────────────────────────────────────────────┤
│ 5. DIVISOR COMERCIAL MARKETINERO ("Impulsá tu Negocio")                │
├────────────────────────────────────────────────────────────────────────┤
│ 6. CANVAS ENTERPRISE APPLE STYLE (FONDO BLANCO LÍMPIDO)                 │
│    - Header con Branding Emayon Forge                                  │
│    - 3 Planes SaaS (Presencia, Gestión & Growth, Enterprise & IA)       │
│    - Botón de Pago dLocal GO Integrado ($350 USD)                      │
│    - Infraestructura SSL & Garantías Cloud                             │
├────────────────────────────────────────────────────────────────────────┤
│ 7. WIDGET FLOTANTE WHATSAPP (fixed bottom-6 right-6)                   │
└────────────────────────────────────────────────────────────────────────┘
```

### 4.1. Componentes Clave del HTML

1. **Glassmorphic Cards (`.glass-card`)**:
   ```css
   background: rgba(255, 255, 255, 0.03);
   backdrop-filter: blur(16px);
   -webkit-backdrop-filter: blur(16px);
   border: 1px solid rgba(...);
   box-shadow: 0 20px 40px -15px rgba(0,0,0,0.5);
   ```
2. **Carrusel de Noticias Interactivo**:
   * Utiliza `overflow-x-auto`, `snap-x` y `scroll-smooth` sin librerías pesadas.
   * Navegación controlada mediante Javascript nativo inline:
     ```javascript
     document.getElementById('news-carousel').scrollBy({left: 350, behavior: 'smooth'})
     ```
3. **Google Maps Iframe con Filtro Dark Nativo**:
   * Transforma el iframe de Google Maps tradicional a un mapa nocturno mediante filtros CSS:
     ```css
     filter: invert(90%) hue-rotate(180deg) contrast(120%) grayscale(20%);
     ```
   * Al pasar el cursor (`hover:filter-none`), se revela el color original del mapa.
4. **Canvas Blanco SaaS (Sección Enterprise)**:
   * Cambia deliberadamente el fondo de oscuro a blanco límpido (`bg-white text-slate-950`), ofreciendo un contraste visual dramático tipo Apple/Stripe para presentar los planes de cobro comercial.
   * Incluye la tarjeta destacada con borde dorado y badge `"MÁS POPULAR"`.
   * Enlace directo a la pasarela de pagos: `https://checkout.dlocalgo.com/v1/pay/demo-{precio}-usd`.

---

## 5. Flujo de Ejecución del Endpoint API

El proceso se ejecuta al invocar `POST /api/v1/agencia/prospectos_b2b/generar-demo/{place_id}` en `backend/main.py`:

```python
# 1. Recuperar datos del prospecto desde la DB SQLite
prospecto = buscar_prospecto_por_place_id(db, place_id)

# 2. Clasificar rubro e inferir tema visual
resultado_landing = generar_landing_page(nombre_negocio=nombre, rubro=rubro)
theme = obtener_theme_config(resultado_landing.categoria_visual, prospecto_seed=place_id)

# 3. Enriquecer contexto web y buscar reseñas reales en Google Maps
ctx_web = obtener_contexto_web_empresa(nombre, ciudad)
resenas_autenticas = obtener_resenas_reales_google(nombre, ciudad)

# 4. Formatear componentes HTML (features_html, news_html, reviews_html, pricing_html)
# ...

# 5. Escribir archivo estático en frontend/demos/{place_id}.html
with open(filepath, "w", encoding="utf-8") as f:
    f.write(html_demo_content)

# 6. Retornar JSON de respuesta con URL pública y link directo de WhatsApp
return {
    "nombre": nombre,
    "precio_usd": precio,
    "dominio_elegido": dominio,
    "url_demo": f"/static/demos/{place_id}.html",
    "link_wa": link_wa
}
```

---

## 6. Archivos Relacionados en el Código Fuente

| Archivo | Responsabilidad / Función Principal |
| :--- | :--- |
| [backend/main.py](file:///Users/fgabrielbustos/Documents/Apps/landing_factory/backend/main.py#L420-L1035) | Endpoint API `/generar-demo/{place_id}` y ensamblador de plantilla HTML. |
| [backend/services/landing_theme_engine.py](file:///Users/fgabrielbustos/Documents/Apps/landing_factory/backend/services/landing_theme_engine.py) | Diccionario de temas visuales, paletas HSL, fuentes, servicios por rubro y contexto web. |
| [backend/services/generator.py](file:///Users/fgabrielbustos/Documents/Apps/landing_factory/backend/services/generator.py) | Motor de inferencia de categorías por palabras clave del rubro (`inferir_categoria_por_rubro`). |
| [backend/services/agent_reach_service.py](file:///Users/fgabrielbustos/Documents/Apps/landing_factory/backend/services/agent_reach_service.py) | Scraping DuckDuckGo en directo y validación Poka-Yoke en Google Maps. |
| [backend/services/google_reviews_service.py](file:///Users/fgabrielbustos/Documents/Apps/landing_factory/backend/services/google_reviews_service.py) | Verificación y extracción de opiniones auténticas de Google Maps. |
| [backend/services/real_gis_scraper.py](file:///Users/fgabrielbustos/Documents/Apps/landing_factory/backend/services/real_gis_scraper.py) | Geolocalización Nominatim OSM y extracción de datos vía Overpass API. |
| [backend/services/phone_enricher.py](file:///Users/fgabrielbustos/Documents/Apps/landing_factory/backend/services/phone_enricher.py) | Extracción de WhatsApp, validación cruzada con prefijos telefónicos AR y formato E.164. |
