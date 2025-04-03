# state_locator.py
import json
from shapely.geometry import Polygon, MultiPolygon, Point
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StateLocator:
    def __init__(self, geojson_path):
        self.states = self._load_states(geojson_path)
        logger.info(f"🗺️ Loaded {len(self.states)} states")

    def _load_states(self, file_path):
        try:
            with open(file_path) as f:
                data = json.load(f)
            
            states = []
            for state_code, geometries in data.items():
                polygons = []
                for geometry in geometries:
                    try:
                        polygons.extend(self._parse_geometry(geometry))
                    except Exception as e:
                        logger.warning(f"⚠️ Error processing {state_code}: {str(e)}")
                
                if polygons:
                    state_name = self._get_state_name(state_code)
                    geometry = MultiPolygon(polygons) if len(polygons) > 1 else polygons[0]
                    states.append((state_name, geometry))
            
            return states
        except Exception as e:
            logger.error(f"🔥 Error loading states: {str(e)}")
            raise

    def _parse_geometry(self, geometry):
        polygons = []
        for item in geometry:
            if isinstance(item[0][0], list):  # MultiPolygon
                for polygon in item:
                    polygons.append(self._create_polygon(polygon))
            else:  # Single Polygon
                polygons.append(self._create_polygon(item))
        return polygons

    def _create_polygon(self, coords):
        try:
            shell = coords[0]
            holes = coords[1:] if len(coords) > 1 else []
            return Polygon(shell, holes)
        except Exception as e:
            logger.warning(f"⚠️ Invalid polygon: {str(e)}")
            raise

    def locate(self, lat, lon):
        point = Point(lon, lat)
        for name, geometry in self.states:
            if geometry.contains(point):
                return name
        return 'Unknown'

    def test_locations(self):
        test_points = [
            (34.0522, -118.2437, "California"),
            (40.7128, -74.0060, "New York"),
            (41.8781, -87.6298, "Illinois"),
            (0, 0, "Unknown")
        ]
        
        logger.info("🧪 Testing locations:")
        for lat, lon, expected in test_points:
            result = self.locate(lat, lon)
            status = "✅" if result == expected else "❌"
            logger.info(f"{status} ({lat}, {lon}) => {result} (expected: {expected})")


    def _get_state_name(self, code):
        state_names = {
            "AL": "Alabama",
            "AK": "Alaska",
            "AZ": "Arizona",
            "AR": "Arkansas",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "FL": "Florida",
            "GA": "Georgia",
            "HI": "Hawaii",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "IA": "Iowa",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "ME": "Maine",
            "MD": "Maryland",
            "MA": "Massachusetts",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MS": "Mississippi",
            "MO": "Missouri",
            "MT": "Montana",
            "NE": "Nebraska",
            "NV": "Nevada",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NY": "New York",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VT": "Vermont",
            "VA": "Virginia",
            "WA": "Washington",
            "WV": "West Virginia",
            "WI": "Wisconsin",
            "WY": "Wyoming",
            "DC": "District of Columbia"
        }
        return state_names.get(code, "Unknown")