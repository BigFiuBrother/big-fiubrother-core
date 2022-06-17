from shovel import task
import modules.db.helper as db_helper

DATABASE = 'big_fiubrother'
LOCALHOST = 'localhost'


@task
def create(username, password, host=LOCALHOST, database=DATABASE):
    db_helper.create(username=username,
                     password=password,
                     host=host,
                     database=database)


@task
def drop(username, password, host=LOCALHOST, database=DATABASE):
    db_helper.drop(username=username,
                   password=password,
                   host=host,
                   database=database)
