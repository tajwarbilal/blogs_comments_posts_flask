from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json

db = SQLAlchemy()

# We will load Configration from the json file into our main file
with open('config.json', 'r') as c:
    params = json.load(c)["params"]


def create_app():
    app = Flask(__name__, template_folder='templates')
    from app.blogs.blogs_blueprint import blogs_bluprints
    app.register_blueprint(blogs_bluprints)
    from app.admin.admin_blueprints import admin_bluprints
    app.register_blueprint(admin_bluprints)

    from app.users.user_blueprints import user_blueprints
    app.register_blueprint(user_blueprints)

    app.secret_key = 'super-secret-key'
    # Import the os module
    import os
    # Get the current working directory
    cwd = os.getcwd()
    app.config['UPLOAD_FOLDER'] = cwd + "\static\img"
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT='465',
        MAIL_USE_SSL=True,
    )
    local_server = True
    if local_server:
        app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

    db.init_app(app)

    return app
