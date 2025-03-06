# config.py
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.db_path = self.base_dir / 'DataBase' / 'DataTweets.db'
        self.sentiments_path = self.base_dir / 'Data' / 'sentiments.csv'
        self.states_path = self.base_dir / 'Data' / 'states.json'