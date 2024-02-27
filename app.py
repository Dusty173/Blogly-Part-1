"""Blogly application."""

from flask import Flask, redirect, request, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

connect_db(app)


@app.route('/')
def base_root():
    """Display homepage"""
    
    posts = Post.query.order_by(Post.created_at.desc()).limit(3).all()
    return render_template('/posts/homepage.html', posts=posts)

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

@app.route('/users/<int:user_id>/edit', methods=["POST"])
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


@app.route('/users/<int:user_id>/posts/new')
def add_post_form(user_id):
    """Add a post for current user"""

    user = User.query.get_or_404(user_id)
    return render_template('posts/post_form.html')

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_post(user_id):
    """Submits post to db"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'], content = request.form['content'], user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Added '{new_post.title}'")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """Show post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show-post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Give user form to edit a post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Update edited/existing post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Succesfully edited '{post.title}'.")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def remove_post(post_id):
    """Removes current post"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Removed '{post.title}' permanently.")

    return redirect(f"/users/{post.user_id}")

@app.route('/tags')
def tags_list():
    """Get a list of tags"""
    tags = Tag.query.all()
    return render_template('tags/tags_pg.html', tags=tags)

@app.route('/tags/new')
def new_tag_form():
    """Give user form for creating tags"""
    posts = Post.query.all()
    return render_template('tags/tag_form.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def send_tag():
    """Send tag to db/add to post"""

    post_ids = [int(num) for num in request.form.getList('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Added '{new_tag.name}'")

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def get_tags(tag_id):
    """Info page for certain tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/tginfo.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """Show form to edit tags"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html',tag=tag ,posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """Update tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Remove a tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Deleted '{tag.name}'")

    return redirect("/tags")