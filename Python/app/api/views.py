from flask import jsonify, request, url_for, redirect, abort, g, session, current_app
from flask import Blueprint, render_template, abort
import app.query as query
import app.models as models
import app.forms as forms
from datetime import datetime
from app.database import db
from sqlalchemy_utils import dependent_objects
from sqlalchemy.inspection import inspect
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
        "Message": str(message),
        "Dependencies" : []
        })

def get_dependencies(record):
    deps = list(dependent_objects(record).limit(5))
    dependencies = []
    if deps:
        for item in deps:
            dependencies.append({item.__class__.__name__: inspect(item).identity[0]})
    return dependencies

def dependency_detected(dependencies,message="Dependency Detected"):
    return jsonify({
        "Success": False,
        "Message": message,
        "Dependencies" : dependencies
    }), 400
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
    try:
        if arcReviewID is None:
            return jsonify(arcReviews = [i.dict() for i in query.get_arc_reviews()])
        else:
            arcReview = query.get_arc_review(arcReviewID)
            if arcReview is not None:
                return arcReview.json()
            else:
                return item_not_found("ArcReviewID {} not found".format(arcReviewID))
    except Exception as e:
        return internal_error(e)

@api.route('/arcreviews/<int:arcReviewID>/', methods = ['PUT'])
def update_arc_review(arcReviewID):
    try:
        arcReview = query.get_arc_review(arcReviewID)
        if arcReviewID is not None:
            form = forms.ArcReviewForm(request.form)
            if form.validate():
                arcReview.projectID = request.form['projectID']
                arcReview.reviewType = request.form['reviewType']
                arcReview.dateSentToReviewer = datetime.strptime(request.form['dateSentToReviewer'],"%Y-%m-%d")
                arcReview.reviewer1 = request.form['reviewer1']
                arcReview.reviewer1Rec = request.form['reviewer1Rec']
                arcReview.reviewer1SigDate = datetime.strptime(request.form['reviewer1SigDate'],"%Y-%m-%d")
                arcReview.reviewer1Comments = request.form['reviewer1Comments']
                arcReview.reviewer2 = request.form['reviewer2']
                arcReview.reviewer2Rec = request.form['reviewer2Rec']
                arcReview.reviewer2SigDate = datetime.strptime(request.form['reviewer2SigDate'],"%Y-%m-%d")
                arcReview.reviewer2Comments = request.form['reviewer2Comments']
                arcReview.research = request.form['research']
                arcReview.contact = "true" == request.form['contact'].lower()
                arcReview.contact = "true" == request.form['contact'].lower()
                arcReview.lnkage = "true" == request.form['lnkage'].lower()
                arcReview.engaged = "true" == request.form['engaged'].lower()
                arcReview.nonPublicData = "true" == request.form['nonPublicData'].lower()
                query.commit()
                return arcReview.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ArcReviewID {} not found".format(arcReviewID))
    except Exception as e:
        return internal_error(e)

@api.route('/arcreviews/', methods = ['POST'])
def create_arc_review():
    try:
        form = forms.ArcReviewForm(request.form)
        if form.validate():
            arcReview = models.ArcReview(
                projectID = request.form['projectID'],
                reviewType = request.form['reviewType'],
                dateSentToReviewer = datetime.strptime(request.form['dateSentToReviewer'],"%Y-%m-%d"),
                reviewer1 = request.form['reviewer1'],
                reviewer1Rec = request.form['reviewer1Rec'],
                reviewer1SigDate = datetime.strptime(request.form['reviewer1SigDate'],"%Y-%m-%d"),
                reviewer1Comments = request.form['reviewer1Comments'],
                reviewer2 = request.form['reviewer2'],
                reviewer2Rec = request.form['reviewer2Rec'],
                reviewer2SigDate = datetime.strptime(request.form['reviewer2SigDate'],"%Y-%m-%d"),
                reviewer2Comments = request.form['reviewer2Comments'],
                research = request.form['research'],
                contact = "true" == request.form['contact'].lower(),
                lnkage = "true" == request.form['lnkage'].lower(),
                engaged = "true" == request.form['engaged'].lower(),
                nonPublicData = "true" == request.form['nonPublicData'].lower()
            )
            query.add(arcReview)
            return jsonify({"arcReviewID" : arcReview.arcReviewID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/arcreviews/<int:arcReviewID>/', methods = ['DELETE'])
def delete_arc_review(arcReviewID):
    try:
        arcReview = query.get_arc_review(arcReviewID)
        if arcReview is not None:
            deps = get_dependencies(arcReview)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(arcReview)
                return item_deleted("ArcReviewID {} deleted".format(arcReviewID))
        else:
            return item_not_found("ArcReviewID {} not found".format(arcReviewID))
    except Exception as e:
        return internal_error(e)

#############################################################################
# Budget
#############################################################################
@api.route('/budgets/', methods = ['GET'])
@api.route('/budgets/<int:budgetID>/', methods = ['GET'])
def get_budget(budgetID = None):
    try:
        if budgetID is None:
            return jsonify(budgets = [i.dict() for i in query.get_budgets()])
        else:
            budget = query.get_budget(budgetID)
            if budget is not None:
                return budget.json()
            else:
                return item_not_found("BudgetID {} not found".format(budgetID))
    except Exception as e:
        return internal_error(e)

@api.route('/budgets/<int:budgetID>/',methods = ['PUT'])
def update_budget(budgetID):
    try:
        budget = query.get_budget(budgetID)
        if budget is not None:
            form = forms.BudgetForm(request.form)
            if form.validate():
                budget.projectID = request.form['projectID']
                budget.numPeriods = request.form['numPeriods']
                budget.periodStart = datetime.strptime(request.form['periodStart'],"%Y-%m-%d")
                budget.periodEnd = datetime.strptime(request.form['periodEnd'],"%Y-%m-%d")
                budget.periodTotal = request.form['periodTotal']
                budget.periodComment = request.form['periodComment']
                query.commit()
                return budget.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("BudgetID {} not found".format(budgetID))
    except Exception as e:
        return internal_error(e)

@api.route('/budgets/',methods=['POST'])
def create_budget():
    try:
        form = forms.BudgetForm(request.form)
        if form.validate():
            budget = models.Budget(
                projectID = request.form['projectID'],
                numPeriods = request.form['numPeriods'],
                periodStart = datetime.strptime(request.form['periodStart'],"%Y-%m-%d"),
                periodEnd = datetime.strptime(request.form['periodEnd'],"%Y-%m-%d"),
                periodTotal = request.form['periodTotal'],
                periodComment = request.form['periodComment']
            )
            query.add(budget)
            return jsonify({"budgetID" : budget.budgetID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/budgets/<int:budgetID>/', methods = ['DELETE'])
def delete_budget(budgetID):
    try:
        budget = query.get_budget(budgetID)
        if budget is not None:
            deps = get_dependencies(budget)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(budget)
                return item_deleted("BudgetID {} deleted".format(budgetID))
        else:
            return item_not_found("BudgetID {} not found".format(budgetID))
    except Exception as e:
        return internal_error(e)

#############################################################################
# Contact 
#############################################################################
@api.route('/contacts/', methods = ['GET'])
@api.route('/contacts/<int:contactID>/', methods = ['GET'])
def get_contact(contactID = None):
    try:
        if contactID is None:
            return jsonify(Contacts = [i.dict() for i in query.get_contacts()])
        else:
            contact = query.get_contact(contactID)
            if contact is not None:
                return contact.json()
            else:
                return item_not_found("ContactID {} not found".format(contactID))
    except Exception as e:
        return internal_error(e)

@api.route('/contacts/<int:contactID>/',methods = ['PUT'])
def update_contact(contactID):
    try:
        contact = query.get_contact(contactID)
        if contact is not None:
            form = forms.ContactForm(request.form)
            if form.validate():
                contact.contactTypeLUTID = request.form['contactTypeLUTID']
                contact.projectPatientID = request.form['projectPatientID']
                contact.staffID = request.form['staffID']
                contact.informantID = request.form['informantID']
                contact.facilityID = request.form['facilityID']
                contact.physicianID = request.form['physicianID']
                contact.description = request.form['description']
                contact.contactDate = datetime.strptime(request.form['contactDate'],"%Y-%m-%d")
                contact.initials = request.form['initials']
                contact.notes = request.form['notes']
                query.commit()
                return contact.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ContactID {} not found".format(contactID))
    except Exception as e:
        return internal_error(e)

@api.route('/contacts/',methods=['POST'])
def create_contact():
    try:
        form = forms.ContactForm(request.form)
        if form.validate():
            contact = models.Contact(
                contactTypeLUTID = request.form['contactTypeLUTID'],
                projectPatientID = request.form['projectPatientID'],
                staffID = request.form['staffID'],
                informantID = request.form['informantID'],
                facilityID = request.form['facilityID'],
                physicianID = request.form['physicianID'],
                description = request.form['description'],
                contactDate = datetime.strptime(request.form['contactDate'],"%Y-%m-%d"),
                initials = request.form['initials'],
                notes = request.form['notes'],
            )
            query.add(contact)
            return jsonify({"contactID" : contact.contactID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/contacts/<int:contactID>/', methods = ['DELETE'])
def delete_contact(contactID):
    try:
        contact = query.get_contact(contactID)
        if contact is not None:
            deps = get_dependencies(contact)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(contact)
                return item_deleted("ContactID {} deleted".format(contactID))
        else:
            return item_not_found("ContactID {} not found".format(contactID))
    except Exception as e:
        return internal_error(e)

#############################################################################
# Contact Type
#############################################################################
@api.route('/contacttypes/', methods = ['GET'])
@api.route('/contacttypes/<int:contactTypeLUTID>/', methods = ['GET'])
def get_contact_type(contactTypeID = None):
    try:
        if contactTypeID is None:
            return jsonify(ContactTypes = [i.dict() for i in query.get_contact_types()])
        else:
            contactType = query.get_contact_type(contactTypeID)
            if contactType is not None:
                return contactType.json()
            else:
                return item_not_found("ContactTypeID {} not found".format(contactTypeID))
    except Exception as e:
        return internal_error(e)

@api.route('/contacttypes/<int:contactTypeID>/',methods = ['PUT'])
def update_contact_type(contactTypeID):
    try:
        contactType = query.get_contact_type(contactTypeID)
        if contactType is not None:
            form = forms.ContactTypeLUTForm(request.form)
            if form.validate():
                contactType.contactDefinition = request.form['contactDefinition']
                query.commit()
                return contactType.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ContactTypeID {} not found".format(contactTypeID))
    except Exception as e:
        return internal_error(e)

@api.route('/contacttypes/',methods=['POST'])
def create_contact_type():
    try:
        form = forms.ContactTypeLUTForm(request.form)
        if form.validate():
            contactType = models.ContactTypeLUT(
                contactDefinition = request.form['contactDefinition'],
            )
            query.add(contactType)
            return jsonify({"contactTypeID" : contactType.contactTypeID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/contacttypes/<int:contactTypeID>/', methods = ['DELETE'])
def delete_contact_type(contactTypeID):
    try:
        contactType = query.get_contact_type(contactTypeID)
        if contactType is not None:
            deps = get_dependencies(contactType)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(contactType)
                return item_deleted("ContactTypeID {} deleted".format(contactTypeID))
        else:
            return item_not_found("ContactTypeID {} not found".format(contactTypeID))
    except Exception as e:
        return internal_error(e)

#############################################################################
# Contact Info Source
#############################################################################
@api.route('/contactinfosources/', methods = ['GET'])
@api.route('/contactinfosources/<int:contactInfoSourceID>/', methods = ['GET'])
def get_contact_info_source(contactInfoSourceID = None):
    try:
        if contactInfoSourceID is None:
            return jsonify(ContactInfoSources = [i.dict() for i in query.get_contact_info_sources()])
        else:
            contactInfoSource = query.get_contact_info_source(contactInfoSourceID)
            if contactInfoSource is not None:
                return contactInfoSource.json()
            else:
                return item_not_found("ContactInfoSourceID {} not found".format(contactInfoSourceID))
    except Exception as e:
        return internal_error(e)

@api.route('/contactinfosources/<int:contactInfoSourceID>/',methods = ['PUT'])
def update_contact_info_source(contactInfoSourceID):
    try:
        contactInfoSource = query.get_contact_info_source(contactInfoSourceID)
        if contactInfoSource is not None:
            form = forms.ContactInfoSourceForm(request.form)
            if form.validate():
                contactInfoSource.contactInfoSource = request.form['contactInfoSource']
                query.commit()
                return contactInfoSource.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ContactInfoSourceID {} not found".format(contactInfoSourceID))
    except Exception as e:
        return internal_error(e)

@api.route('/contactinfosources/',methods=['POST'])
def create_contact_info_source():
    try:
        form = forms.ContactInfoSourceForm(request.form)
        if form.validate():
            contactInfoSource = models.ContactInfoSourceLUT(
                contactInfoSource = request.form['contactInfoSource'],
            )
            query.add(contactInfoSource)
            return jsonify({"contactInfoSourceID" : contactInfoSource.contactInfoSourceID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/contactinfosources/<int:contactInfoSourceID>/', methods = ['DELETE'])
def delete_contact_info_source(contactInfoSourceID):
    try:
        contactInfoSource = query.get_contact_info_source(contactInfoSourceID)
        if contactInfoSource is not None:
            deps = get_dependencies(contactInfoSource)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(contactInfoSource)
                return item_deleted("ContactInfoSourceID {} deleted".format(contactInfoSourceID))
        else:
            return item_not_found("ContactInfoSourceID {} not found".format(contactInfoSourceID))
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
    try:
        contactInfoStatus = query.get_contact_info_status(contactInfoStatusID)
        if contactInfoStatus is not None:
            form = forms.ContactInfoStatusForm(request.form)
            if form.validate():
                contactInfoStatus.contactInfoStatus = request.form['contactInfoStatus']
                query.commit()
                return contactInfoStatus.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ContactInfoStatusID {} not found".format(contactInfoStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/contactinfostatuses/',methods=['POST'])
def create_contact_info_status():
    try:
        form = forms.ContactInfoStatusForm(request.form)
        if form.validate():
            contactInfoStatus = models.ContactInfoStatusLUT(
                contactInfoStatus = request.form['contactInfoStatus'],
            )
            query.add(contactInfoStatus)
            return jsonify({"contactInfoStatusID" : contactInfoStatus.contactInfoStatusID})
        else:
            missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/contactinfostatuses/<int:contactInfoStatusID>/', methods = ['DELETE'])
def delete_contact_info_status(contactInfoStatusID):
    try:
        contactInfoStatus = query.get_contact_info_status(contactInfoStatusID)
        if contactInfoStatus is not None:
            deps = get_dependencies(contactInfoStatus)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(contactInfoStatus)
                return item_deleted("ContactInfoStatusID {} deleted".format(contactInfoStatusID))
        else:
            return item_not_found("ContactInfoStatusID {} not found".format(contactInfoStatusID))
    except Exception as e:
        return internal_error(e)

#############################################################################
# ctc
#############################################################################
@api.route('/ctcs/', methods = ['GET'])
@api.route('/ctcs/<int:ctcID>/', methods = ['GET'])
def get_ctc(ctcID = None):
    try:
        if ctcID is None:
            return jsonify(CTCs = [i.dict() for i in query.get_ctcs()])
        else:
            ctc = query.get_ctc(ctcID)
            if ctc is not None:
                return ctc.json()
            else:
                return item_not_found("CtcID {} not found".format(ctcID))
    except Exception as e:
        return internal_error(e)

@api.route('/ctcs/<int:ctcID>/',methods = ['PUT'])
def update_ctc(ctcID):
    try:
        ctc = query.get_ctc(ctcID)
        if ctc is not None:
            form = forms.CTCForm(request.form)
            if form.validate():
                ctc.patientID = request.form['patientID']
                ctc.dxDate = datetime.strptime(request.form['dxDate'],"%Y-%m-%d")
                ctc.site = request.form['site']
                ctc.histology = request.form['histology']
                ctc.behavior = request.form['behavior']
                ctc.ctcSequence = request.form['ctcSequence']
                ctc.stage = request.form['stage']
                ctc.dxAge = request.form['dxAge']
                ctc.dxStreet1 = request.form['dxStreet1']
                ctc.dxStreet2 = request.form['dxStreet2']
                ctc.dxCity = request.form['dxCity']
                ctc.dxState = request.form['dxState']
                ctc.dxZip = request.form['dxZip']
                ctc.dxCounty = request.form['dxCounty']
                ctc.dnc = request.form['dnc']
                ctc.dncReason = request.form['dncReason']
                query.commit()
                return ctc.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("CtcID {} not found".format(ctcID))
    except Exception as e:
        return internal_error(e)

@api.route('/ctcs/',methods=['POST'])
def create_ctc():
    try:
        form = forms.CTCForm(request.form)
        if form.validate():
            ctc = models.CTC(
                patientID = request.form['patientID'],
                dxDate = datetime.strptime(request.form['dxDate'],"%Y-%m-%d"),
                site = request.form['site'],
                histology = request.form['histology'],
                behavior = request.form['behavior'],
                ctcSequence = request.form['ctcSequence'],
                stage = request.form['stage'],
                dxAge = request.form['dxAge'],
                dxStreet1 = request.form['dxStreet1'],
                dxStreet2 = request.form['dxStreet2'],
                dxCity = request.form['dxCity'],
                dxState = request.form['dxState'],
                dxZip = request.form['dxZip'],
                dxCounty = request.form['dxCounty'],
                dnc = request.form['dnc'],
                dncReason = request.form['dncReason']
            )
            query.add(ctc)
            return jsonify({"ctcID" : ctc.ctcID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/ctcs/<int:ctcID>/', methods = ['DELETE'])
def delete_ctc(ctcID):
    try:
        ctc = query.get_ctc(ctcID)
        if ctc is not None:
            deps = get_dependencies(ctc)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(ctc)
                return item_deleted("CtcID {} deleted".format(ctcID))
        else:
            return item_not_found("CtcID {} not found".format(ctcID))
    except Exception as e:
        return internal_error(e)

#############################################################################
# CTCFacility
#############################################################################
@api.route('/ctcfacilities/', methods = ['GET'])
@api.route('/ctcfacilities/<int:CTCFacilityID>/', methods = ['GET'])
def get_ctc_facility(CTCFacilityID = None):
    try:
        if CTCFacilityID is None:
            return jsonify(CTCFacilities = [i.dict() for i in query.get_ctc_facilities()])
        else:
            ctcFacility = query.get_ctc_facility(CTCFacilityID)
            if ctcFacility is not None:
                return ctcFacility.json()
            else:
                return item_not_found("CTCFacilityID {} not found".format(CTCFacilityID))
    except Exception as e:
        return internal_error(e)

@api.route('/ctcfacilities/<int:CTCFacilityID>/',methods = ['PUT'])
def update_ctc_facility(CTCFacilityID):
    try:
        ctcFacility = query.get_ctc_facility(CTCFacilityID)
        if ctcFacility is not None:
            form = forms.CTCFacilityForm(request.form)
            if form.validate():
                ctcFacility.ctcID = request.form['ctcID']
                ctcFacility.facilityID = request.form['facilityID']
                query.commit()
                return ctcFacility.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("CTCFacilityID {} not found".format(CTCFacilityID))
    except Exception as e:
        return internal_error(e)

@api.route('/ctcfacilities/',methods=['POST'])
def create_ctc_facility():
    try:
        form = forms.CTCFacilityForm(request.form)
        if form.validate():
            ctcFacility = models.CTCFacility(
                ctcID = request.form['ctcID'],
                facilityID = request.form['facilityID']
            )
            query.add(ctcFacility)
            return jsonify({"CTCFacilityID" : ctcFacility.CTCFacilityID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/ctcfacilities/<int:CTCFacilityID>/', methods = ['DELETE'])
def delete_ctc_facility(CTCFacilityID):
    try:
        ctcFacility = query.get_ctc_facility(CTCFacilityID)
        if ctcFacility is not None:
            deps = get_dependencies(ctcFacility)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(ctcFacility)
                return item_deleted("CTCFacilityID {} deleted".format(CTCFacilityID))
        else:
            return item_not_found("CTCFacilityID {} not found".format(CTCFacilityID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Funding
##############################################################################
@api.route('/fundings/', methods = ['GET'])
@api.route('/fundings/<int:fundingID>/', methods = ['GET'])
def get_funding(fundingID=None):
    try:
        if fundingID is None:
            return jsonify(Fundings = [i.dict() for i in query.get_fundings()])
        else:
            funding = query.get_funding(fundingID)
            if funding is not None:
                return funding.json()
            else:
                return item_not_found("FundingID {} not found".format(fundingID))
    except Exception as e:
        return internal_error(e)

@api.route('/fundings/<int:fundingID>/', methods = ['PUT'])
def update_funding(fundingID):
    try:
        funding = query.get_funding(fundingID)
        if funding is not None:
            form = forms.FundingForm(request.form)
            if form.validate():
                funding.grantStatusID = request.form['grantStatusID']
                funding.projectID = request.form['projectID']
                funding.fundingSourceID = request.form['fundingSourceID']
                funding.primaryFundingSource = request.form['primaryFundingSource']
                funding.secondaryFundingSource = request.form['secondaryFundingSource']
                funding.fundingNumber = request.form['fundingNumber']
                funding.grantTitle = request.form['grantTitle']
                funding.dateStatus = datetime.strptime(request.form['dateStatus'],"%Y-%m-%d")
                funding.grantPi = request.form['grantPi']
                funding.primaryChartfield = request.form['primaryChartfield']
                funding.secondaryChartfield = request.form['secondaryChartfield']
                query.commit()
                return funding.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("FundingID {} not found".format(fundingID))
    except Exception as e:
        return internal_error(e)

@api.route('/fundings/', methods=['POST'])
def create_funding():
    try:
        form = forms.FundingForm(request.form)
        if form.validate():
            funding = models.Funding(
                grantStatusID = request.form['grantStatusID'],
                projectID = request.form['projectID'],
                fundingSourceID = request.form['fundingSourceID'],
                primaryFundingSource = request.form['primaryFundingSource'],
                secondaryFundingSource = request.form['secondaryFundingSource'],
                fundingNumber = request.form['fundingNumber'],
                grantTitle = request.form['grantTitle'],
                dateStatus = datetime.strptime(request.form['dateStatus'],"%Y-%m-%d"),
                grantPi = request.form['grantPi'],
                primaryChartfield = request.form['primaryChartfield'],
                secondaryChartfield = request.form['secondaryChartfield']
            )
            query.add(funding)
            return jsonify({'fundingID':funding.fundingID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/fundings/<int:fundingID>/', methods = ['DELETE'])
def delete_funding(fundingID):
    try:
        funding = query.get_funding(fundingID)
        if funding is not None:
            deps = get_dependencies(funding)
            if deps:
                return dependency_detected(deps)
            else:
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
@api.route('/facilityphones/<int:facilityPhoneID>/',methods = ['GET'])
def get_facility_phone(facilityPhoneID=None):
    try:
        if facilityPhoneID is None:
            return jsonify(FacilityPhones = [i.dict() for i in query.get_facility_phones()])
        else:
            facilityPhone = query.get_facility_phone(facilityPhoneID)
            if facilityPhone is not None:
                return facilityPhone.json()
            else:
                return item_not_found("FacilityPhoneID {} not found".format(facilityPhoneID))
    except Exception as e:
        return internal_error(e)

@api.route('/facilityphones/<int:facilityPhoneID>/',methods = ['PUT'])
def update_facility_phone(facilityPhoneID):
    try:
        facilityPhone = query.get_facility_phone(facilityPhoneID)
        if facilityPhone is not None:
            form = forms.FacilityPhoneForm(request.form)
            if form.validate():
                facilityPhone.contactInfoSourceID = request.form['contactInfoSourceID']
                facilityPhone.facilityID = request.form['facilityID']
                facilityPhone.contactInfoStatusID = request.form['contactInfoStatusID']
                facilityPhone.clinicName = request.form['clinicName']
                facilityPhone.phoneType = request.form['phoneType']
                facilityPhone.phoneNumber = request.form['phoneNumber']
                facilityPhone.phoneSource = request.form['phoneSource']
                facilityPhone.phoneStatus = request.form['phoneStatus']
                facilityPhone.phoneStatusDate = datetime.strptime(request.form['phoneStatusDate'],"%Y-%m-%d")
                query.commit()
                return facilityPhone.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("FacilityPhoneID {} not found".format(facilityPhoneID))
    except Exception as e:
        return internal_error(e)

@api.route('/facilityphones/', methods=['POST'])
def create_facility_phone():
    try:
        form = forms.FacilityPhoneForm(request.form)
        if form.validate():
            facilityPhone = models.FacilityPhone(
                contactInfoSourceID = request.form['contactInfoSourceID'],
                facilityID = request.form['facilityID'],
                contactInfoStatusID = request.form['contactInfoStatusID'],
                clinicName = request.form['clinicName'],
                phoneNumber = request.form['phoneNumber'],
                phoneSource = request.form['phoneSource'],
                phoneStatus = request.form['phoneStatus'],
                phoneStatusDate = datetime.strptime(request.form['phoneStatusDate'],"%Y-%m-%d")
                )
            query.add(facilityPhone)
            return jsonify({'facilityPhoneID':facilityPhone.facilityPhoneID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/facilityphones/<int:facilityPhoneID>/',methods = ['DELETE'])
def delete_facility_phone(facilityPhoneID):
    try:
        facilityPhone = query.get_facility_phone(facilityPhoneID)
        if facilityPhone is not None:
            deps = get_dependencies(facilityPhone)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(facilityPhone)
                return item_deleted("FacilityPhoneID {} deleted".format(facilityPhoneID))
        else:
            return item_not_found("FacilityPhoneID {} not found".format(facilityPhoneID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Facility
##############################################################################
@api.route('/facilities/', methods=['GET'])
@api.route('/facilities/<int:facilityID>/',methods = ['GET'])
def get_facility(facilityID=None):
    try:
        if facilityID is None:
            return jsonify(Facilities = [i.dict() for i in query.get_facilities()])
        else:
            facility = query.get_facility(facilityID)
            if facility is not None:
                return facility.json()
            else:
                return item_not_found("FacilityID {} not found".format(facilityID))
    except Exception as e:
        return internal_error(e)

@api.route('/facilities/<int:facilityID>/',methods = ['PUT'])
def update_facility(facilityID):
    try:
        facility = query.get_facility(facilityID)
        if facility is not None:
            form = forms.FacilityForm(request.form)
            if form.validate():
                facility.facilityName = request.form['facilityName']
                facility.contactFirstName = request.form['contactFirstName']
                facility.contactLastName = request.form['contactLastName']
                facility.facilityStatus = request.form['facilityStatus']
                facility.facilityStatusDate = datetime.strptime(request.form['facilityStatusDate'],"%Y-%m-%d")
                facility.contact2FirstName = request.form['contact2FirstName']
                facility.contact2LastName = request.form['contact2LastName']
                query.commit()
                return facility.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("FacilityID {} not found".format(facilityID))
    except Exception as e:
        return internal_error(e)

@api.route('/facilities/', methods=['POST'])
def create_facility():
    try:
        facility = models.Facility(
            facilityName = request.form['facilityName'],
            contactFirstName = request.form['contactFirstName'],
            contactLastName = request.form['contactLastName'],
            facilityStatus = request.form['facilityStatus'],
            facilityStatusDate = datetime.strptime(request.form['facilityStatusDate'],"%Y-%m-%d"),
            contact2FirstName = request.form['contact2FirstName'],
            contact2LastName = request.form['contact2LastName']
            )
        ret = query.add(facility)
    except KeyError as e:
       return missing_params(e)
    except Exception as e:
       return internal_error(e)
    return jsonify({'facilityID':facility.facilityID})

@api.route('/facilities/<int:facilityID>/',methods = ['DELETE'])
def delete_facility(facilityID):
    try:
        facility = query.get_facility(facilityID)
        if facility is not None:
            deps = get_dependencies(facility)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(facility)
                return item_deleted("FacilityID {} deleted".format(facilityID))
        else:
            return item_not_found("FacilityID {} not found".format(facilityID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Facility Address
##############################################################################
@api.route('/facilityaddresses/', methods=['GET'])
@api.route('/facilityaddresses/<int:facilityAddressID>/',methods = ['GET'])
def get_facility_address(facilityAddressID=None):
    try:
        if facilityAddressID is None:
            return jsonify(FacilityAddresses = [i.dict() for i in query.get_facility_addresses()])
        else:
            facilityAddress = query.get_facility_address(facilityAddressID)
            if facilityAddress is not None:
                return facilityAddress.json()
            else:
                return item_not_found("FacilityAddressID {} not found".format(facilityAddressID))
    except Exception as e:
        return internal_error(e)

@api.route('/facilityaddresses/<int:facilityAddressID>/',methods = ['PUT'])
def update_facility_address(facilityAddressID):
    try:
        facilityAddress = query.get_facility_address(facilityAddressID)
        if facilityAddress is not None:
            form = forms.FacilityAddressForm(request.form)
            if form.validate():
                facilityAddress.contactInfoSourceID = request.form['contactInfoSourceID']
                facilityAddress.facilityID = request.form['facilityID']
                facilityAddress.contactInfoStatusID = request.form['contactInfoStatusID']
                facilityAddress.street = request.form['street']
                facilityAddress.street2 = request.form['street2']
                facilityAddress.city = request.form['city']
                facilityAddress.state = request.form['state']
                facilityAddress.zip = request.form['zip']
                facilityAddress.addressStatus = request.form['addressStatus']
                facilityAddress.addressStatusDate = datetime.strptime(request.form['addressStatusDate'],"%Y-%m-%d")
                facilityAddress.addressStatusSource = request.form['addressStatusSource']
                query.commit()
            else:
                return missing_params(form.errors)
            return facilityAddress.json()
        else:
            return item_not_found("FacilityAddressID {} not found".format(facilityAddressID))
    except Exception as e:
        return internal_error(e)

@api.route('/facilityaddresses/', methods=['POST'])
def create_facility_address():
    try:
        form = forms.FacilityAddressForm(request.form)
        if form.validate():
            facilityAddress = models.FacilityAddress(
                contactInfoSourceID = request.form['contactInfoSourceID'],
                facilityID = request.form['facilityID'],
                contactInfoStatusID = request.form['contactInfoStatusID'],
                street = request.form['street'],
                street2 = request.form['street2'],
                city = request.form['city'],
                state = request.form['state'],
                zip = request.form['zip'],
                addressStatus = request.form['addressStatus'],
                addressStatusDate = datetime.strptime(request.form['addressStatusDate'],"%Y-%m-%d"),
                addressStatusSource = request.form['addressStatusSource']
                )
            query.add(facilityAddress)
            return jsonify({'facilityAddressID':facilityAddress.facilityAddressID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/facilityaddresses/<int:facilityAddressID>/',methods = ['DELETE'])
def delete_facility_address(facilityAddressID):
    try:
        facilityAddress = query.get_facility_address(facilityAddressID)
        if facilityAddress is not None:
            deps = get_dependencies(facilityAddress)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(facilityAddress)
                return item_deleted("FacilityAddressID {} deleted".format(facilityAddressID))
        else:
            return item_not_found("FacilityAddressID {} not found".format(facilityAddressID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Funding Source LUT
##############################################################################
@api.route('/fundingsources/', methods = ['GET'])
@api.route('/fundingsources/<int:fundingSourceID>/', methods = ['GET'])
def get_funding_source(fundingSourceID=None):
    try:
        if fundingSourceID is None:
            return jsonify(FundingSources = [i.dict() for i in query.get_funding_sources()])
        else:
            fundingSource = query.get_funding_source(fundingSourceID)
            if fundingSource is not None:
                return fundingSource.json()
            else:
                return item_not_found("FundingSourceID {} not found".format(fundingSourceID))
    except Exception as e:
        return internal_error(e)

@api.route('/fundingsources/<int:fundingSourceID>/', methods = ['PUT'])
def update_funding_source(fundingSourceID):
    try:
        fundingSource = query.get_funding_source(fundingSourceID)
        if fundingSource is not None:
            form = forms.FundingSourceLUTForm(request.form)
            if form.validate():
                fundingSource.fundingSource = request.form['fundingSource']
                query.commit()
                return fundingSource.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("FundingSourceID {} not found".format(fundingSourceID))
    except Exception as e:
        return internal_error(e)

@api.route('/fundingsources/', methods=['POST'])
def create_funding_source():
    try:
        form = forms.FundingSourceLUTForm(request.form)
        if form.validate():
            fundingSource = models.FundingSourceLUT(
                fundingSource = request.form['fundingSource']
            )
            query.add(fundingSource)
            return jsonify({'fundingSourceID':fundingSource.fundingSourceID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/fundingsources/<int:fundingSourceID>/', methods = ['DELETE'])
def delete_funding_source(fundingSourceID):
    try:
        fundingSource = query.get_funding_source(fundingSourceID)
        if fundingSource is not None:
            deps = get_dependencies(fundingSource)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(fundingSource)
                return item_deleted("FundingSourceID {} deleted".format(fundingSourceID))
        else:
            return item_not_found("fundingSourceID {} not found".format(fundingSourceID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Grant Status LUT
##############################################################################
@api.route('/grantstatuses/', methods = ['GET'])
@api.route('/grantstatuses/<int:grantStatusID>/', methods = ['GET'])
def get_grant_status(grantStatusID=None):
    try:
        if grantStatusID is None:
            return jsonify(GrantStatuses = [i.dict() for i in query.get_grant_statuses()])
        else:
            grantStatus = query.get_grant_status(grantStatusID)
            if grantStatus is not None:
                return grantStatus.json()
            else:
                return item_not_found("GrantStatusID {} not found".format(grantStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/grantstatuses/<int:grantStatusID>/', methods = ['PUT'])
def update_grant_status(grantStatusID):
    try:
        grantStatus = query.get_grant_status(grantStatusID)
        if grantStatus is not None:
            form = forms.GrantStatusLUTForm(request.form)
            if form.validate():
                grantStatus.grantStatus = request.form['grantStatus']
                query.commit()
                return grantStatus.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("GrantStatusID {} not found".format(grantStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/grantstatuses/', methods=['POST'])
def create_grant_status():
    try:
        form = forms.GrantStatusLUTForm(request.form)
        if form.validate():
            grantStatus = models.GrantStatusLUT(
                grantStatus = request.form['grantStatus']
            )
            query.add(grantStatus)
            return jsonify({'grantStatusID':grantStatus.grantStatusID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/grantstatuses/<int:grantStatusID>/', methods = ['DELETE'])
def delete_grant_status(grantStatusID):
    try:
        grantStatus = query.get_grant_status(grantStatusID)
        if grantStatus is not None:
            deps = get_dependencies(grantStatus)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(grantStatus)
                return item_deleted("GrantStatusID {} deleted".format(grantStatusID))
        else:
            return item_not_found("GrantStatusID {} not found".format(grantStatusID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Humand Subject Training LUT
##############################################################################
@api.route('/humansubjecttrainings/', methods = ['GET'])
@api.route('/humansubjecttrainings/<int:humanSubjectTrainingID>/', methods = ['GET'])
def get_human_subject_training(humanSubjectTrainingID=None):
    try:
        if humanSubjectTrainingID is None:
            return jsonify(HumanSubjectTrainings = [i.dict() for i in query.get_human_subject_trainings()])
        else:
            humanSubjectTraining = query.get_human_subject_training(humanSubjectTrainingID)
            if humanSubjectTraining is not None:
                return humanSubjectTraining.json()
            else:
                return item_not_found("HumanSubjectTrainingID {} not found".format(humanSubjectTrainingID))
    except Exception as e:
        return internal_error(e)

@api.route('/humansubjecttrainings/<int:humanSubjectTrainingID>/', methods = ['PUT'])
def update_human_subject_training(humanSubjectTrainingID):
    try:
        humanSubjectTraining = query.get_human_subject_training(humanSubjectTrainingID)
        if humanSubjectTraining is not None:
            form = forms.HumanSubjectTrainingLUTForm(request.form)
            if form.validate():
                humanSubjectTraining.trainingType = request.form['trainingType']
                query.commit()
                return humanSubjectTraining.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("HumanSubjectTrainingID {} not found".format(humanSubjectTrainingID))
    except Exception as e:
        return internal_error(e)

@api.route('/humansubjecttrainings/', methods=['POST'])
def create_human_subject_training():
    try:
        form = forms.HumanSubjectTrainingLUTForm(request.form)
        if form.validate():
            humanSubjectTraining = models.HumanSubjectTrainingLUT(
                trainingType = request.form['trainingType']
            )
            query.add(humanSubjectTraining)
            return jsonify({'humanSubjectTrainingID':humanSubjectTraining.humanSubjectTrainingID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/humansubjecttrainings/<int:humanSubjectTrainingID>/', methods = ['DELETE'])
def delete_human_subject_training(humanSubjectTrainingID):
    try:
        humanSubjectTraining = query.get_human_subject_training(humanSubjectTrainingID)
        if humanSubjectTraining is not None:
            deps = get_dependencies(humanSubjectTraining)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(humanSubjectTraining)
                return item_deleted("HumanSubjectTrainingID {} deleted".format(humanSubjectTrainingID))
        else:
            return item_not_found("HumanSubjectTrainingID {} not found".format(humanSubjectTrainingID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Informant
##############################################################################
@api.route('/informants/', methods=['GET'])
@api.route('/informants/<int:informantID>/',methods = ['GET'])
def get_informant(informantID=None):
    try:
        if informantID is None:
            return jsonify(Informants = [i.dict() for i in query.get_informants()])
        else:
            informant = query.get_informant(informantID)
            if informant is not None:
                return informant.json()
            else:
                return item_not_found("InformantID {} not found".format(informantID))
    except Exception as e:
        return internal_error(e)

@api.route('/informants/<int:informantID>/',methods = ['PUT'])
def update_informant(informantID):
    try:
        informant = query.get_informant(informantID)
        if informant is not None:
            form = forms.InformantForm(request.form)
            if form.validate():
                informant.patientID = request.form['patientID']
                informant.firstName = request.form['firstName']
                informant.lastName = request.form['lastName']
                informant.middleName = request.form['middleName']
                informant.informantPrimary = request.form['informantPrimary']
                informant.informantRelationship = request.form['informantRelationship']
                informant.notes = request.form['notes']
                query.commit()
                return informant.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("InformantID {} not found".format(informantID))
    except Exception as e:
        return internal_error(e)

@api.route('/informants/', methods=['POST'])
def create_informant():
    try:
        form = forms.InformantForm(request.form)
        if form.validate():
            informant = models.Informant(
                patientID = request.form['patientID'],
                firstName = request.form['firstName'],
                lastName = request.form['lastName'],
                middleName = request.form['middleName'],
                informantPrimary = request.form['informantPrimary'],
                informantRelationship = request.form['informantRelationship'],
                notes = request.form['notes']
                )
            query.add(informant)
            return jsonify({'informantID':informant.informantID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/informants/<int:informantID>/',methods = ['DELETE'])
def delete_informant(informantID):
    try:
        informant = query.get_informant(informantID)
        if informant is not None:
            deps = get_dependencies(informant)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if informantAddressID is None:
            return jsonify(InformantAddresses = [i.dict() for i in query.get_informant_addresses()])
        else:
            informantAddress = query.get_informant_address(informantAddressID)
            if informantAddress is not None:
                return informantAddress.json()
            else:
                return item_not_found("InformantAddressID {} not found".format(informantAddressID))
    except Exception as e:
        return internal_error(e)

@api.route('/informantaddresses/<int:informantAddressID>/',methods = ['PUT'])
def update_informant_address(informantAddressID):
    try:
        informantAddress = query.get_informant_address(informantAddressID)
        if informantAddress is not None:
            form = forms.InformantAddressForm(request.form)
            if form.validate():
                informantAddress.contactInfoSourceID = request.form['contactInfoSourceID']
                informantAddress.informantID = request.form['informantID']
                informantAddress.contactInfoStatusID = request.form['contactInfoStatusID']
                informantAddress.street = request.form['street']
                informantAddress.street2 = request.form['street2']
                informantAddress.city = request.form['city']
                informantAddress.state = request.form['state']
                informantAddress.zip = request.form['zip']
                informantAddress.addressStatus = request.form['addressStatus']
                informantAddress.addressStatusDate = datetime.strptime(request.form['addressStatusDate'],"%Y-%m-%d")
                informantAddress.addressStatusSource = request.form['addressStatusSource']
                query.commit()
                return informantAddress.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("InformantAddressID {} not found".format(informantAddressID))
    except Exception as e:
        return internal_error(e)

@api.route('/informantaddresses/', methods=['POST'])
def create_informant_address():
    try:
        form = forms.InformantAddressForm(request.form)
        if form.validate():
            informantAddress = models.InformantAddress(
                contactInfoSourceID = request.form['contactInfoSourceID'],
                informantID = request.form['informantID'],
                contactInfoStatusID = request.form['contactInfoStatusID'],
                street = request.form['street'],
                street2 = request.form['street2'],
                city = request.form['city'],
                state = request.form['state'],
                zip = request.form['zip'],
                addressStatus = request.form['addressStatus'],
                addressStatusDate = datetime.strptime(request.form['addressStatusDate'],"%Y-%m-%d"),
                addressStatusSource = request.form['addressStatusSource']
                )
            query.add(informantAddress)
            return jsonify({'informantAddressID':informantAddress.informantAddressID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/informantaddresses/<int:informantAddressID>/',methods = ['DELETE'])
def delete_informant_address(informantAddressID):
    try:
        informantAddress = query.get_informant_address(informantAddressID)
        if informantAddress is not None:
            deps = get_dependencies(informantAddress)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if informantPhoneID is None:
            return jsonify(InformantPhones = [i.dict() for i in query.get_informant_phones()])
        else:
            informantPhone = query.get_informant_phone(informantPhoneID)
            if informantPhone is not None:
                return informantPhone.json()
            else:
                return item_not_found("InformantPhoneID {} not found".format(informantPhoneID))
    except Exception as e:
        return internal_error(e)

@api.route('/informantphones/<int:informantPhoneID>/',methods = ['PUT'])
def update_informant_phone(informantPhoneID):
    try:
        informantPhone = query.get_informant_phone(informantPhoneID)
        if informantPhone is not None:
            form = forms.InformantPhoneForm(request.form)
            if form.validate():
                informantPhone.contactInfoSourceID = request.form['contactInfoSourceID']
                informantPhone.informantID = request.form['informantID']
                informantPhone.contactInfoStatusID = request.form['contactInfoStatusID']
                informantPhone.phoneNumber = request.form['phoneNumber']
                informantPhone.phoneSource = request.form['phoneSource']
                informantPhone.phoneStatus = request.form['phoneStatus']
                informantPhone.phoneStatusDate = datetime.strptime(request.form['phoneStatusDate'],"%Y-%m-%d")
                query.commit()
                return informantPhone.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("InformantPhoneID {} not found".format(informantPhoneID))
    except Exception as e:
        return internal_error(e)

@api.route('/informantphones/', methods=['POST'])
def create_informant_phone():
    try:
        form = forms.InformantPhoneForm(request.form)
        if form.validate():
            informantPhone = models.InformantPhone(
                contactInfoSourceID = request.form['contactInfoSourceID'],
                informantID = request.form['informantID'],
                contactInfoStatusID = request.form['contactInfoStatusID'],
                phoneNumber = request.form['phoneNumber'],
                phoneSource = request.form['phoneSource'],
                phoneStatus = request.form['phoneStatus'],
                phoneStatusDate = datetime.strptime(request.form['phoneStatusDate'],"%Y-%m-%d")
                )
            query.add(informantPhone)
            return jsonify({'informantPhoneID':informantPhone.informantPhoneID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/informantphones/<int:informantPhoneID>/',methods = ['DELETE'])
def delete_informant_phone(informantPhoneID):
    try:
        informantPhone = query.get_informant_phone(informantPhoneID)
        if informantPhone is not None:
            deps = get_dependencies(informantPhone)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if irbHolderID is None:
            return jsonify(irbHolders = [i.dict() for i in query.get_irb_holders()])
        else:
            irb = query.get_irb_holder(irbHolderID)
            if irb is not None:
                return irb.json()
            else:
                return item_not_found("IrbHolderID {} not found".format(irbHolderID))
    except Exception as e:
        return internal_error(e)

@api.route('/irbholders/<int:irbHolderID>/', methods = ['PUT'])
def update_irb_holder(irbHolderID):
    try:
        irb = query.get_irb_holder(irbHolderID)
        if irb is not None:
            form = forms.IRBHolderLUTForm(request.form)
            if form.validate():
                irb.holder = request.form['holder']
                irb.holderDefinition = request.form['holderDefinition']
                query.commit()
                return irb.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("IrbHolderID {} not found".format(irbHolderID))
    except Exception as e:
        return internal_error(e)

@api.route('/irbholders/', methods = ['POST'])
def create_irb_holder():
    try:
        form = forms.IRBHolderLUTForm(request.form)
        if form.validate():
            irb = models.IRBHolderLUT(
                holder = request.form['holder'],
                holderDefinition = request.form['holderDefinition']
            )
            query.add(irb)
            return jsonify({"irbHolderID":irb.irbHolderID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/irbholders/<int:irbHolderID>/',methods=['DELETE'])
def delete_irb_holder(irbHolderID):
    try:
        irb = query.get_irb_holder(irbHolderID)
        if irb is not None:
            deps = get_dependencies(irb)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if logID is None:
            return jsonify(Logs = [i.dict() for i in query.get_logs()])
        else:
            log = query.get_log(logID)
            if log is not None:
                return log.json()
            else:
                return item_not_found("LogID {} not found".format(logID))
    except Exception as e:
        internal_error(e)

@api.route('/logs/<int:logID>/', methods = ['PUT'])
def update_log(logID):
    try:
        log = query.get_log(logID)
        if log is not None:
            form = forms.LogForm(request.form)
            if form.validate():
                log.logSubjectID = request.form['logSubjectID']
                log.projectID = request.form['projectID']
                log.staffID = request.form['staffID']
                log.phaseStatusID = request.form['phaseStatusID']
                log.note = request.form['note']
                log.date = datetime.strptime(request.form['date'],"%Y-%m-%d")
                query.commit()
                return log.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("LogID {} not found".format(logID))
    except Exception as e:
        return internal_error(e)

@api.route('/logs/', methods = ['POST'])
def create_log():
    try:
        form = forms.LogForm(request.form)
        if form.validate():
            log  = models.Log(
                logSubjectLUTID = request.form['logSubjectID'],
                projectID = request.form['projectID'],
                staffID = request.form['staffID'],
                phaseStatusID = request.form['phaseStatusID'],
                note = request.form['note'],
                date = datetime.strptime(request.form['date'],"%Y-%m-%d")
            )
            query.add(log)
            return jsonify({"logID":log.logID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/logs/<int:logID>/',methods=['DELETE'])
def delete_log(logID):
    try:
        log = query.get_log(logID)
        if log is not None:
            deps = get_dependencies(log)
            if deps:
                return dependency_detected(deps)
            else:
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
@api.route('/logsubjects/<int:logSubjectID>/', methods = ['GET'])
def get_log_subject(logSubjectID=None):
    try:
        if logSubjectID is None:
            return jsonify(LogSubjects = [i.dict() for i in query.get_log_subjects()])
        else:
            logSubject = query.get_log_subject(logSubjectID)
            if logSubject is not None:
                return logSubject.json()
            else:
                return item_not_found("LogSubjectID {} not found".format(logSubjectID))
    except Exception as e:
        return internal_error(e)

@api.route('/logsubjects/<int:logSubjectID>/', methods = ['PUT'])
def update_log_subject(logSubjectID):
    try:
        logSubject = query.get_log_subject(logSubjectID)
        if logSubject is not None:
            form = forms.LogSubjectLUTForm(request.form)
            if form.validate():
                logSubject.logSubject = request.form['logSubject']
                query.commit()
                return logSubject.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("logSubjectID {} not found".format(logSubjectID))
    except Exception as e:
        internal_error(e)

@api.route('/logsubjects/', methods = ['POST'])
def create_log_subject():
    try:
        form = forms.LogSubjectLUTForm(request.form)
        if form.validate():
            logSubject = models.LogSubjectLUT(
                logSubject = request.form['logSubject']
            )
            query.add(logSubject)
            return jsonify({"logSubjectID":logSubject.logSubjectID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/logsubjects/<int:logSubjectID>/',methods=['DELETE'])
def delete_log_subject(logSubjectID):
    try:
        logSubject = query.get_log_subject(logSubjectID)
        if logSubject is not None:
            deps = get_dependencies(logSubject)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(logSubject)
                return item_deleted("LogSubjectID {} deleted".format(logSubjectID))
        else:
            return item_not_found("LogSubjectID {} not found".format(logSubjectID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Patient
##############################################################################
@api.route('/patients/', methods=['GET'])
@api.route('/patients/<int:patAutoID>/',methods = ['GET'])
def get_patient(patAutoID=None):
    try:
        if patAutoID is None:
            return jsonify(Patients = [i.dict() for i in query.get_patients()])
        else:
            patient = query.get_patient(patAutoID)
            if patient is not None:
                return patient.json()
            else:
                return item_not_found("PatientID {} not found".format(patAutoID))
    except Exception as e:
        return internal_error(e)

@api.route('/patients/<int:patientID>/',methods = ['PUT'])
def update_patient(patientID):
    try:
        patient = query.get_patient(patientID)
        if patient is not None:
            form = forms.PatientForm(request.form)
            if form.validate():
                patient.patID = request.form['patID']
                patient.recordID = request.form['recordID']
                patient.ucrDistID = request.form['ucrDistID']
                patient.UPDBID = request.form['UPDBID']
                patient.firstName = request.form['firstName']
                patient.lastName = request.form['lastName']
                patient.middleName = request.form['middleName']
                patient.maidenName = request.form['maidenName']
                patient.aliasFirstName = request.form['aliasFirstName']
                patient.aliasLastName = request.form['aliasLastName']
                patient.aliasMiddleName = request.form['aliasMiddleName']
                patient.dob = datetime.strptime(request.form['dob'],"%Y-%m-%d")
                patient.SSN = request.form['SSN']
                patient.sex = request.form['sex']
                patient.race = request.form['race']
                patient.ethnicity = request.form['ethnicity']
                patient.vitalStatus = request.form['vitalStatus']
                query.commit()
                return patient.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PatientID {} not found".format(patientID))
    except Exception as e:
        return internal_error(e)

@api.route('/patients/', methods=['POST'])
def create_patient():
    try:
        form = forms.PatientForm(request.form)
        if form.validate():
            patient = models.Patient(
               patID = request.form['patID'],
               recordID = request.form['recordID'],
               ucrDistID = request.form['ucrDistID'],
               UPDBID = request.form['UPDBID'],
               firstName = request.form['firstName'],
               lastName = request.form['lastName'],
               middleName = request.form['middleName'],
               maidenName = request.form['maidenName'],
               aliasFirstName = request.form['aliasFirstName'],
               aliasLastName = request.form['aliasLastName'],
               aliasMiddleName = request.form['aliasMiddleName'],
               dob = datetime.strptime(request.form['dob'],"%Y-%m-%d"),
               SSN = request.form['SSN'],
               sex = request.form['sex'],
               ethnicity = request.form['ethnicity'],
               vitalStatus = request.form['vitalStatus']
                )
            query.add(patient)
            return jsonify({'patientID':patient.patientID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/patients/<int:patientID>/',methods = ['DELETE'])
def delete_patient(patientID):
    try:
        patient = query.get_patient(patientID)
        if patient is not None:
            deps = get_dependencies(patient)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(patient)
                return item_deleted("PatientID {} deleted".format(patientID))
        else:
            return item_not_found("PatientID {} not found".format(patientID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Patient Address
##############################################################################
@api.route('/patientaddresses/', methods=['GET'])
@api.route('/patientaddresses/<int:patAddressID>/',methods = ['GET'])
def get_patient_address(patAddressID=None):
    try:
        if patAddressID is None:
            return jsonify(PatientAddresses = [i.dict() for i in query.get_patient_addresses()])
        else:
            patientaddress = query.get_patient_address(patAddressID)
            if patientaddress is not None:
                return patientaddress.json()
            else:
                return item_not_found("PatAddressID {} not found".format(patAddressID))
    except Exception as e:
        return internal_error(e)

@api.route('/patientaddresses/<int:patAddressID>/',methods = ['PUT'])
def update_patient_address(patAddressID):
    try:
        patientAddress = query.get_patient_address(patAddressID)
        if patientAddress is not None:
            form = forms.PatientAddressForm(request.form)
            if form.validate():
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
                return patientAddress.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PatAddressID {} not found".format(patAddressID))
    except Exception as e:
        return internal_error(e)

@api.route('/patientaddresses/', methods=['POST'])
def create_patient_address():
    try:
        form = forms.PatientAddressForm(request.form)
        if form.validate():
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
            query.add(patientaddress)
            return jsonify({'patAddressID':patientaddress.patAddressID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/patientaddresses/<int:patAddressID>/',methods = ['DELETE'])
def delete_patient_address(patAddressID):
    try:
        patientaddress = query.get_patient_address(patAddressID)
        if patientaddress is not None:
            deps = get_dependencies(patientaddress)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if emailID is None:
            return jsonify(PatientEmails = [i.dict() for i in query.get_patient_emails()])
        else:
            patientEmail = query.get_patient_email(emailID)
            if patientEmail is not None:
                return patientEmail.json()
            else:
                return item_not_found("EmailID {} not found".format(emailID))
    except Exception as e:
        internal_error(e)

@api.route('/patientemails/<int:emailID>/',methods = ['PUT'])
def update_patient_email(emailID):
    try:
        patientEmail = query.get_patient_email(emailID)
        if patientEmail is not None:
            form = forms.PatientEmailForm(request.form)
            if form.validate():
                patientEmail.contactInfoSourceLUTID = request.form['contactInfoSourceLUTID']
                patientEmail.patientID = request.form['patientID']
                patientEmail.contactInfoStatusID = request.form['contactInfoStatusID']
                patientEmail.email = request.form['email']
                patientEmail.email_status = request.form['email_status']
                patientEmail.email_source = request.form['email_source']
                patientEmail.email_status_date = datetime.strptime(request.form['email_status_date'],"%Y-%m-%d")
                query.commit()
                return patientEmail.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("EmailID {} not found".format(emailID))
    except Exception as e:
        return internal_error(e)

@api.route('/patientemails/', methods=['POST'])
def create_patient_email():
    try:
        form = forms.PatientEmailForm(request.form)
        if form.validate():
            patientEmail = models.PatientEmail(
                contactInfoSourceLUTID = request.form['contactInfoSourceLUTID'],
                patientID = request.form['patientID'],
                contactInfoStatusID = request.form['contactInfoStatusID'],
                email = request.form['email'],
                email_status = request.form['email_status'],
                email_source = request.form['email_source'],
                email_status_date = datetime.strptime(request.form['email_status_date'],"%Y-%m-%d")
                )
            query.add(patientEmail)
            return jsonify({'emailID':patientEmail.emailID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/patientemails/<int:emailID>/',methods = ['DELETE'])
def delete_patient_email(emailID):
    try:
        patientEmail = query.get_patient_email(emailID)
        if patientEmail is not None:
            deps = get_dependencies(patientEmail)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if patPhoneID is None:
            return jsonify(PatientPhones = [i.dict() for i in query.get_patient_phones()])
        else:
            patientPhone = query.get_patient_phone(patPhoneID)
            if patientPhone is not None:
                return patientPhone.json()
            else:
                return item_not_found("PatPhoneID {} not found".format(patPhoneID))
    except Exception as e:
        return internal_error(e)

@api.route('/patientphones/<int:patPhoneID>/',methods = ['PUT'])
def update_patient_phone(patPhoneID):
    try:
        patientPhone = query.get_patient_phone(patPhoneID)
        if patientPhone is not None:
            form = forms.PatientPhoneForm(request.form)
            if form.validate():
                patientPhone.contactInfoSourceLUTID = request.form['contactInfoSourceLUTID']
                patientPhone.patientID = request.form['patientID']
                patientPhone.contactInfoStatusID = request.form['contactInfoStatusID']
                patientPhone.phone = request.form['phone']
                patientPhone.phone_source = request.form['phone_source']
                patientPhone.phone_status = request.form['phone_status']
                patientPhone.phone_status_date = datetime.strptime(request.form['phone_status_date'],"%Y-%m-%d")
                query.commit()
                return patientPhone.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PatPhoneID {} not found".format(patPhoneID))
    except Exception as e:
        return internal_error(e)
@api.route('/patientphones/', methods=['POST'])
def create_patient_phone():
    try:
        form = forms.PatientPhoneForm(request.form)
        if form.validate():
            patientPhone = models.PatientPhone(
                contactInfoSourceLUTID = request.form['contactInfoSourceLUTID'],
                patientID = request.form['patientID'],
                contactInfoStatusID = request.form['contactInfoStatusID'],
                phone = request.form['phone'],
                phone_source = request.form['phone_source'],
                phone_status = request.form['phone_status'],
                phone_status_date = datetime.strptime(request.form['phone_status_date'],"%Y-%m-%d")
                )
            query.add(patientPhone)
            return jsonify({'patPhoneID':patientPhone.patPhoneID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/patientphones/<int:patPhoneID>/',methods = ['DELETE'])
def delete_patient_phone(patPhoneID):
    try:
        patientPhone = query.get_patient_phone(patPhoneID)
        if patientPhone is not None:
            deps = get_dependencies(patientPhone)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if patientProjectStatusID is None:
            return jsonify(PatientProjectStatuses = [i.dict() for i in query.get_patient_project_statuses()])
        else:
            patientProjectStatus = query.get_patient_project_status(patientProjectStatusID)
            if patientProjectStatus is not None:
                return patientProjectStatus.json()
            else:
                return item_not_found("PatientProjectStatusID {} not found".format(patientProjectStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/patientprojectstatuses/<int:patientProjectStatusID>/', methods = ['PUT'])
def update_patient_project_status(patientProjectStatusID):
    try:
        patientProjectStatus = query.get_patient_project_status(patientProjectStatusID)
        if patientProjectStatus is not None:
            form = forms.PatientProjectStatusForm(request.form)
            if form.validate():
                patientProjectStatus.patientProjectStatusLUTID = request.form['patientProjectStatusLUTID']
                patientProjectStatus.projectPatientID = request.form['projectPatientID']
                query.commit()
                return patientProjectStatus.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PatientProjectStatusID {} not found".format(patientProjectStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/patientprojectstatuses/', methods=['POST'])
def create_patient_project_status():
    try:
        form = forms.PatientProjectStatusForm(request.form)
        if form.validate():
            patientProjectStatus = models.PatientProjectStatus(
                patientProjectStatusLUTID = request.form['patientProjectStatusLUTID'],
                projectPatientID = request.form['projectPatientID']
            )
            query.add(patientProjectStatus)
            return jsonify({'patientProjectStatusID':patientProjectStatus.patientProjectStatusID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/patientprojectstatuses/<int:patientProjectStatusID>/', methods = ['DELETE'])
def delete_patient_project_status(patientProjectStatusID):
    try:
        patientProjectStatus = query.get_patient_project_status(patientProjectStatusID)
        if patientProjectStatus is not None:
            deps = get_dependencies(patientProjectStatus)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if patientProjectStatusTypeID is None:
            return jsonify(PatientProjectStatusTypes = [i.dict() for i in query.get_patient_project_status_types()])
        else:
            patientProjectStatusType = query.get_patient_project_status_type(patientProjectStatusTypeID)
            if patientProjectStatusType is not None:
                return patientProjectStatusType.json()
            else:
                return item_not_found("PatientProjectStatusTypeID {} not found".format(patientProjectStatusTypeID))
    except Exception as e:
        return internal_error(e)

@api.route('/patientprojectstatustypes/<int:patientProjectStatusTypeID>/', methods = ['PUT'])
def update_patient_project_status_type(patientProjectStatusTypeID):
    try:
        patientProjectStatusType = query.get_patient_project_status_type(patientProjectStatusTypeID)
        if patientProjectStatusType is not None:
            form = forms.PatientProjectStatusLUTForm(request.form)
            if form.validate():
                patientProjectStatusType.status_description = request.form['status_description']
                query.commit()
                return patientProjectStatusType.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PatientProjectStatusTypeID {} not found".format(patientProjectStatusTypeID))
    except Exception as e:
        return internal_error(e)

@api.route('/patientprojectstatustypes/', methods=['POST'])
def create_patient_project_status_type():
    try:
        form = forms.PatientProjectStatusLUTForm(request.form)
        if form.validate():
            patientProjectStatusType = models.PatientProjectStatusLUT(
                status_description = request.form['status_description']
            )
            query.add(patientProjectStatusType)
            return jsonify({'patientProjectStatusTypeID':patientProjectStatusType.patientProjectStatusTypeID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/patientprojectstatustypes/<int:patientProjectStatusTypeID>/', methods = ['DELETE'])
def delete_patient_project_status_type(patientProjectStatusTypeID):
    try:
        patientProjectStatusType = query.get_patient_project_status_type(patientProjectStatusTypeID)
        if patientProjectStatusType is not None:
            deps = get_dependencies(patientProjectStatusType)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if logPhaseID is None:
            return jsonify(PhaseStatuses = [i.dict() for i in query.get_phase_statuses()])
        else:
            phaseStatus = query.get_phase_status(logPhaseID)
            if phaseStatus is not None:
                return phaseStatus.json()
            else:
                return item_not_found("LogPhaseID {} not found".format(logPhaseID))
    except Exception as e:
        return internal_error(e)

@api.route('/phasestatuses/<int:logPhaseID>/', methods = ['PUT'])
def update_phase_status(logPhaseID):
    try:
        phaseStatus = query.get_phase_status(logPhaseID)
        if phaseStatus is not None:
            form = forms.PhaseStatusForm(request.form)
            if form.validate():
                phaseStatus.phase_status = request.form['phase_status']
                phaseStatus.phase_description = request.form['phase_description']
                query.commit()
                return phaseStatus.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("LogPhaseID {} not found".format(logPhaseID))
    except Exception as e:
        return internal_error(e)

@api.route('/phasestatuses/', methods=['POST'])
def create_phase_status():
    try:
        form = forms.PhaseStatusForm(request.form)
        if form.validate():
            phaseStatus = models.PhaseStatus(
                phase_status = request.form['phase_status'],
                phase_description = request.form['phase_description']
            )
            ret = query.add(phaseStatus)
            return jsonify({'logPhaseID':phaseStatus.logPhaseID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/phasestatuses/<int:logPhaseID>/', methods = ['DELETE'])
def delete_phase_status(logPhaseID):
    try:
        phaseStatus = query.get_phase_status(logPhaseID)
        if phaseStatus is not None:
            deps = get_dependencies(phaseStatus)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(phaseStatus)
                return item_deleted("LogPhaseID {} deleted".format(logPhaseID))
        else:
            return item_not_found("LogPhaseID {} not found".format(logPhaseID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Physician
##############################################################################
@api.route('/physicians/', methods = ['GET'])
@api.route('/physicians/<int:physicianID>/', methods = ['GET'])
def get_physician(physicianID=None):
    try:
        if physicianID is None:
            return jsonify(Physicians = [i.dict() for i in query.get_physicians()])
        else:
            physician = query.get_physician(physicianID)
            if physician is not None:
                return physician.json()
            else:
                return item_not_found("PhysicianID {} not found".format(physicianID))
    except Exception as e:
        return internal_error(e)

@api.route('/physicians/<int:physicianID>/', methods = ['PUT'])
def update_physician(physicianID):
    try:
        physician = query.get_physician(physicianID)
        if physician is not None:
            form = forms.PhysicianForm(request.form)
            if form.validate():
                physician.fname = request.form['fname']
                physician.lname = request.form['lname']
                physician.middle_name = request.form['middle_name']
                physician.credentials = request.form['credentials']
                physician.specialty = request.form['specialty']
                physician.alias_fname = request.form['alias_fname']
                physician.alias_lname = request.form['alias_lname']
                physician.alias_middle_name = request.form['alias_middle_name']
                physician.physician_status = request.form['physician_status']
                physician.physician_status_date = datetime.strptime(request.form['physician_status_date'],"%Y-%m-%d")
                physician.email = request.form['email']
                query.commit()
                return physician.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysicianID {} not found".format(physicianID))
    except Exception as e:
        return internal_error(e)

@api.route('/physicians/', methods=['POST'])
def create_physician():
    try:
        form = forms.PhysicianForm(request.form)
        if form.validate():
            physician = models.Physician(
                fname = request.form['fname'],
                lname = request.form['lname'],
                middle_name = request.form['middle_name'],
                credentials = request.form['credentials'],
                specialty = request.form['specialty'],
                alias_fname = request.form['alias_fname'],
                alias_lname = request.form['alias_lname'],
                alias_middle_name = request.form['alias_middle_name'],
                physician_status = request.form['physician_status'],
                physician_status_date = datetime.strptime(request.form['physician_status_date'],"%Y-%m-%d"),
                email = request.form['email']
            )
            query.add(physician)
            return jsonify({'physicianID':physician.physicianID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/physicians/<int:physicianID>/', methods = ['DELETE'])
def delete_physician(physicianID):
    try:
        physician = query.get_physician(physicianID)
        if physician is not None:
            deps = get_dependencies(physician)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(physician)
                return item_deleted("PhysicianID {} deleted".format(physicianID))
        else:
            return item_not_found("PhysicianID {} not found".format(physicianID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Physician Address
##############################################################################
@api.route('/physicianaddresses/', methods=['GET'])
@api.route('/physicianaddresses/<int:physicianAddressID>/',methods = ['GET'])
def get_physician_address(physicianAddressID=None):
    try:
        if physicianAddressID is None:
            return jsonify(PhysicianAddresses = [i.dict() for i in query.get_physician_addresses()])
        else:
            physicianAddress = query.get_physician_address(physicianAddressID)
            if physicianAddress is not None:
                return physicianAddress.json()
            else:
                return item_not_found("PhysicianAddressID {} not found".format(physicianAddressID))
    except Exception as e:
        return internal_error(e)

@api.route('/physicianaddresses/<int:physicianAddressID>/',methods = ['PUT'])
def update_physician_address(physicianAddressID):
    try:
        physicianAddress = query.get_physician_address(physicianAddressID)
        if physicianAddress is not None:
            form = forms.PhysicianAddressForm(request.form)
            if form.validate():
                physicianAddress.contactInfoSourceLUTID = request.form['contactInfoSourceLUTID']
                physicianAddress.physicianID = request.form['physicianID']
                physicianAddress.contactInfoStatusLUTID = request.form['contactInfoStatusLUTID']
                physicianAddress.street = request.form['street']
                physicianAddress.street2 = request.form['street2']
                physicianAddress.city = request.form['city']
                physicianAddress.state = request.form['state']
                physicianAddress.zip = request.form['zip']
                physicianAddress.address_status = request.form['address_status']
                physicianAddress.address_status_date = datetime.strptime(request.form['address_status_date'],"%Y-%m-%d")
                physicianAddress.address_status_source = request.form['address_status_source']
                query.commit()
                return physicianAddress.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysicianAddressID {} not found".format(physicianAddressID))
    except Exception as e:
        return internal_error(e)

@api.route('/physicianaddresses/', methods=['POST'])
def create_physician_address():
    try:
        form = forms.PhysicianAddressForm(request.form)
        if form.validate():
            physicianAddress = models.PhysicianAddress(
                contactInfoSourceLUTID = request.form['contactInfoSourceLUTID'],
                physicianID = request.form['physicianID'],
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
            query.add(physicianAddress)
            return jsonify({'physicianAddressID':physicianAddress.physicianAddressID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/physicianaddresses/<int:physicianAddressID>/',methods = ['DELETE'])
def delete_physician_address(physicianAddressID):
    try:
        physicianAddress = query.get_physician_address(physicianAddressID)
        if physicianAddress is not None:
            deps = get_dependencies(physicianAddress)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(physicianAddress)
                return item_deleted("PhysicianAddressID {} deleted".format(physicianAddressID))
        else:
            return item_not_found("PhysicianAddressID {} not found".format(physicianAddressID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Physician Facility
##############################################################################
@api.route('/physicianfacilities/', methods=['GET'])
@api.route('/physicianfacilities/<int:physFacilityID>/',methods = ['GET'])
def get_physician_facility(physFacilityID=None):
    try:
        if physFacilityID is None:
            return jsonify(PhysicianFacilities = [i.dict() for i in query.get_physician_facilities()])
        else:
            physicianFacility = query.get_physician_facility(physFacilityID)
            if physicianFacility is not None:
                return physicianFacility.json()
            else:
                return item_not_found("PhysFacilityID {} not found".format(physFacilityID))
    except Exception as e:
        return internal_error(e)

@api.route('/physicianfacilities/<int:physFacilityID>/',methods = ['PUT'])
def update_physician_facility(physFacilityID):
    try:
        physicianFacility = query.get_physician_facility(physFacilityID)
        if physicianFacility is not None:
            form = forms.PhysicianFacilityForm(request.form)
            if form.validate():
                physicianFacility.facilityID = request.form['facilityID']
                physicianFacility.physicianID = request.form['physicianID']
                physicianFacility.phys_facility_status = request.form['phys_facility_status']
                physicianFacility.phys_facility_status_date = datetime.strptime(request.form['phys_facility_status_date'],"%Y-%m-%d")
                query.commit()
                return physicianFacility.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysFacilityID {} not found".format(physFacilityID))
    except Exception as e:
        return internal_error(e)

@api.route('/physicianfacilities/', methods=['POST'])
def create_physician_facility():
    try:
        form = forms.PhysicianFacilityForm(request.form)
        if form.validate():
            physicianFacility = models.PhysicianFacility(
                facilityID = request.form['facilityID'],
                physicianID = request.form['physicianID'],
                phys_facility_status = request.form['phys_facility_status'],
                phys_facility_status_date = datetime.strptime(request.form['phys_facility_status_date'],"%Y-%m-%d"),
                )
            query.add(physicianFacility)
            return jsonify({'physFacilityID':physicianFacility.physFacilityID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/physicianfacilities/<int:physFacilityID>/',methods = ['DELETE'])
def delete_physician_facility(physFacilityID):
    try:
        physicianFacility = query.get_physician_facility(physFacilityID)
        if physicianFacility is not None:
            deps = get_dependencies(physicianFacility)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(physicianFacility)
                return item_deleted("PhysFacilityID {} deleted".format(physFacilityID))
        else:
            return item_not_found("PhysFacilityID {} not found".format(physFacilityID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Physician Phone
##############################################################################
@api.route('/physicianphones/', methods=['GET'])
@api.route('/physicianphones/<int:physicianPhoneID>/',methods = ['GET'])
def get_physician_phone(physicianPhoneID=None):
    try:
        if physicianPhoneID is None:
            return jsonify(PhysicianPhones = [i.dict() for i in query.get_physician_phones()])
        else:
            physicianPhone = query.get_physician_phone(physicianPhoneID)
            if physicianPhone is not None:
                return physicianPhone.json()
            else:
                return item_not_found("PhysicianPhoneID {} not found".format(physicianPhoneID))
    except Exception as e:
        return internal_error(e)

@api.route('/physicianphones/<int:physicianPhoneID>/',methods = ['PUT'])
def update_physician_phone(physicianPhoneID):
    try:
        physicianPhone = query.get_physician_phone(physicianPhoneID)
        if physicianPhone is not None:
            form = forms.PhysicianPhoneForm(request.form)
            if form.validate():
                physicianPhone.contactInfoSourceLUTID = request.form['contactInfoSourceLUTID']
                physicianPhone.physicianID = request.form['physicianID']
                physicianPhone.contactInfoStatusID = request.form['contactInfoStatusID']
                physicianPhone.phone = request.form['phone']
                physicianPhone.phone_type = request.form['phone_type']
                physicianPhone.phone_source = request.form['phone_source']
                physicianPhone.phone_status = request.form['phone_status']
                physicianPhone.phone_status_date = datetime.strptime(request.form['phone_status_date'],"%Y-%m-%d")
                query.commit()
                return physicianPhone.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysicianPhoneID {} not found".format(physicianPhoneID))
    except Exception as e:
        return internal_error(e)

@api.route('/physicianphones/', methods=['POST'])
def create_physician_phone():
    try:
        form = forms.PhysicianPhoneForm(request.form)
        if form.validate():
            physicianPhone = models.PhysicianPhone(
                contactInfoSourceLUTID = request.form['contactInfoSourceLUTID'],
                physicianID = request.form['physicianID'],
                contactInfoStatusID = request.form['contactInfoStatusID'],
                phone = request.form['phone'],
                phone_type = request.form['phone_type'],
                phone_source = request.form['phone_source'],
                phone_status = request.form['phone_status'],
                phone_status_date = datetime.strptime(request.form['phone_status_date'],"%Y-%m-%d")
                )
            query.add(physicianPhone)
            return jsonify({'physicianPhoneID':physicianPhone.physicianPhoneID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/physicianphones/<int:physicianPhoneID>/',methods = ['DELETE'])
def delete_physician_phone(physicianPhoneID):
    try:
        physicianPhone = query.get_physician_phone(physicianPhoneID)
        if physicianPhone is not None:
            deps = get_dependencies(physicianPhone)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(physicianPhone)
                return item_deleted("PhysicianPhoneID {} deleted".format(physicianPhoneID))
        else:
            return item_not_found("PhysicianPhoneID {} not found".format(physicianPhoneID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# PhysicianToCTC
##############################################################################
@api.route('/physiciantoctcs/', methods = ['GET'])
@api.route('/physiciantoctcs/<int:physicianCTCID>/', methods = ['GET'])
def get_physician_to_ctc(physicianCTCID=None):
    try:
        if physicianCTCID is None:
            return jsonify(PhysicianToCTCs = [i.dict() for i in query.get_physician_to_ctcs()])
        else:
            physicianToCTC = query.get_physician_to_ctc(physicianCTCID)
            if physicianToCTC is not None:
                return physicianToCTC.json()
            else:
                return item_not_found("PhysicianCTCID {} not found".format(physicianCTCID))
    except Exception as e:
        return internal_error(e)

@api.route('/physiciantoctcs/<int:physicianCTCID>/', methods = ['PUT'])
def update_physician_to_ctc(physicianCTCID):
    try:
        physicianToCTC = query.get_physician_to_ctc(physicianCTCID)
        if physicianToCTC is not None:
            form = forms.PhysicianToCTCForm(request.form)
            if form.validate():
                physicianToCTC.physicianID = request.form['physicianID']
                physicianToCTC.ctcID = request.form['ctcID']
                query.commit()
                return physicianToCTC.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysicianCTCID {} not found".format(physicianCTCID))
    except Exception as e:
        return internal_error(e)

@api.route('/physiciantoctcs/', methods=['POST'])
def create_physician_to_ctc():
    try:
        form = forms.PhysicianToCTCForm(request.form)
        if form.validate():
            physicianToCTC = models.PhysicianToCTC(
               physicianID = request.form['physicianID'],
               ctcID = request.form['ctcID']
            )
            query.add(physicianToCTC)
            return jsonify({'physicianCTCID':physicianToCTC.physicianCTCID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/physiciantoctcs/<int:physicianCTCID>/', methods = ['DELETE'])
def delete_physician_to_ctc(physicianCTCID):
    try:
        physicianToCTC = query.get_physician_to_ctc(physicianCTCID)
        if physicianToCTC is not None:
            deps = get_dependencies(physicianToCTC)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(physicianToCTC)
                return item_deleted("PhysicianCTCID {} deleted".format(physicianCTCID))
        else:
            return item_not_found("PhysicianCTCID {} not found".format(physicianCTCID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# PreApplication
##############################################################################
@api.route('/preapplications/', methods = ['GET'])
@api.route('/preapplications/<int:preApplicationID>/', methods = ['GET'])
def get_pre_application(preApplicationID=None):
    try:
        if preApplicationID is None:
            return jsonify(PreApplications = [i.dict() for i in query.get_pre_applications()])
        else:
            preApplication = query.get_pre_application(preApplicationID)
            if preApplication is not None:
                return preApplication.json()
            else:
                return item_not_found("PreApplicationID {} not found".format(preApplicationID))
    except Exception as e:
        return internal_error(e)

@api.route('/preapplications/<int:preApplicationID>/', methods = ['PUT'])
def update_pre_application(preApplicationID):
    try:
        preApplication = query.get_pre_application(preApplicationID)
        if preApplication is not None:
            form = forms.PreApplicationForm(request.form)
            if form.validate():
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
                return preApplication.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PreApplicationID {} not found".format(preApplicationID))
    except Exception as e:
        return internal_error(e)

@api.route('/preapplications/', methods=['POST'])
def create_pre_application():
    print("here")
    try:
        form = forms.PreApplicationForm(request.form)
        if form.validate():
            print("validated")
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
            query.add(preApplication)
            return jsonify({'preApplicationID':preApplication.preApplicationID})
        else:
            print("error")
            print(form.errors)
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/preapplications/<int:preApplicationID>/', methods = ['DELETE'])
def delete_pre_application(preApplicationID):
    try:
        preApplication = query.get_pre_application(preApplicationID)
        if preApplication is not None:
            deps = get_dependencies(preApplication)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if projectID is None:
            return jsonify(projects = [i.dict() for i in query.get_projects()])
        else:
            proj = query.get_project(projectID)
            if proj is not None:
                return proj.json()
            else:
                return item_not_found("ProjectID {} not found".format(projectID))
    except Exception as e:
        return internal_error(e)

@api.route('/projects/<int:projectID>/',methods = ['PUT'])
def update_project(projectID):
    try:
        proj = query.get_project(projectID)
        if proj is not None:
            form = forms.ProjectForm(request.form)
            if form.validate():
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
                return proj.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ProjectID {} not found".format(projectID))
    except Exception as e:
        return internal_error(e)

@api.route('/projects/', methods=['POST'])
def create_project():
    try:
        form = forms.ProjectForm(request.form)
        if form.validate():
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
            query.add(proj)
            return jsonify({'projectID':proj.projectID})
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/projects/<int:projectID>/',methods = ['DELETE'])
def delete_project(projectID):
    try:
        proj = query.get_project(projectID)
        if proj is not None:
            deps = get_dependencies(proj)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if participantID is None:
            return jsonify(ProjectPatients = [i.dict() for i in query.get_project_patients()])
        else:
            projectPatient = query.get_project_patient(participantID)
            if projectPatient is not None:
                return projectPatient.json()
            else:
                return item_not_found("ParticipantID {} not found".format(participantID))
    except Exception as e:
        return internal_error(e)

@api.route('/projectpatients/<int:participantID>/', methods = ['PUT'])
def update_project_patient(participantID):
    try:
        projectPatient = query.get_project_patient(participantID)
        if projectPatient is not None:
            form = forms.ProjectPatientForm(request.form)
            if form.validate():
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
                return projectPatient.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ParticipantID {} not found".format(participantID))
    except Exception as e:
        return internal_error(e)

@api.route('/projectpatients/', methods=['POST'])
def create_project_patient():
    try:
        form = forms.ProjectPatientForm(request.form)
        if form.validate():
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
            query.add(projectPatient)
            return jsonify({'participantID':projectPatient.participantID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/projectpatients/<int:participantID>/', methods = ['DELETE'])
def delete_project_patient(participantID):
    try:
        projectPatient = query.get_project_patient(participantID)
        if projectPatient is not None:
            deps = get_dependencies(projectPatient)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if projectStaffID is None:
            return jsonify(ProjectStaff = [i.dict() for i in query.get_project_staffs()])
        else:
            projectStaff = query.get_project_staff(projectStaffID)
            if projectStaff is not None:
                return projectStaff.json()
            else:
                return item_not_found("ProjectStaffID {} not found".format(projectStaffID))
    except Exception as e:
        internal_error(e)

@api.route('/projectstaff/<int:projectStaffID>/', methods = ['PUT'])
def update_project_staff(projectStaffID):
    try:
        projectStaff = query.get_project_staff(projectStaffID)
        if projectStaff is not None:
            form = forms.ProjectStaffForm(request.form)
            if form.validate():
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
                return projectStaff.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ProjectStaffID {} not found".format(projectStaffID))
    except Exception as e:
        return internal_error(e)

@api.route('/projectstaff/', methods=['POST'])
def create_project_staff():
    try:
        form = forms.ProjectStaffForm(request.form)
        if form.validate():
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
            query.add(projectStaff)
            return jsonify({'projectStaffID':projectStaff.projectStaffID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/projectstaff/<int:projectStaffID>/', methods = ['DELETE'])
def delete_project_staff(projectStaffID):
    try:
        projectStaff = query.get_project_staff(projectStaffID)
        if projectStaff is not None:
            deps = get_dependencies(projectStaff)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if projectStatusID is None:
            return jsonify(ProjectStatuses = [i.dict() for i in query.get_project_statuses()])
        else:
            projectStatus = query.get_project_status(projectStatusID)
            if projectStatus is not None:
                return projectStatus.json()
            else:
                return item_not_found("ProjectStatusID {} not found".format(projectStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/projectstatuses/<int:projectStatusID>/', methods = ['PUT'])
def update_project_status(projectStatusID):
    try:
        projectStatus = query.get_project_status(projectStatusID)
        if projectStatus is not None:
            form = forms.ProjectStatusForm(request.form)
            if form.validate():
                projectStatus.projectStatusLUTID = request.form['projectStatusLUTID']
                projectStatus.projectID = request.form['projectID']
                projectStatus.staffID = request.form['staffID']
                projectStatus.status_date = datetime.strptime(request.form['status_date'],"%Y-%m-%d")
                projectStatus.status_notes = request.form['status_notes']
                query.commit()
                return projectStatus.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ProjectStatusID {} not found".format(projectStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/projectstatuses/', methods=['POST'])
def create_project_status():
    try:
        form = forms.ProjectStatusForm(request.form)
        if form.validate():
            projectStatus = models.ProjectStatus(
                projectStatusLUTID = request.form['projectStatusLUTID'],
                projectID = request.form['projectID'],
                staffID = request.form['staffID'],
                status_date = datetime.strptime(request.form['status_date'],"%Y-%m-%d"),
                status_notes = request.form['status_notes']
            )
            query.add(projectStatus)
            return jsonify({'projectStatusID':projectStatus.projectStatusID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/projectstatuses/<int:projectStatusID>/', methods = ['DELETE'])
def delete_project_status(projectStatusID):
    try:
        projectStatus = query.get_project_status(projectStatusID)
        if projectStatus is not None:
            deps = get_dependencies(projectStatus)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if projectStatusTypeID is None:
            return jsonify(ProjectStatusTypes = [i.dict() for i in query.get_project_status_luts()])
        else:
            projectStatusType = query.get_project_status_lut(projectStatusTypeID)
            if projectStatusType is not None:
                return projectStatusType.json()
            else:
                return item_not_found("ProjectStatusTypeID {} not found".format(projectStatusTypeID))
    except Exception as e:
        return internal_error(e)

@api.route('/projectstatustypes/<int:projectStatusTypeID>/', methods = ['PUT'])
def update_project_status_lut(projectStatusTypeID):
    try:
        projectStatusType = query.get_project_status_lut(projectStatusTypeID)
        if projectStatusType is not None:
            form = forms.ProjectStatusLUTForm(request.form)
            if form.validate():
                projectStatusType.project_status = request.form['project_status']
                projectStatusType.status_definition = request.form['status_definition']
                query.commit()
                return projectStatusType.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ProjectStatusTypeID {} not found".format(projectStatusTypeID))
    except Exception as e:
        return internal_error(e)

@api.route('/projectstatustypes/', methods=['POST'])
def create_project_status_lut():
    try:
        form = forms.ProjectStatusLUTForm(request.form)
        if form.validate():
            projectStatusType = models.ProjectStatusLUT(
                project_status = request.form['project_status'],
                status_definition = request.form['status_definition']
            )
            query.add(projectStatusType)
            return jsonify({'projectStatusTypeID':projectStatusType.projectStatusTypeID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/projectstatustypes/<int:projectStatusTypeID>/', methods = ['DELETE'])
def delete_project_status_lut(projectStatusTypeID):
    try:
        projectStatusType = query.get_project_status_lut(projectStatusTypeID)
        if projectStatusType is not None:
            deps = get_dependencies(projectStatusType)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(projectStatusType)
                return item_deleted("ProjectStatusTypeID {} deleted".format(projectStatusTypeID))
        else:
            return item_not_found("ProjectStatusTypeID {} not found".format(projectStatusTypeID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# ProjectType
##############################################################################
@api.route('/projecttypes/', methods = ['GET'])
@api.route('/projecttypes/<int:projectTypeID>/', methods = ['GET'])
def get_project_type(projectTypeID=None):
    try:
        if projectTypeID is None:
            return jsonify(ProjectTypes = [i.dict() for i in query.get_project_types()])
        else:
            projectType = query.get_project_type(projectTypeID)
            if projectType is not None:
                return projectType.json()
            else:
                return item_not_found("ProjectTypeID {} not found".format(projectTypeID))
    except Exception as e:
        return internal_error(e)

@api.route('/projecttypes/<int:projectTypeID>/', methods = ['PUT'])
def update_project_type(projectTypeID):
    try:
        projectType = query.get_project_type(projectTypeID)
        if projectType is not None:
            form = forms.ProjectTypeForm(request.form)
            if form.validate():
                projectType.project_type = request.form['project_type']
                projectType.project_type_definition = request.form['project_type_definition']
                query.commit()
                return projectType.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ProjectTypeID {} not found".format(projectTypeID))
    except Exception as e:
        return internal_error(e)

@api.route('/projecttypes/', methods=['POST'])
def create_project_type():
    try:
        form = forms.ProjectTypeForm(request.form)
        if form.validate():
            projectType = models.ProjectType(
                project_type = request.form['project_type'],
                project_type_definition = request.form['project_type_definition']
            )
            query.add(projectType)
            return jsonify({'projectTypeID':projectType.projectTypeID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/projecttypes/<int:projectTypeID>/', methods = ['DELETE'])
def delete_project_type(projectTypeID):
    try:
        projectType = query.get_project_type(projectTypeID)
        if projectType is not None:
            deps = get_dependencies(projectType)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if rcStatusID is None:
            return jsonify(RCStatusList = [i.dict() for i in query.get_rc_statuses()])
        else:
            rcStatus = query.get_rc_status(rcStatusID)
            if rcStatus is not None:
                return rcStatus.json()
            else:
                return item_not_found("RCStatusID {} not found".format(rcStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/rcstatuslist/<int:rcStatusID>/', methods = ['PUT'])
def update_rc_status_list(rcStatusID):
    try:
        rcStatus = query.get_rc_status(rcStatusID)
        if rcStatus is not None:
            form = forms.RCStatusListForm(request.form)
            if form.validate():
                rcStatus.rc_status = request.form['rc_status']
                rcStatus.rc_status_definition = request.form['rc_status_definition']
                query.commit()
                return rcStatus.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("RCStatusListID {} not found".format(rcStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/rcstatuslist/', methods=['POST'])
def create_rc_status_list():
    try:
        form = forms.RCStatusListForm(request.form)
        if form.validate():
            rcStatus = models.RCStatusList(
                rc_status = request.form['rc_status'],
                rc_status_definition = request.form['rc_status_definition']
            )
            query.add(rcStatus)
            return jsonify({'rcStatusListID':rcStatus.rcStatusID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/rcstatuslist/<int:rcStatusID>/', methods = ['DELETE'])
def delete_rc_status_list(rcStatusID):
    try:
        rcStatusList = query.get_rc_status(rcStatusID)
        if rcStatusList is not None:
            deps = get_dependencies(rcStatusList)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if reviewCommitteeID is None:
            return jsonify(reviewCommittees = [i.dict() for i in query.get_review_committees()])
        else:
            reviewCommittee = query.get_review_committee(reviewCommitteeID)
            if reviewCommittee is not None:
                return reviewCommittee.json()
            else:
                return item_not_found("ReviewCommitteeID {} not found".format(reviewCommitteeID))
    except Exception as e:
        return internal_error(e)

@api.route('/reviewcommittees/<int:reviewCommitteeID>/', methods = ['PUT'])
def update_review_committee(reviewCommitteeID):
    try:
        rc = query.get_review_committee(reviewCommitteeID)
        if rc is not None:
            form = forms.ReviewCommitteeForm(request.form)
            if form.validate():
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
                return rc.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ReviewCommitteeID {} not found".format(reviewCommitteeID))
    except Exception as e:
        return internal_error(e)

@api.route('/reviewcommittees/', methods = ['POST'])
def create_review_committee():
    try:
        form = forms.ReviewCommitteeForm(request.form)
        if form.validate():
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
            query.add(rc)
            return jsonify({'reviewCommitteeID':rc.reviewCommitteeID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/reviewcommittees/<int:reviewCommitteeID>/', methods = ['DELETE'])
def delete_review_committee(reviewCommitteeID):
    try:
        rc = query.get_review_committee(reviewCommitteeID)
        if rc is not None:
            deps = get_dependencies(rc)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if rcListID is None:
            return jsonify(reviewCommitteeList = [i.dict() for i in query.get_review_committee_lists()])
        else:
            review_committee_list = query.get_review_committee_list(rcListID)
            if review_committee_list is not None:
                return review_committee_list.json()
            else:
                return item_not_found("RCListID {} not found".format(rcListID))
    except Exception as e:
        return internal_error(e)

@api.route('/reviewcommitteelist/<int:rcListID>/',methods = ['PUT'])
def update_review_committee_list(rcListID):
    try:
        rcList = query.get_review_committee_list(rcListID)
        if rcList is not None:
            form = forms.ReviewCommitteeListForm(request.form)
            if form.validate():
                rcList.review_committee = request.form['review_committee']
                rcList.rc_description = request.form['rc_description']
                query.commit()
                return rcList.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("RCListID {} not found".format(rcListID))
    except Exception as e:
        return internal_error(e)

@api.route('/reviewcommitteelist/',methods = ['POST'])
def create_review_committee_list():
    try:
        form = forms.ReviewCommitteeListForm(request.form)
        if form.validate():
            reviewCommitteeList = models.ReviewCommitteeList(
                review_committee = request.form['review_committee'],
                rc_description = request.form['rc_description']
                )
            query.add(reviewCommitteeList)
            return jsonify({'rcListID':reviewCommitteeList.rcListID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/reviewcommitteelist/<int:rcListID>/', methods = ['DELETE'])
def delete_review_committee_list(rcListID):
    try:
        reviewCommittee = query.get_rc_status(rcListID)
        if reviewCommittee is not None:
            deps = get_dependencies(reviewCommittee)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(reviewCommittee)
                return item_deleted("RCListID {} deleted".format(rcListID))
        else:
            return item_not_found("RCListID {} not found".format(rcListID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Staff
##############################################################################
@api.route('/staff/', methods = ['GET'])
@api.route('/staff/<int:staffID>/', methods = ['GET'])
def get_staff(staffID=None):
    try:
        if staffID is None:
            return jsonify(Staff = [i.dict() for i in query.get_staffs()])
        else:
            staff = query.get_staff(staffID)
            if staff is not None:
                return staff.json()
            else:
                return item_not_found("StaffID {} not found".format(staffID))
    except Exception as e:
        internal_error(e)

@api.route('/staff/<int:staffID>/',methods = ['PUT'])
def update_staff(staffID):
    try:
        staff = query.get_staff(staffID)
        if staff is not None:
            form = forms.StaffForm(request.form)
            if form.validate():
                staff.fname = request.form['fname']
                staff.lname = request.form['lname']
                staff.middle_name = request.form['middle_name']
                staff.email = request.form['email']
                staff.phone = request.form['phone']
                staff.phoneComment = request.form['phoneComment']
                staff.institution = request.form['institution']
                staff.department = request.form['department']
                staff.position = request.form['position']
                staff.credentials = request.form['credentials']
                staff.street = request.form['street']
                staff.city = request.form['city']
                staff.state = request.form['state']
                staff.human_sub_training_exp = datetime.strptime(request.form['human_sub_training_exp'],"%Y-%m-%d")
                staff.UCR_role = request.form['UCR_role']
                query.commit()
                return staff.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("StaffID {} not found".format(staffID))
    except Exception as e:
        internal_error(e)

@api.route('/staff/',methods = ['POST'])
def create_staff():
    try:
        form = forms.StaffForm(request.form)
        if form.validate():
            staff = models.Staff(
                fname = request.form['fname'],
                lname = request.form['lname'],
                middle_name = request.form['middle_name'],
                email = request.form['email'],
                phone = request.form['phone'],
                phoneComment = request.form['phoneComment'],
                institution = request.form['institution'],
                department = request.form['department'],
                position = request.form['position'],
                credentials = request.form['credentials'],
                street = request.form['street'],
                city = request.form['city'],
                state = request.form['state'],
                human_sub_training_exp = datetime.strptime(request.form['human_sub_training_exp'],"%Y-%m-%d"),
                UCR_role = request.form['UCR_role']
            )
            query.add(staff)
            return jsonify({'staffID':staff.staffID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/staff/<int:staffID>/', methods = ['DELETE'])
def delete_staff(staffID):
    try:
        staff = query.get_staff(staffID)
        if staff is not None:
            deps = get_dependencies(staff)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(staff)
                return item_deleted("StaffID {} deleted".format(staffID))
        else:
            return item_not_found("StaffID {} not found".format(staffID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Staff Role
##############################################################################
@api.route('/staffroles/', methods = ['GET'])
@api.route('/staffroles/<int:staffRoleLUTID>/', methods = ['GET'])
def get_staff_role(staffRoleLUTID=None):
    try:
        if staffRoleLUTID is None:
            return jsonify(StaffRoles = [i.dict() for i in query.get_staff_roles()])
        else:
            staffRole = query.get_staff_role(staffRoleLUTID)
            if staffRole is not None:
                return staffRole.json()
            else:
                return item_not_found("StaffRoleLUTID {} not found".format(staffRoleLUTID))
    except Exception as e:
        return internal_error(e)

@api.route('/staffroles/<int:staffRoleLUTID>/',methods = ['PUT'])
def update_staff_role(staffRoleLUTID):
    try:
        staffRole = query.get_staff_role(staffRoleLUTID)
        if staffRole is not None:
            form = forms.StaffRoleLUTForm(request.form)
            if form.validate():
                staffRole.staffRole = request.form['staffRole']
                staffRole.staffRoleDescription = request.form['staffRoleDescription']
                query.commit()
                return staffRole.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("StaffRoleLUTID {} not found".format(staffRoleLUTID))
    except Exception as e:
        return internal_error(e)

@api.route('/staffroles/',methods = ['POST'])
def create_staff_role():
    try:
        form = forms.StaffRoleLUTForm(request.form)
        if form.validate():
            staffRole = models.StaffRoleLUT(
                staffRole = request.form['staffRole'],
                staffRoleDescription = request.form['staffRoleDescription'],
            )
            query.add(staffRole)
            return jsonify({'staffRoleLUTID':staffRole.staffRoleLUTID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/staffroles/<int:staffRoleLUTID>/', methods = ['DELETE'])
def delete_staff_role(staffRoleLUTID):
    try:
        staffRole = query.get_staff_role(staffRoleLUTID)
        if staffRole is not None:
            deps = get_dependencies(staffRole)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(staffRole)
                return item_deleted("StaffRoleLUTID {} deleted".format(staffRoleLUTID))
        else:
            return item_not_found("StaffRoleLUTID {} not found".format(staffRoleLUTID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Staff Training
##############################################################################
@api.route('/stafftrainings/', methods = ['GET'])
@api.route('/stafftrainings/<int:staffTrainingID>/', methods = ['GET'])
def get_staff_training(staffTrainingID=None):
    try:
        if staffTrainingID is None:
            return jsonify(StaffTrainings = [i.dict() for i in query.get_staff_trainings()])
        else:
            stafftraining = query.get_staff_training(staffTrainingID)
            if stafftraining is not None:
                return stafftraining.json()
            else:
                return item_not_found("StaffTrainingID {} not found".format(staffTrainingID))
    except Exception as e:
        return internal_error(e)

@api.route('/stafftrainings/<int:staffTrainingID>/',methods = ['PUT'])
def update_staff_training(staffTrainingID):
    try:
        stafftraining = query.get_staff_training(staffTrainingID)
        if stafftraining is not None:
            form = forms.StaffTrainingForm(request.form)
            if form.validate():
                stafftraining.staffID = request.form['staffID']
                stafftraining.humanSubjectTrainingLUTID = request.form['humanSubjectTrainingLUTID']
                stafftraining.date_taken = datetime.strptime(request.form['date_taken'],"%Y-%m-%d")
                stafftraining.exp_date = datetime.strptime(request.form['exp_date'],"%Y-%m-%d")
                query.commit()
                return stafftraining.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("StaffTrainingID {} not found".format(staffTrainingID))
    except Exception as e:
        return internal_error(e)

@api.route('/stafftrainings/',methods = ['POST'])
def create_staff_training():
    try:
        form = forms.StaffTrainingForm(request.form)
        if form.validate():
            stafftraining = models.StaffTraining(
                staffID = request.form['staffID'],
                humanSubjectTrainingLUTID = request.form['humanSubjectTrainingLUTID'],
                date_taken = datetime.strptime(request.form['date_taken'],"%Y-%m-%d"),
                exp_date = datetime.strptime(request.form['exp_date'],"%Y-%m-%d")
                )
            query.add(stafftraining)
            return jsonify({'staffTrainingID':stafftraining.staffTrainingID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/stafftrainings/<int:staffTrainingID>/', methods = ['DELETE'])
def delete_staff_training(staffTrainingID):
    try:
        stafftraining = query.get_staff_training(staffTrainingID)
        if stafftraining is not None:
            deps = get_dependencies(stafftraining)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(stafftraining)
                return item_deleted("StaffTrainingID {} deleted".format(staffTrainingID))
        else:
            return item_not_found("StaffTrainingID {} not found".format(staffTrainingID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Tracing
##############################################################################
@api.route('/tracings/', methods = ['GET'])
@api.route('/tracings/<int:tracingID>/', methods = ['GET'])
def get_tracing(tracingID=None):
    try:
        if tracingID is None:
            return jsonify(Tracings = [i.dict() for i in query.get_tracings()])
        else:
            tracing = query.get_tracing(tracingID)
            if tracing is not None:
                return tracing.json()
            else:
                return item_not_found("TracingID {} not found".format(tracingID))
    except Exception as e:
        return internal_error(e)

@api.route('/tracings/<int:tracingID>/',methods = ['PUT'])
def update_tracing(tracingID):
    try:
        tracing = query.get_tracing(tracingID)
        if tracing is not None:
            form = forms.TracingForm(request.form)
            if form.validate():
                tracing.tracingSourceLUTID = request.form['tracingSourceLUTID']
                tracing.projectPatientID = request.form['projectPatientID']
                tracing.date = datetime.strptime(request.form['date'],"%Y-%m-%d")
                tracing.staff = request.form['staff']
                tracing.notes = request.form['notes']
                query.commit()
                return tracing.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("TracingID {} not found".format(tracingID))
    except Exception as e:
        return internal_error(e)

@api.route('/tracings/',methods = ['POST'])
def create_tracing():
    try:
        form = forms.TracingForm(request.form)
        if form.validate():
            tracing = models.Tracing(
                tracingSourceLUTID = request.form['tracingSourceLUTID'],
                projectPatientID = request.form['projectPatientID'],
                date = datetime.strptime(request.form['date'],"%Y-%m-%d"),
                staff = request.form['staff'],
                notes = request.form['notes']
                )
            query.add(tracing)
            return jsonify({'tracingID':tracing.tracingID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/tracings/<int:tracingID>/', methods = ['DELETE'])
def delete_tracing(tracingID):
    try:
        tracing = query.get_tracing(tracingID)
        if tracing is not None:
            deps = get_dependencies(tracing)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if tracingSourceLUTID is None:
            return jsonify(TracingSources = [i.dict() for i in query.get_tracing_sources()])
        else:
            tracing = query.get_tracing_source(tracingSourceLUTID)
            if tracing is not None:
                return tracing.json()
            else:
                return item_not_found("TracingSourceLUTID {} not found".format(tracingSourceLUTID))
    except Exception as e:
        return internal_error(e)

@api.route('/tracingsources/<int:tracingSourceLUTID>/',methods = ['PUT'])
def update_tracing_source(tracingSourceLUTID):
    try:
        tracingSource = query.get_tracing_source(tracingSourceLUTID)
        if tracingSource is not None:
            form = forms.TracingSourceLUTForm(request.form)
            if form.validate():
                tracingSource.description = request.form['description']
                query.commit()
                return tracingSource.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("TracingSourceLUTID {} not found".format(tracingSourceLUTID))
    except Exception as e:
        return internal_error(e)

@api.route('/tracingsources/',methods = ['POST'])
def create_tracing_source():
    try:
        form = forms.TracingSourceLUTForm(request.form)
        if form.validate():
            tracingSource = models.TracingSourceLUT(
                description = request.form['description']
                )
            ret = query.add(tracingSource)
            return jsonify({'tracingSourceLUTID':tracingSource.tracingSourceLUTID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/tracingsources/<int:tracingSourceLUTID>/', methods = ['DELETE'])
def delete_tracing_source(tracingSourceLUTID):
    try:
        tracingSource = query.get_tracing_source(tracingSourceLUTID)
        if tracingSource is not None:
            deps = get_dependencies(tracingSource)
            if deps:
                return dependency_detected(deps)
            else:
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
    try:
        if ucrReportID is None:
            return jsonify(ucrReports = [i.dict() for i in query.get_ucr_reports()])
        else:
            ucr = query.get_ucr_report(ucrReportID)
            if ucr is not None:
                return ucr.json()
            else:
                return item_not_found("UcrReportID {} not found".format(ucrReportID))
    except Exception as e:
        internal_error(e)

@api.route('/ucrreports/<int:ucrReportID>/', methods = ['PUT'])
def update_ucr_report(ucrReportID):
    try:
        ucr = query.get_ucr_report(ucrReportID)
        if ucr is not None:
            form = forms.UCRReportForm(request.form)
            if form.validate():
                ucr.projectID = request.form['projectID']
                ucr.report_type = request.form['report_type']
                ucr.report_submitted = datetime.strptime(request.form['report_submitted'],"%Y-%m-%d")
                ucr.report_due = datetime.strptime(request.form['report_due'],"%Y-%m-%d")
                ucr.report_doc = request.form['report_doc']
                query.commit()
                return ucr.json()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("UcrReportID {} not found.".format(ucrReportID))
    except Exception as e:
        return internal_error(e)

@api.route('/ucrreports/', methods = ['POST'])
def create_ucr_report():
    try:
        form = forms.UCRReportForm(request.form)
        if form.validate():
            ucr = models.UCRReport(
                projectID = request.form['projectID'],
                report_type = request.form['report_type'],
                report_submitted = datetime.strptime(request.form['report_submitted'],"%Y-%m-%d"),
                report_due = datetime.strptime(request.form['report_due'],"%Y-%m-%d"),
                report_doc = request.form['report_doc']
            )
            query.add(ucr)
            query.commit()
            return jsonify({'ucrReportID': ucr.ucrReportID})
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/ucrreports/<int:ucrReportID>/',methods = ['DELETE'])
def delete_ucr_report(ucrReportID):
    try:
        ucr = query.get_ucr_report(ucrReportID)
        if ucr is not None:
            deps = get_dependencies(ucr)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(ucr)
                return item_deleted("UcrReportID {} deleted".format(ucrReportID))
    except Exception as e:
        return internal_error(e)