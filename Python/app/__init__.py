from flask import Flask
from app.api.views import api
from app.website.views import website
from app.database import db
from app.helpers import DateTimeEncoder
from flask.ext.sqlalchemy import SQLAlchemy

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.register_blueprint(api, url_prefix = '/api')
    app.register_blueprint(website, url_prefix = '/website')
    app.json_encoder = DateTimeEncoder
    return app
    
app = create_app('config')