from gevent import monkey
monkey.patch_all()

import models.base
from models import CustomerFamily, Dependent, ShoppingCategory, ShoppingItem, Visit
from forms.checkin_form import CheckinForm

import bottle
from bottle import HTTPError, HTTPResponse, template
from bottle.ext import sqlalchemy
from cork import Cork, AAAException, AuthException
from cork.backends import SqlAlchemyBackend
from beaker.middleware import SessionMiddleware

import os
import json
from datetime import datetime
from bson import json_util

postgresConn = os.environ.get("POSTGRES_CONN", "")
corkBackend = SqlAlchemyBackend(postgresConn, initialize=False)
aaa = Cork(backend=corkBackend, email_sender='', smtp_url='')
authorize = aaa.make_auth_decorator(fail_redirect="/login", role="user")

app = bottle.default_app()
dbPlugin = sqlalchemy.Plugin(models.base.engine, keyword='db')
app.install(dbPlugin)

session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'ASD342sad856vsd',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}
sessionApp = SessionMiddleware(app, session_opts)

def setupDB():
    corkBackend.roles.insert({'role': 'admin', 'level': 100})
    corkBackend.roles.insert({'role': 'user', 'level': 50})
    
    corkBackend.users.insert({
            "username": "admin",
            "email_addr": "admin@localhost.local",
            "desc": "admin test user",
            "role": "admin",
            "hash": "cLzRnzbEwehP6ZzTREh3A4MXJyNo+TV8Hs4//EEbPbiDoo+dmNg22f2RJC282aSwgyWv/O6s3h42qrA6iHx8yfw=",
            "creation_date": "2012-10-28 20:50:26.286723",
            "last_login": "2012-10-28 20:50:26.286723"
        })
    assert len(corkBackend.roles) == 2
    assert len(corkBackend.users) == 1
    
def postd():
    return bottle.request.forms

def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()

@app.route('/', apply=[authorize()])
def show(db):
    fam = db.query(CustomerFamily).first()
    visit_checkin = fam.visits[0].checkin.strftime("%m/%d/%Y %H:%M:%S")
    if fam:
        jsonInfo = json.dumps({'id': fam.id, 'name': fam.email, 'city': fam.city, 'zip': fam.zip, 'visit checkin': visit_checkin}, default=json_util.default)
        return HTTPResponse(jsonInfo, status=200,
                        header={'Content-Type': 'application/json'})
    return HTTPError(404, 'Entity not found.')

@app.route('/checkin', method=['GET','POST'], apply=[authorize()])
def checkin(db):
    form = CheckinForm(bottle.request.POST)
    return template('checkin', form=form)

@app.get('/login')
@bottle.view('login_form')
def login_form():
    """Serve login form"""
    return {}

@app.post('/login')
def login():
    """Authenticate users"""
    username = post_get('username')
    password = post_get('password')
    aaa.login(username, password, success_redirect='/', fail_redirect='/login')

@app.route('/logout')
def logout():
    aaa.logout(success_redirect='/login')
    
# Admin-only pages

@app.get('/admin')
@bottle.view('admin_page')
@authorize(role="admin", fail_redirect='/sorry_page')
def admin():
    """Only admin users can see this"""
    #aaa.require(role='admin', fail_redirect='/sorry_page')
    return dict(
        current_user = aaa.current_user,
        users = aaa.list_users(),
        roles = aaa.list_roles()
    )


@app.post('/create_user')
@authorize(role="admin", fail_redirect='/sorry_page')
def create_user():
    try:
        aaa.create_user(postd().username, postd().role, postd().password)
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@app.post('/delete_user')
@authorize(role="admin", fail_redirect='/sorry_page')
def delete_user():
    try:
        aaa.delete_user(post_get('username'))
        return dict(ok=True, msg='')
    except Exception, e:
        print repr(e)
        return dict(ok=False, msg=e.message)


@app.post('/create_role')
@authorize(role="admin", fail_redirect='/sorry_page')
def create_role():
    try:
        aaa.create_role(post_get('role'), post_get('level'))
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@app.post('/delete_role')
@authorize(role="admin", fail_redirect='/sorry_page')
def delete_role():
    try:
        aaa.delete_role(post_get('role'))
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)

@app.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'

#setupDB()