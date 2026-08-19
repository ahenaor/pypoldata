import hashlib
import json
import os
import shutil
import tempfile
from importlib import resources
from pathlib import Path
import geopandas as gpd
import pandas as pd
import platformdirs
import requests

# 1. Configuración del repositorio remoto
GITHUB_OWNER = "ahenaor"
GITHUB_REPO = "pypoldata"


def get_data_home(data_home: str | None = None) -> Path:
    """Devuelve la ruta donde se guardará la caché local."""
    if data_home:
        return Path(data_home)
    env = os.getenv("PYPOLDATA_DATA_HOME")
    if env:
        return Path(env)
    return Path(platformdirs.user_cache_dir("pypoldata"))


def _verify_sha256(filepath: Path, expected_sha: str) -> bool:
    """Calcula el hash del archivo descargado y lo compara con el esperado."""
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest().lower() == expected_sha.lower()


def _load_catalog() -> dict:
    """Lee el archivo catalog.json empaquetado dentro de la librería."""
    ref = resources.files("pypoldata").joinpath("catalog.json")
    with ref.open("r", encoding="utf-8") as f:
        return json.load(f)


def _fetch_asset(
    dataset_id: str,
    version: str,
    release_tag: str,
    asset_name: str,
    expected_sha: str,
    *,
    force_download: bool = False,
    data_home: str | None = None,
) -> Path:
    """Descarga de forma segura y atómica el dataset a la caché local."""
    cache_dir = get_data_home(data_home) / dataset_id / version
    target_file = cache_dir / asset_name

    # Si ya existe en la caché y el hash es correcto, no lo descargamos de nuevo
    if target_file.exists() and not force_download:
        if _verify_sha256(target_file, expected_sha):
            return target_file

    cache_dir.mkdir(parents=True, exist_ok=True)
    url = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/download/{release_tag}/{asset_name}"

    print(f"Descargando {dataset_id} ({asset_name}) desde GitHub...")

    # Descargar a un archivo temporal primero para evitar archivos corruptos
    with tempfile.NamedTemporaryFile(delete=False, dir=cache_dir) as tmp_file:
        tmp_path = Path(tmp_file.name)
        with requests.get(url, stream=True, timeout=60) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=65536):
                tmp_file.write(chunk)

    # Validar integridad
    if not _verify_sha256(tmp_path, expected_sha):
        tmp_path.unlink()
        raise ValueError(
            f"Error de integridad: el hash SHA-256 de {asset_name} no coincide con el catálogo."
        )

    # Mover el archivo ya validado a su ubicación definitiva en caché
    shutil.move(str(tmp_path), str(target_file))
    return target_file


def list_datasets() -> list[dict]:
    """Lista todos los datasets disponibles en el catálogo."""
    catalog = _load_catalog()
    return [
        {
            "dataset_id": ds_id,
            "title": info["title"],
            "description": info["description"],
            "latest_version": info["latest_version"],
        }
        for ds_id, info in catalog["datasets"].items()
    ]


def load(
    dataset_id: str,
    version: str = "latest",
    *,
    data_home: str | None = None,
    force_download: bool = False,
):
    """Carga un dataset como DataFrame o GeoDataFrame."""
    catalog = _load_catalog()
    if dataset_id not in catalog["datasets"]:
        raise KeyError(f"El dataset '{dataset_id}' no está registrado en el catálogo.")

    ds_info = catalog["datasets"][dataset_id]
    v = ds_info["latest_version"] if version == "latest" else version
    if v not in ds_info["versions"]:
        raise ValueError(f"La versión '{v}' no existe para '{dataset_id}'.")

    meta = ds_info["versions"][v]
    data_meta = meta["artifacts"]["data"]

    # 1. Obtener la ruta del archivo (desde la caché o descargándolo)
    file_path = _fetch_asset(
        dataset_id=dataset_id,
        version=v,
        release_tag=meta["data_release"],
        asset_name=data_meta["asset_name"],
        expected_sha=data_meta["sha256"],
        force_download=force_download,
        data_home=data_home,
    )

    # 2. Cargar en memoria según el formato
    if data_meta.get("format") == "geoparquet":
        return gpd.read_parquet(file_path)
    return pd.read_parquet(file_path)