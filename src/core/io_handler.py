import fiona
from qgis.core import QgsRasterLayer
from typing import List, Dict, Iterator
from pathlib import Path
from .utilities import logger
from .exceptions import InvalidCRSError, DataValidationError

class GeoDataManager:
    def __init__(self, vector_path: str, raster_path: str):
        self.vector_path = vector_path
        self.raster_path = raster_path
        self._validate_inputs()

    def _validate_inputs(self):
        """Validate CRS consistency and file integrity."""
        with fiona.open(self.vector_path) as src:
            vector_crs = src.crs.to_epsg()
        
        raster = QgsRasterLayer(self.raster_path)
        raster_crs = raster.crs().postgisSrid()
        
        if vector_crs != raster_crs:
            raise InvalidCRSError(
                f"CRS mismatch: Vector {vector_crs} vs Raster {raster_crs}"
            )

        if not raster.isValid():
            raise DataValidationError("Invalid raster file")

    def read_boulders(self) -> Iterator[Dict]:
        """Stream features with geometry validation."""
        with fiona.open(self.vector_path) as src:
            for feature in src:
                geom = feature['geometry']
                if geom['type'] != 'Polygon':
                    logger.warning(f"Invalid geometry type {geom['type']} for feature {feature['id']}")
                    continue
                
                yield {
                    'geometry': geom,
                    'properties': feature['properties']
                }

    def write_results(self, features: List[Dict], output_path: str):
        """Write results to new shapefile."""
        schema = {
            'geometry': 'Point',
            'properties': {
                'boulder_id': 'int',
                'length_m': 'float',
                'width_m': 'float',
                'height_m': 'float',
                'depth_avg': 'float'
            }
        }
        
        with fiona.open(
            output_path, 'w',
            driver='ESRI Shapefile',
            crs=self.vector_crs,
            schema=schema
        ) as dst:
            for feat in features:
                dst.write({
                    'geometry': {'type': 'Point', 'coordinates': feat['centroid']},
                    'properties': {
                        'boulder_id': feat['properties']['boulder_id'],
                        'length_m': round(feat['length_m'], 2),
                        'width_m': round(feat['width_m'], 2),
                        'height_m': round(feat['height_m'], 2),
                        'depth_avg': round(feat['properties']['depth_avg'], 1)
                    }
                })
