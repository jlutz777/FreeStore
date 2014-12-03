from gevent import monkey
monkey.patch_all()

import models.base
from models import CustomerFamily, Dependent, ShoppingCategory, ShoppingItem, Visit
from forms.customer import CustomerForm, DependentForm

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms.fields import FormField

import bottle
from bottle import HTTPError, HTTPResponse, template, static_file, TEMPLATE_PATH
from bottle.ext import sqlalchemy
from cork import Cork, AAAException, AuthException
from cork.backends import SqlAlchemyBackend
from beaker.middleware import SessionMiddleware

import os
import json
from bson import json_util
import logging
from datetime import datetime, timedelta

MODULEPATH = os.path.dirname(__file__)
TEMPLATE_PATH.insert(0, os.path.join(MODULEPATH, "views"))

logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s',
                    level=logging.DEBUG)
log = logging.getLogger(__name__)

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
    
# Utilities

def postd():
    return bottle.request.forms

def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()

def td_format(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('day',         60*60*24),
        ('hour',        60*60),
        ('minute',      60)#,
        #('second',      1)
    ]

    strings=[]
    for period_name,period_seconds in periods:
        if seconds > period_seconds:
            period_value , seconds = divmod(seconds,period_seconds)
            if period_value == 1:
                strings.append("%s %s" % (period_value, period_name))
            else:
                strings.append("%s %ss" % (period_value, period_name))

    return ", ".join(strings)

# App Pages

#@app.route('/practice')
#def practice():
#    return template('practice')

@app.route('/', apply=[authorize()])
def main(db):
    return template('main', currentVisits=currentVisits)

@app.route('/currentVisits', apply=[authorize()])
def currentVisits(db):
    currentVisits = db.query(Visit).filter(Visit.checkout == None)
    currentVisitsArray = []
    for visit in currentVisits:
        for dependent in visit.family.dependents:
            if dependent.isPrimary:
                thisVisit = {}
                thisVisit["lastName"] = dependent.lastName
                thisVisit["timeInStore"] = td_format(datetime.now()-visit.checkin)
                currentVisitsArray.append(thisVisit)
                break
    jsonInfo = json.dumps(currentVisitsArray, default=json_util.default)
    return HTTPResponse(jsonInfo, status=200,
        header={'Content-Type': 'application/json'})

@app.route('/customer', method=['GET','POST'], apply=[authorize()])
@app.route('/customer/<customer_id>', method=['GET','POST'], apply=[authorize()])
def customer(db, customer_id=None):
    form = CustomerForm(bottle.request.POST)
    visits = None
    if bottle.request.method == 'POST':
        if form.validate():
            family = CustomerFamily()
            family.fromForm(customer_id, form)
            family = db.merge(family)
            db.commit()
            return bottle.redirect('/customer/' + str(family.id))
    elif customer_id is not None:
        fams = db.query(CustomerFamily).filter(CustomerFamily.id == customer_id)
        if len(fams.all()) != 1:
            return "Customer request bad"
        form = CustomerForm(obj=fams[0])
        visits = fams[0].visits
        
    return template('customer', form=form, customer_id=customer_id, visits=visits, post_url=bottle.request.path)

@app.route('/customersearch', method=['POST'], apply=[authorize()])
def customersearch(db):
    searchTerm = post_get('searchTerm')
    dependents = db.query(Dependent).filter(Dependent.lastName.like("%" + searchTerm + "%"))
    depDict = []
    for dep in dependents:
        depDict.append(dep.getDict())
    jsonInfo = json.dumps(depDict, default=json_util.default)
    return HTTPResponse(jsonInfo, status=200,
        header={'Content-Type': 'application/json'})
    #subq = sess.query(Dependent.firstName, Dependent.lastName).filter(Dependent.lastName.like("%" + searchTerm + "%").\
    #              group_by(Score.user_id).subquery()
    #sess.query(User).join((subq, subq.c.user_id==User.user_id)).order_by(subq.c.score_increase)

@app.route('/checkin', method=['POST'], apply=[authorize()])
def visit(db):
    customer_id = post_get('customer_id')
    visit = Visit()
    visit.setStatus(status='checkin', family_id=customer_id)
    db.add(visit)
    db.commit()
    return bottle.redirect('/customer/' + str(customer_id))

# Login/logout pages

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
    success_url = bottle.request.url.replace('http', 'https').replace('login', '')
    fail_url = bottle.request.url.replace('http', 'https')
    aaa.login(username, password, success_redirect=success_url, fail_redirect=fail_url)

@app.route('/logout')
def logout():
    login_url = bottle.request.url.replace('http', 'https').replace('logout', 'login')
    aaa.logout(success_redirect=login_url)

# General and Static pages
@app.route('/js/<filename>', 'GET')
def js_static(filename):
    """Get static javascript files.

    :param filename: the name of the javascript file
    :type filename: str
    :returns: The given js file
    :rtype: file

    """

    return static_file(filename, root=os.path.join(MODULEPATH, 'static/js'))

@app.route('/css/<filename>', 'GET')
def css_static(filename):
    """Get static css files.

    :param filename: the name of the css file
    :type filename: str
    :returns: The given css file
    :rtype: file

    """

    return static_file(filename, root=os.path.join(MODULEPATH, 'static/css'))

@app.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'

# Admin pages

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

# Setup stuff
# def setupDB():
#     corkBackend.roles.insert({'role': 'admin', 'level': 100})
#     corkBackend.roles.insert({'role': 'user', 'level': 50})
    
#     corkBackend.users.insert({
#             "username": "admin",
#             "email_addr": "admin@localhost.local",
#             "desc": "admin test user",
#             "role": "admin",
#             "hash": "cLzRnzbEwehP6ZzTREh3A4MXJyNo+TV8Hs4//EEbPbiDoo+dmNg22f2RJC282aSwgyWv/O6s3h42qrA6iHx8yfw=",
#             "creation_date": "2012-10-28 20:50:26.286723",
#             "last_login": "2012-10-28 20:50:26.286723"
#         })
#     assert len(corkBackend.roles) == 2
#     assert len(corkBackend.users) == 1

#setupDB()
