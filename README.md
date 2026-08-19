# PyPolData

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: MVP](https://img.shields.io/badge/Status-Alpha%20%2F%20MVP-orange.svg)]()

> **Acceso reproducible y transparente a datasets abiertos para Ciencia Política y Ciencias Sociales.**

PyPolData es una biblioteca en Python diseñada para reducir la fricción técnica y metodológica que enfrentan estudiantes e investigadores al localizar, descargar, procesar, documentar y citar datos politológicos y territoriales.

---

## 🎯 ¿Por qué PyPolData?

El análisis de datos en ciencias políticas suele enfrentarse a barreras innecesarias:
* Datasets dispersos en formatos pesados e ineficientes (e.g. GeoJSONs de +200 MB, CSVs sin tipado).
* Pérdida de trazabilidad y procedencia de los archivos.
* Dificultades para asegurar la reproducibilidad exacta en aulas y publicaciones académicas.

PyPolData resuelve esto combinando **formatos analíticos modernos (Parquet / GeoParquet)**, **distribución versionada en GitHub Releases**, **validación criptográfica de integridad (SHA-256)** y **caché local transparente**.

---

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/ahenaor/pypoldata.git
cd pypoldata

# Instalar en modo desarrollo / editable
pip install -e .
```

*Próximamente disponible vía PyPI:*
```bash
pip install pypoldata
```

---

## 💡 Uso Rápido

### 1. Listar datasets disponibles en el catálogo
```python
import pypoldata as ppd

# Explorar los datasets indexados
ppd.list_datasets()
```

### 2. Cargar un dataset analítico
Carga datos directamente a memoria (`pandas.DataFrame` o `geopandas.GeoDataFrame`). La primera llamada descarga el artefacto optimizado a tu caché local verificando su huella SHA-256; las siguientes llamadas son instantáneas y funcionan sin conexión.

```python
import pypoldata as ppd

# Cargar cartografía municipal de Colombia optimizada en GeoParquet
gdf = ppd.load("colombia_municipios")

# Visualizar
gdf.plot(color="#e0f3f8", edgecolor="#1b7837", linewidth=0.5)
```

---

## 📦 Datasets Disponibles en el MVP

| `dataset_id` | Descripción | Nivel / Unidad | Formato | Fuente |
| :--- | :--- | :--- | :--- | :--- |
| `colombia_municipios` | Cartografía vectorial de los 1.122 municipios de Colombia (simplificada y optimizada). | Municipio | GeoParquet (~3.5 MB) | DANE / IGAC |

---

## ⚙️ Arquitectura y Principios de Diseño

1. **Separación entre Código y Datos:** La versión del paquete (`v0.1.0`), las versiones de los datasets (`1.0.0`) y las etiquetas de release de datos (`data-v2026.08`) se gestionan de manera independiente.
2. **Integridad por Defecto:** Todo archivo descargado es validado contra su hash **SHA-256** registrado en el catálogo central. Si el archivo sufre alteraciones o descargas truncadas, se rechaza de forma atómica.
3. **Caché Inteligente:** Los archivos se almacenan localmente respetando los estándares del sistema operativo (vía `platformdirs` o la variable de entorno `PYPOLDATA_DATA_HOME`).
4. **Eficiencia Analítica:** Estandarización sobre **Parquet / GeoParquet** con compresión nativa, preservando tipos de datos y reduciendo el consumo de ancho de banda hasta en un 98%.

---

## 🛠️ Estructura del Repositorio

```text
pypoldata/
├── src/
│   └── pypoldata/
│       ├── __init__.py        # Exportación de la API pública (load, list_datasets)
│       ├── core.py            # Motor de caché, descarga atómica y validación SHA-256
│       └── catalog.json       # Manifiesto central con metadatos y hashes de datasets
├── notebook/
│   └── dev.ipynb              # Notebooks de prueba y exploración
├── pyproject.toml             # Configuración del paquete y dependencias
├── README.md
└── LICENSE
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Cada dataset distribuido mediante PyPolData conserva y documenta su propia licencia de origen (generalmente Creative Commons o datos abiertos gubernamentales).
