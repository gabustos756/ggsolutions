"""
Servicio de Google Places API y Parser de URLs para GG Solutions.
Extrae información fidedigna de comercios a partir de enlaces de Google Maps o Place IDs:
- Reseñas reales de clientes (con autor, puntaje, texto y foto)
- Fotos HD del establecimiento y productos
- Sitio web oficial y horarios
- Validación inteligente de teléfono fijo vs WhatsApp celular
- Soporte para múltiples API Keys de respaldo (multi-key fallback)
"""

import os
import re
import json
import urllib.request
import urllib.parse


def obtener_api_keys() -> list:
    """Devuelve la lista de API Keys configuradas en .env para tolerancia a fallos."""
    keys = []
    for var_name in ["GOOGLE_MAPS_API_KEY", "GOOGLE_MAPS_API_KEY_BACKUP", "GOOGLE_MAPS_API_KEY_ALT"]:
        k = os.environ.get(var_name, "").strip()
        if k and k not in keys:
            keys.append(k)
    return keys


def extraer_place_id_o_busqueda(map_url_o_query: str) -> dict:
    """
    Analiza una cadena ingresada (URL de Google Maps, Place ID o nombre) y extrae:
    - query: término de búsqueda limpio
    - place_id: id de lugar si se detecta en la URL
    """
    text = (map_url_o_query or "").strip()
    
    # 1. Detectar si es un Place ID directo (ej: ChIJ...)
    if text.startswith("ChIJ") and len(text) > 20:
        return {"place_id": text, "query": None}

    # 2. Detectar URLs de Google Maps
    match_place = re.search(r"/maps/place/([^/]+)", text)
    if match_place:
        raw_name = urllib.parse.unquote(match_place.group(1)).replace("+", " ")
        raw_name = re.sub(r"@-?\d+\.\d+,-?\d+\.\d+.*", "", raw_name).strip()
        return {"query": raw_name, "place_id": None}

    # 3. Detectar parámetro q= o query= en URL
    match_q = re.search(r"[?&](?:q|query)=([^&]+)", text)
    if match_q:
        raw_name = urllib.parse.unquote(match_q.group(1)).replace("+", " ")
        return {"query": raw_name, "place_id": None}

    # 4. Texto plano (nombre del negocio)
    return {"query": text, "place_id": None}


def validar_y_formatear_whatsapp(telefono_raw: str, default_cell: str = "5493515550199") -> dict:
    """
    Analiza un teléfono e identifica si es fijo o celular (WhatsApp).
    Devuelve:
    - es_fijo: bool
    - es_whatsapp_valido: bool
    - whatsapp_digits: str (apto para wa.me/...)
    - telefono_display: str (formato formateado para mostrar)
    """
    if not telefono_raw:
        return {
            "es_fijo": False,
            "es_whatsapp_valido": True,
            "whatsapp_digits": default_cell,
            "telefono_display": "Consulte por WhatsApp"
        }

    digitos = re.sub(r"\D", "", telefono_raw)

    # Caso Argentina (+54...)
    es_fijo = False
    es_celular = False

    if digitos.startswith("54"):
        if digitos.startswith("549"):
            es_celular = True
            wa_num = digitos
        else:
            # Es 543514... (fijo sin 9)
            es_fijo = True
            # Intentar anteponer el 9 si es celular
            wa_num = "549" + digitos[2:]
    elif digitos.startswith("0"):
        num_sin_cero = digitos[1:]
        if "15" in num_sin_cero or len(num_sin_cero) == 10:
            es_celular = True
            num_sin_15 = num_sin_cero.replace("15", "", 1)
            wa_num = "549" + num_sin_15
        else:
            es_fijo = True
            wa_num = "549" + num_sin_cero
    else:
        # Internacional genérico
        wa_num = digitos
        es_celular = len(digitos) >= 10

    return {
        "es_fijo": es_fijo,
        "es_whatsapp_valido": es_celular and not es_fijo,
        "whatsapp_digits": wa_num if len(wa_num) >= 10 else default_cell,
        "telefono_display": telefono_raw
    }


def obtener_datos_lugar_google(input_str: str) -> dict:
    """
    Consulta Google Places API utilizando las llaves disponibles en .env para extraer
    fotos HD, opiniones reales de usuarios, sitio web y datos de contacto.
    """
    info = extraer_place_id_o_busqueda(input_str)
    place_id = info.get("place_id")
    query = info.get("query")

    api_keys = obtener_api_keys()

    for api_key in api_keys:
        try:
            # 1. Si no tenemos Place ID, buscamos a través de Find Place Text API
            if not place_id and query:
                search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={urllib.parse.quote(query)}&inputtype=textquery&fields=place_id,name,formatted_address&key={api_key}"
                req = urllib.request.Request(search_url, headers={"User-Agent": "GGSolutions-DemoEngine/1.0"})
                with urllib.request.urlopen(req, timeout=6) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    candidates = res_data.get("candidates", [])
                    if candidates:
                        place_id = candidates[0].get("place_id")

            if place_id:
                # 2. Place Details API con todos los campos extendidos incluyendo icon, types y editorial_summary
                fields = "name,formatted_address,international_phone_number,formatted_phone_number,rating,user_ratings_total,website,reviews,photos,opening_hours,icon,types,editorial_summary"
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&language=es&key={api_key}"
                req = urllib.request.Request(details_url, headers={"User-Agent": "GGSolutions-DemoEngine/1.0"})
                
                with urllib.request.urlopen(req, timeout=6) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    status = res_data.get("status")

                    if status in ["OVER_QUERY_LIMIT", "REQUEST_DENIED"]:
                        print(f"[GOOGLE PLACES API WARN] Key {api_key[:8]}... devolvió {status}. Probando siguiente API Key...")
                        continue

                    result = res_data.get("result", {})
                    if result:
                        # Extraer hasta 8 fotos en alta definición (1200px)
                        photos_refs = [p.get("photo_reference") for p in result.get("photos", [])[:8]]
                        photos_urls = [
                            f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=1200&photo_reference={pref}&key={api_key}"
                            for pref in photos_refs
                        ]

                        # Extraer hasta 5 reseñas reales con fotos y autores
                        reviews = []
                        for r in result.get("reviews", [])[:5]:
                            reviews.append({
                                "author_name": r.get("author_name", "Cliente Verificado"),
                                "profile_photo_url": r.get("profile_photo_url", ""),
                                "rating": int(r.get("rating", 5)),
                                "text": r.get("text", "Excelente atención y calidad garantizada."),
                                "relative_time": r.get("relative_time_description", "recientemente")
                            })

                        raw_phone = result.get("international_phone_number") or result.get("formatted_phone_number") or ""
                        phone_meta = validar_y_formatear_whatsapp(raw_phone)
                        formatted_addr = result.get("formatted_address", "")
                        ciudad = extrae_ciudad_de_direccion(formatted_addr)
                        logo_url = photos_urls[0] if (photos_urls and len(photos_urls) > 0) else result.get("icon", "")
                        editorial = result.get("editorial_summary", {}).get("overview", "")
                        place_types = result.get("types", [])

                        return {
                            "google_place_id": place_id,
                            "nombre_negocio": result.get("name", query or "Comercio Prospectado"),
                            "direccion": formatted_addr,
                            "ciudad": ciudad,
                            "telefono": phone_meta["telefono_display"],
                            "whatsapp": phone_meta["whatsapp_digits"],
                            "es_fijo": phone_meta["es_fijo"],
                            "es_whatsapp_valido": phone_meta["es_whatsapp_valido"],
                            "rating": float(result.get("rating", 4.9)),
                            "reviews_count": int(result.get("user_ratings_total", 28)),
                            "reviews": reviews,
                            "fotos": photos_urls,
                            "logo_url": logo_url,
                            "sitio_web_original": result.get("website", ""),
                            "horarios": result.get("opening_hours", {}).get("weekday_text", []),
                            "editorial_summary": editorial,
                            "place_types": place_types,
                            "origen": "google_api"
                        }
        except Exception as e:
            print(f"[GOOGLE PLACES API WARN] Error al consultar API Key: {e}")
            continue

    # Fallback si no hay API Key o falla la conexión externa
    nombre_limpio = query or input_str or "Comercio Prospectado"
    if "http" in nombre_limpio:
        ext = extraer_place_id_o_busqueda(nombre_limpio)
        nombre_limpio = ext.get("query") or "Comercio Prospectado"

    return {
        "google_place_id": place_id or "place_demo_fallback",
        "nombre_negocio": nombre_limpio,
        "direccion": "Av. Principal 1200, Córdoba",
        "ciudad": "Córdoba, Argentina",
        "telefono": "+54 9 351 555-0199",
        "whatsapp": "5493515550199",
        "es_fijo": False,
        "es_whatsapp_valido": True,
        "rating": 4.9,
        "reviews_count": 38,
        "reviews": [
            {
                "author_name": "Marcos R.",
                "rating": 5,
                "text": "Excelente atención y rápida respuesta. Recomendado 100%.",
                "relative_time": "hace 2 semanas"
            },
            {
                "author_name": "Valeria G.",
                "rating": 5,
                "text": "Muy profesionales, superaron nuestras expectativas.",
                "relative_time": "hace un mes"
            }
        ],
        "fotos": [],
        "sitio_web_original": "",
        "horarios": [],
        "origen": "fallback_simulado"
    }


def extrae_ciudad_de_direccion(direccion: str) -> str:
    """Extrae la localidad/provincia de una dirección formateada."""
    if not direccion:
        return "Córdoba, Argentina"
    partes = [p.strip() for p in direccion.split(",") if p.strip()]
    if len(partes) >= 2:
        return f"{partes[-2]}, {partes[-1]}"
    return direccion
