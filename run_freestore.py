import bottle
from bottle import route, run

@route('/')
def index():
    return '<h1>Hello Bottle!</h1>'

if __name__ == "__main__":
    bottle.run(server='gunicorn')

app = bottle.default_app()

