import logging
import yaml
from pathlib import Path
from typing import Dict, Any
from qgis.core import QgsVectorLayer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_layer(path: str) -> Optional[QgsVectorLayer]:
    """Load a vector layer with validation."""
    layer = QgsVectorLayer(path, Path(path).stem, "ogr")
    if not layer.isValid():
        logger.error(f"Failed to load layer: {path}")
        return None
    return layer

def load_config(config_path: str = "config.yml") -> Dict[str, Any]:
    """Load project configuration."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.warning("Config file not found, using defaults.")
        return {}
