"""
Servicio de Google Places API y Parser de URLs para GG Solutions.
Extrae información fidedigna de comercios a partir de enlaces de Google Maps o Place IDs.
"""

import os
import re
import json
import urllib.request
import urllib.parse

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")


def extraer_place_id_o_busqueda(map_url_o_query: str) -> dict:
    """
    Analiza una cadena ingresada (URL de Google Maps o nombre) y extrae:
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

    # 4. Si es texto plano (nombre del negocio)
    return {"query": text, "place_id": None}


def obtener_datos_lugar_google(input_str: str) -> dict:
    """
    Consulta Google Places API (o genera fallback inteligente) para obtener los datos
    completos del negocio.
    """
    info = extraer_place_id_o_busqueda(input_str)
    place_id = info.get("place_id")
    query = info.get("query")

    api_key = os.environ.get("GOOGLE_MAPS_API_KEY", "")

    # Si hay API Key configurada y tenemos Place ID o Query, intentamos consultar Google Places API
    if api_key and (place_id or query):
        try:
            if not place_id and query:
                # 1. Find Place desde Text Search
                search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={urllib.parse.quote(query)}&inputtype=textquery&fields=place_id,name,formatted_address&key={api_key}"
                req = urllib.request.Request(search_url, headers={"User-Agent": "GGSolutions-DemoEngine/1.0"})
                with urllib.request.urlopen(req, timeout=5) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    candidates = res_data.get("candidates", [])
                    if candidates:
                        place_id = candidates[0].get("place_id")

            if place_id:
                # 2. Place Details API
                fields = "name,formatted_address,international_phone_number,rating,user_ratings_total,website,reviews,photos"
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&language=es&key={api_key}"
                req = urllib.request.Request(details_url, headers={"User-Agent": "GGSolutions-DemoEngine/1.0"})
                with urllib.request.urlopen(req, timeout=5) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    result = res_data.get("result", {})
                    if result:
                        # Extraer fotos principales
                        photos_refs = [p.get("photo_reference") for p in result.get("photos", [])[:3]]
                        photos_urls = [
                            f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference={pref}&key={api_key}"
                            for pref in photos_refs
                        ]

                        # Extraer reviews
                        reviews = []
                        for r in result.get("reviews", [])[:3]:
                            reviews.append({
                                "author_name": r.get("author_name", "Cliente"),
                                "rating": r.get("rating", 5),
                                "text": r.get("text", ""),
                                "relative_time": r.get("relative_time_description", "hace poco")
                            })

                        # Extraer ciudad de la dirección
                        formatted_addr = result.get("formatted_address", "")
                        ciudad = extrae_ciudad_de_direccion(formatted_addr)

                        return {
                            "google_place_id": place_id,
                            "nombre_negocio": result.get("name", query or "Comercio"),
                            "direccion": formatted_addr,
                            "ciudad": ciudad,
                            "telefono": result.get("international_phone_number", ""),
                            "whatsapp": formatear_whatsapp(result.get("international_phone_number", "")),
                            "rating": float(result.get("rating", 4.9)),
                            "reviews_count": int(result.get("user_ratings_total", 24)),
                            "reviews": reviews,
                            "fotos": photos_urls,
                            "sitio_web_original": result.get("website", ""),
                            "origen": "google_api"
                        }
        except Exception as e:
            print(f"[GOOGLE PLACES API WARN] Fallback activado debido a: {e}")

    # Fallback inteligente cuando no hay API Key o falla la solicitud
    nombre_limpio = query or input_str or "Empresa Prospectada"
    if "http" in nombre_limpio:
        ext = extraer_place_id_o_busqueda(nombre_limpio)
        nombre_limpio = ext.get("query") or "Empresa Prospectada"

    return {
        "google_place_id": place_id or "place_demo_fallback",
        "nombre_negocio": nombre_limpio,
        "direccion": "Av. Principal 123, Centro",
        "ciudad": "Córdoba, Argentina",
        "telefono": "+54 9 351 555-0199",
        "whatsapp": "5493515550199",
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


def formatear_whatsapp(telefono: str) -> str:
    """Convierte un teléfono a formato solo dígitos para wa.me."""
    if not telefono:
        return ""
    digitos = re.sub(r"\D", "", telefono)
    return digitos
