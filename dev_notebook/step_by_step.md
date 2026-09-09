# Manual de Procedimiento: Ampliación de Catálogo y Publicación en PyPolData

Este manual documenta el procedimiento paso a paso para procesar y optimizar nuevos datasets, alojar los artefactos binarios en GitHub Releases, registrar los metadatos en el catálogo interno y compilar/publicar una nueva versión de la biblioteca en PyPI.

---

## Flujo General del Proceso

```
[1. Curaduría & Optimización] ──> [2. GitHub Release] ──> [3. catalog.json] ──> [4. Bump Version] ──> [5. Build & Publish]
```

---

## 1. Curaduría y Optimización del Dataset

Los archivos crudos (especialmente GeoJSONs o CSVs pesados) deben transformarse a formatos analíticos de alto rendimiento (**Parquet** o **GeoParquet**) antes de su distribución.

### 1.1. Script de conversión y cálculo de Hash SHA-256

Crea o ejecuta un script de procesamiento (por ejemplo, dentro de `data_pipeline/<nombre_dataset>/transform.py`):

```python
import hashlib
from pathlib import Path
import geopandas as gpd
import pandas as pd

INPUT_FILE = "datos_originales.geojson"
OUTPUT_FILE = "nombre_dataset.parquet"

# Para datos geoespaciales
gdf = gpd.read_file(INPUT_FILE)

# Opcional: Simplificación topológica si es cartografía de alta resolución
if "geometry" in gdf.columns:
    gdf["geometry"] = gdf["geometry"].simplify(tolerance=0.001, preserve_topology=True)
    gdf.to_parquet(OUTPUT_FILE, compression="snappy", index=False)
else:
    # Para datos tabulares estándar
    df = pd.read_csv(INPUT_FILE)
    df.to_parquet(OUTPUT_FILE, compression="snappy", index=False)

# Cálculo de integridad SHA-256
sha256 = hashlib.sha256()
with open(OUTPUT_FILE, "rb") as f:
    for chunk in iter(lambda: f.read(65536), b""):
        sha256.update(chunk)

print(f"Archivo generado: {OUTPUT_FILE}")
print(f"SHA-256 calculado: {sha256.hexdigest()}")
```

---

## 2. Alojamiento del Binario en GitHub Releases

Los datos analíticos no deben versionarse en el historial de Git del repositorio principal. Se distribuyen como activos asociados a un Release.

1. Ve al repositorio en GitHub: `https://github.com/ahenaor/pypoldata/releases`.
2. Haz clic en **Draft a new release** (o edita el release del ciclo de datos actual, ej. `data-v2026.08`).
3. En **Tag version**, usa el estándar de releases de datos: `data-vYYYY.MM`.
4. En **Target**, selecciona la rama `main`.
5. En la sección **Attach binaries by dropping them here**, sube el archivo `.parquet` optimizado.
6. Publica el release (**Publish release**).

---

## 3. Registro en `catalog.json`

Abre el archivo `src/pypoldata/catalog.json` y añade la nueva entrada dentro del objeto `"datasets"`.

### Estructura estándar de entrada:

```json
{
  "catalog_version": "0.1.0",
  "datasets": {
    "nombre_dataset_nuevo": {
      "title": "Título descriptivo del dataset",
      "description": "Breve resumen del contenido y alcance analítico.",
      "latest_version": "1.0.0",
      "versions": {
        "1.0.0": {
          "data_release": "data-v2026.08",
          "artifacts": {
            "data": {
              "asset_name": "nombre_dataset.parquet",
              "format": "geoparquet",
              "sha256": "<HASH_SHA256_CALCULADO_EN_EL_PASO_1>"
            }
          },
          "source": {
            "name": "Entidad o Fuente Oficial",
            "url": "https://url-fuente-oficial.gov.co",
            "accessed_at": "2026-08-18"
          },
          "license": "CC-BY-4.0",
          "unit_of_analysis": "municipio",
          "geography": "Colombia",
          "time_coverage": "2022"
        }
      }
    }
  }
}
```

---

## 4. Incremento de Versión en `pyproject.toml`

Cada vez que se modifica el código fuente o el catálogo empaquetado, se debe incrementar la versión del paquete para poder subirlo a PyPI (PyPI rechaza sobrescrituras de una misma versión).

Abre `pyproject.toml` y actualiza el campo `version` siguiendo [Semantic Versioning](https://semver.org/):

```toml
[project]
name = "pypoldata"
version = "0.1.3"  # Incrementar patch para nuevos datasets o fixes
```

---

## 5. Validación Local

Antes de compilar y distribuir, comprueba en tu entorno local que el paquete reconoce el dataset y resuelve la descarga:

```bash
# 1. Instalar cambios locales en modo editable
pip install -e .

# 2. Ejecutar prueba rápida en consola interactiva de Python
python -c "import pypoldata as ppd; print(ppd.list_datasets()); df = ppd.load('nombre_dataset_nuevo'); print(df.head())"
```

---

## 6. Compilación y Publicación en PyPI

Sigue esta secuencia exacta de comandos en la terminal desde la raíz del proyecto con el entorno virtual activo:

```bash
# 1. Instalar/actualizar herramientas de empaquetado
pip install --upgrade build twine

# 2. Limpiar compilaciones previas
rm -rf dist/ build/ *.egg-info

# 3. Construir los artefactos (Wheel y tarball)
python -m build

# 4. Validar la integridad de los artefactos
twine check dist/*

# 5. Subir a PyPI
twine upload dist/* --verbose
```

> **Credenciales:**
> * **Username:** `__token__`
> * **Password:** `pypi-TU_API_TOKEN_COMPLETO`

---

## 7. Control de Versiones en Git

Registra los cambios en el repositorio de código:

```bash
# 1. Añadir archivos modificados
git add pyproject.toml src/pypoldata/catalog.json

# 2. Confirmar cambios
git commit -m "feat(catalog): add dataset <nombre_dataset> and bump version to 0.1.3"

# 3. Crear tag de versión de software
git tag -a v0.1.3 -m "Release v0.1.3"

# 4. Empujar commits y tags al remoto
git push origin main
git push origin v0.1.3
```

---

## Checklist de Publicación

- [ ] Dataset convertido a `.parquet` / `.geoparquet` y optimizado.
- [ ] Hash SHA-256 calculado sobre el binario final.
- [ ] Binario subido a los releases de GitHub bajo la etiqueta correspondiente.
- [ ] Metadatos y SHA-256 actualizados en `src/pypoldata/catalog.json`.
- [ ] Versión incrementada en `pyproject.toml`.
- [ ] Verificación local exitosa (`pip install -e .`).
- [ ] `twine check dist/*` en estado `PASSED`.
- [ ] Paquete subido exitosamente a PyPI.
- [ ] Tag de Git creado y sincronizado con GitHub.
