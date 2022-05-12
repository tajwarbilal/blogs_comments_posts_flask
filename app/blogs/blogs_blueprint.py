from flask import Blueprint, render_template, request, session, redirect
from werkzeug.utils import secure_filename
from datetime import datetime
from models import Posts, Contacts
from app import db
import os
import math
import json

# We will load Configration from the json file into our main file
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

blogs_bluprints = Blueprint('blogs_blueprints', __name__)


# This is a general Route after first hitting the local Uri you will redirect to this
@blogs_bluprints.route("/")
def Here_is_the_main_home_page():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts) / int(params['no_of_posts']))
    # [0: params['no_of_posts']]
    # posts = posts[]
    page = request.args.get('page')
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    posts = posts[(page - 1) * int(params['no_of_posts']): (page - 1) * int(params['no_of_posts']) + int(
        params['no_of_posts'])]
    # Pagination Logic
    # First
    if page == 1:
        prev = "#"
        next = "/?page=" + str(page + 1)
    elif page == last:
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)

    return render_template('index.html', params=params, posts=posts, prev=prev, next=next)


# This Route will get you all the posts from database and will show you in page
@blogs_bluprints.route("/post/<string:post_slug>", methods=['GET'])
def we_have_post_function_which_can_post_article(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)


# This route will show you that how we work like each and every detail about us
@blogs_bluprints.route("/about")
def here_is_the_about():
    return render_template('about.html', params=params)


# This Routes is Use to load the page and send that response to our email
@blogs_bluprints.route("/contact", methods=['GET', 'POST'])
def all_the_details_about_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num=phone, msg=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)
