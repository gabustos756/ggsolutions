# 📖 Guía Definitiva para Creación de Demos Especializadas B2B / B2C
> **GG Solutions Platform Architecture**  
> *Manual de desarrollo y estructura de Master Prompt para creación autónoma de demos comerciales e industriales en un solo paso.*

---

## 📌 1. Resumen Arquitectónico: Caso de Éxito "Zapatería Loribell"

La demo de **Zapatería Loribell** sirve como estándar de referencia para construir verticales de negocio donde conviven una **experiencia pública de marca (B2C)** y un **software operativo interno de gestión (B2B)**.

### Componentes Clave Implementados:
1. **Resolución de Google Places Link**: Parser automático en `services/google_places.py` para enlaces cortos de Maps (`maps.app.goo.gl`) extrayendo calificaciones, fotos y dirección real.
2. **Copy Engine Artesanal**: `generar_copy_negocio` en `services/demo_engine.py` configurado para mantener la identidad humana y artesanal en la vista pública (evitando jerga técnica B2B en el Hero del cliente).
3. **Separación Estricta de Vistas**:
   - `view-software-publico`: Renders exclusivamente la landing del cliente (Hero, Instagram Feed, Protocolo de Entrega, Formulario de Diagnóstico de 10 preguntas, Buscador de Remito Digital, Opiniones Google).
   - `view-software-admin`: Renders exclusivamente el sistema operativo de taller (`zapateria_admin.html`) con KPIs, Remitos por división, Carga de Evidencia Fotográfica HD, Envíos por WhatsApp y Control de Insumos.
4. **Trial Store en `sessionStorage`**: `static/js/zapateria_store.js` que mantiene un estado dinámico en sesión de prueba sin depender de base de datos persistente, reaccionando a eventos `window.dispatchEvent(new CustomEvent("zapateriaStateChanged"))`.

---

## 🛠️ 2. Estructura de Archivos por Nueva Demo Especializada

Para agregar una demo de un nuevo rubro (ej: `mecanica`, `lavanderia`, `optica`, `estetica`, `imprenta`), se deben crear/modificar los siguientes 5 archivos:

| Componente | Archivo a Crear / Modificar | Propósito |
| :--- | :--- | :--- |
| **Data Seed** | [app.py](file:///Users/fgabrielbustos/Documents/Apps/ggsolutions/ggsolutions/app.py) | Sembrado inicial del slug con `diseno_template="layered-reveal"`. |
| **Copy Engine** | [services/demo_engine.py](file:///Users/fgabrielbustos/Documents/Apps/ggsolutions/ggsolutions/services/demo_engine.py) | Definición de headlines artesanales públicos según `rubro_key`. |
| **Session Store** | `static/js/[rubro]_store.js` | Estado trial en `sessionStorage` con KPIs, pedidos e insumos. |
| **Vista Cliente** | `templates/demos/components/[rubro].html` | Landing B2C 100% enfocada en el cliente final. |
| **Vista Admin** | `templates/demos/components/[rubro]_admin.html` | Software interno B2B para control de operaciones. |
| **Render Include** | `templates/demos/base_demo.html` | Renderizado condicional en `view-software-admin`. |

---

## 🚀 3. Master Prompt Template (Para solicitar un desarrollo completo en 1 solo paso)

Copiar y completar la siguiente plantilla cuando se necesite crear un módulo especializado para un nuevo cliente o rubro:

```markdown
PROMPT DE CREACIÓN DE DEMO ESPECIALIZADA EN GG SOLUTIONS:

Quiero implementar un nuevo módulo de demo especializada para el rubro [NOMBRE_DEL_RUBRO] (ej: Taller Mecánico, Lavandería, Clínica Veterinaria, Imprenta).

1. DATOS DEL NEGOCIO / GOOGLE MAPS:
- Nombre Comercial: [Ej: Mecánica San Martín]
- Enlace de Google Maps / Ubicación: [URL de Maps o Dirección]
- WhatsApp de atención: [Ej: 351XXXXXXX]
- Link de Instagram o Redes: [Ej: https://instagram.com/...]

2. REGION Y DIVISIONES OPERATIVAS (ADMIN B2B):
- División 1: [Ej: Mecánica Ligera & Motores]
- División 2: [Ej: Electricidad & Diagnóstico Computarizado]

3. FORMULARIO DE DIAGNÓSTICO / RESERVA PÚBLICO (CLIENTE B2C):
- Lienzo en blanco de preguntas del cliente (Nombre, Teléfono, Vehículo/Artículo, Síntomas/Trabajo a realizar, Fecha requerida, Adjuntar foto).

4. PROTOCOLO O REGLAS DE ENTREGA EN LOCAL:
- Regla 1: [Ej: Presentar cédula verde]
- Regla 2: [Ej: Tanque con al menos 1/4 de combustible]
- Regla 3: [Ej: Retirar objetos de valor del habitáculo]

5. CONTROL DE INSUMOS Y REMITOS EN ADMIN:
- Datos de remito/comprobante trial inicial (Cliente, Estado, Precio, Foto de trabajo listo).
- Lista de insumos clave de taller/negocio para control de stock.

REQUISITOS ARQUITECTÓNICOS (OBLIGATORIOS):
1. Separar 100% la Vista Pública del Cliente (`templates/demos/components/[rubro].html`) de la Vista de Administración Interna (`templates/demos/components/[rubro]_admin.html`).
2. El Hero público NO debe contener jerga técnica ni textos de remitos/compras. Debe reflejar la identidad artesanal y las publicaciones reales de Instagram del negocio.
3. El botón en la barra superior debe invocar `switchSoftwareView('admin')` para conmutar directamente al software de gestión.
4. Usar `sessionStorage` para el Trial Store (`static/js/[rubro]_store.js`) despachando el evento `[rubro]StateChanged`.
5. Ejecutar la validación con el script de test `test_context.py` asegurando HTTP 200.
```

---

## 📋 4. Pasos Técnicos para el Desarrollador / Agente

### Paso 1: Configurar el Copy Engine
En `services/demo_engine.py`, añadir el rubro en `generar_copy_negocio`:
```python
elif rubro_key == "mecanica":
    headline = "¿Tu vehículo necesita service o presenta alguna falla?"
    subheadline = "Diagnóstico computarizado, mecánica especializada y repuestos originales en Córdoba."
```

### Paso 2: Crear el Store de Sesión (`static/js/[rubro]_store.js`)
El store debe exponer los métodos:
- `getData()`, `saveData(data)`, `reset()`
- `getRemitos(categoria)`, `getRemitoById(id)`
- `crearRemito(nuevoData)`
- `actualizarEstadoRemito(id, nuevoEstado, fotoUrl)`
- `actualizarInsumo(id, delta)`
- `generarMensajeWhatsApp(id)`

### Paso 3: Construir la Vista Cliente (`templates/demos/components/[rubro].html`)
- Contiene: Monograma/Logo, Instagram Feed real o tarjetas de casos de éxito, Protocolo de Recepción, Formulario de Diagnóstico de N preguntas, Buscador de Remitos para clientes, Google Maps Card.
- Debe estar vinculado a `buscarRemitoCliente()` y `enviarDiagnosticoWhatsApp()`.

### Paso 4: Construir la Vista Admin (`templates/demos/components/[rubro]_admin.html`)
- Contiene: Botón `[🌐 Volver a Vista Cliente]`, Cards de KPIs, Tablero de Remitos con filtros de división, Modal Nuevo Remito, Modal Adjuntar Evidencia Fotográfica HD, Acciones de cambio de estado y Notificación WA, Control de Insumos.

### Paso 5: Registrar en `base_demo.html` y `_modules_render.html`
En `templates/demos/base_demo.html`:
```html
{% if demo.rubro == 'mecanica' %}
    {% include "demos/components/mecanica_admin.html" %}
{% else %}
    {% include "demos/admin_panel.html" %}
{% endif %}
```

---

## 🧪 5. Verificación de Calidad

Ejecutar siempre la verificación local de Flask:
```bash
./venv/bin/python scratch/test_context.py
```
Criterio de éxito: `HTTP Status Route /demo/[slug]: 200` sin errores de Jinja2 ni scripts rotos.
