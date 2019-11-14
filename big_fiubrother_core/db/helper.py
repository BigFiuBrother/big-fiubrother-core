from . import Base
from sqlalchemy import create_engine
import psycopg2


def create(username, password, host, database):
    con = psycopg2.connect(dbname='postgres', host=host, user=username, password=password)
    con.autocommit = True

    cursor = con.cursor()
    cursor.execute('CREATE DATABASE {};'.format(database))

    engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(username, password, host, database))
    Base.metadata.create_all(engine)

def drop(username, password, host, database):
    con = psycopg2.connect(dbname='postgres', host=host, user=username, password=password)
    con.autocommit = True

    cursor = con.cursor()
    cursor.execute('DROP DATABASE {};'.format(database))