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

api = Blueprint('api',__name__,template_folder='api_templates')

##############################################################################
# Error Handlers
##############################################################################    
def item_not_found(e):
    return jsonify({"Error": str(e)}), 404

def missing_params(e):
    return jsonify({"Error": str(e)}), 400

def out_of_date_error():
    message = "Conflict detected. Object has been changed. Please refresh data and update."
    return jsonify({message}), 409

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


@api.route('/abstractstatuses/', methods=['GET'])
@api.route('/abstractstatuses/<int:abstractStatusID>/', methods=['GET'])
def get_abstract_status(abstractStatusID=None):
    try:
        if abstractStatusID is None:
            return jsonify(abstractStatuses=[i.dict() for i in query.get_abstract_statuses()])
        else:
            abstractStatus = query.get_abstract_status(abstractStatusID)
            if abstractStatus is not None:
                return abstractStatus.json()
            else:
                return item_not_found("AbstractStatusID {} not found".format(abstractStatusID))
    except Exception as e:
        return internal_error(e)


@api.route('/abstractstatuses/<int:abstractStatusID>/', methods=['PUT'])
def update_abstract_status(abstractStatusID):
    try:
        abstractStatus = query.get_abstract_status(abstractStatusID)
        if abstractStatus is not None:
            form = forms.AbstractStatusForm(request.form)
            if form.validate():
                if int(form.versionID.data) == abstractStatus.versionID:
                    abstractStatus.abstractStatus = form.abstractStatus.data
                    query.commit()
                    return abstractStatus.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("AbstractStatusID {} not found".format(abstractStatusID))
    except Exception as e:
        return internal_error(e)


@api.route('/abstractstatuses/', methods=['POST'])
def create_abstract_status():
    try:
        form = forms.AbstractStatusForm(request.form)
        if form.validate():
            abstractStatus = models.AbstractStatus(
                abstractStatus=form.abstractStatus.data,
            )
            query.add(abstractStatus)
            return abstractStatus.json()
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@api.route('/abstractstatuses/<int:abstractStatusID>/', methods=['DELETE'])
def delete_abstract_status(abstractStatusID):
    try:
        abstractStatus = query.get_abstract_status(abstractStatusID)
        if abstractStatus is not None:
            deps = get_dependencies(abstractStatus)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(abstractStatus)
                return item_deleted("AbstractStatusID {} deleted".format(abstractStatusID))
        else:
            return item_not_found("AbstractStatusID {} not found".format(abstractStatusID))
    except Exception as e:
        return internal_error(e)


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
                if int(request.form['versionID']) == arcReview.versionID:
                    arcReview.projectID = form.projectID.data
                    arcReview.reviewType = form.reviewType.data
                    arcReview.dateSentToReviewer = form.dateSentToReviewer.data
                    arcReview.reviewer1 = form.reviewer1.data
                    arcReview.reviewer1Rec = form.reviewer1Rec.data
                    arcReview.reviewer1SigDate = form.reviewer1SigDate.data
                    arcReview.reviewer1Comments = form.reviewer1Comments.data
                    arcReview.reviewer2 = form.reviewer2.data
                    arcReview.reviewer2Rec = form.reviewer2Rec.data
                    arcReview.reviewer2SigDate = form.reviewer2SigDate.data
                    arcReview.reviewer2Comments = form.reviewer2Comments.data
                    arcReview.research = form.research.data
                    arcReview.contact = form.contact.data
                    arcReview.contact = form.contact.data
                    arcReview.linkage = form.linkage.data
                    arcReview.engaged = form.engaged.data
                    arcReview.nonPublicData = form.nonPublicData.data
                    query.add(arcReview)
                    query.flush()
                    query.commit()
                    return arcReview.json()
                else:
                    return out_of_date_error()
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
                projectID=form.projectID.data,
                reviewType=form.reviewType.data,
                dateSentToReviewer=form.dateSentToReviewer.data,
                reviewer1=form.reviewer1.data,
                reviewer1Rec=form.reviewer1Rec.data,
                reviewer1SigDate=form.reviewer1SigDate.data,
                reviewer1Comments=form.reviewer1Comments.data,
                reviewer2=form.reviewer2.data,
                reviewer2Rec=form.reviewer2Rec.data,
                reviewer2SigDate=form.reviewer2SigDate.data,
                reviewer2Comments=form.reviewer2Comments.data,
                research=form.research.data,
                contact = form.contact.data,
                linkage = form.linkage.data,
                engaged =form.engaged.data,
                nonPublicData = form.nonPublicData.data
            )
            query.add(arcReview)
            return arcReview.json()
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
                if int(request.form['versionID']) == budget.versionID:
                    budget.projectID = form.projectID.data
                    budget.numPeriods = form.numPeriods.data
                    budget.periodStart = form.periodStart.data
                    budget.periodEnd = form.periodEnd.data
                    budget.periodTotal = form.periodTotal.data
                    budget.periodComment = form.periodComment.data
                    query.commit()
                    return budget.json()
                else:
                    return out_of_date_error()
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
                projectID=form.projectID.data,
                numPeriods=form.numPeriods.data,
                periodStart=form.periodStart.data,
                periodEnd=form.periodEnd.data,
                periodTotal=form.periodTotal.data,
                periodComment=form.periodComment.data
            )
            query.add(budget)
            return budget.json()
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
                if int(request.form['versionID']) == contact.versionID:
                    contact.contactTypeLUTID = form.contactTypeLUTID.data
                    contact.participantID = form.participantID.data
                    contact.staffID = form.staffID.data
                    contact.informantID = form.informantID.data
                    contact.informantPhoneID = form.informantPhoneID.data
                    contact.facilityID = form.facilityID.data
                    contact.facilityPhoneID = form.facilityPhoneID.data
                    contact.physicianID = form.physicianID.data
                    contact.physicianPhoneID = form.physicianPhoneID.data
                    contact.patientPhoneID = form.patientPhoneID.data
                    contact.contactDate = form.contactDate.data
                    contact.initials = form.initials.data
                    contact.notes = form.notes.data
                    query.commit()
                    return contact.json()
                else:
                    return out_of_date_error()
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
                contactTypeLUTID=form.contactTypeLUTID.data,
                participantID=form.participantID.data,
                staffID=form.staffID.data,
                informantID=form.informantID.data,
                informantPhoneID=form.informantPhoneID.data,
                facilityID=form.facilityID.data,
                facilityPhoneID=form.facilityPhoneID.data,
                physicianID=form.physicianID.data,
                physicianPhoneID=form.physicianPhoneID.data,
                patientPhoneID=form.patientPhoneID.data,
                contactDate=form.contactDate.data,
                initials=form.initials.data,
                notes=form.notes.data,
            )
            query.add(contact)
            return contact.json()
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
@api.route('/contacttypes/<int:contactTypeID>/', methods = ['GET'])
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
                if int(request.form['versionID']) == contactType.versionID:
                    contactType.contactDefinition = form.contactDefinition.data
                    contactType.contactCode = form.contactCode.data
                    query.commit()
                    return contactType.json()
                else:
                    return out_of_date_error()
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
            contactType2 = query.get_contact_type_by_code(form.contactCode.data)
            if contactType2:
                form.contactCode.errors.append("Contact code already exists in the database.")
                return missing_params(form.errors)
            contactType = models.ContactTypeLUT(
                contactDefinition=form.contactDefinition.data,
                contactCode=form.contactCode.data
            )
            query.add(contactType)
            return contactType.json()
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
                if int(request.form['versionID']) == contactInfoSource.versionID:
                    contactInfoSource.contactInfoSource = form.contactInfoSource.data
                    query.commit()
                    return contactInfoSource.json()
                else:
                    return out_of_date_error()
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
                contactInfoSource=form.contactInfoSource.data,
            )
            query.add(contactInfoSource)
            return contactInfoSource.json()
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
                if int(request.form['versionID']) == contactInfoStatus.versionID:
                    contactInfoStatus.contactInfoStatus = form.contactInfoStatus.data
                    query.commit()
                    return contactInfoStatus.json()
                else:
                    return out_of_date_error()
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
                contactInfoStatus=form.contactInfoStatus.data,
            )
            query.add(contactInfoStatus)
            return contactInfoStatus.json()
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
                if int(request.form['versionID']) == ctc.versionID:
                    ctc.participantID = form.participantID.data
                    ctc.dxDateDay = form.dxDateDay.data
                    ctc.dxDateMonth = form.dxDateMonth.data
                    ctc.dxDateYear = form.dxDateYear.data
                    ctc.site = form.site.data
                    ctc.histology = form.histology.data
                    ctc.behavior = form.behavior.data
                    ctc.ctcSequence = form.ctcSequence.data
                    ctc.stage = form.stage.data
                    ctc.dxAge = form.dxAge.data
                    ctc.dxStreet1 = form.dxStreet1.data
                    ctc.dxStreet2 = form.dxStreet2.data
                    ctc.dxCity = form.dxCity.data
                    ctc.dxStateID = form.dxStateID.data
                    ctc.dxZip = form.dxZip.data
                    ctc.dxCounty = form.dxCounty.data
                    ctc.dnc = form.dnc.data
                    ctc.dncReason = form.dncReason.data
                    ctc.recordID = form.recordID.data
                    query.commit()
                    return ctc.json()
                else:
                    return out_of_date_error()
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
                participantID=form.participantID.data,
                dxDateDay=form.dxDateDay.data,
                dxDateMonth=form.dxDateMonth.data,
                dxDateYear=form.dxDateYear.data,
                site=form.site.data,
                histology=form.histology.data,
                behavior=form.behavior.data,
                ctcSequence=form.ctcSequence.data,
                stage=form.stage.data,
                dxAge=form.dxAge.data,
                dxStreet1=form.dxStreet1.data,
                dxStreet2=form.dxStreet2.data,
                dxCity=form.dxCity.data,
                dxStateID=form.dxStateID.data,
                dxZip=form.dxZip.data,
                dxCounty=form.dxCounty.data,
                dnc=form.dnc.data,
                dncReason=form.dncReason.data,
                recordID=form.recordID.data
            )
            query.add(ctc)
            return ctc.json()
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
                if int(request.form['versionID']) == ctcFacility.versionID:
                    ctcFacility.ctcID = form.ctcID.data
                    ctcFacility.facilityID = form.facilityID.data
                    ctcFacility.coc = form.coc.data
                    query.commit()
                    return ctcFacility.json()
                else:
                    return out_of_date_error()
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
                ctcID=form.ctcID.data,
                facilityID=form.facilityID.data,
                coc=form.coc.data
            )
            query.add(ctcFacility)
            return ctcFacility.json()
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
                if int(request.form['versionID']) == funding.versionID:
                    funding.grantStatusID = form.grantStatusID.data
                    funding.projectID = form.projectID.data
                    funding.fundingSourceID = form.fundingSourceID.data
                    funding.primaryFundingSource = form.primaryFundingSource.data
                    funding.secondaryFundingSource = form.secondaryFundingSource.data
                    funding.fundingNumber = form.fundingNumber.data
                    funding.grantTitle = form.grantTitle.data
                    funding.dateStatus = form.dateStatus.data
                    funding.grantPi = form.grantPi.data
                    funding.primaryChartfield = form.primaryChartfield.data
                    funding.secondaryChartfield = form.secondaryChartfield.data
                    query.commit()
                    return funding.json()
                else:
                    return out_of_date_error()
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
                grantStatusID=form.grantStatusID.data,
                projectID=form.projectID.data,
                fundingSourceID=form.fundingSourceID.data,
                primaryFundingSource=form.primaryFundingSource.data,
                secondaryFundingSource=form.secondaryFundingSource.data,
                fundingNumber=form.fundingNumber.data,
                grantTitle=form.grantTitle.data,
                dateStatus=form.dateStatus.data,
                grantPi=form.grantPi.data,
                primaryChartfield=form.primaryChartfield.data,
                secondaryChartfield=form.secondaryChartfield.data
            )
            query.add(funding)
            return funding.json()
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
                if int(request.form['versionID']) == facilityPhone.versionID:
                    facilityPhone.contactInfoSourceID = form.contactInfoSourceID.data
                    facilityPhone.facilityID = form.facilityID.data
                    facilityPhone.contactInfoStatusID = form.contactInfoStatusID.data
                    facilityPhone.clinicName = form.clinicName.data
                    facilityPhone.phoneTypeID = form.phoneTypeID.data
                    facilityPhone.phoneNumber = form.phoneNumber.data
                    facilityPhone.phoneStatusDate = form.phoneStatusDate.data
                    query.commit()
                    return facilityPhone.json()
                else:
                    return out_of_date_error()
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
                contactInfoSourceID=form.contactInfoSourceID.data,
                facilityID=form.facilityID.data,
                contactInfoStatusID=form.contactInfoStatusID.data,
                clinicName=form.clinicName.data,
                phoneNumber=form.phoneNumber.data,
                phoneTypeID=form.phoneTypeID.data,
                phoneStatusDate=form.phoneStatusDate.data
                )
            query.add(facilityPhone)
            return facilityPhone.json()
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
                if int(request.form['versionID']) == facility.versionID:
                    facility.facilityName = form.facilityName.data
                    facility.contactFirstName = form.contactFirstName.data
                    facility.contactLastName = form.contactLastName.data
                    facility.facilityStatus = form.facilityStatus.data
                    facility.facilityStatusDate = form.facilityStatusDate.data
                    facility.contact2FirstName = form.contact2FirstName.data
                    facility.contact2LastName = form.contact2LastName.data
                    query.commit()
                    return facility.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("FacilityID {} not found".format(facilityID))
    except Exception as e:
        return internal_error(e)

@api.route('/facilities/', methods=['POST'])
def create_facility():
    try:
        form = forms.FacilityForm(request.form)
        if form.validate():
            facility = models.Facility(
                facilityName=form.facilityName.data,
                contactFirstName=form.contactFirstName.data,
                contactLastName=form.contactLastName.data,
                facilityStatus=form.facilityStatus.data,
                facilityStatusDate=form.facilityStatusDate.data,
                contact2FirstName=form.contact2FirstName.data,
                contact2LastName=form.contact2LastName.data
                )
            ret = query.add(facility)
            return facility.json()
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

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
                if int(request.form['versionID']) == facilityAddress.versionID:
                    facilityAddress.contactInfoSourceID = form.contactInfoSourceID.data
                    facilityAddress.facilityID = form.facilityID.data
                    facilityAddress.contactInfoStatusID = form.contactInfoStatusID.data
                    facilityAddress.street = form.street.data
                    facilityAddress.street2 = form.street2.data
                    facilityAddress.city = form.city.data
                    facilityAddress.stateID = form.stateID.data
                    facilityAddress.zip = form.zip.data
                    facilityAddress.addressStatusDate = form.addressStatusDate.data
                    query.commit()
                else:
                    return out_of_date_error()
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
                contactInfoSourceID=form.contactInfoSourceID.data,
                facilityID=form.facilityID.data,
                contactInfoStatusID=form.contactInfoStatusID.data,
                street=form.street.data,
                street2=form.street2.data,
                city=form.city.data,
                stateID=form.stateID.data,
                zip=form.zip.data,
                addressStatusDate=form.addressStatusDate.data,
                )
            query.add(facilityAddress)
            return facilityAddress.json()
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

@api.route('/finalcodes/', methods=['GET'])
@api.route('/finalcodes/<int:finalCodeID>/', methods=['GET'])
def get_final_code(finalCodeID=None):
    try:
        if finalCodeID is None:
            return jsonify(FinalCodes=[i.dict() for i in query.get_final_codes()])
        else:
            finalCode = query.get_final_code(finalCodeID)
            if finalCode is not None:
                return finalCode.json()
            else:
                return item_not_found("FinalCodeID {} not found".format(finalCodeID))
    except Exception as e:
        return internal_error(e)

@api.route('/finalcodes/<int:finalCodeID>/', methods=['PUT'])
def update_final_code(finalCodeID):
    try:
        finalCode = query.get_final_code(finalCodeID)
        if finalCode is not None:
            form = forms.FinalCodeForm(request.form)
            if form.validate():
                if finalCode.finalCode != form.finalCode.data:
                    finalCode2 = query.get_final_code_by_code(form.finalCode.data)
                    if finalCode2:
                        form.finalCode.errors.append("Final Code already exists in database.")
                        return missing_params(form.errors)
                if int(form.versionID.data) == finalCode.versionID:
                    finalCode.finalCode = form.finalCode.data
                    finalCode.finalCodeDefinition = form.finalCodeDefinition.data
                    query.commit()
                    return finalCode.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("FinalCodeID {} not found".format(finalCodeID))
    except Exception as e:
        return internal_error(e)

@api.route('/finalcodes/', methods=['POST'])
def create_final_code():
    try:
        form = forms.FinalCodeForm(request.form)
        if form.validate():
            finalCode2 = query.get_final_code_by_code(form.finalCode.data)
            if finalCode2:
                form.finalCode.errors.append("Final code already exists in the database.")
                return missing_params(form.errors)
            finalCode = models.FinalCode(
                finalCode=form.finalCode.data,
                finalCodeDefinition=form.finalCodeDefinition.data
            )
            query.add(finalCode)
            return finalCode.json()
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/finalcodes/<int:finalCodeID>/', methods=['DELETE'])
def delete_final_code(finalCodeID):
    try:
        finalCode = query.get_final_code(finalCodeID)
        if finalCode is not None:
            deps = get_dependencies(finalCode)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(finalCode)
                return item_deleted("FinalCodeID {} deleted".format(finalCodeID))
        else:
            return item_not_found("finalCodeID {} not found".format(finalCodeID))
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
                if int(request.form['versionID']) == fundingSource.versionID:
                    fundingSource.fundingSource = form.fundingSource.data
                    query.commit()
                    return fundingSource.json()
                else:
                    return out_of_date_error()
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
                fundingSource=form.fundingSource.data
            )
            query.add(fundingSource)
            return fundingSource.json()
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
                if int(request.form['versionID']) == grantStatus.versionID:
                    grantStatus.grantStatus = form.grantStatus.data
                    query.commit()
                    return grantStatus.json()
                else:
                    return out_of_date_error()
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
                grantStatus=form.grantStatus.data
            )
            query.add(grantStatus)
            return grantStatus.json()
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
                if int(request.form['versionID']) == humanSubjectTraining.versionID:
                    humanSubjectTraining.trainingType = form.trainingType.data
                    query.commit()
                    return humanSubjectTraining.json()
                else:
                    return out_of_date_error()
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
                trainingType=form.trainingType.data
            )
            query.add(humanSubjectTraining)
            return humanSubjectTraining.json()
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
# Incentive
##############################################################################
@api.route('/incentives/', methods = ['GET'])
@api.route('/incentives/<int:incentiveID>/', methods = ['GET'])
def get_incentive(incentiveID=None):
    try:
        if incentiveID is None:
            return jsonify(Incentives = [i.dict() for i in query.get_incentives()])
        else:
            incentive = query.get_incentive(incentiveID)
            if incentive is not None:
                return incentive.json()
            else:
                return item_not_found("IncentiveID {} not found".format(incentiveID))
    except Exception as e:
        return internal_error(e)

@api.route('/incentives/<int:incentiveID>/', methods = ['PUT'])
def update_incentive(incentiveID):
    try:
        incentive = query.get_incentive(incentiveID)
        if incentive is not None:
            form = forms.IncentiveForm(request.form)
            if form.validate():
                if incentive.barcode != form.barcode.data:
                    incentive2 = query.get_incentive_by_barcode(form.barcode.data)
                    if incentive2:
                        form.barcode.errors.append("Barcode was already used for a different incentive.")
                        return missing_params(form.errors)
                if int(request.form['versionID']) == incentive.versionID:
                    incentive.participantID = form.participantID.data
                    incentive.incentiveDescription = form.incentiveDescription.data
                    incentive.barcode = form.barcode.data
                    incentive.dateGiven = form.dateGiven.data
                    query.commit()
                    return incentive.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("IncentiveID {} not found".format(incentiveID))
    except Exception as e:
        return internal_error(e)

@api.route('/incentives/', methods=['POST'])
def create_incentive():
    try:
        form = forms.IncentiveForm(request.form)
        if form.validate():
            # make sure the barcode isn't used for another incentive (DB won't allow it but we want a useful message)
            incentive2 = query.get_incentive_by_barcode(form.barcode.data)
            if incentive2:
                form.barcode.errors.append("Barcode was already used for a different incentive.")
                return missing_params(form.errors)
            incentive = models.Incentive(
                participantID=form.participantID.data,
                incentiveDescription=form.incentiveDescription.data,
                barcode=form.barcode.data,
                dateGiven=form.dateGiven.data
            )
            query.add(incentive)
            return incentive.json()
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/incentives/<int:incentiveID>/', methods = ['DELETE'])
def delete_incentive(incentiveID):
    try:
        incentive = query.get_incentive(incentiveID)
        if incentive is not None:
            deps = get_dependencies(incentive)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(incentive)
                return item_deleted("IncentiveID {} deleted".format(incentiveID))
        else:
            return item_not_found("IncentiveID {} not found".format(incentiveID))
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
                if int(request.form['versionID']) == informant.versionID:
                    informant.participantID = form.participantID.data
                    informant.firstName = form.firstName.data
                    informant.lastName = form.lastName.data
                    informant.middleName = form.middleName.data
                    informant.informantPrimary = form.informantPrimary.data
                    informant.informantRelationshipID = form.informantRelationshipID.data
                    informant.notes = form.notes.data
                    query.commit()
                    return informant.json()
                else:
                    return out_of_date_error()
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
                participantID=form.participantID.data,
                firstName=form.firstName.data,
                lastName=form.lastName.data,
                middleName=form.middleName.data,
                informantPrimary=form.informantPrimary.data,
                informantRelationshipID=form.informantRelationshipID.data,
                notes=form.notes.data
                )
            query.add(informant)
            return informant.json()
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
                if int(request.form['versionID']) == informantAddress.versionID:
                    informantAddress.contactInfoSourceID = form.contactInfoSourceID.data
                    informantAddress.informantID = form.informantID.data
                    informantAddress.contactInfoStatusID = form.contactInfoStatusID.data
                    informantAddress.street = form.street.data
                    informantAddress.street2 = form.street2.data
                    informantAddress.city = form.city.data
                    informantAddress.stateID = form.stateID.data
                    informantAddress.zip = form.zip.data
                    informantAddress.addressStatusDate = form.addressStatusDate.data
                    query.commit()
                    return informantAddress.json()
                else:
                    return out_of_date_error()
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
                contactInfoSourceID=form.contactInfoSourceID.data,
                informantID=form.informantID.data,
                contactInfoStatusID=form.contactInfoStatusID.data,
                street=form.street.data,
                street2=form.street2.data,
                city=form.city.data,
                stateID=form.stateID.data,
                zip=form.zip.data,
                addressStatusDate=form.addressStatusDate.data,
                )
            query.add(informantAddress)
            return informantAddress.json()
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
                if int(request.form['versionID']) == informantPhone.versionID:
                    informantPhone.contactInfoSourceID = form.contactInfoSourceID.data
                    informantPhone.informantID = form.informantID.data
                    informantPhone.contactInfoStatusID = form.contactInfoStatusID.data
                    informantPhone.phoneTypeID = form.phoneTypeID.data
                    informantPhone.phoneNumber = form.phoneNumber.data
                    informantPhone.phoneStatusDate = form.phoneStatusDate.data
                    query.commit()
                    return informantPhone.json()
                else:
                    return out_of_date_error()
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
                contactInfoSourceID=form.contactInfoSourceID.data,
                informantID=form.informantID.data,
                contactInfoStatusID=form.contactInfoStatusID.data,
                phoneTypeID=form.phoneTypeID.data,
                phoneNumber=form.phoneNumber.data,
                phoneStatusDate=form.phoneStatusDate.data
                )
            query.add(informantPhone)
            return informantPhone.json()
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
                if int(request.form['versionID']) == irb.versionID:
                    irb.holder = form.holder.data
                    irb.holderDefinition = form.holderDefinition.data
                    query.commit()
                    return irb.json()
                else:
                    return out_of_date_error()
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
                holder=form.holder.data,
                holderDefinition=form.holderDefinition.data
            )
            query.add(irb)
            return irb.json()
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
                if int(request.form['versionID']) == log.versionID:
                    log.logSubjectID = form.logSubjectID.data
                    log.projectID = form.projectID.data
                    log.staffID = form.staffID.data
                    log.phaseStatusID = form.phaseStatusID.data
                    log.note = form.note.data
                    log.date = form.date.data
                    query.commit()
                    return log.json()
                else:
                    return out_of_date_error()
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
                logSubjectID=form.logSubjectID.data,
                projectID=form.projectID.data,
                staffID=form.staffID.data,
                phaseStatusID=form.phaseStatusID.data,
                note=form.note.data,
                date=form.date.data
            )
            query.add(log)
            return log.json()
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
                if int(request.form['versionID']) == logSubject.versionID:
                    logSubject.logSubject = form.logSubject.data
                    query.commit()
                    return logSubject.json()
                else:
                    return out_of_date_error()
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
                logSubject=form.logSubject.data
            )
            query.add(logSubject)
            return logSubject.json()
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
                if int(request.form['versionID']) == patient.versionID:
                    patient.patID = form.patID.data
                    patient.ucrDistID = form.ucrDistID.data
                    patient.UPDBID = form.UPDBID.data
                    patient.firstName = form.firstName.data
                    patient.lastName = form.lastName.data
                    patient.middleName = form.middleName.data
                    patient.maidenName = form.maidenName.data
                    patient.aliasFirstName = form.aliasFirstName.data
                    patient.aliasLastName = form.aliasLastName.data
                    patient.aliasMiddleName = form.aliasMiddleName.data
                    patient.dobDay = form.dobDay.data
                    patient.dobMonth = form.dobMonth.data
                    patient.dobYear = form.dobYear.data
                    patient.SSN = form.SSN.data
                    patient.sexID = form.sexID.data
                    patient.raceID = form.raceID.data
                    patient.ethnicityID = form.ethnicityID.data
                    patient.vitalStatusID = form.vitalStatusID.data
                    query.commit()
                    return patient.json()
                else:
                    return out_of_date_error()
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
                patID=form.patID.data,
                ucrDistID=form.ucrDistID.data,
                UPDBID=form.UPDBID.data,
                firstName=form.firstName.data,
                lastName=form.lastName.data,
                middleName=form.middleName.data,
                maidenName=form.maidenName.data,
                aliasFirstName=form.aliasFirstName.data,
                aliasLastName=form.aliasLastName.data,
                aliasMiddleName=form.aliasMiddleName.data,
                dobDay=form.dobDay.data,
                dobMonth=form.dobMonth.data,
                dobYear=form.dobYear.data,
                SSN=form.SSN.data,
                raceID=form.raceID.data,
                sexID=form.sexID.data,
                ethnicityID=form.ethnicityID.data,
                vitalStatusID=form.vitalStatusID.data
                )
            query.add(patient)
            return patient.json()
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
                if int(request.form['versionID']) == patientAddress.versionID:
                    patientAddress.contactInfoSourceID = form.contactInfoSourceID.data
                    patientAddress.participantID = form.participantID.data
                    patientAddress.contactInfoStatusID = form.contactInfoStatusID.data
                    patientAddress.street = form.street.data
                    patientAddress.street2 = form.street2.data
                    patientAddress.city = form.city.data
                    patientAddress.stateID = form.stateID.data
                    patientAddress.zip = form.zip.data
                    patientAddress.addressStatusDate = form.addressStatusDate.data
                    query.commit()
                    return patientAddress.json()
                else:
                    return out_of_date_error()
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
                contactInfoSourceID=form.contactInfoSourceID.data,
                participantID=form.participantID.data,
                contactInfoStatusID=form.contactInfoStatusID.data,
                street=form.street.data,
                street2=form.street2.data,
                city=form.city.data,
                stateID=form.stateID.data,
                zip=form.zip.data,
                addressStatusDate=form.addressStatusDate.data,
                )
            query.add(patientaddress)
            return patientaddress.json()
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
                if int(request.form['versionID']) == patientEmail.versionID:
                    patientEmail.contactInfoSourceID = form.contactInfoSourceID.data
                    patientEmail.participantID = form.participantID.data
                    patientEmail.contactInfoStatusID = form.contactInfoStatusID.data
                    patientEmail.email = form.email.data
                    patientEmail.emailStatusDate = form.emailStatusDate.data
                    query.commit()
                    return patientEmail.json()
                else:
                    return out_of_date_error()
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
                contactInfoSourceID=form.contactInfoSourceID.data,
                participantID=form.participantID.data,
                contactInfoStatusID=form.contactInfoStatusID.data,
                email=form.email.data,
                emailStatusDate=form.emailStatusDate.data
                )
            query.add(patientEmail)
            return patientEmail.json()
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
                if int(request.form['versionID']) == patientPhone.versionID:
                    patientPhone.contactInfoSourceID = form.contactInfoSourceID.data
                    patientPhone.participantID = form.participantID.data
                    patientPhone.contactInfoStatusID = form.contactInfoStatusID.data
                    patientPhone.phoneTypeID = form.phoneTypeID.data
                    patientPhone.phoneNumber = form.phoneNumber.data
                    patientPhone.phoneStatusDate = form.phoneStatusDate.data
                    query.commit()
                    return patientPhone.json()
                else:
                    return out_of_date_error()
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
                contactInfoSourceID=form.contactInfoSourceID.data,
                participantID=form.participantID.data,
                contactInfoStatusID=form.contactInfoStatusID.data,
                phoneTypeID=form.phoneTypeID.data,
                phoneNumber=form.phoneNumber.data,
                phoneStatusDate=form.phoneStatusDate.data
                )
            query.add(patientPhone)
            return patientPhone.json()
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
                if int(request.form['versionID']) == patientProjectStatus.versionID:
                    patientProjectStatus.patientProjectStatusTypeID = form.patientProjectStatusTypeID.data
                    patientProjectStatus.participantID = form.participantID.data
                    patientProjectStatus.statusDate = form.statusDate.data
                    query.commit()
                    return patientProjectStatus.json()
                else:
                    return out_of_date_error()
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
                patientProjectStatusTypeID=form.patientProjectStatusTypeID.data,
                participantID=form.participantID.data,
                statusDate = form.statusDate.data
            )
            query.add(patientProjectStatus)
            return patientProjectStatus.json()
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
                if int(request.form['versionID']) == patientProjectStatusType.versionID:
                    patientProjectStatusType.statusDescription = form.statusDescription.data
                    query.commit()
                    return patientProjectStatusType.json()
                else:
                    return out_of_date_error()
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
                statusDescription=form.statusDescription.data
            )
            query.add(patientProjectStatusType)
            return patientProjectStatusType.json()
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
                if int(request.form['versionID']) == phaseStatus.versionID:
                    phaseStatus.phaseStatus = form.phaseStatus.data
                    phaseStatus.phaseDescription = form.phaseDescription.data
                    query.commit()
                    return phaseStatus.json()
                else:
                    return out_of_date_error()
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
                phaseStatus=form.phaseStatus.data,
                phaseDescription=form.phaseDescription.data
            )
            query.add(phaseStatus)
            return phaseStatus.json()
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

#############################################################################
# Phone Type
#############################################################################
@api.route('/phonetypes/', methods = ['GET'])
@api.route('/phonetypes/<int:phoneTypeID>/', methods=['GET'])
def get_phone_type(phoneTypeID = None):
    try:
        if phoneTypeID is None:
            return jsonify(PhoneTypes = [i.dict() for i in query.get_phone_types()])
        else:
            phoneType = query.get_phone_type(phoneTypeID)
            if phoneType is not None:
                return phoneType.json()
            else:
                return item_not_found("PhoneTypeID {} not found".format(phoneTypeID))
    except Exception as e:
        return internal_error(e)

@api.route('/phonetypes/<int:phoneTypeID>/',methods=['PUT'])
def update_phone_type(phoneTypeID):
    try:
        phoneType = query.get_phone_type(phoneTypeID)
        if phoneType is not None:
            form = forms.PhoneTypeForm(request.form)
            if form.validate():
                if int(request.form['versionID']) == phoneType.versionID:
                    phoneType.phoneType = form.phoneType.data
                    query.commit()
                    return phoneType.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhoneTypeID {} not found".format(phoneTypeID))
    except Exception as e:
        return internal_error(e)

@api.route('/phonetypes/', methods=['POST'])
def create_phone_type():
    try:
        form = forms.PhoneTypeForm(request.form)
        if form.validate():
            phoneType = models.PhoneTypeLUT(
                phoneType=form.phoneType.data
            )
            query.add(phoneType)
            return phoneType.json()
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/phonetypes/<int:phoneTypeID>/', methods=['DELETE'])
def delete_phone_type(phoneTypeID):
    try:
        phoneType = query.get_phone_type(phoneTypeID)
        if phoneType is not None:
            deps = get_dependencies(phoneType)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(phoneType)
                return item_deleted("PhoneTypeID {} deleted".format(phoneTypeID))
        else:
            return item_not_found("PhoneTypeID {} not found".format(phoneTypeID))
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
                if int(request.form['versionID']) == physician.versionID:
                    physician.firstName = form.firstName.data
                    physician.lastName = form.lastName.data
                    physician.middleName = form.middleName.data
                    physician.credentials = form.credentials.data
                    physician.specialty = form.specialty.data
                    physician.aliasFirstName = form.aliasFirstName.data
                    physician.aliasLastName = form.aliasLastName.data
                    physician.aliasMiddleName = form.aliasMiddleName.data
                    physician.physicianStatusID = form.physicianStatusID.data
                    physician.physicianStatusDate = form.physicianStatusDate.data
                    query.commit()
                    return physician.json()
                else:
                    return out_of_date_error()
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
                firstName=form.firstName.data,
                lastName=form.lastName.data,
                middleName=form.middleName.data,
                credentials=form.credentials.data,
                specialty=form.specialty.data,
                aliasFirstName=form.aliasFirstName.data,
                aliasLastName=form.aliasLastName.data,
                aliasMiddleName=form.aliasMiddleName.data,
                physicianStatusID=form.physicianStatusID.data,
                physicianStatusDate=form.physicianStatusDate.data,
            )
            query.add(physician)
            return physician.json()
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
                if int(request.form['versionID']) == physicianAddress.versionID:
                    physicianAddress.contactInfoSourceID = form.contactInfoSourceID.data
                    physicianAddress.physicianID = form.physicianID.data
                    physicianAddress.contactInfoStatusID = form.contactInfoStatusID.data
                    physicianAddress.street = form.street.data
                    physicianAddress.street2 = form.street2.data
                    physicianAddress.city = form.city.data
                    physicianAddress.stateID = form.stateID.data
                    physicianAddress.zip = form.zip.data
                    physicianAddress.addressStatusDate = form.addressStatusDate.data
                    query.commit()
                    return physicianAddress.json()
                else:
                    return out_of_date_error()
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
                contactInfoSourceID=form.contactInfoSourceID.data,
                physicianID=form.physicianID.data,
                contactInfoStatusID=form.contactInfoStatusID.data,
                street=form.street.data,
                street2=form.street2.data,
                city=form.city.data,
                stateID=form.stateID.data,
                zip=form.zip.data,
                addressStatusDate=form.addressStatusDate.data,
                )
            query.add(physicianAddress)
            return physicianAddress.json()
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
# Physician Email
##############################################################################
@api.route('/physicianemails/', methods=['GET'])
@api.route('/physicianemails/<int:physicianEmailID>/',methods = ['GET'])
def get_physician_email(physicianEmailID=None):
    try:
        if physicianEmailID is None:
            return jsonify(PhysicianEmails = [i.dict() for i in query.get_physician_emails()])
        else:
            physicianEmail = query.get_physician_email(physicianEmailID)
            if physicianEmail is not None:
                return physicianEmail.json()
            else:
                return item_not_found("PhysicianEmailID {} not found".format(physicianEmailID))
    except Exception as e:
        internal_error(e)

@api.route('/physicianemails/<int:physicianEmailID>/',methods = ['PUT'])
def update_physician_email(physicianEmailID):
    try:
        physicianEmail = query.get_physician_email(physicianEmailID)
        if physicianEmail is not None:
            form = forms.PhysicianEmailForm(request.form)
            if form.validate():
                if int(request.form['versionID']) == physicianEmail.versionID:
                    physicianEmail.contactInfoSourceID = form.contactInfoSourceID.data
                    physicianEmail.physicianID = form.physicianID.data
                    physicianEmail.contactInfoStatusID = form.contactInfoStatusID.data
                    physicianEmail.email = form.email.data
                    physicianEmail.emailStatusDate = form.emailStatusDate.data
                    query.commit()
                    return physicianEmail.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysicianEmailID {} not found".format(physicianEmailID))
    except Exception as e:
        return internal_error(e)

@api.route('/physicianemails/', methods=['POST'])
def create_physician_email():
    try:
        form = forms.PhysicianEmailForm(request.form)
        if form.validate():
            physicianEmail = models.PhysicianEmail(
                contactInfoSourceID=form.contactInfoSourceID.data,
                physicianID=form.physicianID.data,
                contactInfoStatusID=form.contactInfoStatusID.data,
                email=form.email.data,
                emailStatusDate=form.emailStatusDate.data
                )
            query.add(physicianEmail)
            return physicianEmail.json()
        else:
            return missing_params(form.errors)
    except Exception as e:
       return internal_error(e)

@api.route('/physicianemails/<int:physicianEmailID>/',methods = ['DELETE'])
def delete_physician_email(physicianEmailID):
    try:
        physicianEmail = query.get_patient_email(physicianEmailID)
        if physicianEmail is not None:
            deps = get_dependencies(physicianEmail)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(physicianEmail)
                return item_deleted("PhysicianEmailID {} deleted".format(physicianEmailID))
        else:
            return item_not_found("PhysicianEmailID {} not found".format(physicianEmailID))
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
                if int(request.form['versionID']) == physicianFacility.versionID:
                    physicianFacility.facilityID = form.facilityID.data
                    physicianFacility.physicianID = form.physicianID.data
                    physicianFacility.physFacilityStatusID = form.physFacilityStatusID.data
                    physicianFacility.physFacilityStatusDate = form.physFacilityStatusDate.data
                    query.commit()
                    return physicianFacility.json()
                else:
                    return out_of_date_error()
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
                facilityID=form.facilityID.data,
                physicianID=form.physicianID.data,
                physFacilityStatusID=form.physFacilityStatusID.data,
                physFacilityStatusDate=form.physFacilityStatusDate.data,
                )
            query.add(physicianFacility)
            return physicianFacility.json()
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
                if int(request.form['versionID']) == physicianPhone.versionID:
                    physicianPhone.contactInfoSourceID = form.contactInfoSourceID.data
                    physicianPhone.physicianID = form.physicianID.data
                    physicianPhone.contactInfoStatusID = form.contactInfoStatusID.data
                    physicianPhone.phoneNumber = form.phoneNumber.data
                    physicianPhone.phoneTypeID = form.phoneTypeID.data
                    physicianPhone.phoneStatusDate = form.phoneStatusDate.data
                    query.commit()
                    return physicianPhone.json()
                else:
                    return out_of_date_error()
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
                contactInfoSourceID=form.contactInfoSourceID.data,
                physicianID=form.physicianID.data,
                contactInfoStatusID=form.contactInfoStatusID.data,
                phoneNumber=form.phoneNumber.data,
                phoneTypeID=form.phoneTypeID.data,
                phoneStatusDate=form.phoneStatusDate.data
                )
            query.add(physicianPhone)
            return physicianPhone.json()
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

@api.route('/physicianstatuses/', methods=['GET'])
@api.route('/physicianstatuses/<int:physicianStatusID>/', methods=['GET'])
def get_physician_status(physicianStatusID=None):
    try:
        if physicianStatusID is None:
            return jsonify(PhysicianStatuses=[i.dict() for i in query.get_physician_statuses()])
        else:
            physicianStatus = query.get_physician_status(physicianStatusID)
            if physicianStatus is not None:
                return physicianStatus.json()
            else:
                return item_not_found("PhysicianStatusID {} not found".format(physicianStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/physicianstatuses/<int:physicianStatusID>/', methods=['PUT'])
def update_physician_status(physicianStatusID):
    try:
        physicianStatus = query.get_physician_status(physicianStatusID)
        if physicianStatus is not None:
            form = forms.PhysicianStatusForm(request.form)
            if form.validate():
                if int(form.versionID.data) == physicianStatus.versionID:
                    physicianStatus.physicianStatus = form.physicianStatus.data
                    query.commit()
                    return physicianStatus.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysicianStatusID {} not found".format(physicianStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/physicianstatuses/', methods=['POST'])
def create_physician_status():
    try:
        form = forms.PhysicianStatusForm(request.form)
        if form.validate():
            physicianStatus = models.PhysicianStatus(
                physicianStatus=form.physicianStatus.data,
            )
            query.add(physicianStatus)
            return physicianStatus.json()
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/physicianstatuses/<int:physicianStatusID>/', methods=['DELETE'])
def delete_physician_status(physicianStatusID):
    try:
        physicianStatus = query.get_physician_status(physicianStatusID)
        if physicianStatus is not None:
            deps = get_dependencies(physicianStatus)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(physicianStatus)
                return item_deleted("PhysicianStatusID {} deleted".format(physicianStatusID))
        else:
            return item_not_found("PhysicianStatusID {} not found".format(physicianStatusID))
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
                if int(request.form['versionID']) == physicianToCTC.versionID:
                    physicianToCTC.physicianID = form.physicianID.data
                    physicianToCTC.ctcID = form.ctcID.data
                    query.commit()
                    return physicianToCTC.json()
                else:
                    return out_of_date_error()
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
                physicianID=form.physicianID.data,
                ctcID=form.ctcID.data
            )
            query.add(physicianToCTC)
            return physicianToCTC.json()
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
                if int(request.form['versionID']) == preApplication.versionID:
                    preApplication.projectID = form.projectID.data
                    preApplication.piFirstName = form.piFirstName.data
                    preApplication.piLastName = form.piLastName.data
                    preApplication.piPhone = form.piPhone.data
                    preApplication.piEmail = form.piEmail.data
                    preApplication.contactFirstName = form.contactFirstName.data
                    preApplication.contactLastName = form.contactLastName.data
                    preApplication.contactPhone = form.contactPhone.data
                    preApplication.contactEmail = form.contactEmail.data
                    preApplication.institution = form.institution.data
                    preApplication.institution2 = form.institution2.data
                    preApplication.uid = form.uid.data
                    preApplication.udoh = form.udoh.data
                    preApplication.projectTitle = form.projectTitle.data
                    preApplication.purpose = form.purpose.data
                    preApplication.irb0 = form.irb0.data
                    preApplication.irb1 = form.irb1.data
                    preApplication.irb2 = form.irb2.data
                    preApplication.irb3 = form.irb3.data
                    preApplication.irb4 = form.irb4.data
                    preApplication.otherIrb = form.otherIrb.data
                    preApplication.updb = form.updb.data
                    preApplication.ptContact = form.ptContact.data
                    preApplication.startDate = form.startDate.data
                    preApplication.link = form.link.data
                    preApplication.deliveryDate = form.deliveryDate.data
                    preApplication.description = form.description.data
                    query.commit()
                    return preApplication.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PreApplicationID {} not found".format(preApplicationID))
    except Exception as e:
        return internal_error(e)

@api.route('/preapplications/', methods=['POST'])
def create_pre_application():
    try:
        form = forms.PreApplicationForm(request.form)
        if form.validate():
            preApplication = models.PreApplication(
                projectID=form.projectID.data,
                piFirstName=form.piFirstName.data,
                piLastName=form.piLastName.data,
                piPhone=form.piPhone.data,
                piEmail=form.piEmail.data,
                contactFirstName=form.contactFirstName.data,
                contactLastName=form.contactLastName.data,
                contactPhone=form.contactPhone.data,
                contactEmail=form.contactEmail.data,
                institution=form.institution.data,
                institution2=form.institution2.data,
                uid=form.uid.data,
                udoh=form.udoh.data,
                projectTitle=form.projectTitle.data,
                purpose=form.purpose.data,
                irb0 = form.irb0.data,
                irb1 = form.irb1.data,
                irb2 = form.irb2.data,
                irb3 = form.irb3.data,
                irb4 = form.irb4.data,
                otherIrb=form.otherIrb.data,
                updb = form.updb.data,
                ptContact = form.ptContact.data,
                startDate=form.startDate.data,
                link = form.link.data,
                deliveryDate=form.deliveryDate.data,
                description=form.description.data
            )
            query.add(preApplication)
            return preApplication.json()
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
                if int(request.form['versionID']) == proj.versionID:
                    proj.projectTypeID = form.projectTypeID.data
                    proj.irbHolderID = form.irbHolderID.data
                    proj.projectTitle = form.projectTitle.data
                    proj.shortTitle = form.shortTitle.data
                    proj.projectSummary = form.projectSummary.data
                    proj.sop = form.sop.data
                    proj.ucrProposal = form.ucrProposal.data
                    proj.budgetDoc = form.budgetDoc.data
                    proj.ucrFee = form.ucrFee.data
                    proj.ucrNoFee = form.ucrNoFee.data
                    proj.previousShortTitle = form.previousShortTitle.data
                    proj.dateAdded = form.dateAdded.data
                    proj.finalRecruitmentReport = form.finalRecruitmentReport.data
                    proj.ongoingContact = form.ongoingContact.data
                    proj.activityStartDate = form.activityStartDate.data
                    proj.activityEndDate = form.activityEndDate.data
                    query.commit()
                    return proj.json()
                else:
                    return out_of_date_error()
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
                projectTypeID=form.projectTypeID.data,
                irbHolderID=form.irbHolderID.data,
                projectTitle=form.projectTitle.data,
                shortTitle=form.shortTitle.data,
                projectSummary=form.projectSummary.data,
                sop=form.sop.data,
                ucrProposal=form.ucrProposal.data,
                budgetDoc=form.budgetDoc.data,
                ucrFee=form.ucrFee.data,
                ucrNoFee=form.ucrNoFee.data,
                previousShortTitle=form.previousShortTitle.data,
                dateAdded=form.dateAdded.data,
                finalRecruitmentReport=form.finalRecruitmentReport.data,
                ongoingContact = form.ongoingContact.data,
                activityStartDate=form.activityStartDate.data,
                activityEndDate=form.activityEndDate.data
                )
            query.add(proj)
            return proj.json()
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
                if int(request.form['versionID']) == projectPatient.versionID:
                    projectPatient.projectID = form.projectID.data
                    projectPatient.staffID = form.staffID.data
                    projectPatient.ctcID = form.ctcID.data
                    projectPatient.currentAge = form.currentAge.data
                    projectPatient.batch = form.batch.data
                    projectPatient.siteGrp = form.siteGrp.data
                    projectPatient.finalCodeID = form.finalCodeID.data
                    projectPatient.finalCodeDate = form.finalCodeDate.data
                    projectPatient.enrollmentDate = form.enrollmentDate.data
                    projectPatient.dateCoordSigned = form.dateCoordSigned.data
                    projectPatient.importDate = form.importDate.data
                    projectPatient.finalCodeStaffID = form.finalCodeStaffID.data
                    projectPatient.enrollmentStaffID = form.enrollmentStaffID.data
                    projectPatient.dateCoordSignedStaffID = form.dateCoordSignedStaffID.data
                    projectPatient.abstractStatusID = form.abstractStatusID.data
                    projectPatient.abstractStatusDate = form.abstractStatusDate.data
                    projectPatient.abstractStatusStaffID = form.abstractStatusStaffID.data
                    projectPatient.sentToAbstractorDate = form.sentToAbstractorDate.data
                    projectPatient.sentToAbstractorStaffID = form.sentToAbstractorStaffID.data
                    projectPatient.abstractedDate = form.abstractedDate.data
                    projectPatient.abstractorStaffID = form.abstractorStaffID.data
                    projectPatient.researcherDate = form.researcherDate.data
                    projectPatient.researcherStaffID = form.researcherStaffID.data
                    projectPatient.consentLink = form.consentLink.data
                    projectPatient.medRecordReleaseSigned = form.medRecordReleaseSigned.data
                    projectPatient.medRecordReleaseLink = form.medRecordReleaseLink.data
                    projectPatient.medRecordReleaseStaffID = form.medRecordReleaseStaffID.data
                    projectPatient.medRecordReleaseDate = form.medRecordReleaseDate.data
                    projectPatient.surveyToResearcher = form.surveyToResearcher.data
                    projectPatient.surveyToResearcherStaffID = form.surveyToResearcherStaffID.data
                    projectPatient.qualityControl = form.qualityControl.data
                    query.commit()
                    return projectPatient.json()
                else:
                    return out_of_date_error()
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
                projectID=form.projectID.data,
                staffID=form.staffID.data,
                ctcID=form.ctcID.data,
                currentAge=form.currentAge.data,
                batch=form.batch.data,
                siteGrp=form.siteGrp.data,
                finalCodeID=form.finalCodeID.data,
                finalCodeDate=form.finalCodeDate.data,
                enrollmentDate=form.enrollmentDate.data,
                dateCoordSigned=form.dateCoordSigned.data,
                importDate=form.importDate.data,
                finalCodeStaffID=form.finalCodeStaffID.data,
                enrollmentStaffID=form.enrollmentStaffID.data,
                dateCoordSignedStaffID=form.dateCoordSignedStaffID.data,
                abstractStatusID=form.abstractStatusID.data,
                abstractStatusDate=form.abstractStatusDate.data,
                abstractStatusStaffID=form.abstractStatusStaffID.data,
                sentToAbstractorDate=form.sentToAbstractorDate.data,
                sentToAbstractorStaffID=form.sentToAbstractorStaffID.data,
                abstractedDate=form.abstractedDate.data,
                abstractorStaffID=form.abstractorStaffID.data,
                researcherDate=form.researcherDate.data,
                researcherStaffID=form.researcherStaffID.data,
                consentLink=form.consentLink.data,
                medRecordReleaseSigned = form.medRecordReleaseSigned.data,
                medRecordReleaseLink=form.medRecordReleaseLink.data,
                medRecordReleaseStaffID=form.medRecordReleaseStaffID.data,
                medRecordReleaseDate=form.medRecordReleaseDate.data,
                surveyToResearcher=form.surveyToResearcher.data,
                surveyToResearcherStaffID=form.surveyToResearcherStaffID.data,
                qualityControl=form.qualityControl.data
            )
            query.add(projectPatient)
            return projectPatient.json()
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
                if int(request.form['versionID']) == projectStaff.versionID:
                    projectStaff.staffRoleID = form.staffRoleID.data
                    projectStaff.projectID = form.projectID.data
                    projectStaff.staffID = form.staffID.data
                    projectStaff.datePledge = form.datePledge.data
                    projectStaff.dateRevoked = form.dateRevoked.data
                    projectStaff.contactID = form.contactID.data
                    projectStaff.inactiveID = form.inactiveID.data
                    query.commit()
                    return projectStaff.json()
                else:
                    return out_of_date_error()
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
                staffRoleID=form.staffRoleID.data,
                projectID=form.projectID.data,
                staffID=form.staffID.data,
                datePledge=form.datePledge.data,
                dateRevoked=form.dateRevoked.data,
                contactID=form.contactID.data,
                inactiveID=form.inactiveID.data,
            )
            query.add(projectStaff)
            return projectStaff.json()
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
                if int(request.form['versionID']) == projectStatus.versionID:
                    projectStatus.projectStatusTypeID = form.projectStatusTypeID.data
                    projectStatus.projectID = form.projectID.data
                    projectStatus.staffID = form.staffID.data
                    projectStatus.statusDate = form.statusDate.data
                    projectStatus.statusNotes = form.statusNotes.data
                    query.commit()
                    return projectStatus.json()
                else:
                    return out_of_date_error()
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
                projectStatusTypeID=form.projectStatusTypeID.data,
                projectID=form.projectID.data,
                staffID=form.staffID.data,
                statusDate=form.statusDate.data,
                statusNotes=form.statusNotes.data
            )
            query.add(projectStatus)
            return projectStatus.json()
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
                if int(request.form['versionID']) == projectStatusType.versionID:
                    projectStatusType.projectStatus = form.projectStatus.data
                    projectStatusType.projectStatusDefinition = form.projectStatusDefinition.data
                    query.commit()
                    return projectStatusType.json()
                else:
                    return out_of_date_error()
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
                projectStatus=form.projectStatus.data,
                projectStatusDefinition=form.projectStatusDefinition.data
            )
            query.add(projectStatusType)
            return projectStatusType.json()
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
                if int(request.form['versionID']) == projectType.versionID:
                    projectType.projectType = form.projectType.data
                    projectType.projectTypeDefinition = form.projectTypeDefinition.data
                    query.commit()
                    return projectType.json()
                else:
                    return out_of_date_error()
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
                projectType=form.projectType.data,
                projectTypeDefinition=form.projectTypeDefinition.data
            )
            query.add(projectType)
            return projectType.json()
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
@api.route('/reviewcommitteestatuses/', methods = ['GET'])
@api.route('/reviewcommitteestatuses/<int:reviewCommitteeStatusID>/', methods = ['GET'])
def get_rc_status_list(reviewCommitteeStatusID=None):
    try:
        if reviewCommitteeStatusID is None:
            return jsonify(ReviewCommitteeStatuses = [i.dict() for i in query.get_review_committee_statuses()])
        else:
            rcStatus = query.get_review_committee_status(reviewCommitteeStatusID)
            if rcStatus is not None:
                return rcStatus.json()
            else:
                return item_not_found("ReviewCommitteeStatusID {} not found".format(reviewCommitteeStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/reviewcommitteestatuses/<int:reviewCommitteeStatusID>/', methods = ['PUT'])
def update_rc_status_list(reviewCommitteeStatusID):
    try:
        rcStatus = query.get_review_committee_status(reviewCommitteeStatusID)
        if rcStatus is not None:
            form = forms.ReviewCommitteeStatusLUTForm(request.form)
            if form.validate():
                if int(request.form['versionID']) == rcStatus.versionID:
                    rcStatus.reviewCommitteeStatus = form.reviewCommitteeStatus.data
                    rcStatus.reviewCommitteeStatusDefinition = form.reviewCommitteeStatusDefinition.data
                    query.commit()
                    return rcStatus.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ReviewCommitteeStatusID {} not found".format(reviewCommitteeStatusID))
    except Exception as e:
        return internal_error(e)

@api.route('/reviewcommitteestatuses/', methods=['POST'])
def create_rc_status_list():
    try:
        form = forms.ReviewCommitteeStatusLUTForm(request.form)
        if form.validate():
            rcStatus = models.ReviewCommitteeStatusLUT(
                reviewCommitteeStatus=form.reviewCommitteeStatus.data,
                reviewCommitteeStatusDefinition=form.reviewCommitteeStatusDefinition.data
            )
            query.add(rcStatus)
            return rcStatus.json()
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/reviewcommitteestatuses/<int:reviewCommitteeStatusID>/', methods = ['DELETE'])
def delete_rc_status_list(reviewCommitteeStatusID):
    try:
        rcStatusList = query.get_review_committee_status(reviewCommitteeStatusID)
        if rcStatusList is not None:
            deps = get_dependencies(rcStatusList)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(rcStatusList)
                return item_deleted("ReviewCommitteeStatusID {} deleted".format(reviewCommitteeStatusID))
        else:
            return item_not_found("ReviewCommitteeStatusID {} not found".format(reviewCommitteeStatusID))
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
                if int(request.form['versionID']) == rc.versionID:
                    rc.projectID = form.projectID.data
                    rc.reviewCommitteeStatusID = form.reviewCommitteeStatusID.data
                    rc.reviewCommitteeLUTID = form.reviewCommitteeLUTID.data
                    rc.reviewCommitteeNumber = form.reviewCommitteeNumber.data
                    rc.dateInitialReview = form.dateInitialReview.data
                    rc.dateExpires = form.dateExpires.data
                    rc.rcNote = form.rcNote.data
                    rc.rcProtocol = form.rcProtocol.data
                    rc.rcApproval = form.rcApproval.data
                    query.commit()
                    return rc.json()
                else:
                    return out_of_date_error()
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
                projectID=form.projectID.data,
                reviewCommitteeStatusID=form.reviewCommitteeStatusID.data,
                reviewCommitteeLUTID=form.reviewCommitteeLUTID.data,
                reviewCommitteeNumber=form.reviewCommitteeNumber.data,
                dateInitialReview=form.dateInitialReview.data,
                dateExpires=form.dateExpires.data,
                rcNote=form.rcNote.data,
                rcProtocol=form.rcProtocol.data,
                rcApproval=form.rcApproval.data
            )
            query.add(rc)
            return rc.json()
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
@api.route('/reviewcommitteelist/<int:reviewCommitteeID>/', methods = ['GET'])
def get_review_committee_list(reviewCommitteeID=None):
    try:
        if reviewCommitteeID is None:
            return jsonify(ReviewCommitteeList = [i.dict() for i in query.get_review_committee_luts()])
        else:
            review_committee_list = query.get_review_committee_lut(reviewCommitteeID)
            if review_committee_list is not None:
                return review_committee_list.json()
            else:
                return item_not_found("ReviewCommitteeID {} not found".format(reviewCommitteeID))
    except Exception as e:
        return internal_error(e)

@api.route('/reviewcommitteelist/<int:reviewCommitteeID>/',methods = ['PUT'])
def update_review_committee_list(reviewCommitteeID):
    try:
        rcList = query.get_review_committee_lut(reviewCommitteeID)
        if rcList is not None:
            form = forms.ReviewCommitteeLUTForm(request.form)
            if form.validate():
                if int(request.form['versionID']) == rcList.versionID:
                    rcList.reviewCommittee = form.reviewCommittee.data
                    rcList.reviewCommitteeDescription = form.reviewCommitteeDescription.data
                    query.commit()
                    return rcList.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ReviewCommitteeID {} not found".format(reviewCommitteeID))
    except Exception as e:
        return internal_error(e)

@api.route('/reviewcommitteelist/',methods = ['POST'])
def create_review_committee_list():
    try:
        form = forms.ReviewCommitteeLUTForm(request.form)
        if form.validate():
            reviewCommitteeList = models.ReviewCommitteeLUT(
                reviewCommittee=form.reviewCommittee.data,
                reviewCommitteeDescription=form.reviewCommitteeDescription.data
                )
            query.add(reviewCommitteeList)
            return reviewCommitteeList.json()
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/reviewcommitteelist/<int:reviewCommitteeID>/', methods = ['DELETE'])
def delete_review_committee_list(reviewCommitteeID):
    try:
        reviewCommittee = query.get_review_committee_lut(reviewCommitteeID)
        if reviewCommittee is not None:
            deps = get_dependencies(reviewCommittee)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(reviewCommittee)
                return item_deleted("ReviewCommitteeID {} deleted".format(reviewCommitteeID))
        else:
            return item_not_found("ReviewCommitteeID {} not found".format(reviewCommitteeID))
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
                if int(request.form['versionID']) == staff.versionID:
                    staff.firstName = form.firstName.data
                    staff.lastName = form.lastName.data
                    staff.middleName = form.middleName.data
                    staff.email = form.email.data
                    staff.phoneNumber = form.phoneNumber.data
                    staff.phoneComment = form.phoneComment.data
                    staff.institution = form.institution.data
                    staff.department = form.department.data
                    staff.position = form.position.data
                    staff.credentials = form.credentials.data
                    staff.street = form.street.data
                    staff.city = form.city.data
                    staff.stateID = form.stateID.data
                    staff.ucrRoleID = form.ucrRoleID.data
                    # don't allow user id to be changed
                    #staff.userID = form.userID.data
                    query.commit()
                    return staff.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("StaffID {} not found".format(staffID))
    except Exception as e:
        return internal_error(e)

@api.route('/staff/',methods = ['POST'])
def create_staff():
    try:
        form = forms.StaffForm(request.form)
        if form.validate():
            staff = models.Staff(
                firstName=form.firstName.data,
                lastName=form.lastName.data,
                middleName=form.middleName.data,
                email=form.email.data,
                phoneNumber=form.phoneNumber.data,
                phoneComment=form.phoneComment.data,
                institution=form.institution.data,
                department=form.department.data,
                position=form.position.data,
                credentials=form.credentials.data,
                street=form.street.data,
                city=form.city.data,
                stateID=form.stateID.data,
                ucrRoleID=form.ucrRoleID.data,
                userID = form.userID.data
            )
            query.add(staff)
            return staff.json()
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
@api.route('/staffroles/<int:staffRoleID>/', methods = ['GET'])
def get_staff_role(staffRoleID=None):
    try:
        if staffRoleID is None:
            return jsonify(StaffRoles = [i.dict() for i in query.get_staff_roles()])
        else:
            staffRole = query.get_staff_role(staffRoleID)
            if staffRole is not None:
                return staffRole.json()
            else:
                return item_not_found("StaffRoleID {} not found".format(staffRoleID))
    except Exception as e:
        return internal_error(e)

@api.route('/staffroles/<int:staffRoleID>/',methods = ['PUT'])
def update_staff_role(staffRoleID):
    try:
        staffRole = query.get_staff_role(staffRoleID)
        if staffRole is not None:
            form = forms.StaffRoleLUTForm(request.form)
            if form.validate():
                if int(request.form['versionID']) == staffRole.versionID:
                    staffRole.staffRole = form.staffRole.data
                    staffRole.staffRoleDescription = form.staffRoleDescription.data
                    query.commit()
                    return staffRole.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("StaffRoleID {} not found".format(staffRoleID))
    except Exception as e:
        return internal_error(e)

@api.route('/staffroles/',methods = ['POST'])
def create_staff_role():
    try:
        form = forms.StaffRoleLUTForm(request.form)
        if form.validate():
            staffRole = models.StaffRoleLUT(
                staffRole=form.staffRole.data,
                staffRoleDescription=form.staffRoleDescription.data,
            )
            query.add(staffRole)
            return staffRole.json()
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/staffroles/<int:staffRoleID>/', methods = ['DELETE'])
def delete_staff_role(staffRoleID):
    try:
        staffRole = query.get_staff_role(staffRoleID)
        if staffRole is not None:
            deps = get_dependencies(staffRole)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(staffRole)
                return item_deleted("StaffRoleID {} deleted".format(staffRoleID))
        else:
            return item_not_found("StaffRoleID {} not found".format(staffRoleID))
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
                if int(request.form['versionID']) == stafftraining.versionID:
                    stafftraining.staffID = form.staffID.data
                    stafftraining.humanSubjectTrainingID = form.humanSubjectTrainingID.data
                    stafftraining.dateTaken = form.dateTaken.data
                    stafftraining.dateExpires = form.dateExpires.data
                    query.commit()
                    return stafftraining.json()
                else:
                    return  out_of_date_error()
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
                staffID=form.staffID.data,
                humanSubjectTrainingID=form.humanSubjectTrainingID.data,
                dateTaken=form.dateTaken.data,
                dateExpires=form.dateExpires.data
                )
            query.add(stafftraining)
            return stafftraining.json()
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
                if int(request.form['versionID']) == tracing.versionID:
                    tracing.tracingSourceID = form.tracingSourceID.data
                    tracing.participantID = form.participantID.data
                    tracing.date = form.date.data
                    tracing.staffID = form.staffID.data
                    tracing.notes = form.notes.data
                    query.commit()
                    return tracing.json()
                else:
                    return out_of_date_error()
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
                tracingSourceID=form.tracingSourceID.data,
                participantID=form.participantID.data,
                date=form.date.data,
                staffID=form.staffID.data,
                notes=form.notes.data
                )
            query.add(tracing)
            return tracing.json()
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
@api.route('/tracingsources/<int:tracingSourceID>/', methods = ['GET'])
def get_tracing_source(tracingSourceID=None):
    try:
        if tracingSourceID is None:
            return jsonify(TracingSources = [i.dict() for i in query.get_tracing_sources()])
        else:
            tracing = query.get_tracing_source(tracingSourceID)
            if tracing is not None:
                return tracing.json()
            else:
                return item_not_found("TracingSourceID {} not found".format(tracingSourceID))
    except Exception as e:
        return internal_error(e)

@api.route('/tracingsources/<int:tracingSourceID>/',methods = ['PUT'])
def update_tracing_source(tracingSourceID):
    try:
        tracingSource = query.get_tracing_source(tracingSourceID)
        if tracingSource is not None:
            form = forms.TracingSourceLUTForm(request.form)
            if form.validate():
                if int(request.form['versionID']) == tracingSource.versionID:
                    tracingSource.description = form.description.data
                    query.commit()
                    return tracingSource.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("TracingSourceID {} not found".format(tracingSourceID))
    except Exception as e:
        return internal_error(e)

@api.route('/tracingsources/',methods = ['POST'])
def create_tracing_source():
    try:
        form = forms.TracingSourceLUTForm(request.form)
        if form.validate():
            tracingSource = models.TracingSourceLUT(
                description=form.description.data
                )
            ret = query.add(tracingSource)
            return tracingSource.json()
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@api.route('/tracingsources/<int:tracingSourceID>/', methods = ['DELETE'])
def delete_tracing_source(tracingSourceID):
    try:
        tracingSource = query.get_tracing_source(tracingSourceID)
        if tracingSource is not None:
            deps = get_dependencies(tracingSource)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(tracingSource)
                return item_deleted("TracingSourceID {} deleted".format(tracingSourceID))
        else:
            return item_not_found("TracingSourceID {} not found".format(tracingSourceID))
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
                if int(request.form['versionID']) == ucr.versionID:
                    ucr.projectID = form.projectID.data
                    ucr.reportTypeID = form.reportTypeID.data
                    ucr.reportSubmitted = form.reportSubmitted.data
                    ucr.reportDue = form.reportDue.data
                    ucr.reportDoc = form.reportDoc.data
                    query.commit()
                    return ucr.json()
                else:
                    return out_of_date_error()
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
                projectID=form.projectID.data,
                reportTypeID=form.reportTypeID.data,
                reportSubmitted=form.reportSubmitted.data,
                reportDue=form.reportDue.data,
                reportDoc=form.reportDoc.data
            )
            query.add(ucr)
            return ucr.json()
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


@api.route('/ucrroles/', methods=['GET'])
@api.route('/ucrroles/<int:ucrRoleID>/', methods=['GET'])
def get_ucr_role(ucrRoleID=None):
    try:
        if ucrRoleID is None:
            return jsonify(ucrRoles=[i.dict() for i in query.get_ucr_roles()])
        else:
            ucrRole = query.get_ucr_role(ucrRoleID)
            if ucrRole is not None:
                return ucrRole.json()
            else:
                return item_not_found("UCRRoleID {} not found".format(ucrRoleID))
    except Exception as e:
        return internal_error(e)


@api.route('/ucrroles/<int:ucrRoleID>/', methods=['PUT'])
def update_ucr_role(ucrRoleID):
    try:
        ucrRole = query.get_ucr_role(ucrRoleID)
        if ucrRole is not None:
            form = forms.UCRRoleForm(request.form)
            if form.validate():
                if int(form.versionID.data) == ucrRole.versionID:
                    ucrRole.ucrRole = form.ucrRole.data
                    query.commit()
                    return ucrRole.json()
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("UCRRoleID {} not found".format(ucrRoleID))
    except Exception as e:
        return internal_error(e)


@api.route('/ucrroles/', methods=['POST'])
def create_ucr_role():
    try:
        form = forms.UCRRoleForm(request.form)
        if form.validate():
            ucrRole = models.UCRRole(
                ucrRole=form.ucrRole.data,
            )
            query.add(ucrRole)
            return ucrRole.json()
        else:
            return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@api.route('/ucrroles/<int:ucrRoleID>/', methods=['DELETE'])
def delete_ucr_role(ucrRoleID):
    try:
        ucrRole = query.get_project_type(ucrRoleID)
        if ucrRole is not None:
            deps = get_dependencies(ucrRole)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(ucrRole)
                return item_deleted("UCRRoleID {} deleted".format(ucrRoleID))
        else:
            return item_not_found("UCRRoleID {} not found".format(ucrRoleID))
    except Exception as e:
        return internal_error(e)
