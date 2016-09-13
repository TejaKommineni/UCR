from flask import Flask
from app.api.views import api
from app.website.views import website
from app.database import db
from app.helpers import DateTimeEncoder
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cas import CAS
from flask import redirect, session
from datetime import timedelta

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.register_blueprint(api, url_prefix = '/api')
    app.register_blueprint(website, url_prefix = '/website')
    app.json_encoder = DateTimeEncoder
    # Only CASify the app if DEV MODE is disabled
    if not('DEV_MODE' in app.config and app.config['DEV_MODE']):
        CAS(app)

    # redirect root to website blueprint
    @app.route('/')
    def redirect_to_site():
        return redirect("/website")

    return app
    
app = create_app('config')