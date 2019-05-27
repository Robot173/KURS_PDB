
from flask import Flask, render_template, request
from ServiceLayer import ServiceOperations as Service
from constants import *
from flask import Flask, session, redirect, url_for, escape, request
from flask_session import Session
from functools import wraps
from flask import g, request, redirect, url_for


app = Flask(__name__, static_url_path='/static')
SESSION_TYPE = 'redis'
PERMANENT_SESSION_LIFETIME = 2400
app.config.from_object(__name__)
Session(app)


def get_role():
    return session.get('role', 'none')


def get_id():
    return session.get('id', 'none')


def login_required(role='tester', main_page_flag=False):
    def decorated_decorator(func):
        @wraps(func)
        def wrapped():
            if (session.get('role', 'none') == role) or main_page_flag:
                return func()
            return redirect(url_for('login_form', next=request.url))
        wrapped.__name__ = func.__name__
        return wrapped
    return decorated_decorator


@app.route('/login', methods=["POST", "GET"])
def login_form():
    message = None
    if request.method == "POST":
        parameters = request.form.to_dict()
        user = Service.get_objects('user', 'email', value=parameters['email'])
        if len(user) != 0:
            if user[0]['password'] == parameters['password']:
                print(user[0]['user_id'])
                session['id'] = user[0]['user_id']
                session['role'] = user[0]['role']
                return redirect(url_for('main_page', next=request.url))
            else:
                message = "Неверная пара логин/пароль!"
        else:
            message = "Форма не заполнена!"
    return render_template('src/login.html', messages=message)


@app.route('/')
@login_required(main_page_flag=True)
def main_page():
    role = get_role()
    if role == 'developer':
        return render_template('src/developer_index.html')
    elif role == 'tester':
        return render_template('src/tester_index.html')
    elif role == 'admin':
        return render_template('src/admin_index.html')
    else:
        return redirect(url_for('login_form', next=request.url))


@app.route('/logout')
@login_required(main_page_flag=True)
def logout_page():
    session.pop('role', 'none')
    session.pop('id', 'none')
    return redirect(url_for('login_form', next=request.url))


@app.route('/register', methods=["POST", "GET"])
def register_page():
    message = None
    if request.method == "POST":
        parameters = request.form.to_dict()
        print(parameters['role'])
        code, message = Service.registration(parameters, 'add', role=parameters['role'])
    return render_template('src/register.html', messages=message)


@app.route('/add_device', methods=["POST", "GET"])
@login_required(role='developer')
def add_device_form():
    message = None
    users = Service.get_objects('user', 'id', value=get_id())
    if request.method == "POST":
        parameters = request.form.to_dict()
        code, message = Service.device_management(parameters, 'add', get_role())
    return render_template('src/add_device.html', user=users[0], messages=message, device_types=DEVICE_TYPES)


@app.route('/change_device', methods=["POST", "GET"])
@login_required(role='developer')
def change_device_forms():
    id_user = session.get('id', 'none')
    users = Service.get_objects('user', 'id', value=id_user)
    if request.method == "POST":
        parameters = request.form.to_dict()
        device_id = parameters['device_id']
        device = Service.get_objects('device', 'id', device_id)
        if 'device_type' in parameters:
            code, message = Service.device_management(parameters, 'edit', get_role())
            return render_template('src/developer_index.html', messages=message)
        return render_template('src/change_device.html', device=device[0], user=users[0], device_types=DEVICE_TYPES)
    devices = Service.get_objects('device', 'author_id', id_user)
    return render_template('src/get_device.html', devices=devices)


@app.route('/delete_device', methods=["POST", "GET"])
@login_required(role='developer')
def delete_device_form():
    role = get_role()
    if request.method == "POST":
        parameters = request.form.to_dict()
        code, message = Service.device_management(parameters, 'delete', get_role())
        return render_template('src/developer_index.html', messages=message)
    devices = Service.get_objects('device', 'author_id', get_id())
    return render_template('src/delete_device.html', devices=devices)


@app.route('/add_test', methods=["POST", "GET"])
@login_required(role='developer')
def add_test_form():
    message = None
    devices = Service.get_objects('device', 'author_id', get_id())
    if request.method == "POST":
        parameters = request.form.to_dict()
        code, message = Service.test_management(parameters, 'add', get_role())
    return render_template('src/add_test.html', devices=devices, messages=message, test_types=DEVICE_TYPES)


@app.route('/change_test', methods=["POST", "GET"])
@login_required(role='developer')
def change_test_forms():
    id_user = get_id()
    message = None
    if request.method == "POST":
        parameters = request.form.to_dict()
        devices = Service.get_objects('device', 'author_id', id_user)
        if 'requirements' in request.form:
            code, message = Service.test_management(parameters, 'edit', get_role())
            return render_template('src/developer_index.html', messages=message)
        elif 'name' in request.form:
            tests = Service.get_objects('test', 'name_title', parameters['name'])
            code, test = Service.find_specific_test(tests, parameters['title'])
        else:
            test = Service.get_objects('test', 'id', parameters['test_id'])[0]
        return render_template('src/change_test.html', test=test, devices=devices)
    tests = Service.get_objects('test', 'author', id_user)
    return render_template('src/get_test_change.html', tests=tests)


@app.route('/delete_test', methods=["POST", "GET"])
@login_required(role='developer')
def delete_test_form():
    if request.method == "POST":
        parameters = request.form.to_dict()
        if 'name' in request.form:
            tests = Service.get_objects('test', 'name_title', parameters['name'])
            code, test = Service.find_specific_test(tests, parameters['title'])
        else:
            test = Service.get_objects('test', 'id', parameters['test_id'])[0]
        code, message = Service.test_management(test, 'delete', get_role())
        return render_template('src/developer_index.html', messages=message)
    tests = Service.get_objects('test')
    return render_template('src/get_test_delete.html', tests=tests)


@app.route('/find_tests', methods=["POST", "GET"])
@login_required(role='tester')
def find_tests():
    if request.method == "POST":
        devices = Service.get_objects('user')
        test_id = request.form['test_id']
        test = Service.get_objects('test', 'id', test_id)
        if 'title' in request.form:
            code, message = Service.update_to_db(request.form, 'test')
            return render_template('src/developer_index.html', messages=message)
        return render_template('src/show_test.html', test=test, devices=devices)
    tests = Service.get_objects('test', 'author', session.get('id', 'none'))
    return render_template('src/get_tests.html', tests=tests)







@app.route('/add_user', methods=["POST", "GET"])
@login_required(role='developer')
def register_form():
    message = None
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        message = Service.add_user(email, password)
    return render_template('src/register.html', messages=message)


@app.route('/get_devices_by_user', methods=["POST", "GET"])
@login_required(role='developer')
def show_devices_form():
    if request.method == "POST":
        user = Service.get_user(request.form['InputUser'])
        devices = Service.read_devices_by_user(user[0][0])
        return render_template('src/show_devices.html', devices=devices, user=user[0])
    users = Service.get_users()
    return render_template('src/get_user.html', users=users)


@app.route('/test', methods=["POST", "GET"])
def some_form():
    pass


if __name__ == '__main__':
    app.run()


