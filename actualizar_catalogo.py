import json
import logging
import os
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

URL_ORIGEN = "https://cinubo.com/app/catalog.json"
RUTA_SALIDA = "catalog.json"


def actualizar_catalogo():
  logging.info("Iniciando actualización para Movie Engine Pro...")

  try:
    response = requests.get(URL_ORIGEN, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Soportar tanto si la raíz es una lista como si es un diccionario con 'items' o 'results'
    if isinstance(data, dict):
      items = data.get("items", data.get("results", []))
    elif isinstance(data, list):
      items = data
    else:
      items = []

    nuevo_catalogo = []

    for item in items:
      # Mapeo exacto compatible con los campos que lee Movie Engine Pro
      pelicula = {
          "id": str(item.get("id", "")),
          "title": item.get("title")
          or item.get("nombre")
          or "Sin título",
          "original_title": item.get("original_title")
          or item.get("title")
          or "",
          "overview": item.get("overview")
          or item.get("sinopsis")
          or "Sin descripción disponible.",
          "poster_path": item.get("poster_path") or item.get("imagen") or "",
          "backdrop_path": item.get("backdrop_path") or item.get("fondo") or "",
          "release_date": str(
              item.get("release_year") or item.get("anyo") or "2026"
          ),
          "type": item.get("type", "movie"),
          "language": "es",
          "link": item.get("url") or item.get("link") or "",
      }
      nuevo_catalogo.append(pelicula)

    # Movie Engine Pro puede aceptar un array directo o un objeto con la clave 'results'
    # Guardamos el formato de objeto con resultados para evitar fallos de lectura en WP
    output_data = {"results": nuevo_catalogo}

    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
      json.dump(output_data, f, ensure_ascii=False, indent=4)

    logging.info(
        f"Catálogo generado correctamente con {len(nuevo_catalogo)} elementos."
    )

  except Exception as e:
    logging.error(f"Error procesando el catálogo: {e}")


if __name__ == "__main__":
  actualizar_catalogo()
