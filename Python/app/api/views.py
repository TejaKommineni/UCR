from flask import jsonify, request, url_for, redirect, abort, g, session, current_app
from flask import Blueprint, render_template, abort
import app.query as query
import app.models as models
from datetime import datetime
from app.database import db
import json

api = Blueprint('api',__name__,template_folder='templates')

##############################################################################
# create_data
#
# A test endpoint that adds some junk to test with
##############################################################################
@api.route('/createData')
def create_data():
    arcReview = models.ArcReview(
        review_type = 1,
        date_sent_to_reviewer = datetime.now(),
        reviewer1 = 1,
        reviewer1_rec = 1,
        reviewer1_sig_date = datetime.now(),
        reviewer1_comments = "test comment",
        reviewer2 = 2,
        reviewer2_rec  =2 ,
        reviewer2_sig_date = datetime.now(),
        reviewer2_comments = datetime.now(),
        research = 1,
        lnkage=False,
        contact = True,
        engaged = True,
        non_public_data = True)
        
    budget = models.Budget(
        numPeriods = 1,
        periodStart = datetime.now(),
        periodEnd = datetime.now(),
        periodTotal = 1.23,
        periodComment = "Budget Period")
        
    p = models.Project(
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
    rc = models.ReviewCommittee(
        project_projectID=p.projectID,
        review_committee_number=1,
        date_initial_review=datetime.now(),
        date_expires = datetime.now(),
        rc_note = "rc_note",
        rc_protocol = "rc_proto",
        rc_approval="rc_approval")
    
    rcsl = models.RCStatusList(
        rc_status = "Status 1",
        rc_status_definition = "rc status def")
        
    irb = models.IRBHolderLUT(
        irb_holder = "holder 1",
        irb_holder_definition= "IRB 1")
        
    rcl = models.ReviewCommitteeList(
        reviewCommittee = "rc",
        rc_description = "rc desc")
        
    pt = models.ProjectType(
        project_type = "Type 1",
        project_type_definition = "Def 1")
    
    rc.RCStatusList = rcsl
    rc.reviewCommitteeList = rcl
    p.IRBHolderLUT = irb
    p.projectType = pt
    p.reviewCommittees.append(rc)
    p.budgets.append(budget)
    p.arcReview = arcReview

    db.session.add(p)
    db.session.commit()
    return "Added Data"

##############################################################################
# Error Handlers
##############################################################################    
def item_not_found(e):
    return jsonify({"Error": str(e)}), 404   

def missing_params(e):
    return jsonify({"Error": str(e)}), 400
    
def internal_error(e):
    return jsonify({"Error": str(e)}), 500

def item_deleted(message):
    return jsonify({
        "Success": True,
        "Message": str(message)
        })
    
##############################################################################
# Root Node
##############################################################################    
@api.route('/')
def root():
    return jsonify({
    "version" : 0.01,
    "endpoints" : [
        "projects",
        "staff"
    ]})

##############################################################################
# IRBHolderLUT
##############################################################################
@api.route('/irbholders/',methods=['GET'])
@api.route('/irbholders/<int:irbHolderID>/', methods = ['GET'])
def get_irb_holder(irbHolderID=None):
    if irbHolderID is None:
        return jsonify(irbHolders = [i.dict() for i in query.get_irb_holders()])
    else:
        irb = query.get_irb_holder(irbHolderID)
        if irb is not None:
            return irb.json()
        else:
            return item_not_found("IrbHolderID {} not found".format(irbHolderID))
            
@api.route('/irbholders/<int:irbHolderID>/', methods = ['PUT'])
def update_irb_holder(irbHolderID):
    irb = query.get_irb_holder(irbHolderID)
    print(irb)
    if irb is not None:
        try:
            irb.irb_holder = request.form['irb_holder']
            irb.irb_holder_definition = request.form['irb_holder_definition']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return irb.json()
    else:
        return item_not_found("IrbHolderID {} not found".format(irbHolderID))
        
@api.route('/irbholders/', methods = ['POST'])
def create_irb_holder():
    try:
        irb = models.IRBHolderLUT(
            irb_holder = request.form['irb_holder'],
            irb_holder_definition = request.form['irb_holder_definition']
        )
        ret = query.add(irb)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({"irbHolderID":irb.irbHolderID})
    
@api.route('/irbholders/<int:irbHolderID>/',methods=['DELETE'])
def delete_irb_holder(irbHolderID):
    try:
        irb = query.get_irb_holder(irbHolderID)
        if irb is not None:
            query.delete(irb)
            return item_deleted("IrbHolderID {} deleted".format(irbHolderID))
        else:
            return item_not_found("IrbHolderID {} not found".format(irbHolderID))
    except Exception as e:
        return internal_error(e)
    
##############################################################################
# Project 
##############################################################################
""" 
    Get project(s)
"""
@api.route('/projects/', methods=['GET'])
@api.route('/projects/<int:projectID>/',methods = ['GET'])
def get_project(projectID=None):
    if projectID is None:
        return jsonify(projects = [i.dict() for i in query.get_projects()])
    else:
        proj = query.get_project(projectID)
        if proj is not None:
            return proj.json()
        else:
            return item_not_found("ProjectID {} not found".format(projectID))

"""
    Update a project
"""
@api.route('/projects/<int:projectID>/',methods = ['PUT'])
def update_project(projectID):
    proj = query.get_project(projectID)
    if proj is not None:
        try:
            proj.projectType_projectTypeID = request.form['projectType_projectTypeID']
            proj.IRBHolderLUT_irbHolderID = request.form['IRBHolderLUT_irbHolderID']
            proj.project_name = request.form['project_name']
            proj.short_title = request.form['short_title']
            proj.project_summary = request.form['project_summary']
            proj.sop = request.form['sop']
            proj.UCR_proposal = request.form['UCR_proposal']
            proj.budget_doc = request.form['budget_doc']
            proj.UCR_fee = request.form['UCR_fee']
            proj.UCR_no_fee = request.form['UCR_no_fee']
            proj.budget_end_date = datetime.strptime(request.form['budget_end_date'],"%Y-%m-%d")
            proj.previous_short_title = request.form['previous_short_title']
            proj.date_added = datetime.strptime(request.form['date_added'],"%Y-%m-%d")
            proj.final_recruitment_report = request.form['final_recruitment_report']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return proj.json()
    else:
        return item_not_found("ProjectID {} not found".format(projectID))

"""
    Create new project
"""
@api.route('/projects/', methods=['POST'])
def create_project():
    try:
        proj = models.Project(
            projectType_projectTypeID = request.form['projectType_projectTypeID'],
            IRBHolderLUT_irbHolderID = request.form['IRBHolderLUT_irbHolderID'],
            project_name = request.form['project_name'],
            short_title = request.form['short_title'],
            project_summary = request.form['project_summary'],
            sop = request.form['sop'],
            UCR_proposal = request.form['UCR_proposal'],
            budget_doc = request.form['budget_doc'],
            UCR_fee = request.form['UCR_fee'],
            UCR_no_fee = request.form['UCR_no_fee'],
            budget_end_date = datetime.strptime(request.form['budget_end_date'],"%Y-%m-%d"),
            previous_short_title = request.form['previous_short_title'],
            date_added = datetime.strptime(request.form['date_added'],"%Y-%m-%d"),
            final_recruitment_report = request.form['final_recruitment_report']
            )
        ret = query.add(proj)
    except KeyError as e:
       return missing_params(e)
    except Exception as e:
       return internal_error(e)
    return jsonify({'projectID':proj.projectID})

@api.route('/projects/<int:projectID>/',methods = ['DELETE'])
def delete_project(projectID):
    try:
        proj = query.get_project(projectID)
        if proj is not None:
            query.delete(proj)
            return item_deleted("ProjectID {} deleted".format(projectID))
        else:
            return item_not_found("ProjectID {} not found".format(projectID))
    except Exception as e:
        return internal_error(e)
    
##############################################################################
# RCStatusList
##############################################################################
@api.route('/rcstatuslist/', methods = ['GET'])
@api.route('/rcstatuslist/<int:rcStatusID>/', methods = ['GET'])
def get_rc_status_list(rcStatusID=None):
    if rcStatusID is None:
        return jsonify(RCStatusList = [i.dict() for i in query.get_rc_statuses()])
    else:
        rcStatus = query.get_rc_status(rcStatusID)
        if rcStatus is not None:
            return rcStatus.json()
        else:
            return item_not_found("RCStatusID {} not found".format(rcStatusID))
            
@api.route('/rcstatuslist/<int:rcStatusID>/', methods = ['PUT'])
def update_rc_status_list(rcStatusID):
    rcStatus = query.get_rc_status(rcStatusID)
    if rcStatus is not None:
        try:
            rcStatus.rc_status = request.form['rc_status']
            rcStatus.rc_status_definition = request.form['rc_status_definition']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return rcStatus.json()
    else:
        return item_not_found("RCStatusListID {} not found".format(rcStatusID))
        
@api.route('/rcstatuslist/', methods=['POST'])
def create_rc_status_list():
    try:
        rcStatus = models.RCStatusList(
            rc_status = request.form['rc_status'],
            rc_status_definition = request.form['rc_status_definition']
        )
        ret = query.add(rcStatus)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'rcStatusListID':rcStatus.rcStatusID})

@api.route('/rcstatuslist/<int:rcStatusID>/', methods = ['DELETE'])
def delete_rc_status_list(rcStatusID):
    try:
        rcStatusList = query.get_rc_status(rcStatusID)
        if rcStatusList is not None:
            query.delete(rcStatusList)
            return item_deleted("RCStatusListID {} deleted".format(rcStatusID))
        else:
            return item_not_found("RCStatusListID {} not found".format(rcStatusID))
    except Exception as e:
        return internal_error(e)
        
##############################################################################
# Review CommitteeList
##############################################################################
@api.route('/reviewcommitteelist/', methods = ['GET'])
@api.route('/reviewcommitteelist/<int:rcListID>/', methods = ['GET'])
def get_review_committee_list(rcListID=None):
    if rcListID is None:
        return jsonify(ReviewCommitteeList = [i.dict() for i in query.get_review_committee_lists()])
    else:
        review_committee_list = query.get_review_committee_list(rcListID)
        if review_committee_list is not None:
            return review_committee_list.json()
        else:
            return item_not_found("RCListID {} not found".format(rcListID))
            
@api.route('/reviewcommitteelist/<int:rcListID>/',methods = ['PUT'])
def update_review_committee_list(rcListID):
    rcList = query.get_review_committee_list(rcListID)
    if rcList is not None:
        try:
            rcList.reviewCommittee = request.form['reviewCommittee']
            rcList.rc_description = request.form['rc_description']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return rcList.json()
    else:
        return item_not_found("RCListID {} not found".format(rcListID))
        
@api.route('/reviewcommitteelist/',methods = ['POST'])
def create_review_committee_list():
    try:
        reviewCommitteeList = models.ReviewCommitteeList(
            reviewCommittee = request.form['reviewCommittee'],
            rc_description = request.form['rc_description']
            )
        ret = query.add(reviewCommitteeList)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'rcListID':reviewCommitteeList.rcListID})
    
@api.route('/reviewcommitteelist/<int:rcListID>/', methods = ['DELETE'])
def delete_review_committee_list(rcListID):
    try:
        reviewCommittee = query.get_rc_status(rcListID)
        if reviewCommittee is not None:
            query.delete(reviewCommittee)
            return item_deleted("RCListID {} deleted".format(rcListID))
        else:
            return item_not_found("RCListID {} not found".format(rcListID))
    except Exception as e:
        return internal_error(e)