# Boulder Dimension Calculation using QGIS and Python 🗻🌊

[![CI/CD](https://github.com/1244Matt1244/boulder-dimension-calculation/actions/workflows/qgis_tests.yml/badge.svg)](https://github.com/1244Matt1244/boulder-dimension-calculation/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![QGIS 3.28+](https://img.shields.io/badge/QGIS-3.28%2B-orange.svg)](https://qgis.org/)

A production-ready toolkit for calculating boulder dimensions (length, width, height) from **Multibeam Echosounder (MBES)** data. Designed for geologists, marine researchers, and environmental scientists.

---

## Table of Contents
- [Key Features](#key-features)
- [Workflow Diagram](#workflow-diagram)
- [Installation](#installation)
  - [Docker Setup](#docker-setup)
  - [Manual Setup](#manual-setup)
- [Usage](#usage)
  - [Command Line](#command-line)
  - [QGIS Plugin](#qgis-plugin)
- [Data Specifications](#data-specifications)
- [Advanced Features](#advanced-features)
- [Testing & Validation](#testing--validation)
- [Contributing](#contributing)
- [License](#license)

---

## Key Features 🚀
| Feature | Description | Technology Used |
|---------|-------------|-----------------|
| **Automated Dimension Extraction** | Calculates length/width via polygon orientation and height via bathymetric raster analysis. | `GDAL`, `Shapely`, PCA |
| **Parallel Processing** | 4x faster processing using thread pools for large datasets. | `concurrent.futures`, `Dask` |
| **QGIS Integration** | Runs as standalone script or QGIS plugin with GUI. | `PyQGIS`, `Qt Designer` |
| **Error Resilience** | Auto-skipping invalid geometries with detailed error logging. | `logging`, `Sentry` (optional) |
| **3D Visualization** | Optional output for visualizing boulders in 3D space. | `Matplotlib`, `PyVista` |

---

## Workflow Diagram
```plaintext
MBES Data → Polygon Input → Centroid Calculation → PCA Orientation → Raster Sampling → Dimension Export
                         │                          │
                         └── Error Handling ←───────┘
```

---

## Installation

### Docker Setup (Recommended)
```bash
# 1. Build the QGIS-enabled container
docker build -t boulder-calculator .

# 2. Run processing (mount data to /data)
docker run -v /path/to/your/data:/data boulder-calculator \
  --input /data/boulders.shp \
  --raster /data/bathymetry.tif \
  --output /data/results.shp
```

### Manual Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install with PyQGIS support
pip install "qgis>=3.28" geopandas rasterio sentry-sdk
```

---

## Usage

### Command Line
```bash
python boulder_calculator.py \
  --input "path/to/boulders.shp" \
  --raster "path/to/bathymetry.tif" \
  --output "results.shp" \
  --workers 8  # Use 8 CPU cores
```

### QGIS Plugin
1. Copy the `boulder_plugin` folder to `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
2. Enable via **Plugins → Manage and Install Plugins**
3. Access via toolbar:  
   ![QGIS Plugin Interface](docs/images/plugin_ui.png)

---

## Data Specifications

### Input Requirements
| File Type | Fields | CRS | Example |
|-----------|--------|-----|---------|
| **Polygons (SHP)** | `boulder_id`, `geometry` | EPSG:4326 | [Sample Data](data/sample_boulders.zip) |
| **Raster (GeoTIFF)** | Bathymetric depth values | Must match vector CRS | [Sample Raster](data/sample_bathymetry.zip) |

### Output Schema
| Field | Type | Description |
|-------|------|-------------|
| `centroid` | Point | Boulder center (WGS84) |
| `length_m` | Float | Longest axis (meters) |
| `width_m` | Float | Shortest axis (meters) |
| `height_m` | Float | Elevation difference (meters) |
| `confidence` | Float | Data quality score (0-1) |

---

## Advanced Features

### 1. Machine Learning Filtering
```python
from sklearn.ensemble import IsolationForest

# Remove outlier boulders during post-processing
model = IsolationForest(contamination=0.05)
boulders["is_outlier"] = model.fit_predict(boulders[["length_m", "width_m"]])
clean_boulders = boulders[boulders["is_outlier"] != -1]
```

### 2. Cloud Integration
```bash
# Process directly from AWS S3
python boulder_calculator.py \
  --input "s3://marine-data/boulders.shp" \
  --raster "s3://marine-data/bathymetry.tif" \
  --output "s3://results-bucket/output.shp"
```

---

## Testing & Validation
```bash
# Run unit/integration tests
pytest tests/ --cov=src --cov-report=html

# Generate test coverage report
open htmlcov/index.html
```

**Validation Checks:**
- Polygon geometry validity (non-intersecting, closed rings)
- Raster resolution ≥ 1m/pixel
- CRS consistency between vector/raster

---

## Contributing

1. Fork the repository
2. Create feature branch:  
   `git checkout -b feat/new-algorithm`
3. Submit PR with:
   - Tests in `tests/`
   - Updated documentation
   - Type hints for new functions

---

## License
MIT License - see [LICENSE](LICENSE) for details.
```

---
