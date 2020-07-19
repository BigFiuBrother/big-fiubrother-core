from . import Base
from sqlalchemy import create_engine
from contextlib import contextmanager
import psycopg2


@contextmanager
def create_cursor(username, password, host, database='postgres'):
    connection = psycopg2.connect(database=database,
                                  host=host,
                                  user=username,
                                  password=password)

    connection.autocommit = True
    cursor = connection.cursor()

    yield cursor

    cursor.close()
    connection.close()


def create(username, password, host, database):
    with create_cursor(username, password, host) as cursor:
        # cursor.execute('CREATE DATABASE {};'.format(database))

        engine = create_engine(
            'postgresql+psycopg2://{}:{}@{}/{}'.format(username,
                                                       password,
                                                       host,
                                                       database))

        Base.metadata.create_all(engine)


def drop(username, password, host, database):
    with create_cursor(username, password, host) as cursor:
        cursor.execute('DROP DATABASE IF EXISTS {};'.format(database))
