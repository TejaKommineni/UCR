import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db
from models import Project

def get_project(id):
    return db.session.query(Project).filter_by(projectID=id)[0]