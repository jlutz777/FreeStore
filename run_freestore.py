from gevent import monkey
monkey.patch_all()

from forms.customer import CustomerForm
import models.base
from models import CustomerFamily, Dependent, Visit
from models import ShoppingCategory, ShoppingItem

from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import false

from beaker.middleware import SessionMiddleware
import bottle
from bottle import HTTPResponse, HTTPError, template
from bottle import static_file, TEMPLATE_PATH, hook
from bottle.ext import sqlalchemy
from cork import Cork
from cork.backends import SqlAlchemyBackend

from bson import json_util
from datetime import datetime, timedelta, date
import json
import logging
from operator import itemgetter
import os

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
    'session.auto': True
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


@hook('before_request')
def setup_request():
    bottle.request.session = bottle.request.environ['beaker.session']


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
        if visit.family is not None:
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

    currentVisitsArray = sorted(currentVisitsArray, key=itemgetter("lastName"))

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
    checkin_url = get_redirect_url('checkin')
    visits = None
    if bottle.request.method == 'POST':
        family = None
        try:
            if form.validate():
                family = CustomerFamily()
                family.fromForm(customer_id, form)
                family = db.merge(family)

                db.flush()

                if customer_id is None:
                    visit = Visit()
                    visit.setStatus(status='checkin', family_id=family.id)
                    db.add(visit)
                    next_url = get_redirect_url('checkin')
                else:
                    next_url = get_redirect_url('customer/' + str(family.id))

                db.commit()

                return bottle.redirect(next_url)
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
    customerDict['checkin_url'] = checkin_url
    customerDict['visit_url_root'] = visit_url_root

    return template('customer', **customerDict)


@app.route('/customersearch', method=['POST'])
def customersearch(db):
    authorize()

    searchTerm = "%" + post_get('searchTerm') + "%"
    deps = db.query(Dependent).filter(Dependent.isPrimary)\
        .filter(func.concat(Dependent.firstName, ' ', Dependent.lastName)
                .ilike(searchTerm))

    depDict = []
    for dep in deps:
        if dep.family_id is not None:
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

    checkout_url = get_redirect_url('checkin')
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

    now = datetime.utcnow()
    firstOfMonth = date(now.year, now.month, 1)

    categoryTotals = select([ShoppingCategory.id, Dependent.id,
                             func.sum(ShoppingItem.quantity)])\
        .select_from(ShoppingItem.__table__
                     .join(ShoppingCategory).join(Dependent)
                     .join(Visit))\
        .where(Dependent.family_id == visit.family_id)\
        .where(Visit.checkout > firstOfMonth)\
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
@bottle.view('login')
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
    sorryMsg = '<p>Sorry, you are not authorized to perform this action</p>'
    sorryMsg += '<p><a href="/login">Login Here</a></p>'
    return sorryMsg


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


@app.route('/customer/<customer_id>', method=['DELETE'])
def delete_customer(db, customer_id):
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        customer = db.query(CustomerFamily).\
            filter(CustomerFamily.id == customer_id)[0]
        db.delete(customer)
        db.commit()
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)

# Section: Report pages


@app.get('/report')
@bottle.view('report')
def report_landing():
    authorize(fail_redirect='sorry_page', role='admin')

    bottle.BaseTemplate.defaults['page'] = '/report'

    return {}


@app.get('/report/info/<report_num>')
def report_info(db, report_num):
    families = select([func.DATE(CustomerFamily.datecreated), func.count()])\
        .select_from(CustomerFamily.__table__)\
        .group_by(func.DATE(CustomerFamily.datecreated))\
        .order_by(func.DATE(CustomerFamily.datecreated))

    reader = db.execute(families)
    categoryTotals = reader.fetchall()

    bottle.request.session['report_info'] = categoryTotals
    return {}


@app.get('/report/graphdata/<report_num>')
def report_graph_data(db, report_num):
    authorize(fail_redirect='sorry_page', role='admin')

    categoryTotals = bottle.request.session['report_info']
    # Loop through and keep a running total to show the increase over time
    columns = ["date", "count"]
    results = []
    prevVal = 0

    for row in categoryTotals:
        prevVal = prevVal + row[1]
        results.append(dict(zip(columns, [row[0], prevVal])))

    import pandas as pd
    frame = pd.DataFrame().from_records(results, index="date",
                                        columns=["date", "count"])

    import vincent
    vis = vincent.Line(frame)
    vis.scales[0].type = 'time'
    vis.axis_titles(x='Date', y='Customers')
    vis.legend(title='Customer Count Over Time')

    return vis.to_json()
