"""views.py handles the web-browser's requests
"""
import os

from flask import request, render_template, redirect, url_for, g, flash, send_from_directory
from app.forms import MyLoginForm, MyRegisterForm, EditForm, PostForm
from flask_security import login_required, login_user, current_user
from flask_security.utils import verify_password, hash_password
from app.models import User, Post, user_datastore
from datetime import datetime
from app import app, db

# pagination
POST_PER_PAGE = 5


@app.before_request
def before_request():
    """Setup the current_user"""
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    """Website start page"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = {}
    if g.user.is_authenticated:
        posts = g.user.followed_posts().paginate(page, POST_PER_PAGE, False)

    return render_template('index.html',
                           title='Home',
                           form=form,
                           user=g.user,
                           posts=posts)


@app.route('/signin', methods=['GET', 'POST'])
def login():
    """Custom login view. It will be changed further."""
    error = None

    form = MyLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user.username)
        if user is None:
            error = 'Invalid username'
        elif not verify_password(form.password.data, user.password):
            error = 'Invalid password'
        else:
            login_user(user, form.remember.data)
            return redirect(url_for('detail_user', username=user.username))

    return render_template('login.html', error=error, form=form)


@app.route('/signup', methods=['GET', 'POST'])
def register():
    error = None
    form = MyRegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        if User.query.filter_by(username=username).first() is not None:
            error = 'This username is already registered.'
        elif form.password.data != form.password2.data:
            error = 'Entered passwords do not match'
        else:
            user_datastore.create_user(username=username,
                                       email=form.email.data,
                                       password=hash_password(form.password.data))
            db.session.commit()

            user = User.query.filter_by(username=username).first()
            login_user(user, remember=True)

            return redirect('index')

    return render_template('signup.html', error=error, form=form)


@app.route('/user/<username>')
@app.route('/user/<username>/<int:page>')
@login_required
def detail_user(username, page=1):
    """User's profile page"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POST_PER_PAGE, False)
    return render_template('user.html',
                           user=user,
                           posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.about_me = form.about_me.data

        if request.files['file']:
            file = request.files['file']
            filename = file.filename
            path = os.path.dirname(app.config['UPLOAD_FOLDER'] + "/{}/".format(g.user.username) + filename)
            if not os.path.exists(path):
                os.makedirs(path)
            app.config["UPLOAD_FOLDER"] = path
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            g.user.avatar_url = filename
        db.session.add(g.user)
        db.session.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.username.data = g.user.username
        form.about_me.data = g.user.about_me

    return render_template('edit.html', form=form)


@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/follow/<username>')
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself! Fuck your month, bitch.')
        return redirect(url_for('detail_user', username=username))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ().'.format(username))
        return redirect(url_for('detail_user', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You are now following {}!'.format(username))
    return redirect(url_for('detail_user', username=username))


@app.route('/unfollow/<username>')
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('detail_user', username=username))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow {}.'.format(username))
        return redirect(url_for('detail_user', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following {}.'.format(username))
    return redirect(url_for('detail_user', username=username))


# Error handlers


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', error=error), 500
