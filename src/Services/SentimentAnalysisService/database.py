# database.py
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    def __init__(self, db_path):
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.engine)

    def get_tweets(self, table_name):
        session = self.Session()
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            return session.query(table).all()
        finally:
            session.close()