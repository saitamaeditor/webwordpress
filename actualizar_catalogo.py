import json
import logging
import os
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

URL_ORIGEN = "https://cinubo.com"
RUTA_SALIDA = "catalog.json"


def actualizar_catalogo():
  logging.info("Iniciando la actualización para Movie Engine Pro...")

  try:
    response = requests.get(URL_ORIGEN, timeout=30)
    response.raise_for_status()
    data = response.json()

    items = data.get("items", data) if isinstance(data, dict) else data
    nuevo_catalogo = []

    for item in items:
      # Estructura adaptada a los campos estándar que lee Movie Engine Pro
      pelicula = {
          "title": item.get("title") or item.get("nombre"),
          "original_title": item.get("original_title") or item.get("title"),
          "overview": item.get("overview") or item.get("sinopsis", ""),
          "poster_path": item.get("poster_path") or item.get("imagen"),
          "backdrop_path": item.get("backdrop_path") or item.get("fondo"),
          "release_date": item.get("release_year") or item.get("anyo"),
          "type": item.get("type", "movie"),
          "language": "es",
          "link": item.get("url") or item.get("link"),
      }
      nuevo_catalogo.append(pelicula)

    # Movie Engine Pro a veces requiere que el JSON sea un objeto con una clave principal o un array directo.
    # Si el plugin espera un objeto contenedor, usa la estructura de abajo:
    output_data = {"results": nuevo_catalogo}

    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
      json.dump(output_data, f, ensure_ascii=False, indent=4)

    logging.info(
        f"Catálogo generado con éxito: {len(nuevo_catalogo)} elementos."
    )

  except Exception as e:
    logging.error(f"Error procesando el catálogo: {e}")


if __name__ == "__main__":
  actualizar_catalogo()
