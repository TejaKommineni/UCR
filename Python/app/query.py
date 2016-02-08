import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.database import db
from app.models import *

def get_project(id):
    return Project.query.filter_by(projectID=id).first()
    
def get_projects():
    return db.session.query(Project).all()
    
def get_rc_status(id):
    return db.session.query(RCStatusList).filter_by(rcStatusID=id).first()
    
def get_rc_statuses():
    return db.session.query(RCStatusList).all()
    
def commit():
    return db.session.commit()
    
def add(obj):
    db.session.add(obj)
    return db.session.commit()