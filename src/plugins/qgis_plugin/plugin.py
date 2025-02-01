from qgis.PyQt.QtWidgets import QDialog, QFileDialog
from qgis.core import QgsProject
from .resources import *

class BoulderCalculatorPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.dialog = QDialog()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'main.ui'), self.dialog)
        
        # Connect UI elements
        self.dialog.btnBrowseVector.clicked.connect(self.browse_vector)
        self.dialog.btnBrowseRaster.clicked.connect(self.browse_raster)

    def browse_vector(self):
        path, _ = QFileDialog.getOpenFileName(
            self.dialog, "Select Boulder Polygons", "", "Shapefiles (*.shp)")
        self.dialog.txtVectorPath.setText(path)

    def run_analysis(self):
        vector_path = self.dialog.txtVectorPath.text()
        raster_path = self.dialog.txtRasterPath.text()
        
        # Add results to QGIS map
        layer = QgsVectorLayer(output_path, "Boulder Results", "ogr")
        QgsProject.instance().addMapLayer(layer)
