from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import psycopg2

class Database:

    def __init__(self, configuration):
        self.username = configuration['username']
        self.password = configuration['password']
        self.host = configuration['host']
        self.database = configuration['database']

        self.engine = create_engine(
            'postgresql+psycopg2://{}:{}@{}/{}'.format(self.username,
                                                       self.password,
                                                       self.host,
                                                       self.database))

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add(self, mapped_object):
        self.session.add(mapped_object)
        self.session.commit()

    def get(self, db_class, id):
        return self.session.query(db_class).get(id)

    def update(self):
        self.session.commit()

    def delete(self, db_class, condition):
        self.session.query(db_class).filter(condition).delete()
        self.session.commit()

    @contextmanager
    def transaction(self):
        with self.session.begin(subtransactions=True):
            yield

    def truncate_all(self):
        meta = MetaData(bind=self.engine, reflect=True)
        con = self.engine.connect()

        trans = con.begin()

        con.execute('SET CONSTRAINTS ALL DEFERRED;')
        for table in meta.sorted_tables:
            con.execute(table.delete())
        con.execute('SET CONSTRAINTS ALL IMMEDIATE;')

        trans.commit()

    def close(self):
        self.session.close()
        self.engine.dispose()
