import pytest
from qgis.core import QgsGeometry
from src.core.calculator import BoulderDimensionCalculator
from src.core.exceptions import InvalidGeometryError

def test_pca_calculation():
    # Create square polygon
    wkt = "POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))"
    geometry = QgsGeometry.fromWkt(wkt)
    
    calculator = BoulderDimensionCalculator(None)
    result = calculator.calculate_dimensions(geometry)
    
    assert pytest.approx(result['length_m'], 0.01) == 1.41
    assert pytest.approx(result['width_m'], 0.01) == 1.41
    assert result['height_m'] == 0  # Mocked raster

def test_invalid_geometry():
    with pytest.raises(InvalidGeometryError):
        invalid_wkt = "POLYGON ((0 0, 1 1, 2 0))"  # Not closed
        geometry = QgsGeometry.fromWkt(invalid_wkt)
        BoulderDimensionCalculator(None).calculate_dimensions(geometry)
