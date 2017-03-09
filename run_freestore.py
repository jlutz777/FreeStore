from gevent import monkey
monkey.patch_all(socket=False)

from forms.customer import CustomerForm
from forms.volunteervisit import VisitForm
import models.base
from models import CustomerFamily, Dependent, Visit, VolunteerVisit
from models import ShoppingCategory, ShoppingItem
from reporting.utils import availableReports, determineAndCreateReport
from utils.utils import *

from sqlalchemy import select
from sqlalchemy.sql import func

from beaker.middleware import SessionMiddleware
import bottle
from bottle import HTTPResponse, HTTPError, template
from bottle import static_file, TEMPLATE_PATH, hook
from bottle.ext import sqlalchemy
from cork import Cork
from cork.backends import SqlAlchemyBackend

from bson import json_util
from datetime import datetime, date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import logging
import smtplib
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
#app.catchall = False
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


def get_get(name, default=''):
    return bottle.request.GET.get(name, default).strip()


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


def get_first_of_next_month():
    now = datetime.utcnow()

    nextYear = now.year
    nextMonth = now.month+1

    if nextMonth == 13:
        nextMonth = 1
        nextYear += 1

    return date(nextYear, nextMonth, 1)


def send_registered_user_email(registered_user):
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    server = smtplib.SMTP()
    server.connect(smtp_host, smtp_port)
    server._host = 'smtp.gmail.com'
    server.starttls()
    user = os.environ.get("EMAIL_SENDER", "")
    passw = os.environ.get("EMAIL_PASSWORD", "")
    server.login(user, passw)
    tolist = [user, ]

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = ', '.join(tolist)
    msg['Subject'] = 'New volunteer'
    msg.attach(MIMEText('Someone new registered: ' + registered_user))
    server.sendmail(user, tolist, msg.as_string())


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


@app.get('/')
def checkout_search(db):
    authorize()

    bottle.BaseTemplate.defaults['page'] = '/'

    return template('checkout_search')


@app.get('/currentVisits')
def currentVisits(db):
    authorize()

    currentVisits = db.query(Visit).filter(Visit.checkout == None)  # noqa
    searchTerm = get_get('searchTerm')

    currentVisitsArray = []
    for visit in currentVisits:
        if visit.family is not None:
            for dependent in visit.family.dependents:
                if dependent.isPrimary:
                    fullName = dependent.getDict()["fullName"]
                    if searchTerm == '' or \
                            searchTerm.lower() in fullName.lower():
                        thisVisit = {}
                        timeInStore = td_format(datetime.now()-visit.checkin)
                        thisVisit["familyId"] = visit.family.id
                        thisVisit["visitId"] = visit.id
                        thisVisit["lastName"] = dependent.lastName
                        thisVisit["firstName"] = dependent.firstName
                        thisVisit["fullName"] = fullName
                        thisVisit["timeInStore"] = timeInStore
                        currentVisitsArray.append(thisVisit)
                        break

    currentVisitsArray = sorted(currentVisitsArray, key=itemgetter("lastName"))

    bottle.response.content_type = 'application/json'
    jsonInfo = json.dumps(currentVisitsArray, default=json_util.default)
    return jsonInfo


@app.get('/current_volunteers')
def current_volunteers(db):
    authorize()

    bottle.BaseTemplate.defaults['page'] = '/current_volunteers'

    return template('current_volunteers')


@app.get('/current_volunteers_data')
def current_volunteers_data(db):
    authorize()

    currentVisits = db.query(VolunteerVisit).filter(VolunteerVisit.checkout == None)  # noqa

    currentVisitsArray = []
    for visit in currentVisits:
        if visit.family is not None:
            for dependent in visit.family.dependents:
                if dependent.isPrimary:
                    thisVisit = {}
                    thisVisit["familyId"] = visit.family.id
                    thisVisit["visitId"] = visit.id
                    thisVisit["lastName"] = dependent.lastName
                    thisVisit["firstName"] = dependent.firstName
                    checkinStr = utc_time_to_local_time(visit.checkin)
                    thisVisit["checkin"] = checkinStr
                    currentVisitsArray.append(thisVisit)
                    break

    currentVisitsArray = sorted(currentVisitsArray, key=itemgetter("lastName"))

    bottle.response.content_type = 'application/json'
    jsonInfo = json.dumps(currentVisitsArray, default=json_util.default)
    return jsonInfo


@app.route('/customer', method=['GET', 'POST'])
@app.route('/customer/<customer_id:int>', method=['GET', 'POST'])
def customer(db, customer_id=None):
    authorize()

    bottle.BaseTemplate.defaults['page'] = '/customer'

    postData = bottle.request.POST
    form = CustomerForm(postData)
    post_url = get_redirect_url()
    visit_url_root = get_redirect_url('checkout')
    volunteer_url_root = get_redirect_url('volunteer_visit')
    checkin_url = get_redirect_url('checkin')
    visits = None
    volunteerVisits = None
    failedValidation = False

    if bottle.request.method == 'POST':
        family = None
        try:
            if form.validate():
                family = CustomerFamily()
                family.fromForm(customer_id, form)
                family = db.merge(family)

                db.flush()

                activeVisits = family.visits.filter(Visit.checkout == None)  # noqa
                hasNoActiveVisit = len(activeVisits.all()) == 0
                shouldCreateVisit = postData["checkinCust"] == "true"
                isCustomer = "isCustomer" in postData
                isVolunteer = "isVolunteer" in postData

                if hasNoActiveVisit and shouldCreateVisit and isCustomer:
                    visit = Visit()
                    visit.setStatus(status='checkin', family_id=family.id)
                    db.add(visit)
                next_url = get_redirect_url('checkin')

                db.commit()

                if isVolunteer:
                    next_url = get_redirect_url('customer/'+str(family.id))
                return bottle.redirect(next_url)
            else:
                failedValidation = True
        except HTTPError as herr:
            raise herr
        except HTTPResponse as hres:
            raise hres
        except Exception as ex:
            log.debug(ex)
            db.rollback()
            visits = family.visits
            volunteerVisits = family.volunteerVisits

    if customer_id is not None and \
       (failedValidation or bottle.request.method == 'GET'):
        customerQuery = db.query(CustomerFamily)
        fams = customerQuery.filter(CustomerFamily.id == customer_id)

        famCount = len(fams.all())
        if famCount == 0:
            return "No customers were found with this id"
        elif famCount > 1:
            return "There were multiple customers with the same id"

        if not failedValidation:
            form = CustomerForm(obj=fams[0])
        visits = fams[0].visits
        volunteerVisits = fams[0].volunteerVisits
    elif bottle.request.method == 'GET':
        # Mark one of the two dependents as primary
        form.dependents[0].isPrimary.data = True

    customerDict = {}
    customerDict['form'] = form
    customerDict['customer_id'] = customer_id
    customerDict['visits'] = visits
    customerDict['volunteers'] = volunteerVisits
    customerDict['post_url'] = post_url
    customerDict['checkin_url'] = checkin_url
    customerDict['visit_url_root'] = visit_url_root
    customerDict['volunteer_url_root'] = volunteer_url_root

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

    bottle.response.content_type = 'application/json'
    jsonInfo = json.dumps(depDict, default=json_util.default)

    return jsonInfo


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


def getCategoryTotals(db, visit, date_start, date_end):
    categoryTotals = select([ShoppingCategory.id, Dependent.id,
                             func.sum(ShoppingItem.quantity)])\
        .select_from(ShoppingItem.__table__
                     .join(ShoppingCategory).join(Dependent)
                     .join(Visit))\
        .where(Dependent.family_id == visit.family_id)\
        .where(Visit.checkout >= date_start)\
        .where(Visit.checkout < date_end)\
        .where(Visit.id != visit.id)\
        .group_by(ShoppingCategory.id, Dependent.id)
    reader = db.execute(categoryTotals)
    return reader.fetchall()


@app.route('/checkout/<visit_id:int>', method=['GET', 'POST'])
def checkout(db, visit_id):
    authorize()

    bottle.BaseTemplate.defaults['page'] = ''
    previousShoppingItems = {}

    categoryChoices = [cat.__dict__ for cat in db.query(ShoppingCategory)
                       .order_by('"order"').all()]
    post_url = get_redirect_url()

    visits = db.query(Visit).filter(Visit.id == visit_id)

    visitCount = len(visits.all())
    if visitCount == 0:
        return "No customer visits were found with this id"
    elif visitCount > 1:
        return "There were multiple customer visits with the same id"

    visit = visits[0]

    now = datetime.utcnow()
    firstOfMonth = date(now.year, now.month, 1)
    firstOfNextMonth = get_first_of_next_month()

    firstOfYear = date(now.year, 1, 1)
    firstOfNextYear = date(now.year+1, 1, 1)

    monthlyCategoryTotals = getCategoryTotals(db, visit, firstOfMonth, firstOfNextMonth)
    yearlyCategoryTotals = getCategoryTotals(db, visit, firstOfYear, firstOfNextYear)

    if bottle.request.method == 'POST':
        visit.fromPost(visit_id, bottle.request.POST, categoryChoices, db)

        # TODO: need to validate the posted data somehow
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
    checkoutDict["monthlyCategoryTotals"] = monthlyCategoryTotals
    checkoutDict["yearlyCategoryTotals"] = yearlyCategoryTotals
    checkoutDict["previousShoppingItems"] = previousShoppingItems
    timeInStore = td_format(datetime.now()-visit.checkin)
    checkoutDict["timeInStore"] = timeInStore

    return template('checkout', **checkoutDict)


@app.route('/volunteer_visit', method=['GET', 'POST'])
@app.route('/volunteer_visit/<volunteer_visit_id:int>', method=['GET', 'POST'])
def volunteer_visit(db, volunteer_visit_id=None):
    authorize()

    bottle.BaseTemplate.defaults['page'] = ''

    postData = bottle.request.POST
    getData = bottle.request.GET
    form = VisitForm(postData, getData)
    family = None

    if volunteer_visit_id is not None:
        form.id.data = volunteer_visit_id

    if bottle.request.method == 'POST':
        visit = None
        try:
            if form.validate():
                visit = VolunteerVisit()
                visit.fromForm(form)
                visit = db.merge(visit)

                db.flush()
                db.commit()

                next_url = get_redirect_url('checkin')
                return bottle.redirect(next_url)
        except HTTPError as herr:
            raise herr
        except HTTPResponse as hres:
            raise hres
        except Exception as ex:
            log.debug(ex)
            db.rollback()
    else:
        thisCheckin = None
        thisCheckout = None

        if volunteer_visit_id is not None:
            volunteerQuery = db.query(VolunteerVisit)
            volunteerVisit = volunteerQuery.filter(VolunteerVisit.id ==
                                                   volunteer_visit_id)[0]
            family = volunteerVisit.family
            form.family_id.data = family.id
            thisCheckin = volunteerVisit.checkin
            thisCheckout = volunteerVisit.checkout

        if thisCheckin is None:
            thisCheckin = datetime.now()
        form.checkin.data = utc_time_to_local_time(thisCheckin)

        if thisCheckout is None and getData.get('checkout', 'false') == 'true':
            thisCheckout = datetime.now()
        form.checkout.data = utc_time_to_local_time(thisCheckout)

    if family is None:
        customerQuery = db.query(CustomerFamily)
        family = customerQuery.filter(CustomerFamily.id ==
                                      form.family_id.data)[0]

    volunteerDict = {}
    volunteerDict['post_url'] = get_redirect_url('volunteer_visit')
    volunteerDict['family'] = family
    volunteerDict['form'] = form

    return template('volunteer_visit', **volunteerDict)


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
    error_message = ''

    try:
        loginDict = {}
        loginDict["success_redirect"] = success_url
        success = aaa.login(username, password, **loginDict)
        if not success:
            error_message = 'User name and/or password were incorrect.'
    # redirects throw an exception, so ignore
    except HTTPResponse:
        raise
    except Exception:
        error_message = 'Login had an unknown error.'
        log.exception(error_message)
    return template('login', error_message=error_message)


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


@app.route('/components/<folder>/<filename>', 'GET')
def components_static(folder, filename):
    """Get static component files for ractive templates and scripts.

    :param filename: the name of the css file
    :type filename: str
    :returns: The given css file
    :rtype: file

    """

    return static_file(filename,
                       root=os.path.join(MODULEPATH, 'views/components',
                                         folder))


@app.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    sorryMsg = '<p>Sorry, you are not authorized to perform this action</p>'
    sorryMsg += '<p><a href="/login">Login Here</a></p>'
    return sorryMsg


# Section: Admin pages
@app.get('/admin')
def admin(db):
    """Only admin users can see this"""
    authorize(fail_redirect='sorry_page', role='admin')

    bottle.BaseTemplate.defaults['page'] = '/admin'

    adminDict = {}
    adminDict["current_user"] = aaa.current_user.replace("\'", "\\'")
    adminDict["users"] = aaa.list_users()
    adminDict["roles"] = aaa.list_roles()

    categoryChoices = {s.id: {"id": s.id, "name": s.name,
                              "dailyLimit": s.dailyLimit,
                              "monthlyLimit": s.monthlyLimit,
                              "yearlyLimit": s.yearlyLimit,
                              "familyWideLimit": s.familyWideLimit,
                              "minAge": s.minAge,
                              "maxAge": s.maxAge,
                              "disabled": s.disabled,
                              "order": s.order,
                              "existing": True} for s
                       in db.query(ShoppingCategory)
                       .order_by('"order"')}

    adminDict["categories"] = json.dumps(categoryChoices,
                                         default=json_util.default).replace("\'", "\\'")

    return template('admin', adminDict)


@app.post('/create_user')
def create_user():
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        username = postd().username
        role = postd().role
        password = postd().password
        email_addr = postd().email
        description = postd().description
        aaa.create_user(username, role, password, email_addr, description)
        user = aaa.user(username)

        created_info = dict()
        created_info["name"] = user.username
        created_info["role"] = user.role
        created_info["email"] = user.email_addr
        created_info["description"] = user.description
        # You don't want to send the password back to the end user
        created_info["password"] = ""

        return dict(ok=True, msg='', user=created_info)
    except Exception as e:
        return dict(ok=False, msg=str(e))


@app.post('/edit_user')
def edit_user(db):
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        username = postd().username
        role = postd().role
        password = postd().password
        email = postd().email

        if password == '':
            password = None

        user = aaa.user(username)
        if user:
            user.update(role=role, pwd=password, email_addr=email)
            user = aaa.user(username)

        edited_info = dict()
        edited_info["name"] = user.username
        edited_info["role"] = user.role
        edited_info["email"] = user.email_addr
        edited_info["description"] = user.description
        # You don't want to send the password back to the end user
        edited_info["password"] = ""

        return dict(ok=True, msg='', user=edited_info)
    except Exception as e:
        log.debug(e)
        return dict(ok=False, msg=str(e))


@app.post('/delete_user/<username>', method=['DELETE'])
def delete_user(username):
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        aaa.delete_user(username)
        return dict(ok=True, msg='')
    except Exception as e:
        log.debug(e)
        return dict(ok=False, msg=str(e))


@app.post('/create_category')
def create_category(db):
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        cat = ShoppingCategory()
        cat.fromForm(postd())

        cat = db.merge(cat)
        db.flush()

        return dict(ok=True, msg='', category=cat.getDict())
    except Exception as e:
        log.debug(e)
        return dict(ok=False, msg=str(e))


@app.post('/edit_category')
def edit_category(db):
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        cat = db.query(ShoppingCategory).\
                filter(ShoppingCategory.id == postd().id)[0]
        cat.fromForm(postd())

        cat = db.merge(cat)
        db.flush()

        return dict(ok=True, msg='', category=cat.getDict())
    except Exception as e:
        log.debug(e)
        return dict(ok=False, msg=str(e))


'''
@app.post('/delete_category/<category_id:int>', method=['DELETE'])
def delete_category(db, category_id):
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        cat = db.query(ShoppingCategory).\
            filter(ShoppingCategory.id == category_id)[0]
        db.delete(cat)
        db.commit()
        return dict(ok=True, msg='', id=category_id)
    except Exception as e:
        log.debug(e)
        return dict(ok=False, msg=str(e))


@app.post('/create_role')
def create_role():
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        aaa.create_role(post_get('role'), post_get('level'))
        return dict(ok=True, msg='')
    except Exception as e:
        log.debug(e)
        return dict(ok=False, msg=e.message)


@app.post('/delete_role')
def delete_role():
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        aaa.delete_role(post_get('role'))
        return dict(ok=True, msg='')
    except Exception as e:
        log.debug(e)
        return dict(ok=False, msg=e.message)'''


@app.route('/customer/<customer_id:int>', method=['DELETE'])
def delete_customer(db, customer_id):
    authorize(fail_redirect='sorry_page', role='admin')

    try:
        customer = db.query(CustomerFamily).\
            filter(CustomerFamily.id == customer_id)[0]
        db.delete(customer)
        db.commit()
        return dict(ok=True, msg='')
    except Exception as e:
        log.debug(e)
        return dict(ok=False, msg=e.message)

# Section: Report pages


@app.get('/report')
@bottle.view('report')
def report_landing():
    authorize(fail_redirect='sorry_page', role='admin')

    bottle.BaseTemplate.defaults['page'] = '/report'

    return {'report_options': availableReports}


@app.get('/report/info/<report_num:int>')
def report_info(db, report_num):
    authorize(fail_redirect='sorry_page', role='admin')

    sess = bottle.request.session

    # Really simple date checking to avoid sql injection
    startDate = get_get("startDate", "01/01/1901")
    endDate = get_get("endDate", "01/01/2100")
    startDate = datetime.strptime(startDate, "%m/%d/%Y")
    endDate = datetime.strptime(endDate, "%m/%d/%Y")
    startDate = formatted_str_date(startDate)
    endDate = formatted_str_date(endDate)

    myReport = determineAndCreateReport(report_num, startDate, endDate)
    reportInfo = myReport.getDataAndHtml(db, sess)

    bottle.response.content_type = 'application/json'
    jsonInfo = json.dumps(reportInfo, default=json_util.default)

    return jsonInfo

# Section: Open pages (require no session)


@app.route('/volunteer_registration', method=['GET', 'POST'])
def volunteer_registration(db):
    postData = bottle.request.POST
    captcha_success = True
    form = CustomerForm(postData)
    form.isCustomer.data = False
    form.isVolunteer.data = True
    post_url = get_redirect_url('volunteer_registration')

    if bottle.request.method == 'POST':
        try:
            import requests
            captcha_url = "https://www.google.com/recaptcha/api/siteverify"
            captcha_rs = postData.get('g-recaptcha-response')
            params = {
                'secret': os.environ.get("CAPTCHA_KEY", ""),
                'response': captcha_rs
            }
            verify_rs = requests.get(captcha_url, params=params, verify=True)
            verify_rs = verify_rs.json()
            captcha_success = verify_rs.get("success", False)
            if captcha_success and form.validate():
                family = CustomerFamily()

                matchedFam = family.findMatch(form, db)
                if matchedFam is not None:
                    # Note: we aren't taking the data from the form right now
                    matchedFam.updatedFromRegistration(form)
                    family = matchedFam
                else:
                    family.fromForm(None, form)

                family = db.merge(family)

                db.flush()
                db.commit()

                if form.volunteer_date.data is not None:
                    visit = VolunteerVisit()
                    visit.family_id = family.id
                    visit.checkin = local_time_to_utc_time(form.volunteer_date.data)

                    db.add(visit)

                    db.flush()
                    db.commit()

                full_name = form.dependents[0].firstName.data
                full_name += " " + form.dependents[0].lastName.data
                send_registered_user_email(full_name)

                return 'Thanks for registering!'
        except HTTPError as herr:
            raise herr
        except HTTPResponse as hres:
            raise hres
        except Exception as ex:
            log.debug(ex)
            db.rollback()

    volDict = {}
    volDict['form'] = form
    volDict['post_url'] = post_url
    volDict['captcha_success'] = captcha_success
    return template('volunteer_registration', volDict)
