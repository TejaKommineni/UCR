import json
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db

"""
    A base class that all models derive from
"""
class CustomModel(db.Model):
    __abstract__ = True
    def __init__(self):
        super(CustomModel,self).__init__()
        
    def dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
       
    def json(self):
        return DateTimeEncoder().encode(self.dict())

"""
    A custom json encoder that works with dates
"""
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)
            
##############################################################################
# Models
##############################################################################        

class IRBHolderLUT(CustomModel):
    __tablename__ = 'IRBHolderLUT'
    
    irbHolderID = db.Column(db.Integer,primary_key=True)
    irb_holder = db.Column(db.String)
    irb_holder_definition = db.Column(db.String)
    
    def __repr__(self):
        return "<IRBHolderLUT(\
            irbHolderID = {},\
            irb_holder = {},\
            irb_holder_definition = {})>".format(
            self.irbHolderID,
            self.irb_holder,
            self.irb_holder_definition)
    
class RCStatusList(CustomModel):
    __tablename__ = 'RCStatusList'
    
    rcStatusID = db.Column(db.Integer, primary_key=True)
    rc_status = db.Column(db.String)
    rc_status_definition = db.Column(db.String)
    
    def __repr__(self):
        return "<RCStatusList(\
            rcStatusID = {},\
            rc_status = {},\
            rc_status_definition = {})>".format(
            self.rcStatusID,
            self.rc_status,
            self.rc_status_definition)

class ReviewCommittee(CustomModel):
    __tablename__ = 'reviewCommittee'
    
    reviewCommitteeID = db.Column(db.Integer,primary_key=True)
    project_projectID = db.Column(db.Integer,db.ForeignKey('project.projectID'))
    RCStatusList_rc_StatusID = db.Column(db.Integer, db.ForeignKey('RCStatusList.rcStatusID'))
    reviewCommitteeList_rcListID = db.Column(db.Integer,db.ForeignKey('reviewCommitteeList.rcListID'))
    review_committee_number=db.Column(db.String)
    date_initial_review= db.Column(db.Date)
    date_expires = db.Column(db.Date)
    rc_note = db.Column(db.String)
    rc_protocol = db.Column(db.String)
    rc_approval = db.Column(db.String)
    
    project = db.relationship("Project",back_populates="reviewCommittee",foreign_keys=[project_projectID])
    RCStatusList = db.relationship("RCStatusList", foreign_keys=[RCStatusList_rc_StatusID])
    reviewCommitteeList = db.relationship("ReviewCommitteeList",foreign_keys=[reviewCommitteeList_rcListID])
        
    def __repr__(self):
        return "<ReviewCommittee(\
            reviewCommitteeID ={},\
            project_projectID = {},\
            RCStatusList_rc_StatusID={},\
            reviewCommitteeList_rcListID={},\
            review_committee_number={},\
            db.Date_initial_review={},\
            db.Date_expires={},\
            rc_note={},\
            rc_protocol={},\
            rc_approval={})>".format(
            self.reviewCommitteeID,
            self.project_projectID,
            self.RCStatusList_rc_StatusID,
            self.reviewCommitteeList_rcListID,
            self.review_committee_number,
            self.date_initial_review,
            self.date_initial_review,
            self.date_expires,
            self.rc_note,
            self.rc_protocol,
            self.rc_approval)
            
class ReviewCommitteeList(CustomModel):
    __tablename__ ='reviewCommitteeList'
    
    rcListID = db.Column(db.Integer,primary_key=True)
    reviewCommittee = db.Column(db.String)
    rc_description = db.Column(db.String)
    
    def __repr__(self):
        return "<ReviewCommitteeList(\
        rcListID={},\
        reviewCommittee={},\
        rc_description={})>".format(
        self.rcListID,
        self,reviewComittee,
        self.rc_description)
        
class Project(CustomModel):
    __tablename__='project'
    
    projectID = db.Column(db.Integer, primary_key=True)
    projectType_projectTypeID = db.Column(db.Integer, db.ForeignKey('projectType.projectTypeID'))
    IRBHolderLUT_irbHolderID = db.Column(db.Integer, db.ForeignKey('IRBHolderLUT.irbHolderID'))
    project_name = db.Column(db.String)
    short_title = db.Column(db.String)
    project_summary = db.Column(db.String)
    sop = db.Column(db.String)
    UCR_proposal = db.Column(db.String)
    budget_doc = db.Column(db.String)
    UCR_fee = db.Column(db.String)
    UCR_no_fee = db.Column(db.String)
    budget_end_date = db.Column(db.Date)
    previous_short_title = db.Column(db.String)
    date_added = db.Column(db.Date)
    final_recruitment_report = db.Column(db.String)
    
    IRBHolderLUT = db.relationship("IRBHolderLUT")
    projectType = db.relationship("ProjectType")
    reviewCommittee = db.relationship("ReviewCommittee",uselist=False,back_populates="project")
    
    def __repr__(self):
        return "<Project(\
        projectID={},\
        projectType_projectTypeID={},\
        IRBHolderLUT_irbHolderID={},\
        project_name={},\
        short_title={},\
        project_summary={},\
        sop={},\
        UCR_proposal={},\
        budget_doc={},\
        UCR_fee={},\
        UCR_no_fee={},\
        budget_end_db.Date={},\
        previous_short_title={},\
        db.Date_added={},\
        final_recruitment_report={})>".format(
        self.projectID,
        self.projectType_projectTypeID,
        self.IRBHolderLUT_irbHolderID,
        self.project_name,
        self.short_title,
        self.project_summary,
        self.sop,
        self.UCR_proposal,
        self.budget_doc,
        self.UCR_fee,
        self.UCR_no_fee,
        self.budget_end_date,
        self.previous_short_title,
        self.date_added,
        self.final_recruitment_report)
        
class ProjectType(CustomModel):
    __tablename__ = 'projectType'
    
    projectTypeID = db.Column(db.Integer,primary_key=True)
    project_type = db.Column(db.String)
    project_type_definition = db.Column(db.String)
    
    def __repr__(self):
        return "<ProjectType(\
        projectTypeID={},\
        project_type={},\
        project_type_definition={})>".format(
        self.projectTypeID,
        self,project_type,
        self.project_type_definition)
        
        
    