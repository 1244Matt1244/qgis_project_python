class GeoprocessingError(Exception):
    """Base exception for geoprocessing failures."""
    pass

class InvalidLayerError(GeoprocessingError):
    """Raised when an invalid layer is provided."""
    pass
