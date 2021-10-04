from flask import render_template, session, redirect, request, session, flash
from werkzeug.utils import validate_arguments
from flask_app import app
from flask_app.models.user import User
from flask_app.models.show import Show


@app.route('/dashboard')
def dashboard():
    data = {
        'id' : session['logged_user']
    }
    logged_user = User.get_one(data)
    shows = Show.get_all()
    return render_template('dashboard.html', shows = shows, logged_user = logged_user)

@app.route('/shows/new')
def new_show():
    return render_template('new_show.html')

@app.route('/shows/create', methods = ['post'])
def create_show():

    if not Show.validate_show(request.form):
        return redirect('/shows/new')
    
    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'date': request.form['date'],
        'description': request.form['description'],
        'user_id': session['logged_user'],
    }
    Show.save(data)
    return redirect ('/dashboard')

@app.route('/shows/edit/<int:id>')
def edit_show(id):

    data = {
        'id' : id
    }
    show = Show.get_one(data)
    return render_template('edit_show.html', show = show)

@app.route('/shows/update/<int:id>', methods = ['post'])
def update_show(id):

    if not Show.validate_show(request.form):
        return redirect(f'/shows/edit/{id}')
    
    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'date': request.form['date'],
        'description': request.form['description'],
        'user_id': session['logged_user'],
        'id': id
    }
    show_id = Show.update(data)
    print(show_id)
    return redirect ('/dashboard')

@app.route('/shows/<int:id>')
def view_show(id):

    data = {
        'id' : id
    }
    logged_user = User.get_one({ "id" : session['logged_user'] })
    show = Show.get_one(data)
    return render_template('view_show.html', show = show, logged_user = logged_user)

@app.route('/shows/delete/<int:id>')
def delete_show(id):

    data = {
        'id':id
    }
    Show.delete(data)
    return redirect('/dashboard')