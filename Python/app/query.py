import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.database import db
from app.models import *

def get_arc_reviews():
    return db.session.query(ArcReview).all()
    
def get_arc_review(id):
    return db.session.query(ArcReview).filter_by(arcReviewID = id).first()

def get_budgets():
    return db.session.query(Budget).all()
    
def get_budget(id):
    return db.session.query(Budget).filter_by(budgetID = id).first()

def get_irb_holders():
    return db.session.query(IRBHolderLUT).all()

def get_irb_holder(id):
    return db.session.query(IRBHolderLUT).filter_by(irbHolderID=id).first()

def get_project(id):
    return Project.query.filter_by(projectID=id).first()
    
def get_projects():
    return db.session.query(Project).all()
    
def get_rc_status(id):
    return db.session.query(RCStatusList).filter_by(rcStatusID=id).first()
    
def get_rc_statuses():
    return db.session.query(RCStatusList).all()
    
def get_review_committees():
    return db.session.query(ReviewCommittee).all()
    
def get_review_committee(id):
    return db.session.query(ReviewCommittee).filter_by(reviewCommitteeID=id).first()
    
def get_review_committee_list(id):
    return db.session.query(ReviewCommitteeList).filter_by(rcListID=id).first()
    
def get_review_committee_lists():
    return db.session.query(ReviewCommitteeList).all()
    
def get_ucr_reports():
    return db.session.query(UCRReport).all()
    
def get_ucr_report(id):
    return db.session.query(UCRReport).filter_by(ucrReportID = id).first()
    
def commit():
    return db.session.commit()
    
def add(obj):
    db.session.add(obj)
    return db.session.commit()
    
def delete(obj):
    db.session.delete(obj)
    return db.session.commit()