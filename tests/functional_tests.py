import sys
sys.path.append("..")

from webtest import TestApp
from nose.tools import with_setup
import run_freestore

app = TestApp(run_freestore.sessionApp)

def setup_func_user():
    app.post('/login', {'username': 'user', 'password': 'password'})

def setup_func_admin():
    app.post('/login', {'username': 'admin', 'password': 'admin'})

def teardown_func():
    app.get('/logout')
    app.reset()

@with_setup(setup_func_admin, teardown_func)
def test_admin():
    assert app.get('/admin').status == '200 OK'
    assert app.get('/report').status == '200 OK'
    assert app.get('/report/info/1').status == '200 OK'
    assert app.get('/report/graphdata/1').status == '200 OK'
    assert app.post('/create_role', {'role': 'stuff2', 'level': '5'}).status == '200 OK'
    assert app.post('/delete_role', {'role': 'stuff2'}).status == '200 OK'

@with_setup(setup_func_user, teardown_func)
def test_user_cannot_do_admin():
    assert app.get('/admin').status == '302 Found'
    assert app.get('/report').status == '302 Found'
    assert app.get('/').status == '200 OK'
    assert app.get('/currentVisits').status == '200 OK'
    assert app.get('/report/info/1').status == '302 Found'
    assert app.get('/report/graphdata/1').status == '302 Found'
    assert app.post('/create_role', {'role': 'stuff', 'level': '5'}).status == '302 Found'

def test_unauthenticated():
    assert app.get('/').status == '302 Found'
    assert app.get('/login').status == '200 OK'
    assert app.get('/admin').status == '302 Found'
    assert app.get('/report').status == '302 Found'
