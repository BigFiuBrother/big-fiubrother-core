from shovel import task
from big_fiubrother_core.db import Base
from sqlalchemy import create_engine
import psycopg2

DATABASE = 'big_fiubrother'
LOCALHOST='localhost'

@task
def setup(username, password, host=LOCALHOST, database=DATABASE):
    con = psycopg2.connect(dbname='postgres', host=host, user=username, password=password)
    con.autocommit = True

    cursor = con.cursor()
    cursor.execute('CREATE DATABASE {};'.format(database))

    engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(username, password, host, database))
    Base.metadata.create_all(engine)

@task
def drop(username, password, host=LOCALHOST, database=DATABASE):
    con = psycopg2.connect(dbname='postgres', host=host, user=username, password=password)
    con.autocommit = True

    cursor = con.cursor()
    cursor.execute('DROP DATABASE {};'.format(database))