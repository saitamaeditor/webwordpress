import json
import logging
import os
import requests

# Configurar logs para monitorizar el proceso
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("actualizador_catalogo.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

URL_ORIGEN = "https://cinubo.com"
RUTA_SALIDA = "https://morvehtv.es"  # Cambia esta ruta según la ubicación de tu web


def actualizar_catalogo():
  logging.info("Iniciando la actualización del catálogo...")

  try:
    # 1. Descargar el JSON original
    response = requests.get(URL_ORIGEN, timeout=30)
    response.raise_for_status()
    data = response.json()
    logging.info("Catálogo original descargado correctamente.")

    nuevo_catalogo = []

    # 2. Iterar y transformar la estructura según las necesidades de tu web
    items = (
        data.get("items", data) if isinstance(data, dict) else data
    )  # Compatible con varios formatos JSON

    for item in items:
      # Puedes añadir filtros (por ejemplo, asegurar que esté en Castellano)
      pelicula_o_serie = {
          "id": item.get("id"),
          "title": item.get("title") or item.get("nombre"),
          "synopsis": item.get("overview")
          or item.get("sinopsis", "Sin descripción disponible."),
          "poster": item.get("poster_path") or item.get("imagen"),
          "backdrop": item.get("backdrop_path"),
          "year": item.get("release_year") or item.get("anyo"),
          "type": item.get("type", "movie"),  # 'movie' o 'series'
          "audio": "Castellano",
          "stream_url": item.get("url") or item.get("link"),
      }
      nuevo_catalogo.append(pelicula_o_serie)

    # Asegurar que el directorio de destino existe
    os.makedirs(os.path.dirname(RUTA_SALIDA), exist_ok=True)

    # 3. Guardar el archivo JSON transformado
    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
      json.dump(nuevo_catalogo, f, ensure_ascii=False, indent=4)

    logging.info(
        f"¡Catálogo actualizado con éxito! Total de elementos procesados:"
        f" {len(nuevo_catalogo)}"
    )

  except requests.exceptions.RequestException as e:
    logging.error(f"Error de red al descargar el catálogo: {e}")
  except Exception as e:
    logging.error(f"Error inesperado procesando el catálogo: {e}")


if __name__ == "__main__":
  actualizar_catalogo()