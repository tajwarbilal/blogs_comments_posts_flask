from flask import Blueprint, render_template, request, redirect
from models import Login
from app import db

user_blueprints = Blueprint('user_blueprints', __name__)


@user_blueprints.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('uname')
        password = request.form.get('pass')
        entry = Login(email=email, password=password)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')

    return render_template('signup.html')


@user_blueprints.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('uname')
        password = request.form.get('pass')
        login = Login.query.filter_by(email=email, password=password).first()
        if login:
            return redirect('/addpost')

    return render_template('public_login.html')


@user_blueprints.route('/logoutuser')
def logoutuser():
    return redirect('/')

