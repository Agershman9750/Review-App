from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User

@app.route('/')
def login():
    if 'users_id' in session:
        return redirect('/review')
    return render_template('index.html')

@app.route('/login')
def login2():
    if 'users_id' in session:
        return redirect('/review')
    return render_template('index.html')


@app.route('/user/login/process', methods=['POST'])
def login_success():
    user = User.validate_login(request.form)
    if not user:
        return redirect('/login')
    session['users_id'] = user.id
    return redirect('/review')


@app.route('/user/register/process', methods=['POST'])
def register_success():
    if not User.validate_reg(request.form):
        return redirect('/login')

    user_id = User.save(request.form)
    session['users_id'] = user_id
    return redirect('/review')


@app.route('/user/logout')
def logout():
    if 'users_id' in session:
        session.pop('users_id')
    return redirect('/')
