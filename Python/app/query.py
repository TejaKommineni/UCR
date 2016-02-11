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

def get_fundings():
    return db.session.query(Funding).all()
    
def get_funding(id):
    return db.session.query(Funding).filter_by(fundingID = id).first()
    
def get_funding_sources():
    return db.session.query(FundingSourceLUT).all()
    
def get_funding_source(id):
    return db.session.query(FundingSourceLUT).filter_by(fundingSourceLUTID = id).first()
    
def get_grant_statuses():
    return db.session.query(GrantStatusLUT).all()
    
def get_grant_status(id):
    return db.session.query(GrantStatusLUT).filter_by(grantStatusLUTID = id).first()
    
def get_irb_holders():
    return db.session.query(IRBHolderLUT).all()

def get_irb_holder(id):
    return db.session.query(IRBHolderLUT).filter_by(irbHolderID=id).first()

def get_patients():
    return db.session.query(Patient).all()
    
def get_patient(id):
    return db.session.query(Patient).filter_by(patAutoID = id).first()

def get_phase_statuses():
    return db.session.query(PhaseStatus).all()
    
def get_phase_status(id):
    return db.session.query(PhaseStatus).filter_by(logPhaseID=id).first()
    
def get_project(id):
    return Project.query.filter_by(projectID=id).first()
    
def get_projects():
    return db.session.query(Project).all()

def get_project_patients():
    return db.session.query(ProjectPatient).all()
    
def get_project_patient(id):
    return db.session.query(ProjectPatient).filter_by(participantID = id).first()
    
def get_project_statuses():
    return db.session.query(ProjectStatus).all()
    
def get_project_status(id):
    return db.session.query(ProjectStatus).filter_by(projectStatusID = id).first()
    
def get_project_status_luts():
    return db.session.query(ProjectStatusLUT).all()
    
def get_project_status_lut(id):
    return db.session.query(ProjectStatusLUT).filter_by(projectStatusTypeID = id).first()
    
def get_project_types():
    return db.session.query(ProjectType).all()
    
def get_project_type(id):
    return db.session.query(ProjectType).filter_by(projectTypeID=id).first()
    
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