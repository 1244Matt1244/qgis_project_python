import click
from concurrent.futures import ThreadPoolExecutor
from src.core.io_handler import GeoDataManager
from src.core.calculator import BoulderAnalyzer
from src.core.utilities import configure_logging

@click.command()
@click.option('--input', required=True, help='Input shapefile path')
@click.option('--raster', required=True, help='Bathymetry raster path')
@click.option('--output', default='output.shp', help='Output shapefile path')
@click.option('--workers', default=4, help='Parallel workers count')
def main(input: str, raster: str, output: str, workers: int):
    """Calculate boulder dimensions from MBES data."""
    configure_logging()
    
    try:
        data_manager = GeoDataManager(input, raster)
        analyzer = BoulderAnalyzer(QgsRasterLayer(raster))
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(analyzer.analyze_boulder, feature)
                for feature in data_manager.read_boulders()
            ]
            
            results = [f.result() for f in futures]
            data_manager.write_results(results, output)
            
    except Exception as e:
        click.echo(f"Processing failed: {str(e)}", err=True)
        raise

if __name__ == '__main__':
    main()
