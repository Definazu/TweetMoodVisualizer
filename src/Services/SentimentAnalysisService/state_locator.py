# state_locator.py
import json
from shapely.geometry import shape, Point

class StateLocator:
    def __init__(self, geojson_path):
        self.states = self._load_states(geojson_path)

    def _load_states(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
        return [
            (feature['properties']['NAME'], shape(feature['geometry']))
            for feature in data['features']
        ]

    def locate(self, lat, lon):
        point = Point(lon, lat)
        for name, geometry in self.states:
            if geometry.contains(point):
                return name
        return 'Unknown'