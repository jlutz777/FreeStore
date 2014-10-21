import models.base
from models.customerfamily import CustomerFamily

import bottle
from bottle import HTTPError, HTTPResponse
from bottle.ext import sqlalchemy

import json
from bson import json_util

app = bottle.default_app()
plugin = sqlalchemy.Plugin(
    models.base.engine,
    keyword='db', # Keyword used to inject session database in a route (default 'db').
)

app.install(plugin)

@app.get('/')
def show(db):
    entity = db.query(CustomerFamily).first()
    if entity:
        jsonInfo = json.dumps({'id': entity.id, 'name': entity.email, 'city': entity.city, 'zip': entity.zip}, default=json_util.default)
        return HTTPResponse(jsonInfo, status=200,
                        header={'Content-Type': 'application/json'})
    return HTTPError(404, 'Entity not found.')

if __name__ == "main":
    bottle.run(server='gunicorn')