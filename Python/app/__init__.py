from flask import Flask
app = Flask(__name__)
from app.api.views import api
from app.database import db
from app.helpers import DateTimeEncoder
from flask.ext.sqlalchemy import SQLAlchemy

app.config.from_object('config')
db.init_app(app)
app.register_blueprint(api, url_prefix = '/api')
app.json_encoder = DateTimeEncoder

with app.test_request_context():
    db.create_all()