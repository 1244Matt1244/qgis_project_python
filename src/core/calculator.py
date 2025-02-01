import numpy as np
from typing import Dict, Any
from qgis.core import QgsGeometry, QgsRasterLayer
from shapely.geometry import Polygon
from sklearn.decomposition import PCA

class BoulderAnalyzer:
    def __init__(self, raster_layer: QgsRasterLayer):
        self.raster = raster_layer
        self.band = 1  # Assuming depth in first band

    def _calculate_pca_dimensions(self, polygon: Polygon) -> Dict[str, float]:
        """Calculate length/width using PCA on polygon vertices."""
        coords = np.array(polygon.exterior.coords)
        pca = PCA(n_components=2)
        transformed = pca.fit_transform(coords)
        
        return {
            'length_m': np.ptp(transformed[:, 0]),
            'width_m': np.ptp(transformed[:, 1]),
            'orientation': np.degrees(np.arctan2(*pca.components_[0][::-1]))
        }

    def _calculate_height(self, geometry: QgsGeometry) -> float:
        """Extract min/max depth values from raster within polygon."""
        stats = self.raster.dataProvider().bandStatistics(
            self.band,
            QgsRasterBandStats.All,
            geometry.boundingBox(),
            int(geometry.boundingBox().area() ** 0.5)  # Adaptive sample count
        )
        return stats.maximumValue - stats.minimumValue

    def analyze_boulder(self, feature: Dict) -> Dict[str, Any]:
        """Process single boulder feature."""
        qgis_geom = QgsGeometry.fromWkt(feature['geometry'].wkt)
        shapely_poly = Polygon(qgis_geom.asMultiPolygon()[0][0])
        
        dimensions = self._calculate_pca_dimensions(shapely_poly)
        dimensions['height_m'] = self._calculate_height(qgis_geom)
        
        return {
            **feature['properties'],
            **dimensions,
            'centroid': qgis_geom.centroid().asWkt()
        }
