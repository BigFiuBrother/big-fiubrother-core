from shovel import task
from big_fiubrother_core.db import Base
from sqlalchemy import create_engine
import psycopg2


@task
def setup(username, password, host='localhost'):
    con = psycopg2.connect(dbname='postgres', host=host, user=username, password=password)
    con.autocommit = True

    database = 'big_fiubrother'
    cursor = con.cursor()
    cursor.execute('CREATE DATABASE {};'.format(database))

    engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(username, password, host, database))
    Base.metadata.create_all(engine)