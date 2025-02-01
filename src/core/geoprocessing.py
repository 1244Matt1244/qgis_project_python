from qgis.core import (
    QgsVectorLayer,
    QgsProcessingException,
    QgsSpatialIndex,
    QgsFeature
)
from qgis.analysis import QgsNativeAlgorithms
from typing import Optional, Tuple
import processing
from .exceptions import GeoprocessingError
from .utils import logger

# Initialize QGIS algorithms
processing.initialize()

def clip_vector_layer(
    input_layer: QgsVectorLayer, 
    overlay_layer: QgsVectorLayer
) -> Optional[QgsVectorLayer]:
    """Clip a vector layer using another layer as a mask."""
    try:
        params = {
            'INPUT': input_layer,
            'OVERLAY': overlay_layer,
            'OUTPUT': 'memory:'
        }
        result = processing.run("native:clip", params)
        if not result['OUTPUT'].isValid():
            raise GeoprocessingError("Clipping failed: Invalid output layer.")
        return result['OUTPUT']
    except QgsProcessingException as e:
        logger.error(f"Clip error: {str(e)}")
        raise GeoprocessingError(str(e))

def create_spatial_index(layer: QgsVectorLayer) -> QgsSpatialIndex:
    """Create a spatial index for faster spatial queries."""
    index = QgsSpatialIndex()
    for feature in layer.getFeatures():
        index.addFeature(feature)
    return index
