from gevent import monkey
monkey.patch_all()

import models.base
from models import CustomerFamily, Dependent, Visit
from models import ShoppingCategory, ShoppingItem
from forms.customer import CustomerForm

from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import false

import bottle
from bottle import HTTPResponse, HTTPError, template
from bottle import static_file, TEMPLATE_PATH
from bottle.ext import sqlalchemy
from cork import Cork
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
sessionEncryptKey = os.environ.get("SESSION_KEY", "asdfghjkl")
corkBackend = SqlAlchemyBackend(postgresConn, initialize=False)
aaa = Cork(backend=corkBackend, email_sender='', smtp_url='')

app = bottle.default_app()
dbPlugin = sqlalchemy.Plugin(models.base.engine, keyword='db')
app.install(dbPlugin)

session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': sessionEncryptKey,
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}
sessionApp = SessionMiddleware(app, session_opts)

# Put the cork object on the base template
bottle.BaseTemplate.defaults['aaa'] = aaa
bottle.BaseTemplate.defaults['page'] = ''


# Section: Utilities


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
        ('minute',      60)
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 1:
                strings.append("%s %s" % (period_value, period_name))
            else:
                strings.append("%s %ss" % (period_value, period_name))

    if len(strings) == 0:
        strings.append("Less than one minute")

    return ", ".join(strings)


def get_redirect_url(relative_path=None):
    splitted = bottle.request.url.split('/')

    if relative_path is None:
        relative_path = '/'.join(splitted[3:])
    https_url = 'https://' + splitted[2] + '/' + relative_path

    return https_url


def authorize(fail_redirect='login', role='user'):
    full_fail_redirect = get_redirect_url(fail_redirect)
    aaa.require(fail_redirect=full_fail_redirect, role=role)


# Section: App Pages


@app.route('/')
def checkout_search(db):
    authorize()

    bottle.BaseTemplate.defaults['page'] = '/'

    return template('checkout_search', currentVisits=currentVisits)


@app.route('/currentVisits')
def currentVisits(db):
    authorize()

    currentVisits = db.query(Visit).filter(Visit.checkout == None)
    currentVisitsArray = []
    for visit in currentVisits:
        for dependent in visit.family.dependents:
            if dependent.isPrimary:
                thisVisit = {}
                timeInStore = td_format(datetime.now()-visit.checkin)
                thisVisit["familyId"] = visit.family.id
                thisVisit["visitId"] = visit.id
                thisVisit["lastName"] = dependent.lastName
                thisVisit["firstName"] = dependent.firstName
                thisVisit["timeInStore"] = timeInStore
                currentVisitsArray.append(thisVisit)
                break
    jsonInfo = json.dumps(currentVisitsArray, default=json_util.default)
    return HTTPResponse(jsonInfo, status=200,
                        header={'Content-Type': 'application/json'})


@app.route('/customer', method=['GET', 'POST'])
@app.route('/customer/<customer_id>', method=['GET', 'POST'])
def customer(db, customer_id=None):
    authorize()

    bottle.BaseTemplate.defaults['page'] = '/customer'

    form = CustomerForm(bottle.request.POST)
    post_url = get_redirect_url()
    visit_url_root = get_redirect_url('checkout')
    visits = None
    if bottle.request.method == 'POST':
        family = None
        try:
            if form.validate():
                family = CustomerFamily()
                family.fromForm(customer_id, form)
                family = db.merge(family)
                db.flush()
                customer_url = get_redirect_url('customer/' + str(family.id))
                db.commit()
                return bottle.redirect(customer_url)
        except HTTPResponse, hres:
            raise hres
        except HTTPError, herr:
            raise herr
        except Exception, ex:
            log.debug(ex)
            db.rollback()
            visits = family.visits
    elif customer_id is not None:
        customerQuery = db.query(CustomerFamily)
        fams = customerQuery.filter(CustomerFamily.id == customer_id)
        if len(fams.all()) != 1:
            return "Customer request bad"
        form = CustomerForm(obj=fams[0])
        visits = fams[0].visits
    else:
        # Mark one of the two dependents as primary
        form.dependents[0].isPrimary.data = True

    customerDict = {}
    customerDict['form'] = form
    customerDict['customer_id'] = customer_id
    customerDict['visits'] = visits
    customerDict['post_url'] = post_url
    customerDict['visit_url_root'] = visit_url_root

    return template('customer', **customerDict)


@app.route('/customersearch', method=['POST'])
def customersearch(db):
    authorize()

    searchTerm = "%" + post_get('searchTerm') + "%"
    deps = db.query(Dependent).filter(Dependent.isPrimary)\
        .filter(Dependent.lastName.like(searchTerm))
    depDict = []
    for dep in deps:
        depDict.append(dep.getDict())
    jsonInfo = json.dumps(depDict, default=json_util.default)
    return HTTPResponse(jsonInfo, status=200,
                        header={'Content-Type': 'application/json'})


@app.route('/checkin', method=['GET'])
def checkin(db):
    authorize()

    bottle.BaseTemplate.defaults['page'] = '/checkin'

    return template('checkin')


@app.route('/checkin', method=['POST'])
def visit(db):
    authorize()

    customer_id = post_get('customer_id')
    visit = Visit()
    visit.setStatus(status='checkin', family_id=customer_id)
    db.add(visit)
    db.commit()

    checkout_url = get_redirect_url('')
    return bottle.redirect(checkout_url)


@app.route('/checkout/<visit_id>', method=['GET', 'POST'])
def checkout(db, visit_id):
    authorize()

    bottle.BaseTemplate.defaults['page'] = ''
    previousShoppingItems = {}

    categoryChoices = [(s.id, s.name, s.dailyLimit, s.monthlyLimit,
                       s.familyWideLimit, s.minAge, s.maxAge) for s
                       in db.query(ShoppingCategory)
                       .filter(ShoppingCategory.disabled == false())
                       .order_by('"order"')]
    post_url = get_redirect_url()

    visits = db.query(Visit).filter(Visit.id == visit_id)
    if len(visits.all()) != 1:
        return "Visit request bad"
    visit = visits[0]

    oneMonthAgo = datetime.utcnow() - timedelta(days=30)

    categoryTotals = select([ShoppingCategory.id, Dependent.id,
                             func.sum(ShoppingItem.quantity)])\
        .select_from(ShoppingItem.__table__
                     .join(ShoppingCategory).join(Dependent)
                     .join(Visit))\
        .where(Dependent.family_id == visit.family_id)\
        .where(Visit.checkout > oneMonthAgo)\
        .where(Visit.id != visit.id)\
        .group_by(ShoppingCategory.id, Dependent.id)
    reader = db.execute(categoryTotals)
    categoryTotals = reader.fetchall()

    if bottle.request.method == 'POST':
        visit.fromPost(visit_id, bottle.request.POST, categoryChoices, db)

        #TODO: need to validate the posted data somehow
        if True:
            # Why do I have to filter above instead of doing a merge here?
            db.commit()

            return bottle.redirect(get_redirect_url(""))
        else:
            db.rollback()
    else:
        # Get the shopping items
        previousShoppingItems = visit.getShoppingItemsDict()

    checkoutDict = {}
    checkoutDict["visit"] = visit
    checkoutDict["post_url"] = post_url
    checkoutDict["categoryChoices"] = categoryChoices
    checkoutDict["categoryTotals"] = categoryTotals
    checkoutDict["previousShoppingItems"] = previousShoppingItems
    timeInStore = td_format(datetime.now()-visit.checkin)
    checkoutDict["timeInStore"] = timeInStore

    return template('checkout', **checkoutDict)


# Section: Login/logout pages


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
    success_url = get_redirect_url('')
    fail_url = get_redirect_url('login')

    loginDict = {}
    loginDict["success_redirect"] = success_url
    loginDict["fail_redirect"] = fail_url
    aaa.login(username, password, **loginDict)


@app.route('/logout')
def logout():
    login_url = get_redirect_url('login')
    aaa.logout(success_redirect=login_url)


# Section: General and Static pages

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


# Section: Admin pages


@app.get('/admin')
@bottle.view('admin')
def admin():
    """Only admin users can see this"""
    authorize(fail_redirect='sorry_page', role='admin')

    bottle.BaseTemplate.defaults['page'] = '/admin'

    adminDict = {}
    adminDict["current_user"] = aaa.current_user
    adminDict["users"] = aaa.list_users()
    adminDict["roles"] = aaa.list_roles()

    return adminDict


@app.post('/create_user')
def create_user():
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        aaa.create_user(postd().username, postd().role, postd().password)
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@app.post('/delete_user')
def delete_user():
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        aaa.delete_user(post_get('username'))
        return dict(ok=True, msg='')
    except Exception, e:
        print repr(e)
        return dict(ok=False, msg=e.message)


@app.post('/create_role')
def create_role():
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        aaa.create_role(post_get('role'), post_get('level'))
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@app.post('/delete_role')
def delete_role():
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        aaa.delete_role(post_get('role'))
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


# Section: Report pages


@app.get('/report')
@bottle.view('vega')
def report_landing():
    authorize(fail_redirect='sorry_page', role='admin')
    
    return {}


@app.get('/report/1')
@bottle.view('vega')
def example_report():
    authorize(fail_redirect='sorry_page', role='admin')
    
    import vincent
    list_data = [10,20,30,40,50]
    bar = vincent.Bar(list_data)
    return bar.to_json()
