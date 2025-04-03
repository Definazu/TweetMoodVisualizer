# database.py
from sqlalchemy import create_engine, inspect, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path):
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.metadata = MetaData()
        self.inspector = inspect(self.engine)
        logger.info(f"💾 Database initialized: {db_path}")

    def table_exists(self, table_name):
        exists = self.inspector.has_table(table_name)
        logger.info(f"📦 Table '{table_name}' exists: {exists}")
        return exists

    def get_tweets(self, table_name):
        try:
            logger.info(f"🔍 Fetching tweets from '{table_name}'")
            Session = sessionmaker(bind=self.engine)
            session = Session()
            
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            result = session.execute(select(table)).fetchall()
            
            logger.info(f"📥 Retrieved {len(result)} tweets")
            return result
        except Exception as e:
            logger.error(f"🔥 Database error: {str(e)}")
            raise
        finally:
            session.close()