---


# Boulder Dimension Calculation using QGIS and Python

This project is designed to calculate the dimensions (length, width, and height) of boulders from **Multibeam Echosounder (MBES)** data using Python within a QGIS environment. The script processes polygons representing boulders and extracts depth information from bathymetric raster data (GeoTiff).

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Data Input and Output](#data-input-and-output)
- [Parallel Processing](#parallel-processing)
- [Logging](#logging)
- [Error Handling and Validation](#error-handling-and-validation)
- [Testing](#testing)
- [License](#license)

---

## Project Overview

This Python script automates the process of calculating boulder dimensions by processing a vector layer (polygons) and a raster layer (depth information). It returns the dimensions of each boulder, which can be used for further analysis in geology, marine research, or environmental projects.

The core operations include:
- Extracting centroids of boulders.
- Calculating the length, width, and height of boulders using the polygons and depth data.
- Storing the calculated values in an output shapefile.

## Features

- **Efficient Boulder Dimension Calculation**: Automatically calculates the length, width, and height of boulders.
- **Parallel Processing**: Optimized for processing multiple boulders concurrently.
- **Error Handling**: Built-in validation to ensure input data is correct.
- **Logging**: Comprehensive logging to track processing and errors.
- **QGIS Plugin-Ready**: Can be extended into a QGIS plugin for easier interaction.

## Requirements

To run this project, the following software and libraries are required:
- Python 3.x
- QGIS with PyQGIS environment or standalone Python environment
- Libraries:
  - `fiona`: For handling vector layers (shapefiles).
  - `geopandas`: For working with geospatial data.
  - `gdal`: For handling raster data.
  - `logging`: For logging processing and errors.
  - `concurrent.futures`: For parallel processing.
  - `pytest`: For testing (optional, for development).

## Installation

1. **Set up Python environment**: Install the required libraries.
   ```bash
   pip install fiona geopandas gdal pytest
   ```

2. **QGIS Setup** (if working in a QGIS environment):
   - Ensure that QGIS is installed and configure PyQGIS to access the environment.
   - Add the script to your QGIS Python console or set up as a QGIS plugin.

## Usage

1. **Prepare Input Files**:
   - **Shapefile (SHP)**: A vector layer representing boulder polygons.
   - **GeoTiff (TIF)**: A raster layer containing depth information.

2. **Running the Script**:
   Run the Python script from the command line or within QGIS:
   ```bash
   python SimplifiedSnippet.py
   ```

3. **Output**:
   - The script will generate an output shapefile with boulder centroids, dimensions (length, width, height), and other metadata.
   - The output will be saved in the same directory as the input shapefile.

## Data Input and Output

- **Input Data**:
  - **Shapefile (.shp)**: Contains polygons of boulders.
  - **GeoTiff (.tif)**: Bathymetric data representing depth values.
  
- **Output Data**:
  - A new shapefile containing centroids of the boulders and their dimensions (length, width, height).
  - Additional fields like `Poly_ID`, `Target ID`, and `Water depth`.

## Parallel Processing

To enhance performance, the script leverages Python's `concurrent.futures` to process multiple boulders simultaneously. This is particularly useful when working with large datasets.

Example:
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_boulder(boulder):
    # Your function to calculate the dimensions of a single boulder
    return calculate_boulder_dimensions(boulder)

def process_all_boulders(boulders):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_boulder, boulder) for boulder in boulders]
        results = []
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing boulder: {e}")
        return results
```

## Logging

The script logs each step of the process, including any errors, using the `logging` library. The log file is saved as `boulder_processing.log`.

Example:
```python
import logging

logging.basicConfig(filename='boulder_processing.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')
```

## Error Handling and Validation

To ensure valid input data, the script validates both the shapefile and the GeoTiff before processing. If any file is missing necessary fields or is incorrectly formatted, the process will stop, and an error will be logged.

Example:
```python
import fiona

def validate_shapefile(shapefile_path):
    with fiona.open(shapefile_path, 'r') as shp:
        if 'geometry' not in shp.schema:
            raise ValueError("Shapefile does not contain geometries.")
        if not len(shp):
            raise ValueError("Shapefile is empty.")
```

## Testing

Unit tests are provided to ensure the core functionalities of the script work as expected. Testing can be done using the `pytest` framework.

Example:
```python
import pytest

def test_boulder_dimensions():
    boulder = {'geometry': 'Polygon', 'id': 1}
    result = calculate_boulder_dimensions(boulder)
    
    assert result['length'] > 0
    assert result['width'] > 0
    assert result['height'] > 0
```

To run the tests:
```bash
pytest test_boulder.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---
