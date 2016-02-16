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

#############################################################################
# Contact Info Source
#############################################################################
@api.route('/contactinfosources/', methods = ['GET'])
@api.route('/contactinfosources/<int:contactInfoSourceLUTID>/', methods = ['GET'])
def get_contact_info_source(contactInfoSourceLUTID = None):
    if contactInfoSourceLUTID is None:
        return jsonify(ContactInfoSources = [i.dict() for i in query.get_contact_info_sources()])
    else:
        contactInfoSource = query.get_contact_info_source(contactInfoSourceLUTID)
        if contactInfoSource is not None:
            return contactInfoSource.json()
        else:
            return item_not_found("ContactInfoSourceLUTID {} not found".format(contactInfoSourceLUTID))
            
@api.route('/contactinfosources/<int:contactInfoSourceLUTID>/',methods = ['PUT'])
def update_contact_info_source(contactInfoSourceLUTID):
    contactInfoSource = query.get_contact_info_source(contactInfoSourceLUTID)
    if contactInfoSource is not None:
        try:
            contactInfoSource.contact_info_source = request.form['contact_info_source']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return interal_error(e)
        return contactInfoSource.json()
    else:
        return item_not_found("ContactInfoSourceLUTID {} not found".format(contactInfoSourceLUTID))
        
@api.route('/contactinfosources/',methods=['POST'])
def create_contact_info_source():
    try:
        contactInfoSource = models.ContactInfoSourceLUT(
            contact_info_source = request.form['contact_info_source'],
        )
        ret = query.add(contactInfoSource)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({"contactInfoSourceLUTID" : contactInfoSource.contactInfoSourceLUTID})
    
@api.route('/contactinfosources/<int:contactInfoSourceLUTID>/', methods = ['DELETE'])
def delete_contact_info_source(contactInfoSourceLUTID):
    try:
        contactInfoSource = query.get_contact_info_source(contactInfoSourceLUTID)
        if contactInfoSource is not None:
            query.delete(contactInfoSource)
            return item_deleted("ContactInfoSourceLUTID {} deleted".format(contactInfoSourceLUTID))
        else:
            return item_not_found("ContactInfoSourceLUTID {} not found".format(contactInfoSourceLUTID))
    except Exception as e:
        return internal_error(e)        
        
#############################################################################
# Contact Info Status
#############################################################################
@api.route('/contactinfostatuses/', methods = ['GET'])
@api.route('/contactinfostatuses/<int:contactInfoStatusID>/', methods = ['GET'])
def get_contact_info_status(contactInfoStatusID = None):
    if contactInfoStatusID is None:
        return jsonify(ContactInfoStatuses = [i.dict() for i in query.get_contact_info_statuses()])
    else:
        contactInfoStatus = query.get_contact_info_status(contactInfoStatusID)
        if contactInfoStatus is not None:
            return contactInfoStatus.json()
        else:
            return item_not_found("ContactInfoStatusID {} not found".format(contactInfoStatusID))
            
@api.route('/contactinfostatuses/<int:contactInfoStatusID>/',methods = ['PUT'])
def update_contact_info_status(contactInfoStatusID):
    contactInfoStatus = query.get_contact_info_status(contactInfoStatusID)
    if contactInfoStatus is not None:
        try:
            contactInfoStatus.contact_info_status = request.form['contact_info_status']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return interal_error(e)
        return contactInfoStatus.json()
    else:
        return item_not_found("ContactInfoStatusID {} not found".format(contactInfoStatusID))
        
@api.route('/contactinfostatuses/',methods=['POST'])
def create_contact_info_status():
    try:
        contactInfoStatus = models.ContactInfoStatusLUT(
            contact_info_status = request.form['contact_info_status'],
        )
        ret = query.add(contactInfoStatus)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({"contactInfoStatusID" : contactInfoStatus.contactInfoStatusID})
    
@api.route('/contactinfostatuses/<int:contactInfoStatusID>/', methods = ['DELETE'])
def delete_contact_info_status(contactInfoStatusID):
    try:
        contactInfoStatus = query.get_contact_info_status(contactInfoStatusID)
        if contactInfoStatus is not None:
            query.delete(contactInfoStatus)
            return item_deleted("ContactInfoStatusID {} deleted".format(contactInfoStatusID))
        else:
            return item_not_found("ContactInfoStatusID {} not found".format(contactInfoStatusID))
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
# Facility Phone
##############################################################################
@api.route('/facilityphones/', methods=['GET'])
@api.route('/facilityphones/<int:faciltyPhoneID>/',methods = ['GET'])
def get_facility_phone(faciltyPhoneID=None):
    if faciltyPhoneID is None:
        return jsonify(FacilityPhones = [i.dict() for i in query.get_facility_phones()])
    else:
        facilityPhone = query.get_facility_phone(faciltyPhoneID)
        if facilityPhone is not None:
            return facilityPhone.json()
        else:
            return item_not_found("FacilityPhoneID {} not found".format(faciltyPhoneID))

@api.route('/facilityphones/<int:faciltyPhoneID>/',methods = ['PUT'])
def update_facility_phone(faciltyPhoneID):
    facilityPhone = query.get_facility_phone(faciltyPhoneID)
    if facilityPhone is not None:
        try:
            facilityPhone.contactInfoSourceLUTID = request.form['contactInfoSourceLUTID']
            facilityPhone.facilityID = request.form['facilityID']
            facilityPhone.contactInfoStatusLUTID = request.form['contactInfoStatusLUTID']  
            facilityPhone.facility_name = request.form['facility_name']
            facilityPhone.clinic_name = request.form['clinic_name']
            facilityPhone.facility_phone = request.form['facility_phone']  
            facilityPhone.facility_phone_source = request.form['facility_phone_source']  
            facilityPhone.facility_phone_status = request.form['facility_phone_status']  
            facilityPhone.facility_phone_status_date = datetime.strptime(request.form['facility_phone_status_date'],"%Y-%m-%d")
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return facilityPhone.json()
    else:
        return item_not_found("FacilityPhoneID {} not found".format(faciltyPhoneID))

@api.route('/facilityphones/', methods=['POST'])
def create_facility_phone():
    try:
        facilityPhone = models.FacilityPhone(
            contactInfoSourceLUTID = request.form['contactInfoSourceLUTID'],
            facilityID = request.form['facilityID'],
            contactInfoStatusLUTID = request.form['contactInfoStatusLUTID'],
            facility_name = request.form['facility_name'],
            clinic_name = request.form['clinic_name'],
            facility_phone = request.form['facility_phone'],
            facility_phone_source = request.form['facility_phone_source'],
            facility_phone_status = request.form['facility_phone_status'], 
            facility_phone_status_date = datetime.strptime(request.form['facility_phone_status_date'],"%Y-%m-%d")
            )
        ret = query.add(facilityPhone)
    except KeyError as e:
       return missing_params(e)
    except Exception as e:
       return internal_error(e)
    return jsonify({'facilityPhoneID':facilityPhone.facilityPhoneID})

@api.route('/facilityphones/<int:faciltyPhoneID>/',methods = ['DELETE'])
def delete_facility_phone(faciltyPhoneID):
    try:
        facilityPhone = query.get_facility_phone(faciltyPhoneID)
        if facilityPhone is not None:
            query.delete(facilityPhone)
            return item_deleted("FacilityPhoneID {} deleted".format(faciltyPhoneID))
        else:
            return item_not_found("FacilityPhoneID {} not found".format(faciltyPhoneID))
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
# Informant
##############################################################################
@api.route('/informants/', methods=['GET'])
@api.route('/informants/<int:informantID>/',methods = ['GET'])
def get_informant(informantID=None):
    if informantID is None:
        return jsonify(Informants = [i.dict() for i in query.get_informants()])
    else:
        informant = query.get_informant(informantID)
        if informant is not None:
            return informant.json()
        else:
            return item_not_found("InformantID {} not found".format(informantID))

@api.route('/informants/<int:informantID>/',methods = ['PUT'])
def update_informant(informantID):
    informant = query.get_informant(informantID)
    if informant is not None:
        try:
            informant.patAutoID = request.form['patAutoID']
            informant.fname = request.form['fname']
            informant.lname = request.form['lname']
            informant.middle_name = request.form['middle_name']
            informant.informant_primary = request.form['informant_primary']
            informant.informant_relationship = request.form['informant_relationship']
            informant.notes = request.form['notes']        
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return informant.json()
    else:
        return item_not_found("InformantID {} not found".format(informantID))

@api.route('/informants/', methods=['POST'])
def create_informant():
    try:
        informant = models.Informant(
            patAutoID = request.form['patAutoID'],
            fname = request.form['fname'],
            lname = request.form['lname'],
            middle_name = request.form['middle_name'],
            informant_primary = request.form['informant_primary'],
            informant_relationship = request.form['informant_relationship'],
            notes = request.form['notes']   
            )
        ret = query.add(informant)
    except KeyError as e:
       return missing_params(e)
    except Exception as e:
       return internal_error(e)
    return jsonify({'informantID':informant.informantID})

@api.route('/informants/<int:informantID>/',methods = ['DELETE'])
def delete_informant(informantID):
    try:
        informant = query.get_informant(informantID)
        if informant is not None:
            query.delete(informant)
            return item_deleted("InformantID {} deleted".format(informantID))
        else:
            return item_not_found("InformantID {} not found".format(informantID))
    except Exception as e:
        return internal_error(e)
        
##############################################################################
# Informant Address
##############################################################################
@api.route('/informantaddresses/', methods=['GET'])
@api.route('/informantaddresses/<int:informantAddressID>/',methods = ['GET'])
def get_informant_address(informantAddressID=None):
    if informantAddressID is None:
        return jsonify(InformantAddresses = [i.dict() for i in query.get_informant_addresses()])
    else:
        informantAddress = query.get_informant_address(informantAddressID)
        if informantAddress is not None:
            return informantAddress.json()
        else:
            return item_not_found("InformantAddressID {} not found".format(informantAddressID))

@api.route('/informantaddresses/<int:informantAddressID>/',methods = ['PUT'])
def update_informant_address(informantAddressID):
    informantAddress = query.get_informant_address(informantAddressID)
    if informantAddress is not None:
        try:
            informantAddress.contactInfoSourceLUTID = request.form['contactInfoSourceLUTID']
            informantAddress.informantID = request.form['informantID']
            informantAddress.contactInfoStatusID = request.form['contactInfoStatusID']
            informantAddress.street = request.form['street']
            informantAddress.street2 = request.form['street2']
            informantAddress.city = request.form['city']
            informantAddress.state = request.form['state']
            informantAddress.zip = request.form['zip']
            informantAddress.address_status = request.form['address_status']
            informantAddress.address_status_date = datetime.strptime(request.form['address_status_date'],"%Y-%m-%d")
            informantAddress.address_status_source = request.form['address_status_source']          
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return informantAddress.json()
    else:
        return item_not_found("InformantAddressID {} not found".format(informantAddressID))

@api.route('/informantaddresses/', methods=['POST'])
def create_informant_address():
    try:
        informantAddress = models.InformantAddress(
            contactInfoSourceLUTID = request.form['contactInfoSourceLUTID'],
            informantID = request.form['informantID'],
            contactInfoStatusID = request.form['contactInfoStatusID'],
            street = request.form['street'],
            street2 = request.form['street2'],
            city = request.form['city'],
            state = request.form['state'],
            zip = request.form['zip'],
            address_status = request.form['address_status'],
            address_status_date = datetime.strptime(request.form['address_status_date'],"%Y-%m-%d"),
            address_status_source = request.form['address_status_source']  
            )
        ret = query.add(informantAddress)
    except KeyError as e:
       return missing_params(e)
    except Exception as e:
       return internal_error(e)
    return jsonify({'informantAddressID':informantAddress.informantAddressID})

@api.route('/informantaddresses/<int:informantAddressID>/',methods = ['DELETE'])
def delete_informant_address(informantAddressID):
    try:
        informantAddress = query.get_informant_address(informantAddressID)
        if informantAddress is not None:
            query.delete(informantAddress)
            return item_deleted("InformantAddressID {} deleted".format(informantAddressID))
        else:
            return item_not_found("InformantAddressID {} not found".format(informantAddressID))
    except Exception as e:
        return internal_error(e)
               
##############################################################################
# Informant Phone
##############################################################################
@api.route('/informantphones/', methods=['GET'])
@api.route('/informantphones/<int:informantPhoneID>/',methods = ['GET'])
def get_informant_phone(informantPhoneID=None):
    if informantPhoneID is None:
        return jsonify(InformantPhones = [i.dict() for i in query.get_informant_phones()])
    else:
        informantPhone = query.get_informant_phone(informantPhoneID)
        if informantPhone is not None:
            return informantPhone.json()
        else:
            return item_not_found("InformantPhoneID {} not found".format(informantPhoneID))

@api.route('/informantphones/<int:informantPhoneID>/',methods = ['PUT'])
def update_informant_phone(informantPhoneID):
    informantPhone = query.get_informant_phone(informantPhoneID)
    if informantPhone is not None:
        try:
            informantPhone.contactInfoSourceLUTID = request.form['contactInfoSourceLUTID']
            informantPhone.informantID = request.form['informantID']
            informantPhone.contactInfoStatusID = request.form['contactInfoStatusID']  
            informantPhone.phone = request.form['phone']  
            informantPhone.phone_source = request.form['phone_source']  
            informantPhone.phone_status = request.form['phone_status']  
            informantPhone.phone_status_date = datetime.strptime(request.form['phone_status_date'],"%Y-%m-%d")
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return informantPhone.json()
    else:
        return item_not_found("InformantPhoneID {} not found".format(informantPhoneID))

@api.route('/informantphones/', methods=['POST'])
def create_informant_phone():
    try:
        informantPhone = models.InformantPhone(
            contactInfoSourceLUTID = request.form['contactInfoSourceLUTID'],
            informantID = request.form['informantID'],
            contactInfoStatusID = request.form['contactInfoStatusID'],
            phone = request.form['phone'],
            phone_source = request.form['phone_source'],
            phone_status = request.form['phone_status'], 
            phone_status_date = datetime.strptime(request.form['phone_status_date'],"%Y-%m-%d")
            )
        ret = query.add(informantPhone)
    except KeyError as e:
       return missing_params(e)
    except Exception as e:
       return internal_error(e)
    return jsonify({'informantPhoneID':informantPhone.informantPhoneID})

@api.route('/informantphones/<int:informantPhoneID>/',methods = ['DELETE'])
def delete_informant_phone(informantPhoneID):
    try:
        informantPhone = query.get_informant_phone(informantPhoneID)
        if informantPhone is not None:
            query.delete(informantPhone)
            return item_deleted("InformantPhoneID {} deleted".format(informantPhoneID))
        else:
            return item_not_found("InformantPhoneID {} not found".format(informantPhoneID))
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
# Log
##############################################################################
@api.route('/logs/',methods=['GET'])
@api.route('/logs/<int:logID>/', methods = ['GET'])
def get_log(logID=None):
    if logID is None:
        return jsonify(Logs = [i.dict() for i in query.get_logs()])
    else:
        log = query.get_log(logID)
        if log is not None:
            return log.json()
        else:
            return item_not_found("LogID {} not found".format(logID))
            
@api.route('/logs/<int:logID>/', methods = ['PUT'])
def update_log(logID):
    log = query.get_log(logID)
    if log is not None:
        try:
            log.logSubjectLUTID = request.form['logSubjectLUTID']
            log.projectID = request.form['projectID']
            log.staffID = request.form['staffID']
            log.phaseStatusID = request.form['phaseStatusID']
            log.note = request.form['note']
            log.date = datetime.strptime(request.form['date'],"%Y-%m-%d") 
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return log.json()
    else:
        return item_not_found("LogID {} not found".format(logID))
        
@api.route('/logs/', methods = ['POST'])
def create_log():
    try:
        log  = models.Log(
            logSubjectLUTID = request.form['logSubjectLUTID'],
            projectID = request.form['projectID'],
            staffID = request.form['staffID'],
            phaseStatusID = request.form['phaseStatusID'],
            note = request.form['note'],
            date = datetime.strptime(request.form['date'],"%Y-%m-%d") 
        )
        ret = query.add(log)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({"logID":log.logID})
    
@api.route('/logs/<int:logID>/',methods=['DELETE'])
def delete_log(logID):
    try:
        log = query.get_log(logID)
        if log is not None:
            query.delete(log)
            return item_deleted("LogID {} deleted".format(logID))
        else:
            return item_not_found("LogID {} not found".format(logID))
    except Exception as e:
        return internal_error(e)
        
##############################################################################
# Log Subject
##############################################################################
@api.route('/logsubjects/',methods=['GET'])
@api.route('/logsubjects/<int:logSubjectLUTID>/', methods = ['GET'])
def get_log_subject(logSubjectLUTID=None):
    if logSubjectLUTID is None:
        return jsonify(LogSubjects = [i.dict() for i in query.get_log_subjects()])
    else:
        logSubject = query.get_log_subject(logSubjectLUTID)
        if logSubject is not None:
            return logSubject.json()
        else:
            return item_not_found("LogSubjectLUTID {} not found".format(logSubjectLUTID))
            
@api.route('/logsubjects/<int:logSubjectLUTID>/', methods = ['PUT'])
def update_log_subject(logSubjectLUTID):
    logSubject = query.get_log_subject(logSubjectLUTID)
    if logSubject is not None:
        try:
            logSubject.log_subject = request.form['log_subject']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return logSubject.json()
    else:
        return item_not_found("logSubjectLUTID {} not found".format(logSubjectLUTID))
        
@api.route('/logsubjects/', methods = ['POST'])
def create_log_subject():
    try:
        logSubject = models.LogSubjectLUT(
            log_subject = request.form['log_subject']
        )
        ret = query.add(logSubject)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({"logSubjectLUTID":logSubject.logSubjectLUTID})
    
@api.route('/logsubjects/<int:logSubjectLUTID>/',methods=['DELETE'])
def delete_log_subject(logSubjectLUTID):
    try:
        logSubject = query.get_log_subject(logSubjectLUTID)
        if logSubject is not None:
            query.delete(logSubject)
            return item_deleted("LogSubjectLUTID {} deleted".format(logSubjectLUTID))
        else:
            return item_not_found("LogSubjectLUTID {} not found".format(logSubjectLUTID))
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
# Patient Address
##############################################################################
@api.route('/patientaddresses/', methods=['GET'])
@api.route('/patientaddresses/<int:patAddressID>/',methods = ['GET'])
def get_patient_address(patAddressID=None):
    if patAddressID is None:
        return jsonify(PatientAddresses = [i.dict() for i in query.get_patient_addresses()])
    else:
        patientaddress = query.get_patient_address(patAddressID)
        if patientaddress is not None:
            return patientaddress.json()
        else:
            return item_not_found("PatAddressID {} not found".format(patAddressID))

@api.route('/patientaddresses/<int:patAddressID>/',methods = ['PUT'])
def update_patient_address(patAddressID):
    patientAddress = query.get_patient_address(patAddressID)
    if patientAddress is not None:
        try:
            patientAddress.contactInfoSourceLUTID = request.form['contactInfoSourceLUTID']
            patientAddress.patientID = request.form['patientID']
            patientAddress.contactInfoStatusLUTID = request.form['contactInfoStatusLUTID']
            patientAddress.street = request.form['street']
            patientAddress.street2 = request.form['street2']
            patientAddress.city = request.form['city']
            patientAddress.state = request.form['state']
            patientAddress.zip = request.form['zip']
            patientAddress.address_status = request.form['address_status']
            patientAddress.address_status_date = datetime.strptime(request.form['address_status_date'],"%Y-%m-%d")
            patientAddress.address_status_source = request.form['address_status_source']          
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return patientAddress.json()
    else:
        return item_not_found("PatAddressID {} not found".format(patAddressID))

@api.route('/patientaddresses/', methods=['POST'])
def create_patient_address():
    try:
        patientaddress = models.PatientAddress(
            contactInfoSourceLUTID = request.form['contactInfoSourceLUTID'],
            patientID = request.form['patientID'],
            contactInfoStatusLUTID = request.form['contactInfoStatusLUTID'],
            street = request.form['street'],
            street2 = request.form['street2'],
            city = request.form['city'],
            state = request.form['state'],
            zip = request.form['zip'],
            address_status = request.form['address_status'],
            address_status_date = datetime.strptime(request.form['address_status_date'],"%Y-%m-%d"),
            address_status_source = request.form['address_status_source']  
            )
        ret = query.add(patientaddress)
    except KeyError as e:
       return missing_params(e)
    except Exception as e:
       return internal_error(e)
    return jsonify({'patAddressID':patientaddress.patAddressID})

@api.route('/patientaddresses/<int:patAddressID>/',methods = ['DELETE'])
def delete_patient_address(patAddressID):
    try:
        patientaddress = query.get_patient_address(patAddressID)
        if patientaddress is not None:
            query.delete(patientaddress)
            return item_deleted("PatAddressID {} deleted".format(patAddressID))
        else:
            return item_not_found("PatAddressID {} not found".format(patAddressID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Patient Email
##############################################################################
@api.route('/patientemails/', methods=['GET'])
@api.route('/patientemails/<int:emailID>/',methods = ['GET'])
def get_patient_email(emailID=None):
    if emailID is None:
        return jsonify(PatientEmails = [i.dict() for i in query.get_patient_emails()])
    else:
        patientEmail = query.get_patient_email(emailID)
        if patientEmail is not None:
            return patientEmail.json()
        else:
            return item_not_found("EmailID {} not found".format(emailID))

@api.route('/patientemails/<int:emailID>/',methods = ['PUT'])
def update_patient_email(emailID):
    patientEmail = query.get_patient_email(emailID)
    if patientEmail is not None:
        try:
            patientEmail.contactInfoSourceLUTID = request.form['contactInfoSourceLUTID']
            patientEmail.patientID = request.form['patientID']
            patientEmail.contactInfoStatusID = request.form['contactInfoStatusID']  
            patientEmail.email = request.form['email']  
            patientEmail.email_status = request.form['email_status']  
            patientEmail.email_source = request.form['email_source']  
            patientEmail.email_status_date = datetime.strptime(request.form['email_status_date'],"%Y-%m-%d")
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return patientEmail.json()
    else:
        return item_not_found("EmailID {} not found".format(emailID))

@api.route('/patientemails/', methods=['POST'])
def create_patient_email():
    try:
        patientEmail = models.PatientEmail(
            contactInfoSourceLUTID = request.form['contactInfoSourceLUTID'],
            patientID = request.form['patientID'],
            contactInfoStatusID = request.form['contactInfoStatusID'],
            email = request.form['email'],
            email_status = request.form['email_status'],
            email_source = request.form['email_source'], 
            email_status_date = datetime.strptime(request.form['email_status_date'],"%Y-%m-%d")
            )
        ret = query.add(patientEmail)
    except KeyError as e:
       return missing_params(e)
    except Exception as e:
       return internal_error(e)
    return jsonify({'emailID':patientEmail.emailID})

@api.route('/patientemails/<int:emailID>/',methods = ['DELETE'])
def delete_patient_email(emailID):
    try:
        patientEmail = query.get_patient_email(emailID)
        if patientEmail is not None:
            query.delete(patientEmail)
            return item_deleted("EmailID {} deleted".format(emailID))
        else:
            return item_not_found("EmailID {} not found".format(emailID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Patient Phone
##############################################################################
@api.route('/patientphones/', methods=['GET'])
@api.route('/patientphones/<int:patPhoneID>/',methods = ['GET'])
def get_patient_phone(patPhoneID=None):
    if patPhoneID is None:
        return jsonify(PatientPhones = [i.dict() for i in query.get_patient_phones()])
    else:
        patientPhone = query.get_patient_phone(patPhoneID)
        if patientPhone is not None:
            return patientPhone.json()
        else:
            return item_not_found("PatPhoneID {} not found".format(patPhoneID))

@api.route('/patientphones/<int:patPhoneID>/',methods = ['PUT'])
def update_patient_phone(patPhoneID):
    patientPhone = query.get_patient_phone(patPhoneID)
    if patientPhone is not None:
        try:
            patientPhone.contactInfoSourceLUTID = request.form['contactInfoSourceLUTID']
            patientPhone.patientID = request.form['patientID']
            patientPhone.contactInfoStatusID = request.form['contactInfoStatusID']  
            patientPhone.phone = request.form['phone']  
            patientPhone.phone_source = request.form['phone_source']  
            patientPhone.phone_status = request.form['phone_status']  
            patientPhone.phone_status_date = datetime.strptime(request.form['phone_status_date'],"%Y-%m-%d")
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return patientPhone.json()
    else:
        return item_not_found("PatPhoneID {} not found".format(patPhoneID))

@api.route('/patientphones/', methods=['POST'])
def create_patient_phone():
    try:
        patientPhone = models.PatientPhone(
            contactInfoSourceLUTID = request.form['contactInfoSourceLUTID'],
            patientID = request.form['patientID'],
            contactInfoStatusID = request.form['contactInfoStatusID'],
            phone = request.form['phone'],
            phone_source = request.form['phone_source'],
            phone_status = request.form['phone_status'], 
            phone_status_date = datetime.strptime(request.form['phone_status_date'],"%Y-%m-%d")
            )
        ret = query.add(patientPhone)
    except KeyError as e:
       return missing_params(e)
    except Exception as e:
       return internal_error(e)
    return jsonify({'patPhoneID':patientPhone.patPhoneID})

@api.route('/patientphones/<int:patPhoneID>/',methods = ['DELETE'])
def delete_patient_phone(patPhoneID):
    try:
        patientPhone = query.get_patient_phone(patPhoneID)
        if patientPhone is not None:
            query.delete(patientPhone)
            return item_deleted("PatPhoneID {} deleted".format(patPhoneID))
        else:
            return item_not_found("PatPhoneID {} not found".format(patPhoneID))
    except Exception as e:
        return internal_error(e)
                 
##############################################################################
# Patient Project Status
##############################################################################
@api.route('/patientprojectstatuses/', methods = ['GET'])
@api.route('/patientprojectstatuses/<int:patientProjectStatusID>/', methods = ['GET'])
def get_patient_project_status(patientProjectStatusID=None):
    if patientProjectStatusID is None:
        return jsonify(PatientProjectStatuses = [i.dict() for i in query.get_patient_project_statuses()])
    else:
        patientProjectStatus = query.get_patient_project_status(patientProjectStatusID)
        if patientProjectStatus is not None:
            return patientProjectStatus.json()
        else:
            return item_not_found("PatientProjectStatusID {} not found".format(patientProjectStatusID))
            
@api.route('/patientprojectstatuses/<int:patientProjectStatusID>/', methods = ['PUT'])
def update_patient_project_status(patientProjectStatusID):
    patientProjectStatus = query.get_patient_project_status(patientProjectStatusID)
    if patientProjectStatus is not None:
        try:
            patientProjectStatus.patientProjectStatusLUTID = request.form['patientProjectStatusLUTID']
            patientProjectStatus.projectPatientID = request.form['projectPatientID']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return patientProjectStatus.json()
    else:
        return item_not_found("PatientProjectStatusID {} not found".format(patientProjectStatusID)) 

@api.route('/patientprojectstatuses/', methods=['POST'])
def create_patient_project_status():
    try:
        patientProjectStatus = models.PatientProjectStatus(
            patientProjectStatusLUTID = request.form['patientProjectStatusLUTID'],
            projectPatientID = request.form['projectPatientID']
        )
        ret = query.add(patientProjectStatus)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'patientProjectStatusID':patientProjectStatus.patientProjectStatusID})        

@api.route('/patientprojectstatuses/<int:patientProjectStatusID>/', methods = ['DELETE'])
def delete_patient_project_status(patientProjectStatusID):
    try:
        patientProjectStatus = query.get_patient_project_status(patientProjectStatusID)
        if patientProjectStatus is not None:
            query.delete(patientProjectStatus)
            return item_deleted("PatientProjectStatusID {} deleted".format(patientProjectStatusID))
        else:
            return item_not_found("PatientProjectStatusID {} not found".format(patientProjectStatusID))
    except Exception as e:
        return internal_error(e)
    
##############################################################################
# Patient Project Status Type LUT
##############################################################################
@api.route('/patientprojectstatustypes/', methods = ['GET'])
@api.route('/patientprojectstatustypes/<int:patientProjectStatusTypeID>/', methods = ['GET'])
def get_patient_project_status_type(patientProjectStatusTypeID=None):
    if patientProjectStatusTypeID is None:
        return jsonify(PatientProjectStatusTypes = [i.dict() for i in query.get_patient_project_status_types()])
    else:
        patientProjectStatusType = query.get_patient_project_status_type(patientProjectStatusTypeID)
        if patientProjectStatusType is not None:
            return patientProjectStatusType.json()
        else:
            return item_not_found("PatientProjectStatusTypeID {} not found".format(patientProjectStatusTypeID))
            
@api.route('/patientprojectstatustypes/<int:patientProjectStatusTypeID>/', methods = ['PUT'])
def update_patient_project_status_type(patientProjectStatusTypeID):
    patientProjectStatusType = query.get_patient_project_status_type(patientProjectStatusTypeID)
    if patientProjectStatusType is not None:
        try:
            patientProjectStatusType.status_description = request.form['status_description']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return patientProjectStatusType.json()
    else:
        return item_not_found("PatientProjectStatusTypeID {} not found".format(patientProjectStatusTypeID)) 

@api.route('/patientprojectstatustypes/', methods=['POST'])
def create_patient_project_status_type():
    try:
        patientProjectStatusType = models.PatientProjectStatusLUT(
            status_description = request.form['status_description']
        )
        ret = query.add(patientProjectStatusType)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'patientProjectStatusTypeID':patientProjectStatusType.patientProjectStatusTypeID})        

@api.route('/patientprojectstatustypes/<int:patientProjectStatusTypeID>/', methods = ['DELETE'])
def delete_patient_project_status_type(patientProjectStatusTypeID):
    try:
        patientProjectStatusType = query.get_patient_project_status_type(patientProjectStatusTypeID)
        if patientProjectStatusType is not None:
            query.delete(patientProjectStatusType)
            return item_deleted("PatientProjectStatusTypeID {} deleted".format(patientProjectStatusTypeID))
        else:
            return item_not_found("PatientProjectStatusTypeID {} not found".format(patientProjectStatusTypeID))
    except Exception as e:
        return internal_error(e)
                     
##############################################################################
# Phase Status
##############################################################################
@api.route('/phasestatuses/', methods = ['GET'])
@api.route('/phasestatuses/<int:logPhaseID>/', methods = ['GET'])
def get_phase_status(logPhaseID=None):
    if logPhaseID is None:
        return jsonify(PhaseStatuses = [i.dict() for i in query.get_phase_statuses()])
    else:
        phaseStatus = query.get_phase_status(logPhaseID)
        if phaseStatus is not None:
            return phaseStatus.json()
        else:
            return item_not_found("LogPhaseID {} not found".format(logPhaseID))
            
@api.route('/phasestatuses/<int:logPhaseID>/', methods = ['PUT'])
def update_phase_status(logPhaseID):
    phaseStatus = query.get_phase_status(logPhaseID)
    if phaseStatus is not None:
        try:
            phaseStatus.phase_status = request.form['phase_status']
            phaseStatus.phase_description = request.form['phase_description']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return phaseStatus.json()
    else:
        return item_not_found("LogPhaseID {} not found".format(logPhaseID)) 

@api.route('/phasestatuses/', methods=['POST'])
def create_phase_status():
    try:
        phaseStatus = models.PhaseStatus(
            phase_status = request.form['phase_status'],
            phase_description = request.form['phase_description']
        )
        ret = query.add(phaseStatus)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'logPhaseID':phaseStatus.logPhaseID})        

@api.route('/phasestatuses/<int:logPhaseID>/', methods = ['DELETE'])
def delete_phase_status(logPhaseID):
    try:
        phaseStatus = query.get_phase_status(logPhaseID)
        if phaseStatus is not None:
            query.delete(phaseStatus)
            return item_deleted("LogPhaseID {} deleted".format(logPhaseID))
        else:
            return item_not_found("LogPhaseID {} not found".format(logPhaseID))
    except Exception as e:
        return internal_error(e)
    
##############################################################################
# PreApplication
##############################################################################
@api.route('/preapplications/', methods = ['GET'])
@api.route('/preapplications/<int:preApplicationID>/', methods = ['GET'])
def get_pre_application(preApplicationID=None):
    if preApplicationID is None:
        return jsonify(PreApplications = [i.dict() for i in query.get_pre_applications()])
    else:
        preApplication = query.get_pre_application(preApplicationID)
        if preApplication is not None:
            return preApplication.json()
        else:
            return item_not_found("PreApplicationID {} not found".format(preApplicationID))
            
@api.route('/preapplications/<int:preApplicationID>/', methods = ['PUT'])
def update_pre_application(preApplicationID):
    preApplication = query.get_pre_application(preApplicationID)
    print("test")
    if preApplication is not None:
        try:
            preApplication.projectID = request.form['projectID']
            preApplication.pi_fname = request.form['pi_fname']
            preApplication.pi_lname = request.form['pi_lname']
            preApplication.pi_phone = request.form['pi_phone']
            preApplication.pi_email = request.form['pi_email']
            preApplication.contact_fname = request.form['contact_fname']
            preApplication.contact_lname = request.form['contact_lname']
            preApplication.contact_phone = request.form['contact_phone']
            preApplication.contact_email = request.form['contact_email']
            preApplication.institution = request.form['institution']
            preApplication.institution2 = request.form['institution2']
            preApplication.uid = request.form['uid']
            preApplication.udoh = request.form['udoh']
            preApplication.project_title = request.form['project_title']
            preApplication.purpose = request.form['purpose']
            preApplication.irb0 = "true" == request.form['irb0'].lower()
            preApplication.irb1 = "true" == request.form['irb1'].lower()
            preApplication.irb2 = "true" == request.form['irb2'].lower()
            preApplication.irb3 = "true" == request.form['irb3'].lower()
            preApplication.irb4 = "true" == request.form['irb4'].lower()
            preApplication.other_irb = request.form['other_irb']
            preApplication.updb = "true" == request.form['updb'].lower()
            preApplication.pt_contact = "true" == request.form['pt_contact'].lower()
            preApplication.start_date = datetime.strptime(request.form['start_date'],"%Y-%m-%d")
            preApplication.link = "true" == request.form['link'].lower()
            preApplication.delivery_date = datetime.strptime(request.form['delivery_date'], "%Y-%m-%d")
            preApplication.description = request.form['description']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return preApplication.json()
    else:
        return item_not_found("PreApplicationID {} not found".format(preApplicationID)) 

@api.route('/preapplications/', methods=['POST'])
def create_pre_application():
    try:
        preApplication = models.PreApplication(
            projectID = request.form['projectID'],
            pi_fname = request.form['pi_fname'],
            pi_lname = request.form['pi_lname'],
            pi_phone = request.form['pi_phone'],
            pi_email = request.form['pi_email'],
            contact_fname = request.form['contact_fname'],
            contact_lname = request.form['contact_lname'],
            contact_phone = request.form['contact_phone'],
            contact_email = request.form['contact_email'],
            institution = request.form['institution'],
            institution2 = request.form['institution2'],
            uid = request.form['uid'],
            udoh = request.form['udoh'],
            project_title = request.form['project_title'],
            purpose = request.form['purpose'],
            irb0 = "true" == request.form['irb0'].lower(),
            irb1 = "true" == request.form['irb1'].lower(),
            irb2 = "true" == request.form['irb2'].lower(),
            irb3 = "true" == request.form['irb3'].lower(),
            irb4 = "true" == request.form['irb4'].lower(),
            other_irb = request.form['other_irb'],
            updb = "true" == request.form['updb'].lower(),
            pt_contact = "true" == request.form['pt_contact'].lower(),
            start_date = datetime.strptime(request.form['start_date'],"%Y-%m-%d"),
            link = "true" == request.form['link'].lower(),
            delivery_date = datetime.strptime(request.form['delivery_date'], "%Y-%m-%d"),
            description = request.form['description']
        )
        ret = query.add(preApplication)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'preApplicationID':preApplication.preApplicationID})        

@api.route('/preapplications/<int:preApplicationID>/', methods = ['DELETE'])
def delete_pre_application(preApplicationID):
    try:
        preApplication = query.get_pre_application(preApplicationID)
        if preApplication is not None:
            query.delete(preApplication)
            return item_deleted("PreApplicationID {} deleted".format(preApplicationID))
        else:
            return item_not_found("PreApplicationID {} not found".format(preApplicationID))
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
# Project Staff
##############################################################################
@api.route('/projectstaff/', methods = ['GET'])
@api.route('/projectstaff/<int:projectStaffID>/', methods = ['GET'])
def get_project_staff(projectStaffID=None):
    if projectStaffID is None:
        return jsonify(ProjectStaff = [i.dict() for i in query.get_project_staffs()])
    else:
        projectStaff = query.get_project_staff(projectStaffID)
        if projectStaff is not None:
            return projectStaff.json()
        else:
            return item_not_found("ProjectStaffID {} not found".format(projectStaffID))
            
@api.route('/projectstaff/<int:projectStaffID>/', methods = ['PUT'])
def update_project_staff(projectStaffID):
    projectStaff = query.get_project_staff(projectStaffID)
    if projectStaff is not None:
        try:
            projectStaff.staffRoleLUTID = request.form['staffRoleLUTID']
            projectStaff.projectID = request.form['projectID']
            projectStaff.staffID = request.form['staffID']
            projectStaff.role = request.form['role']
            projectStaff.date_pledge = datetime.strptime(request.form['date_pledge'],"%Y-%m-%d")
            projectStaff.date_revoked = datetime.strptime(request.form['date_revoked'],"%Y-%m-%d")
            projectStaff.contact = request.form['contact']
            projectStaff.inactive = request.form['inactive']
            projectStaff.human_sub_training_exp = datetime.strptime(request.form['human_sub_training_exp'],"%Y-%m-%d")
            projectStaff.human_sub_type_id = request.form['human_sub_type_id']
            projectStaff.study_role = request.form['study_role']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return projectStaff.json()
    else:
        return item_not_found("ProjectStaffID {} not found".format(projectStaffID)) 

@api.route('/projectstaff/', methods=['POST'])
def create_project_staff():
    try:
        projectStaff = models.ProjectStaff(
            staffRoleLUTID = request.form['staffRoleLUTID'],
            projectID = request.form['projectID'],
            staffID = request.form['staffID'],
            role = request.form['role'],
            date_pledge = datetime.strptime(request.form['date_pledge'],"%Y-%m-%d"),
            date_revoked = datetime.strptime(request.form['date_revoked'],"%Y-%m-%d"),
            contact = request.form['contact'],
            inactive = request.form['inactive'],
            human_sub_training_exp = datetime.strptime(request.form['human_sub_training_exp'],"%Y-%m-%d"),
            human_sub_type_id = request.form['human_sub_type_id'],
            study_role = request.form['study_role']
        )
        ret = query.add(projectStaff)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'projectStaffID':projectStaff.projectStaffID})        

@api.route('/projectstaff/<int:projectStaffID>/', methods = ['DELETE'])
def delete_project_staff(projectStaffID):
    try:
        projectStaff = query.get_project_staff(projectStaffID)
        if projectStaff is not None:
            query.delete(projectStaff)
            return item_deleted("ProjectStaffID {} deleted".format(projectStaffID))
        else:
            return item_not_found("ProjectStaffID {} not found".format(projectStaffID))
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
# Tracing
##############################################################################
@api.route('/tracings/', methods = ['GET'])
@api.route('/tracings/<int:tracingID>/', methods = ['GET'])
def get_tracing(tracingID=None):
    if tracingID is None:
        return jsonify(Tracings = [i.dict() for i in query.get_tracings()])
    else:
        tracing = query.get_tracing(tracingID)
        if tracing is not None:
            return tracing.json()
        else:
            return item_not_found("TracingID {} not found".format(tracingID))
            
@api.route('/tracings/<int:tracingID>/',methods = ['PUT'])
def update_tracing(tracingID):
    tracing = query.get_tracing(tracingID)
    if tracing is not None:
        try:
            tracing.tracingSourceLUTID = request.form['tracingSourceLUTID']
            tracing.projectPatientID = request.form['projectPatientID']
            tracing.date = datetime.strptime(request.form['date'],"%Y-%m-%d")
            tracing.staff = request.form['staff']
            tracing.notes = request.form['notes']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return tracing.json()
    else:
        return item_not_found("TracingID {} not found".format(tracingID))
        
@api.route('/tracings/',methods = ['POST'])
def create_tracing():
    try:
        tracing = models.Tracing(
            tracingSourceLUTID = request.form['tracingSourceLUTID'],
            projectPatientID = request.form['projectPatientID'],
            date = datetime.strptime(request.form['date'],"%Y-%m-%d"),
            staff = request.form['staff'],
            notes = request.form['notes']
            )
        ret = query.add(tracing)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'tracingID':tracing.tracingID})
    
@api.route('/tracings/<int:tracingID>/', methods = ['DELETE'])
def delete_tracing(tracingID):
    try:
        tracing = query.get_tracing(tracingID)
        if tracing is not None:
            query.delete(tracing)
            return item_deleted("TracingID {} deleted".format(tracingID))
        else:
            return item_not_found("TracingID {} not found".format(tracingID))
    except Exception as e:
        return internal_error(e)
        
##############################################################################
# Tracing Source LUT
##############################################################################
@api.route('/tracingsources/', methods = ['GET'])
@api.route('/tracingsources/<int:tracingSourceLUTID>/', methods = ['GET'])
def get_tracing_source(tracingSourceLUTID=None):
    if tracingSourceLUTID is None:
        return jsonify(TracingSources = [i.dict() for i in query.get_tracing_sources()])
    else:
        tracing = query.get_tracing_source(tracingSourceLUTID)
        if tracing is not None:
            return tracing.json()
        else:
            return item_not_found("TracingSourceLUTID {} not found".format(tracingSourceLUTID))
            
@api.route('/tracingsources/<int:tracingSourceLUTID>/',methods = ['PUT'])
def update_tracing_source(tracingSourceLUTID):
    tracingSource = query.get_tracing_source(tracingSourceLUTID)
    if tracingSource is not None:
        try:
            tracingSource.description = request.form['description']
            query.commit()
        except KeyError as e:
            return missing_params(e)
        except Exception as e:
            return internal_error(e)
        return tracingSource.json()
    else:
        return item_not_found("TracingSourceLUTID {} not found".format(tracingSourceLUTID))
        
@api.route('/tracingsources/',methods = ['POST'])
def create_tracing_source():
    try:
        tracingSource = models.TracingSourceLUT(
            description = request.form['description']
            )
        ret = query.add(tracingSource)
    except KeyError as e:
        return missing_params(e)
    except Exception as e:
        return internal_error(e)
    return jsonify({'tracingSourceLUTID':tracingSource.tracingSourceLUTID})
    
@api.route('/tracingsources/<int:tracingSourceLUTID>/', methods = ['DELETE'])
def delete_tracing_source(tracingSourceLUTID):
    try:
        tracingSource = query.get_tracing_source(tracingSourceLUTID)
        if tracingSource is not None:
            query.delete(tracingSource)
            return item_deleted("TracingSourceLUTID {} deleted".format(tracingSourceLUTID))
        else:
            return item_not_found("TracingSourceLUTID {} not found".format(tracingSourceLUTID))
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