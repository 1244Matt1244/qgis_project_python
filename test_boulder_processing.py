import pytest
from SimplifiedSnippet import calculate_boulder_dimensions, validate_shapefile

def test_calculate_boulder_dimensions():
    boulder = {'id': 1, 'geometry': 'Polygon'}
    result = calculate_boulder_dimensions(boulder)
    
    assert result['length'] > 0
    assert result['width'] > 0
    assert result['height'] > 0

def test_validate_shapefile():
    # Replace with a path to a test shapefile
    shapefile_path = 'path_to_test_shapefile.shp'
    assert validate_shapefile(shapefile_path) is True

if __name__ == "__main__":
    pytest.main()
