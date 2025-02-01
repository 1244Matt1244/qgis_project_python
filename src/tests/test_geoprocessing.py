import pytest
from qgis.testing import start_app, unittest
from qgis.core import QgsVectorLayer
from src.core.geoprocessing import clip_vector_layer
from src.core.utils import load_layer

start_app()  # Initialize QGIS

class TestGeoprocessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input_layer = load_layer("data/input.geojson")
        cls.overlay_layer = load_layer("data/overlay.geojson")

    def test_clip_success(self):
        clipped = clip_vector_layer(self.input_layer, self.overlay_layer)
        self.assertGreater(clipped.featureCount(), 0)

    def test_clip_invalid_input(self):
        with self.assertRaises(InvalidLayerError):
            clip_vector_layer(None, self.overlay_layer)
