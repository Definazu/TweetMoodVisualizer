# state_locator.py
import json
import logging
from typing import List, Tuple, Union, Optional
from shapely.geometry import Polygon, MultiPolygon, Point

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StateLocator:
    def __init__(self, geojson_path: str):
        self.states = self._load_states(geojson_path)
        logger.info(f"🗺️ Loaded {len(self.states)} states")

    def _load_states(self, file_path: str) -> List[Tuple[str, Union[Polygon, MultiPolygon]]]:
        """Load state geometries from GeoJSON file"""
        try:
            with open(file_path) as f:
                data = json.load(f)

            states = []
            for state_code, geometries in data.items():
                if not isinstance(geometries, list):
                    logger.warning(f"⚠️ Invalid geometry format for {state_code}")
                    continue

                polygons = self._process_state_geometry(geometries)
                if not polygons:
                    logger.warning(f"⚠️ No valid geometry for {state_code}")
                    continue

                state_geometry = self._create_geometry(polygons)
                states.append((state_code.upper(), state_geometry))
                logger.debug(f"Added state {state_code} with {len(polygons)} polygon(s)")

            return states

        except Exception as e:
            logger.error(f"🔥 Error loading states: {str(e)}")
            raise

    def _process_state_geometry(self, geometries: list) -> List[Polygon]:
        """Process state geometry into list of Polygon objects"""
        polygons = []
        
        def handle_coordinate_element(element: list) -> list:
            """Handle coordinate pair or vertex list"""
            if len(element) >= 2 and isinstance(element[0], (int, float)):
                return [tuple(element[:2])]
            return []

        def create_polygon_from_coords(coords: list) -> Optional[Polygon]:
            """Create Polygon if valid coordinate sequence"""
            if len(coords) >= 3:
                try:
                    return Polygon(coords)
                except Exception as e:
                    logger.warning(f"Invalid polygon: {str(e)}")
            return None

        def process_nested_elements(elements: list) -> list:
            """Recursively process nested geometry elements"""
            collected_coords = []
            for elem in elements:
                result = process_element(elem)
                if isinstance(result, list) and result and isinstance(result[0], tuple):
                    collected_coords.extend(result)
                elif isinstance(result, list) and result and isinstance(result[0], Polygon):
                    polygons.extend(result)
            return collected_coords

        def process_element(element) -> list:
            """Main element processing dispatcher"""
            if not isinstance(element, list):
                return []
                
            if coord_pair := handle_coordinate_element(element):
                return coord_pair
                
            coords = process_nested_elements(element)
            if polygon := create_polygon_from_coords(coords):
                return [polygon]
                
            return []

        # Main processing loop
        for geometry in geometries:
            if elements := process_element(geometry):
                polygons.extend(elements)
        
        return [p for p in polygons if isinstance(p, Polygon)]

    def _create_geometry(self, polygons: List[Polygon]) -> Union[Polygon, MultiPolygon]:
        """Create final state geometry"""
        if len(polygons) == 1:
            return polygons[0]
        return MultiPolygon(polygons)

    def locate(self, lat: float, lon: float) -> str:
        """Find state code for coordinates"""
        try:
            point = Point(lon, lat)
            for code, geometry in self.states:
                if geometry.contains(point):
                    return code
            return 'Unknown'
        except Exception as e:
            logger.warning(f"⚠️ Location error: {str(e)}")
            return 'Unknown'

    def test_locations(self):
        """Test key locations"""
        test_cases = [
            (34.0522, -118.2437, "CA"),  # Los Angeles
            (40.7128, -74.0060, "NY"),  # New York
            (41.8781, -87.6298, "IL"),  # Chicago
            (21.3069, -157.8583, "HI"),  # Honolulu
            (58.3016, -134.4207, "AK"),  # Juneau
            (47.6062, -122.3321, "WA"),  # Seattle
            (25.7617, -80.1918, "FL"),  # Miami
            (0, 0, "Unknown"),           # Ocean
            (44.9671, -103.7716, "SD"), # South Dakota
            (31.9686, -99.9018, "TX")    # Texas
        ]

        logger.info("🧪 Starting location tests...")
        for lat, lon, expected in test_cases:
            result = self.locate(lat, lon)
            status = "✅" if result == expected else "❌"
            logger.info(f"{status} ({lat:.4f}, {lon:.4f}) => {result.ljust(6)} (expected: {expected})")


if __name__ == "__main__":
    locator = StateLocator("states.json")
    locator.test_locations()