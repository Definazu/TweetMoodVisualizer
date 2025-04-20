# config.py
from pathlib import Path

class Config:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent.parent.parent
        self._validate_paths()
    
    def _validate_paths(self):
        self.db_path = self.base_dir / 'src' / 'Services' / 'DataBase' / 'DataTweets.db'
        self.sentiments_path = self.base_dir / 'Data' / 'sentiments.csv'
        self.states_path = self.base_dir / 'Data' / 'states.json'

        missing = []
        if not self.db_path.exists(): 
            missing.append(self.db_path)
        if not self.sentiments_path.exists(): 
            missing.append(self.sentiments_path)
        if not self.states_path.exists(): 
            missing.append(self.states_path)
        
        if missing:
            raise FileNotFoundError(
                "Missing files:\n" + "\n".join(f"• {p}" for p in missing)
            )