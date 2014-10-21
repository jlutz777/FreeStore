import bottle
from bottle import HTTPError
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
#engine = create_engine('postgresql://postgres:passw0rd@localhost:5432/freestore', echo=True)
engine = create_engine('postgres://root:j9t95X5qpwsbaaQm@172.17.42.1:49160/db', echo=True)

app = bottle.Bottle()
plugin = sqlalchemy.Plugin(
    engine,
    keyword='db', # Keyword used to inject session database in a route (default 'db').
)

app.install(plugin)

class CustomerFamily(Base):
    """Sqlalchemy deals model"""
    __tablename__ = "customerfamily"

    id = Column(Integer, primary_key=True)
    email = Column('email', Unicode)
    phone = Column('phone', Unicode, default=unicode(''))
    address = Column('address', Unicode)
    city = Column('city', Unicode)
    state = Column('state', Unicode)
    zip = Column('zip', Unicode)
    datecreated = Column('datecreated', DateTime)


@app.get('/')
def show(db):
    entity = db.query(CustomerFamily).first()
    if entity:
        return {'id': entity.id, 'name': entity.email}
    return HTTPError(404, 'Entity not found.')

if __name__ == "main":
    bottle.run(server='gunicorn')

app = bottle.default_app()