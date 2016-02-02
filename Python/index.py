import random
import string
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g, session, current_app
from flask.ext.login import login_user , logout_user , current_user , login_required, LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_, or_
from flask_principal import (
    ActionNeed,
    AnonymousIdentity,
    Identity,
    identity_changed,
    identity_loaded,
    Permission,
    Principal,
    RoleNeed,
    UserNeed)
from flask.ext.mail import Mail, Message
from flask import jsonify
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import json

from database import db
from models import IRBHolderLUT, ProjectType, Project, ReviewCommittee, ReviewCommitteeList, RCStatusList
from Query import get_project

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'super-secret'
    app.config['SQLALCHEMY_DATABASE_URI']= r"sqlite:///E:\aaron_temp\UCR-App\Alpha\mock.db"
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    return app
    
def create_data():
    print("test")
    p = Project(
        projectType_projectTypeID = 1,
        IRBHolderLUT_irbHolderID =1,
        project_name = "Test Project",
        short_title = "Test Project",
        project_summary = "Summary",
        sop="sop",
        UCR_proposal="ucr_proposal",
        budget_doc = "budget_doc",
        UCR_fee = "no",
        UCR_no_fee = "yes",
        budget_end_date = datetime.now(),
        previous_short_title = "t short",
        date_added = datetime.now(),
        final_recruitment_report = "report")
    rc = reviewCommitte = ReviewCommittee(
        project_projectID=p.projectID,
        #RCStatusList_rc_StatusID = 1,
        #reviewCommitteList_rcListID = 1,
        review_committee_number=1,
        date_initial_review=datetime.now(),
        date_expires = datetime.now(),
        rc_note = "rc_note",
        rc_protocol = "rc_proto",
        rc_approval="rc_approval")
    
    rcsl = RCStatusList(
        rc_status = "Status 1",
        rc_status_definition = "rc status def")
        
    irb = IRBHolderLUT(
        irb_holder = "holder 1",
        irb_holder_definition= "IRB 1")
        
    rcl = ReviewCommitteeList(
        reviewCommittee = "rc",
        rc_description = "rc desc")
        
    pt = ProjectType(
        project_type = "Type 1",
        project_type_definition = "Def 1")
    
    rc.RCStatusList = rcsl
    rc.reviewCommitteeList = rcl
    p.IRBHolderLUT = irb
    p.projectType = pt
    p.reviewCommittee = rc

    db.session.add(p)
    db.session.commit()
    
app = create_app()

@app.route('/alpha/project/<id>/',methods=['GET'])
def project(id):
    proj = get_project(id)
    return proj.json()
        
if __name__ == '__main__':
    app.run()