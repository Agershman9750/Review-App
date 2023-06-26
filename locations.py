from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.location import Location
from flask_app.models.user import User


@app.route('/review')
def sighting():
    if 'users_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id": session['users_id']})
    if not user:
        return redirect('/user/logout')
    return render_template('review.html', user=user, locations=Location.get_all())

@app.route('/new/review')
def create_location():
    if 'users_id' not in session:
        return redirect('/')
    
    user = User.get_by_id({"id": session['users_id']})
    if not user:
        return redirect('/user/logout')

    return render_template('create.html', user=user)

@app.route('/locations/new/process', methods=['POST'])
def process_location():
    if 'users_id' not in session:
        return redirect('/')
    if not Location.validate_location(request.form):
        return redirect('/review')

    data = {
        'users_id': session['users_id'],
        'type': request.form['type'],
        'address': request.form['address'],
        'description': request.form['description'],
        'date_made': request.form['date_made'],
        'amount': request.form['amount'],
    }
    Location.save(data)
    return redirect('/review')

@app.route('/show/<int:id>')
def view_location(id):
    if 'users_id' not in session:
        return redirect('/')

    user = User.get_by_id({'id': session['users_id']})  
    if not user:
        return redirect('/user/logout')

    location = Location.get_by_id({'id': id})  
    if not location:
        return redirect('/review')

    return render_template('view.html', location=location, user=user)

@app.route('/edit/<int:id>')
def edit_location(id):
    if 'users_id' not in session:
        return redirect('/')

    user = User.get_by_id({'id': session['users_id']})  
    if not user:
        return redirect('/')

    location = Location.get_by_id({'id': id}) 
    if not Location:
        return redirect('/review')

    return render_template('edit.html', location=location, user=user)

@app.route('/edit/process/<int:id>', methods=['POST'])
def process_edit_location(id):
    if 'users_id' not in session:
        return redirect('/')
    if not Location.validate_location(request.form):
        return redirect(f'/edit/{id}')

    data = {
        'id': id,
        'type': request.form['type'],
        'address': request.form['address'],
        'description': request.form['description'],
        'date_made': request.form['date_made'],
        'amount': request.form['amount'],
    }
    Location.update(data)
    return redirect('/review')

@app.route('/destroy/<int:id>')
def destroy_location(id):
    if 'users_id' not in session:
        return redirect('/')

    Location.destroy({'id': id})
    return redirect('/review')

@app.route('/email/<int:id>')
def reveal_email(id):
    if 'users_id' not in session:
        return redirect('/')

    user = User.get_by_id({'id': session['users_id']})  
    if not user:
        return redirect('/user/logout')

    location = Location.get_by_id({'id': id})  
    if not location:
        return redirect('/review')

    return render_template('view.html', location=location, user=user, show_email=True)
