from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2


class Database:

    def __init__(self, configuration):
        self.host = configuration['host']
        self.database_name = configuration['name'] 
        
        self.engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(configuration['user'], configuration['password'], self.host, self.database_name))
        self.session = sessionmaker(bind=self.engine)