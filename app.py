"""Blogly application."""

from flask import Flask, redirect, request, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def base_root():
    return redirect('/users')

@app.route('/users')
def list_of_users():
    """Show all current users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/users.html', users=users)

@app.route('/users/add', methods=["GET"])
def add_user_form():
    """Display form to add a user"""

    return render_template('users/adduser.html')

@app.route('/users/add', methods=["POST"])
def send_new_user():
    """Get data and add to users table"""
    new_user = User(first_name=request.form['first_name'],last_name=request.form['last_name'], image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')


@app.route('/users/<int:user_id>')
def display_users(user_id):
    """Show user info for user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/display.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Edit current user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user.id>/edit', methods=["POST"])
def update_user(user_id):
    """Send new user config to server/db"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']

    db.session.add(user)
    db.session.commit()

@app.route('/user/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Remove user from database"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')