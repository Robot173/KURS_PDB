from flask import Flask, render_template, request
from ServiceLayer import ServiceOperations as Service
from constants import *
from functools import wraps
from flask import g, request, redirect, url_for
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__, static_url_path='/static')


def login_required(f, role='tester', main_page_flag=False):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            if (session['role'] == role) or main_page_flag:
                return f(*args, **kwargs)
        return redirect(url_for('login', next=request.url))
    return decorated_function


@app.route('/login', methods=["POST", "GET"])
def login_form():
    if request.method == "POST":
        Service.registration('read', request.post)
    return render_template('src/login.html')


@app.route('/')
@login_required(main_page_flag=True)
def main_page_developer():
    if session['role'] == 'developer':
        return render_template('src/developer_index.html')


@app.route('/add_device', methods=["POST", "GET"])
@login_required(role='developer')
def add_device_form():
    message = None
    users = Service.get_objects('user')
    if request.method == "POST":
        parameters = request.form.to_dict()
        code, message = Service.device_management(parameters, 'add')
    return render_template('src/add_device.html', users=users, messages=message, device_types=DEVICE_TYPES)


@app.route('/change_device', methods=["POST", "GET"])
@login_required(role='developer')
def change_device_forms():
    if request.method == "POST":
        parameters = request.form.to_dict()
        users = Service.get_objects('user')
        device_id = parameters['device_id']
        device = Service.get_objects('device', 'id', device_id)
        if 'device_type' in parameters:
            code, message = Service.update_to_db(parameters, 'device')
            return render_template('src/developer_index.html', messages=message)
        return render_template('src/change_device.html', device=device, users=users, device_types=DEVICE_TYPES)
    devices = Service.get_objects('device')
    return render_template('src/get_device.html', devices=devices)


@app.route('/delete_device', methods=["POST", "GET"])
@login_required(role='developer')
def delete_device_form():
    if request.method == "POST":
        parameters = request.form.to_dict()
        message = Service.delete_object(parameters, 'device')
        return render_template('src/developer_index.html', messages=message)
    devices = Service.get_objects('device')
    return render_template('src/delete_device.html', devices=devices)


@app.route('/add_test', methods=["POST", "GET"])
@login_required(role='developer')
def add_test_form():
    message = None
    devices = Service.get_objects('device')
    if request.method == "POST":
        parameters = request.form.to_dict()
        code, message = Service.test_management(parameters, 'add')
    return render_template('src/add_test.html', devices=devices, messages=message, test_types=DEVICE_TYPES)


@app.route('/change_test', methods=["POST", "GET"])
@login_required(role='developer')
def change_test_forms():
    if request.method == "POST":
        devices = Service.get_objects('user')
        test_id = request.form['test_id']
        test = Service.get_objects('test', 'id', test_id)
        if 'title' in request.form:
            code, message = Service.update_to_db(request.form, 'test')
            return render_template('src/developer_index.html', messages=message)
        return render_template('src/change_test.html', test=test, devices=devices)
    tests = Service.get_objects('test')
    return render_template('src/get_test.html', tests=tests)


@app.route('/delete_test', methods=["POST", "GET"])
@login_required(role='developer')
def delete_test_form():
    if request.method == "POST":
        message = Service.delete_object(request.form, 'test')
        return render_template('src/developer_index.html', messages=message)
    tests = Service.get_objects('test')
    return render_template('src/delete_test.html', tests=tests)


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


