from flask import Blueprint, render_template, request, session, redirect
from werkzeug.utils import secure_filename
from datetime import datetime
from models import Posts, Contacts, Login
from app import db
import os
import math
import json

# We will load Configration from the json file into our main file
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

# I have created the admin Blueprint with route to have admin permissions
admin_bluprints = Blueprint('admin_bluprints', __name__)


@admin_bluprints.route("/dashboard", methods=['GET', 'POST'])
def here_is_the_dashboard_having_admin_role():
    if 'user' in session and session['user'] == params['admin_user']:
        posts = Posts.query.all()
        user = Login.query.all()
        return render_template('dashboard.html', params=params, posts=posts, user=user)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if username == params['admin_user'] and userpass == params['admin_password']:
            # set the session variable
            session['user'] = username
            posts = Posts.query.all()
            user = Login.query.all()
            return render_template('dashboard.html', params=params, posts=posts, user=user)

    return render_template('login.html', params=params)


# When you got any chance to edit a post you will go through this
@admin_bluprints.route("/edit/<string:sno>", methods=['GET', 'POST'])
def we_can_edit_post(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            box_title = request.form.get('title')
            tline = request.form.get('tline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            f = request.files['file1']
            import os
            # Get the current working directory
            cwd = os.getcwd()
            UPLOAD_FOLDER = cwd + "\/app\static\img"

            f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
            f = f.filename
            f = f.replace(' ', '')
            date = datetime.now()

            if sno == '0':
                post = Posts(title=box_title, slug=slug, content=content, tagline=tline, img_file=f, date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.slug = slug
                post.content = content
                post.tagline = tline
                post.img_file = f
                post.date = date
                db.session.commit()
                return redirect('/edit/' + sno)
        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params, post=post, sno=sno)


# When you got any chance to edit a post you will go through this
@admin_bluprints.route("/addpost", methods=['POST', 'GET'])
def addpost():
    if request.method == 'POST':
        box_title = request.form.get('title')
        tline = request.form.get('tagline')
        slug = request.form.get('slug')
        content = request.form.get('textarea')
        f = request.files['file1']
        import os
        # Get the current working directory
        cwd = os.getcwd()
        UPLOAD_FOLDER = cwd + "\/app\static\img"

        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        f = f.filename
        f = f.replace(' ', '')
        date = datetime.now()
        post = Posts(title=box_title, slug=slug, content=content, tagline=tline, img_file=f, date=date)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    return render_template('addpost.html')


# This route will log you out and remove you from sessions
@admin_bluprints.route("/logout")
def this_logout_will_log_youout_from_admin():
    session.pop('user')
    return redirect('/')


# This route is use to delete a post by serial number
@admin_bluprints.route("/delete/<string:sno>", methods=['GET', 'POST'])
def this_will_delete_post(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')


# This route is use to delete a post by serial number
@admin_bluprints.route("/deleteuser/<string:sno>", methods=['GET', 'POST'])
def this_will_deleteuser_having_admin_permission(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        post = Login.query.filter_by(id=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')
