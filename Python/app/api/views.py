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
# ArcReviews
##############################################################################    
@api.route('/arcreviews/', methods = ['GET'])
@api.route('/arcreviews/<int:arcReviewID>/', methods = ['GET'])
def get_arc_review(arcReviewID = None):
    if arcReviewID is None:
        return jsonify(arcReviews = [i.dict() for i in query.get_arc_reviews()])
    else:
        arcReview = query.get_arc_review(arcReviewID)
        if arcReview is not None:
            return arcReview.json()
        else:
            return item_not_found("ArcReviewID {} not found".format(arcReviewID))
            
@api.route('/arcreviews/<int:arcReviewID>/', methods = ['PUT'])
def update_arc_review(arcReviewID):
    arcReview = query.get_arc_review(arcReviewID)
    if arcReviewID is not None:
        try:
            arcReview.projectID = request.form['projectID']
            arcReview.review_type = request.form['review_type']
            arcReview.date_sent_to_reviewer = datetime.strptime(request.form['date_sent_to_reviewer'],"%Y-%m-%d")
            arcReview.reviewer1 = request.form['reviewer1']
            arcReview.reviewer1_rec = request.form['reviewer1_rec']
            arcReview.reviewer1_sig_date = datetime.strptime(request.form['reviewer1_sig_date'],"%Y-%m-%d")
            arcReview.reviewer1_comments = request.form['reviewer1_comments']
            arcReview.reviewer2 = request.form['reviewer2']
            arcReview.reviewer2_rec = request.form['reviewer2_rec']
            arcReview.reviewer2_sig_date = datetime.strptime(request.form['reviewer2_sig_date'],"%Y-%m-%d")
            arcReview.reviewer2_comments = request.form['reviewer2_comments']
            arcReview.research = request.form['research']
            arcReview.contact = "true" == request.form['contact'].lower()
            arcReview.contact = "true" == request.form['contact'].lower()
            arcReview.lnkage = "true" == request.form['lnkage'].lower()
            arcReview.engaged = "true" == request.form['engaged'].lower()
            arcReview.non_public_data = "true" == request.form['non_public_data'].lower()
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return arcReview.json()
    else:
        return item_not_found("ArcReviewID {} not found".format(arcReviewID))
        
@api.route('/arcreviews/', methods = ['POST'])
def create_arc_review():
    try:
        arcReview = models.ArcReview(
            projectID = request.form['projectID'],
            review_type = request.form['review_type'],
            date_sent_to_reviewer = datetime.strptime(request.form['date_sent_to_reviewer'],"%Y-%m-%d"),
            reviewer1 = request.form['reviewer1'],
            reviewer1_rec = request.form['reviewer1_rec'],
            reviewer1_sig_date = datetime.strptime(request.form['reviewer1_sig_date'],"%Y-%m-%d"),
            reviewer1_comments = request.form['reviewer1_comments'],
            reviewer2 = request.form['reviewer2'],
            reviewer2_rec = request.form['reviewer2_rec'],
            reviewer2_sig_date = datetime.strptime(request.form['reviewer2_sig_date'],"%Y-%m-%d"),
            reviewer2_comments = request.form['reviewer2_comments'],
            research = request.form['research'],
            contact = "true" == request.form['contact'].lower(),
            lnkage = "true" == request.form['lnkage'].lower(),
            engaged = "true" == request.form['engaged'].lower(),
            non_public_data = "true" == request.form['non_public_data'].lower()
        )
        ret = query.add(arcReview)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({"arcReviewID" : arcReview.arcReviewID})
    
@api.route('/arcreviews/<int:arcReviewID>/', methods = ['DELETE'])
def delete_arc_review(arcReviewID):
    try:
        arcReview = query.get_arc_review(arcReviewID)
        if arcReview is not None:
            query.delete(arcReview)
            return item_deleted("ArcReviewID {} deleted".format(arcReviewID))
        else:
            return item_not_found("ArcReviewID {} not found".format(arcReviewID))
    except Exception as e:
        return interal_error(e)
    
#############################################################################
# Budget
#############################################################################
@api.route('/budgets/', methods = ['GET'])
@api.route('/budgets/<int:budgetID>/', methods = ['GET'])
def get_budget(budgetID = None):
    if budgetID is None:
        return jsonify(budgets = [i.dict() for i in query.get_budgets()])
    else:
        budget = query.get_budget(budgetID)
        if budget is not None:
            return budget.json()
        else:
            return item_not_found("BudgetID {} not found".format(budgetID))
            
@api.route('/budgets/<int:budgetID>/',methods = ['PUT'])
def update_budget(budgetID):
    budget = query.get_budget(budgetID)
    if budget is not None:
        try:
            budget.projectID = request.form['projectID']
            budget.numPeriods = request.form['numPeriods']
            budget.periodStart = datetime.strptime(request.form['periodStart'],"%Y-%m-%d")
            budget.periodEnd = datetime.strptime(request.form['periodEnd'],"%Y-%m-%d")
            budget.periodTotal = request.form['periodTotal']
            budget.periodComment = request.form['periodComment']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return interal_error(e)
        return budget.json()
    else:
        return item_not_found("BudgetID {} not found".format(budgetID))
        
@api.route('/budgets/',methods=['POST'])
def create_budget():
    try:
        budget = models.Budget(
            projectID = request.form['projectID'],
            numPeriods = request.form['numPeriods'],
            periodStart = datetime.strptime(request.form['periodStart'],"%Y-%m-%d"),
            periodEnd = datetime.strptime(request.form['periodEnd'],"%Y-%m-%d"),
            periodTotal = request.form['periodTotal'],
            periodComment = request.form['periodComment']
        )
        ret = query.add(budget)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({"budgetID" : budget.budgetID})
    
@api.route('/budgets/<int:budgetID>/', methods = ['DELETE'])
def delete_budget(budgetID):
    try:
        budget = query.get_budget(budgetID)
        if budget is not None:
            query.delete(budget)
            return item_deleted("BudgetID {} deleted".format(budgetID))
        else:
            return item_not_found("BudgetID {} not found".format(budgetID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Funding
##############################################################################
@api.route('/fundings/', methods = ['GET'])
@api.route('/fundings/<int:fundingID>/', methods = ['GET'])
def get_funding(fundingID=None):
    if fundingID is None:
        return jsonify(Fundings = [i.dict() for i in query.get_fundings()])
    else:
        funding = query.get_funding(fundingID)
        if funding is not None:
            return funding.json()
        else:
            return item_not_found("FundingID {} not found".format(fundingID))
            
@api.route('/fundings/<int:fundingID>/', methods = ['PUT'])
def update_funding(fundingID):
    funding = query.get_funding(fundingID)
    if funding is not None:
        try:
            funding.grantStatusLUTID = request.form['grantStatusLUTID']
            funding.projectID = request.form['projectID']
            funding.fundingSourceLUTID = request.form['fundingSourceLUTID']
            funding.primary_funding_source = request.form['primary_funding_source']
            funding.secondary_funding_source = request.form['secondary_funding_source']
            funding.funding_number = request.form['funding_number']
            funding.grant_title = request.form['grant_title']
            funding.grantStatusID = request.form['grantStatusID']
            funding.date_status = datetime.strptime(request.form['date_status'],"%Y-%m-%d")
            funding.grant_pi = request.form['grant_pi']
            funding.primary_chartfield = request.form['primary_chartfield']
            funding.secondary_chartfield = request.form['secondary_chartfield']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return funding.json()
    else:
        return item_not_found("FundingID {} not found".format(fundingID)) 

@api.route('/fundings/', methods=['POST'])
def create_funding():
    try:
        funding = models.Funding(
            grantStatusLUTID = request.form['grantStatusLUTID'],
            projectID = request.form['projectID'],
            fundingSourceLUTID = request.form['fundingSourceLUTID'],
            primary_funding_source = request.form['primary_funding_source'],
            secondary_funding_source = request.form['secondary_funding_source'],
            funding_number = request.form['funding_number'],
            grant_title = request.form['grant_title'],
            grantStatusID = request.form['grantStatusID'],
            date_status = datetime.strptime(request.form['date_status'],"%Y-%m-%d"),
            grant_pi = request.form['grant_pi'],
            primary_chartfield = request.form['primary_chartfield'],
            secondary_chartfield = request.form['secondary_chartfield']
        )
        ret = query.add(funding)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'fundingID':funding.fundingID})        

@api.route('/fundings/<int:fundingID>/', methods = ['DELETE'])
def delete_funding(fundingID):
    try:
        funding = query.get_funding(fundingID)
        if funding is not None:
            query.delete(funding)
            return item_deleted("FundingID {} deleted".format(fundingID))
        else:
            return item_not_found("FundingID {} not found".format(fundingID))
    except Exception as e:
        return internal_error(e)
        
        
##############################################################################
# Funding Source LUT
##############################################################################
@api.route('/fundingsources/', methods = ['GET'])
@api.route('/fundingsources/<int:fundingSourceLUTID>/', methods = ['GET'])
def get_funding_source(fundingSourceLUTID=None):
    if fundingSourceLUTID is None:
        return jsonify(FundingSources = [i.dict() for i in query.get_funding_sources()])
    else:
        fundingSource = query.get_funding_source(fundingSourceLUTID)
        if fundingSource is not None:
            return fundingSource.json()
        else:
            return item_not_found("FundingSourceLUTID {} not found".format(fundingSourceLUTID))
            
@api.route('/fundingsources/<int:fundingSourceLUTID>/', methods = ['PUT'])
def update_funding_source(fundingSourceLUTID):
    fundingSource = query.get_funding_source(fundingSourceLUTID)
    if fundingSource is not None:
        try:
            fundingSource.fundingSource = request.form['fundingSource']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return fundingSource.json()
    else:
        return item_not_found("FundingSourceLUTID {} not found".format(fundingSourceLUTID)) 

@api.route('/fundingsources/', methods=['POST'])
def create_funding_source():
    try:
        fundingSource = models.FundingSourceLUT(
            fundingSource = request.form['fundingSource']
        )
        ret = query.add(fundingSource)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'fundingSourceLUTID':fundingSource.fundingSourceLUTID})        

@api.route('/fundingsources/<int:fundingSourceLUTID>/', methods = ['DELETE'])
def delete_funding_source(fundingSourceLUTID):
    try:
        fundingSource = query.get_funding_source(fundingSourceLUTID)
        if fundingSource is not None:
            query.delete(fundingSource)
            return item_deleted("FundingSourceLUTID {} deleted".format(fundingSourceLUTID))
        else:
            return item_not_found("fundingSourceLUTID {} not found".format(fundingSourceLUTID))
    except Exception as e:
        return internal_error(e)


##############################################################################
# Grant Status LUT
##############################################################################
@api.route('/grantstatuses/', methods = ['GET'])
@api.route('/grantstatuses/<int:grantStatusLUTID>/', methods = ['GET'])
def get_grant_status(grantStatusLUTID=None):
    if grantStatusLUTID is None:
        return jsonify(GrantStatuses = [i.dict() for i in query.get_grant_statuses()])
    else:
        grantStatus = query.get_grant_status(grantStatusLUTID)
        if grantStatus is not None:
            return grantStatus.json()
        else:
            return item_not_found("GrantStatusLUTID {} not found".format(grantStatusLUTID))
            
@api.route('/grantstatuses/<int:grantStatusLUTID>/', methods = ['PUT'])
def update_grant_status(grantStatusLUTID):
    grantStatus = query.get_grant_status(grantStatusLUTID)
    if grantStatus is not None:
        try:
            grantStatus.grant_status = request.form['grant_status']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return grantStatus.json()
    else:
        return item_not_found("GrantStatusLUTID {} not found".format(grantStatusLUTID)) 

@api.route('/grantstatuses/', methods=['POST'])
def create_grant_status():
    try:
        grantStatus = models.GrantStatusLUT(
            grant_status = request.form['grant_status']
        )
        ret = query.add(grantStatus)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'grantStatusLUTID':grantStatus.grantStatusLUTID})        

@api.route('/grantstatuses/<int:grantStatusLUTID>/', methods = ['DELETE'])
def delete_grant_status(grantStatusLUTID):
    try:
        grantStatus = query.get_grant_status(grantStatusLUTID)
        if grantStatus is not None:
            query.delete(grantStatus)
            return item_deleted("GrantStatusLUTID {} deleted".format(grantStatusLUTID))
        else:
            return item_not_found("GrantStatusLUTID {} not found".format(grantStatusLUTID))
    except Exception as e:
        return internal_error(e)

        
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
# Patient
##############################################################################
@api.route('/patients/', methods=['GET'])
@api.route('/patients/<int:patAutoID>/',methods = ['GET'])
def get_patient(patAutoID=None):
    if patAutoID is None:
        return jsonify(Patients = [i.dict() for i in query.get_patients()])
    else:
        patient = query.get_patient(patAutoID)
        if patient is not None:
            return patient.json()
        else:
            return item_not_found("PatAutoID {} not found".format(patAutoID))

@api.route('/patients/<int:patAutoID>/',methods = ['PUT'])
def update_patient(patAutoID):
    patient = query.get_patient(patAutoID)
    if patient is not None:
        try:
            patient.patID = request.form['patID']
            patient.recordID = request.form['recordID']
            patient.ucrDistID = request.form['ucrDistID']
            patient.UPDBID = request.form['UPDBID']
            patient.fname = request.form['fname']
            patient.lname = request.form['lname']
            patient.middle_name = request.form['middle_name']
            patient.maiden_name = request.form['maiden_name']
            patient.alias_fname = request.form['alias_fname']
            patient.alias_lname = request.form['alias_lname']
            patient.alias_middle_name = request.form['alias_middle_name']
            patient.dob = datetime.strptime(request.form['dob'],"%Y-%m-%d")
            patient.SSN = request.form['SSN']
            patient.sex = request.form['sex']
            patient.race = request.form['race']
            patient.ethnicity = request.form['ethnicity']
            patient.vital_status = request.form['vital_status']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return patient.json()
    else:
        return item_not_found("PatAutoID {} not found".format(patAutoID))

@api.route('/patients/', methods=['POST'])
def create_patient():
    try:
        patient = models.Patient(
           patID = request.form['patID'],
           recordID = request.form['recordID'],
           ucrDistID = request.form['ucrDistID'],
           UPDBID = request.form['UPDBID'],
           fname = request.form['fname'],
           lname = request.form['lname'],
           middle_name = request.form['middle_name'],
           maiden_name = request.form['maiden_name'],
           alias_fname = request.form['alias_fname'],
           alias_lname = request.form['alias_lname'],
           alias_middle_name = request.form['alias_middle_name'],
           dob = datetime.strptime(request.form['dob'],"%Y-%m-%d"),
           SSN = request.form['SSN'],
           sex = request.form['sex'],
           ethnicity = request.form['ethnicity'],
           vital_status = request.form['vital_status']
            )
        ret = query.add(patient)
    except KeyError as e:
       return missing_params(e)
    except Exception as e:
       return internal_error(e)
    return jsonify({'patAutoID':patient.patAutoID})

@api.route('/patients/<int:patAutoID>/',methods = ['DELETE'])
def delete_patient(patAutoID):
    try:
        patient = query.get_patient(patAutoID)
        if patient is not None:
            query.delete(patient)
            return item_deleted("PatAutoID {} deleted".format(patAutoID))
        else:
            return item_not_found("PatAutoID {} not found".format(patAutoID))
    except Exception as e:
        return internal_error(e)

        
##############################################################################
# Project 
##############################################################################
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
# Project Patient
##############################################################################
@api.route('/projectpatients/', methods = ['GET'])
@api.route('/projectpatients/<int:participantID>/', methods = ['GET'])
def get_project_patient(participantID=None):
    if participantID is None:
        return jsonify(ProjectPatients = [i.dict() for i in query.get_project_patients()])
    else:
        projectPatient = query.get_project_patient(participantID)
        if projectPatient is not None:
            return projectPatient.json()
        else:
            return item_not_found("ParticipantID {} not found".format(participantID))
            
@api.route('/projectpatients/<int:participantID>/', methods = ['PUT'])
def update_project_patient(participantID):
    projectPatient = query.get_project_patient(participantID)
    if projectPatient is not None:
        try:
            projectPatient.projectID = request.form['projectID']
            projectPatient.staffID = request.form['staffID']
            projectPatient.ctcID = request.form['ctcID']
            projectPatient.current_age = request.form['current_age']
            projectPatient.batch = request.form['batch']
            projectPatient.sitegrp = request.form['sitegrp']
            projectPatient.final_code = request.form['final_code']
            projectPatient.final_code_date = datetime.strptime(request.form['final_code_date'],"%Y-%m-%d")
            projectPatient.enrollment_date = datetime.strptime(request.form['enrollment_date'],"%Y-%m-%d")
            projectPatient.date_coord_signed = datetime.strptime(request.form['date_coord_signed'],"%Y-%m-%d")
            projectPatient.import_date = datetime.strptime(request.form['import_date'],"%Y-%m-%d")
            projectPatient.final_code_staff = request.form['final_code_staff']
            projectPatient.enrollment_staff = request.form['enrollment_staff']
            projectPatient.date_coord_signed_staff = datetime.strptime(request.form['date_coord_signed_staff'],"%Y-%m-%d")
            projectPatient.abstract_status = request.form['abstract_status']
            projectPatient.abstract_status_date = datetime.strptime(request.form['abstract_status_date'],"%Y-%m-%d")
            projectPatient.abstract_status_staff = request.form['abstract_status_staff']
            projectPatient.sent_to_abstractor = datetime.strptime(request.form['sent_to_abstractor'],"%Y-%m-%d")
            projectPatient.sent_to_abstractor_staff = request.form['sent_to_abstractor_staff']
            projectPatient.abstracted_date = datetime.strptime(request.form['abstracted_date'],"%Y-%m-%d")
            projectPatient.abstractor_initials = request.form['abstractor_initials']
            projectPatient.researcher_date = datetime.strptime(request.form['researcher_date'],"%Y-%m-%d")
            projectPatient.researcher_staff = request.form['researcher_staff']
            projectPatient.consent_link = request.form['consent_link']
            projectPatient.tracing_status = request.form['tracing_status']
            projectPatient.med_record_release_signed = "true" == request.form['med_record_release_signed'].lower()
            projectPatient.med_record_release_link = request.form['med_record_release_link']
            projectPatient.med_record_release_staff = request.form['med_record_release_staff']
            projectPatient.med_record_release_date =  datetime.strptime(request.form['med_record_release_date'],"%Y-%m-%d")
            projectPatient.survey_to_researcher =  datetime.strptime(request.form['survey_to_researcher'],"%Y-%m-%d")
            projectPatient.survey_to_researcher_staff = request.form['survey_to_researcher_staff']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return projectPatient.json()
    else:
        return item_not_found("ParticipantID {} not found".format(participantID)) 

@api.route('/projectpatients/', methods=['POST'])
def create_project_patient():
    try:
        projectPatient = models.ProjectPatient(
            projectID = request.form['projectID'],
            staffID = request.form['staffID'],
            ctcID = request.form['ctcID'],
            current_age = request.form['current_age'],
            batch = request.form['batch'],
            sitegrp = request.form['sitegrp'],
            final_code = request.form['final_code'],
            final_code_date = datetime.strptime(request.form['final_code_date'],"%Y-%m-%d"),
            enrollment_date = datetime.strptime(request.form['enrollment_date'],"%Y-%m-%d"),
            date_coord_signed = datetime.strptime(request.form['date_coord_signed'],"%Y-%m-%d"),
            import_date = datetime.strptime(request.form['import_date'],"%Y-%m-%d"),
            final_code_staff = request.form['final_code_staff'],
            enrollment_staff = request.form['enrollment_staff'],
            date_coord_signed_staff = datetime.strptime(request.form['date_coord_signed_staff'],"%Y-%m-%d"),
            abstract_status = request.form['abstract_status'],
            abstract_status_date = datetime.strptime(request.form['abstract_status_date'],"%Y-%m-%d"),
            abstract_status_staff = request.form['abstract_status_staff'],
            sent_to_abstractor = datetime.strptime(request.form['sent_to_abstractor'],"%Y-%m-%d"),
            sent_to_abstractor_staff = request.form['sent_to_abstractor_staff'],
            abstracted_date = datetime.strptime(request.form['abstracted_date'],"%Y-%m-%d"),
            abstractor_initials = request.form['abstractor_initials'],
            researcher_date = datetime.strptime(request.form['researcher_date'],"%Y-%m-%d"),
            researcher_staff = request.form['researcher_staff'],
            consent_link = request.form['consent_link'],
            tracing_status = request.form['tracing_status'],
            med_record_release_signed = "true" == request.form['med_record_release_signed'].lower(),
            med_record_release_link = request.form['med_record_release_link'],
            med_record_release_staff = request.form['med_record_release_staff'],
            med_record_release_date =  datetime.strptime(request.form['med_record_release_date'],"%Y-%m-%d"),
            survey_to_researcher =  datetime.strptime(request.form['survey_to_researcher'],"%Y-%m-%d"),
            survey_to_researcher_staff = request.form['survey_to_researcher_staff']
        )
        ret = query.add(projectPatient)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'participantID':projectPatient.participantID})        

@api.route('/projectpatients/<int:participantID>/', methods = ['DELETE'])
def delete_project_patient(participantID):
    try:
        projectPatient = query.get_project_patient(participantID)
        if projectPatient is not None:
            query.delete(projectPatient)
            return item_deleted("ParticipantID {} deleted".format(participantID))
        else:
            return item_not_found("ParticipantID {} not found".format(participantID))
    except Exception as e:
        return internal_error(e)
    
        
##############################################################################
# Project Status
##############################################################################
@api.route('/projectstatuses/', methods = ['GET'])
@api.route('/projectstatuses/<int:projectStatusID>/', methods = ['GET'])
def get_project_status(projectStatusID=None):
    if projectStatusID is None:
        return jsonify(ProjectStatuses = [i.dict() for i in query.get_project_statuses()])
    else:
        projectStatus = query.get_project_status(projectStatusID)
        if projectStatus is not None:
            return projectStatus.json()
        else:
            return item_not_found("ProjectStatusID {} not found".format(projectStatusID))
            
@api.route('/projectstatuses/<int:projectStatusID>/', methods = ['PUT'])
def update_project_status(projectStatusID):
    projectStatus = query.get_project_status(projectStatusID)
    if projectStatus is not None:
        try:
            projectStatus.projectStatusLUTID = request.form['projectStatusLUTID']
            projectStatus.projectID = request.form['projectID']
            projectStatus.staffID = request.form['staffID']
            projectStatus.status_date = datetime.strptime(request.form['status_date'],"%Y-%m-%d")
            projectStatus.status_notes = request.form['status_notes']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return projectStatus.json()
    else:
        return item_not_found("ProjectStatusID {} not found".format(projectStatusID)) 

@api.route('/projectstatuses/', methods=['POST'])
def create_project_status():
    try:
        projectStatus = models.ProjectStatus(
            projectStatusLUTID = request.form['projectStatusLUTID'],
            projectID = request.form['projectID'],
            staffID = request.form['staffID'],
            status_date = datetime.strptime(request.form['status_date'],"%Y-%m-%d"),
            status_notes = request.form['status_notes']
        )
        ret = query.add(projectStatus)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'projectStatusID':projectStatus.projectStatusID})        

@api.route('/projectstatuses/<int:projectStatusID>/', methods = ['DELETE'])
def delete_project_status(projectStatusID):
    try:
        projectStatus = query.get_project_status(projectStatusID)
        if projectStatus is not None:
            query.delete(projectStatus)
            return item_deleted("ProjectStatusID {} deleted".format(projectStatusID))
        else:
            return item_not_found("ProjectStatusID {} not found".format(projectStatusID))
    except Exception as e:
        return internal_error(e)
    
        
##############################################################################
# ProjectStatusLUT/Type
##############################################################################
@api.route('/projectstatustypes/', methods = ['GET'])
@api.route('/projectstatustypes/<int:projectStatusTypeID>/', methods = ['GET'])
def get_project_status_lut(projectStatusTypeID=None):
    if projectStatusTypeID is None:
        return jsonify(ProjectStatusTypes = [i.dict() for i in query.get_project_status_luts()])
    else:
        projectStatusType = query.get_project_status_lut(projectStatusTypeID)
        if projectStatusType is not None:
            return projectStatusType.json()
        else:
            return item_not_found("ProjectStatusTypeID {} not found".format(projectStatusTypeID))
            
@api.route('/projectstatustypes/<int:projectStatusTypeID>/', methods = ['PUT'])
def update_project_status_lut(projectStatusTypeID):
    projectStatusType = query.get_project_status_lut(projectStatusTypeID)
    if projectStatusType is not None:
        try:
            projectStatusType.project_status = request.form['project_status']
            projectStatusType.status_definition = request.form['status_definition']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return projectStatusType.json()
    else:
        return item_not_found("ProjectStatusTypeID {} not found".format(projectStatusTypeID)) 

@api.route('/projectstatustypes/', methods=['POST'])
def create_project_status_lut():
    try:
        projectStatusType = models.ProjectStatusLUT(
            project_status = request.form['project_status'],
            status_definition = request.form['status_definition']
        )
        ret = query.add(projectStatusType)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'projectStatusTypeID':projectStatusType.projectStatusTypeID})        

@api.route('/projectstatustypes/<int:projectStatusTypeID>/', methods = ['DELETE'])
def delete_project_status_lut(projectStatusTypeID):
    try:
        projectStatusType = query.get_project_status_lut(projectStatusTypeID)
        if projectStatusType is not None:
            query.delete(projectStatusType)
            return item_deleted("ProjectStatusTypeID {} deleted".format(projectStatusTypeID))
        else:
            return item_not_found("ProjectStatusTypeID {} not found".format(projectStatusTypeID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# ProjecType
##############################################################################
@api.route('/projecttypes/', methods = ['GET'])
@api.route('/projecttypes/<int:projectTypeID>/', methods = ['GET'])
def get_project_type(projectTypeID=None):
    if projectTypeID is None:
        return jsonify(ProjectTypes = [i.dict() for i in query.get_project_types()])
    else:
        projectType = query.get_project_type(projectTypeID)
        if projectType is not None:
            return projectType.json()
        else:
            return item_not_found("ProjectTypeID {} not found".format(projectTypeID))
            
@api.route('/projecttypes/<int:projectTypeID>/', methods = ['PUT'])
def update_project_type(projectTypeID):
    projectType = query.get_project_type(projectTypeID)
    if projectType is not None:
        try:
            projectType.project_type = request.form['project_type']
            projectType.project_type_definition = request.form['project_type_definition']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return projectType.json()
    else:
        return item_not_found("ProjectTypeID {} not found".format(projectTypeID)) 

@api.route('/projecttypes/', methods=['POST'])
def create_project_type():
    try:
        projectType = models.ProjectType(
            project_type = request.form['project_type'],
            project_type_definition = request.form['project_type_definition']
        )
        ret = query.add(projectType)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'projectTypeID':projectType.projectTypeID})        

@api.route('/projecttypes/<int:projectTypeID>/', methods = ['DELETE'])
def delete_project_type(projectTypeID):
    try:
        projectType = query.get_project_type(projectTypeID)
        if projectType is not None:
            query.delete(projectType)
            return item_deleted("ProjectTypeID {} deleted".format(projectTypeID))
        else:
            return item_not_found("ProjectTypeID {} not found".format(projectTypeID))
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
# ReviewCommittee
##############################################################################
@api.route('/reviewcommittees/', methods = ['GET'])
@api.route('/reviewcommittees/<int:reviewCommitteeID>/', methods = ['GET'])
def get_review_committee(reviewCommitteeID = None):
    if reviewCommitteeID is None:
        return jsonify(reviewCommittees = [i.dict() for i in query.get_review_committees()])
    else:
        reviewCommittee = query.get_review_committee(reviewCommitteeID)
        if reviewCommittee is not None:
            return reviewCommittee.json()
        else:
            return item_not_found("ReviewCommitteeID {} not found".format(reviewCommitteeID))
 
@api.route('/reviewcommittees/<int:reviewCommitteeID>/', methods = ['PUT'])
def update_review_committee(reviewCommitteeID):
    rc = query.get_review_committee(reviewCommitteeID)
    if rc is not None:
        try:
            rc.project_projectID = request.form['project_projectID']
            rc.RCStatusList_rc_StatusID = request.form['RCStatusList_rc_StatusID']
            rc.reviewCommitteeList_rcListID = request.form['reviewCommitteeList_rcListID']
            rc.review_committee_number = request.form['review_committee_number']
            rc.date_initial_review = datetime.strptime(request.form['date_initial_review'],"%Y-%m-%d")
            rc.date_expires = datetime.strptime(request.form['date_expires'],"%Y-%m-%d")
            rc.rc_note = request.form['rc_note']
            rc.rc_protocol = request.form['rc_protocol']
            rc.rc_approval = request.form['rc_approval']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return rc.json()
    else:
        return item_not_found("ReviewCommitteeID {} not found".format(reviewCommitteeID))
 
@api.route('/reviewcommittees/', methods = ['POST'])
def create_review_committee():
    try:
        rc = models.ReviewCommittee(
            project_projectID = request.form['project_projectID'],
            RCStatusList_rc_StatusID = request.form['RCStatusList_rc_StatusID'],
            reviewCommitteeList_rcListID = request.form['reviewCommitteeList_rcListID'],
            review_committee_number = request.form['review_committee_number'],
            date_initial_review = datetime.strptime(request.form['date_initial_review'],"%Y-%m-%d"),
            date_expires = datetime.strptime(request.form['date_expires'],"%Y-%m-%d"),
            rc_note = request.form['rc_note'],
            rc_protocol = request.form['rc_protocol'],
            rc_approval = request.form['rc_approval']
        )
        ret = query.add(rc)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'reviewCommitteeID':rc.reviewCommitteeID})
    
@api.route('/reviewcommittees/<int:reviewCommitteeID>/', methods = ['DELETE'])
def delete_review_committee(reviewCommitteeID):
    try:
        rc = query.get_review_committee(reviewCommitteeID)
        if rc is not None:
            query.delete(rc)
            return item_deleted("ReviewCommitteeID {} deleted".format(reviewCommitteeID))
        else:
            return item_not_found("ReviewCommitteeID {} not found".format(reviewCommitteeID))
    except Exception as e:
        return internal_error(e)
        
##############################################################################
# Review CommitteeList
##############################################################################
@api.route('/reviewcommitteelist/', methods = ['GET'])
@api.route('/reviewcommitteelist/<int:rcListID>/', methods = ['GET'])
def get_review_committee_list(rcListID=None):
    if rcListID is None:
        return jsonify(reviewCommitteeList = [i.dict() for i in query.get_review_committee_lists()])
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
        
##############################################################################
# UCR Report
##############################################################################
@api.route('/ucrreports/', methods = ['GET'])
@api.route('/ucrreports/<int:ucrReportID>/', methods = ['GET'])
def get_ucr_report(ucrReportID=None):
    if ucrReportID is None:
        return jsonify(ucrReports = [i.dict() for i in query.get_ucr_reports()])
    else:
        ucr = query.get_ucr_report(ucrReportID)
        if ucr is not None:
            return ucr.json()
        else:
            return item_not_found("UcrReportID {} not found".format(ucrReportID))
            
@api.route('/ucrreports/<int:ucrReportID>/', methods = ['PUT'])
def update_ucr_report(ucrReportID):
    ucr = query.get_ucr_report(ucrReportID)
    if ucr is not None:
        try:
            ucr.projectID = request.form['projectID']
            ucr.report_type = request.form['report_type']
            ucr.report_submitted = datetime.strptime(request.form['report_submitted'],"%Y-%m-%d")
            ucr.report_due = datetime.strptime(request.form['report_due'],"%Y-%m-%d")
            ucr.report_doc = request.form['report_doc']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return ucr.json()
    else:
        return item_not_found("UcrReportID {} not found.".format(ucrReportID))
        
@api.route('/ucrreports/', methods = ['POST'])
def create_ucr_report():
    try:
        ucr = models.UCRReport(
            projectID = request.form['projectID'],
            report_type = request.form['report_type'],
            report_submitted = datetime.strptime(request.form['report_submitted'],"%Y-%m-%d"),
            report_due = datetime.strptime(request.form['report_due'],"%Y-%m-%d"),
            report_doc = request.form['report_doc']
        )
        query.add(ucr)
        query.commit()
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'ucrReportID': ucr.ucrReportID})
    
@api.route('/ucrreports/<int:ucrReportID>/',methods = ['DELETE'])
def delete_ucr_report(ucrReportID):
    try:
        ucr = query.get_ucr_report(ucrReportID)
        if ucr is not None:
            query.delete(ucr)
            return item_deleted("UcrReportID {} deleted".format(ucrReportID))
    except Exception as e:
        return internal_error(e)