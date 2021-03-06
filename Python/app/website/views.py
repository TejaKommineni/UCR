import flask
from flask import jsonify, request, make_response, url_for, redirect, abort, g, session, current_app, flash
from flask import Blueprint, render_template, abort
import app.query as query
import app.models as models
import app.forms as forms
from app.helpers import value_or_none
from datetime import datetime
from app.database import db
from sqlalchemy_utils import dependent_objects
from sqlalchemy.inspection import inspect
import json
from io import StringIO
from urllib.parse import urlparse, urljoin
from flask.ext.cas import login as cas_login
from functools import wraps
import datetime
import csv
import re
website = Blueprint('website', __name__, template_folder='website_templates')

@website.context_processor
def add_user_to_jinja():
    """
    This adds the user to the context that is availabe in the Jinja templates
    If DEV_MODE is set, a fake user is created
    If DEV_ROLE is also set, the role will be read from the config.py
    :return:
    """
    if 'DEV_MODE' in current_app.config and current_app.config['DEV_MODE']:
        user = query.get_user(1)
    else:
        user = query.get_user_by_username(flask.session['CAS_USERNAME'])
    return dict(user=user)


def authorization_required(roles):
    """
    A decorator function to make sure the user is logged in via CAS and has proper roles for the
    endpoint they are trying to use

    If DEV_MODE is set, CAS authentication is ignored and a fake user is created
    :param roles:
    :return:
    """
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if 'CAS_USERNAME' not in flask.session and not ('DEV_MODE' in current_app.config and current_app.config['DEV_MODE']):
                flask.session['CAS_AFTER_LOGIN_SESSION_URL'] = flask.request.path
                return cas_login()
            else:
                if 'DEV_MODE' in current_app.config and current_app.config['DEV_MODE']:
                    user = query.get_user(1)
                else:
                    user = query.get_user_by_username(flask.session['CAS_USERNAME'])
                if user is None:
                    return unauthorized("User is not authorized to use this application.")
                if user.staff.ucrRole.ucrRole in roles:
                    return function(*args, **kwargs)
                else:
                    return unauthorized("User is not authorized to use this part of the application. Acceptable roles are: {}".format(", ".join(roles)))
            return unauthorized()
        return wrapper
    return real_decorator


def is_safe_url(target):
    """
    Checks to make sure the target url is safe for redireciton
    :param target:
    :return:
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def get_redirect_target():
    """
    Gets the url to redirect to
    :return:
    """
    if "_redirectlink" in request.values:
        link = "/website/{}".format(request.values["_redirectlink"].lstrip("/").replace("website","").lstrip("/"))
        if is_safe_url(link):
            return link

    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def redirect_back(endpoint, **values):
    """
    Redirect back to endpoint
    :param endpoint:
    :param values:
    :return:
    """
    target = get_redirect_target()
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


##############################################################################
# Error Handlers
##############################################################################
def item_not_found(e):
    """
    The handler when an item or url is not found
    :param e: The error message
    :return: templated html
    """
    message = "Error: {}".format(e)
    return render_template("error.html", message=message), 404


def invalid_method():
    """
    The handler when an invalid method is called
    :param e: The error message
    :return: templated html
    """
    message = "Invalid Method Detected"
    return render_template("error.html", message=message), 400


def missing_params(e):
    """
    The handler when a POST/PUT request is missing a parameter
    :param e: The error message
    :return: templated html
    """
    message = "Error: {}".format(e)
    return render_template("error.html", message=message)


def out_of_date_error():
    """
    The handler when an item PUT item was changed before submitted
    :param e: The error message
    :return: templated html
    """
    message = "Conflict detected. Object has been changed. Please refresh data and update."
    return message, 409


def internal_error(e):
    """
    The handler when an internal error happens
    :param e: The error message
    :return: templated html
    """
    message = "Error: {}".format(e)
    return render_template("error.html", message=message), 500


def item_deleted(message):
    """
    The handler when an item was deleted/ no longer exists
    :param e: The error message
    :return: templated html
    """
    return render_template("error.html", message=message)


def unauthorized(message=""):
    """
    The handler when the user is not authorized to use
    application or part of the application
    :param e: The error message
    :return: templated html
    """
    return render_template("error.html", message="You are not authorized to perform this action. {}".format(message)), 403


def get_dependencies(record):
    """
    Gets in dependencies of an object
    Used to check before deleting
    :param record:
    :return:
    """
    deps = list(dependent_objects(record).limit(5))
    dependencies = []
    if deps:
        for item in deps:
            dependencies.append({item.__class__.__name__: inspect(item).identity[0]})
    return dependencies


def dependency_detected(dependencies, message="Dependency Detected"):
    """
    The handler when trying to delete an item that has dependencies
    :param e: The error message
    :return: templated html
    """
    return "{} - {}".format(message, dependencies), 400


##############################################################################
# Root Node
##############################################################################
@website.route('/')
@authorization_required(roles=['Developer', 'Contact Staff', 'Informatics Staff', 'Director', 'Research Manager'])
def root():
    form = {}
    return render_template("homepage.html", form=form)
    if 'DEV_MODE' in current_app.config and current_app.config['DEV_MODE']:
        user = query.get_user(1)
    else:
        user = query.get_user_by_username(flask.session['CAS_USERNAME'])

    if user.staff.ucrRole.ucrRole == 'Director':
        return render_template("director.html", form=form)
    elif user.staff.ucrRole.ucrRole == 'Research Manager':
        return render_template("research_manager.html", form=form)
    elif user.staff.ucrRole.ucrRole == 'Contact Staff':
        return render_template("contact_staff.html", form=form)
    else:
        return render_template("informatics_staff.html", form=form)



@website.route('/overview/', methods=['GET'])
@authorization_required(roles=['Director', 'Developer', 'Research Manager', 'Informatics Staff'])
def overview():
    form = {}
    form["queryParams"] = {}
    mostRecentProjectStatusTypeID=None
    projectTitle=None
    piLastName=None
    projectTypeID=None
    if "action" in request.args:
        if request.args["action"].lower() == "clear":
            projectTitle = mostRecentProjectStatusTypeID = piLastName = projectTypeID = None
        else:
            if "mostRecentProjectStatusTypeID" in request.args:
                mostRecentProjectStatusTypeID = value_or_none(request.args["mostRecentProjectStatusTypeID"])
                form["queryParams"]["mostRecentProjectStatusTypeID"] = request.args["mostRecentProjectStatusTypeID"]
            if "projectTitle" in request.args:
                projectTitle = value_or_none(request.args["projectTitle"])
                form["queryParams"]["projectTitle"] = request.args["projectTitle"]
            if "piLastName" in request.args:
                piLastName = value_or_none(request.args["piLastName"])
                form["queryParams"]["piLastName"] = request.args["piLastName"]
            if "projectTypeID" in request.args:
                projectTypeID = value_or_none(request.args["projectTypeID"])
                form["queryParams"]["projectTypeID"] = request.args["projectTypeID"]

    form["summary"] = query.summary(projectTitle=projectTitle, mostRecentProjectStatusTypeID=mostRecentProjectStatusTypeID,piLastName=piLastName,projectTypeID=projectTypeID)
    form["projectStatusLUTs"] = query.get_project_status_luts()
    form["projectTypes"] = query.get_project_types()

    return render_template("study_summary_table.html", form=form)


@website.route('/abstractstatuses/', methods=['GET'])
@website.route('/abstractstatuses/<int:abstractStatusID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_abstract_status(abstractStatusID=None):
    try:
        if abstractStatusID is None:
            form = {
                "abstractStatuses": query.get_abstract_statuses(),
                "add": True
            }
            return render_template("abstract_statuses.html", form=form)
        else:
            abstractStatus = query.get_abstract_status(abstractStatusID)
            if abstractStatus is not None:
                form = {
                    "abstractStatuses": [abstractStatus],
                    "add": False
                }
                return render_template('abstract_statuses.html', form=form)
            else:
                return item_not_found("AbstractStatusID {} not found".format(abstractStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/abstractstatuses/<int:abstractStatusID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_abstract_status(abstractStatusID):
    try:
        abstractStatus = query.get_abstract_status(abstractStatusID)
        if abstractStatus is not None:
            form = forms.AbstractStatusForm(request.form)
            if form.validate():
                if int(form.versionID.data) == abstractStatus.versionID:
                    abstractStatus.abstractStatus = form.abstractStatus.data
                    query.commit()
                    flash("Updated Abstract Status")
                    return redirect_back('abstractstatuses/{}/'.format(abstractStatusID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("AbstractStatusID {} not found".format(abstractStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/abstractstatuses/', methods=['POST'])
@website.route('/abstractstatuses/<int:abstractStatusID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_abstract_status(abstractStatusID=None):
    try:
        if abstractStatusID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_abstract_status(abstractStatusID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_abstract_status(abstractStatusID)
            else:
                return invalid_method()
        else:
            form = forms.AbstractStatusForm(request.form)
            if form.validate():
                abstractStatus = models.AbstractStatus(
                    abstractStatus=form.abstractStatus.data,
                )
                query.add(abstractStatus)
                flash("Created Abstract Status")
                return redirect_back('abstractstatuses/{}/'.format(abstractStatus.abstractStatusID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/abstractstatuses/<int:abstractStatusID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/arcreviews/', methods = ['GET'])
@website.route('/arcreviews/<int:arcReviewID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_arc_review(arcReviewID=None):
    try:
        if arcReviewID is None:
            return jsonify(arcReviews=[i.dict() for i in query.get_arc_reviews()])
        else:
            arcReview = query.get_arc_review(arcReviewID)
            if arcReview is not None:
                form = {}
                form["staff"] = query.get_staffs()
                form["projects"] = query.get_projects()
                return render_template("arc_review_form.html", form=form, arcReview=arcReview)
            else:
                return item_not_found("ArcReviewID {} not found".format(arcReviewID))
    except Exception as e:
        return internal_error(e)


@website.route('/arcreviews/<int:arcReviewID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_arc_review(arcReviewID):
    try:
        arcReview = query.get_arc_review(arcReviewID)
        if arcReviewID is not None:
            form = forms.ArcReviewForm(request.form)
            if form.validate():
                if int(form.versionID.data) == arcReview.versionID:
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
                    flash("Updated Arc Review")
                    return redirect_back('arcreviews/{}/'.format(arcReviewID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ArcReviewID {} not found".format(arcReviewID))
    except Exception as e:
        return internal_error(e)


@website.route('/arcreviews/', methods=['POST'])
@website.route('/arcreviews/<int:arcReviewID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_arc_review(arcReviewID=None):
    try:
        if arcReviewID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_arc_review(arcReviewID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_arc_review(arcReviewID)
            else:
                return invalid_method()
        else:
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
                    contact=form.contact.data,
                    linkage=form.linkage.data,
                    engaged=form.engaged.data,
                    nonPublicData=form.nonPublicData.data
                )
                query.add(arcReview)
                flash("Created Arc Review")
                return redirect_back('arcreviews/{}/'.format(arcReview.arcReviewID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/arcreviews/<int:arcReviewID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/budgets/', methods = ['GET'])
@website.route('/budgets/<int:budgetID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_budget(budgetID=None):
    try:
        if budgetID is None:
            return jsonify(budgets=[i.dict() for i in query.get_budgets()])
        else:
            budget = query.get_budget(budgetID)
            if budget is not None:
                form = {}
                form["projects"] = query.get_projects()
                return render_template("budget_form.html", form=form, budget=budget)
            else:
                return item_not_found("BudgetID {} not found".format(budgetID))
    except Exception as e:
        return internal_error(e)


@website.route('/budgets/<int:budgetID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_budget(budgetID):
    try:
        budget = query.get_budget(budgetID)
        if budget is not None:
            form = forms.BudgetForm(request.form)
            if form.validate():
                if int(form.versionID.data) == budget.versionID:
                    budget.projectID = form.projectID.data
                    budget.numPeriods = form.numPeriods.data
                    budget.periodStart = form.periodStart.data
                    budget.periodEnd = form.periodEnd.data
                    budget.periodTotal = form.periodTotal.data
                    budget.periodComment = form.periodComment.data
                    query.commit()
                    flash("Updated Budget")
                    return redirect_back('budgets/{}/'.format(budgetID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("BudgetID {} not found".format(budgetID))
    except Exception as e:
        return internal_error(e)


@website.route('/budgets/', methods=['POST'])
@website.route('/budgets/<int:budgetID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_budget(budgetID=None):
    try:
        if budgetID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_budget(budgetID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_budget(budgetID)
            else:
                return invalid_method()
        else:
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
                flash("Created Budget")
                return redirect_back('budgets/{}/'.format(budget.budgetID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/budgets/<int:budgetID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/contacts/', methods = ['GET'])
@website.route('/contacts/<int:contactID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_contact(contactID=None):
    try:
        if contactID is None:
            return jsonify(Contacts=[i.dict() for i in query.get_contacts()])
        else:
            contact = query.get_contact(contactID)
            if contact is not None:
                form = {}
                form["staff"] = query.get_staffs()
                form["contactTypes"] = query.get_contact_types()
                form["projectPatients"] = query.get_project_patients()
                form["informants"] = contact.projectPatient.ctc.patient.informants
                form["informantPhones"] = []
                for informant in form["informants"]:
                    form["informantPhones"].extend(informant.informantPhones)
                form["facilities"] = [x.facility for x in contact.projectPatient.ctc.ctcFacilities]
                form["facilityPhones"] = []
                for facility in form["facilities"]:
                    form["facilityPhones"].extend(facility.facilityPhones)
                form["physicians"] = [x.physician for x in contact.projectPatient.ctc.physicianToCTC]
                form["physicianPhones"] = []
                for physician in form["physicians"]:
                    form["physicianPhones"].extend(physician.physicianPhones)
                form["patientPhones"] = contact.projectPatient.ctc.patient.patientPhones
                return render_template("contact_form.html", form=form, contact=contact)
            else:
                return item_not_found("ContactID {} not found".format(contactID))
    except Exception as e:
        return internal_error(e)


@website.route('/contacts/<int:contactID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_contact(contactID):
    try:
        contact = query.get_contact(contactID)
        if contact is not None:
            form = forms.ContactForm(request.form)
            if form.validate():
                if int(form.versionID.data) == contact.versionID:
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
                    flash("Updated Contact")
                    return redirect_back("contacts/{}/".format(contactID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ContactID {} not found".format(contactID))
    except Exception as e:
        return internal_error(e)


@website.route('/contacts/', methods=['POST'])
@website.route('/contacts/<int:contactID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_contact(contactID=None):
    try:
        if contactID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_contact(contactID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_contact(contactID)
            else:
                return invalid_method()
        else:
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
                flash("Created Contact")
                return redirect_back("contacts/{}/".format(contact.contactID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/contacts/<int:contactID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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
@website.route('/contacttypes/', methods=['GET'])
@website.route('/contacttypes/<int:contactTypeID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_contact_type(contactTypeID=None):
    try:
        if contactTypeID is None:
            form = {
                "contactTypes": query.get_contact_types(),
                "add": True
            }
            return render_template("contact_types.html", form=form)
        else:
            contactType = query.get_contact_type(contactTypeID)
            if contactType is not None:
                form = {
                    "contactTypes": [contactType],
                    "add": False
                }
                return render_template('contact_types.html', form=form)
            else:
                return item_not_found("ContactTypeID {} not found".format(contactTypeID))
    except Exception as e:
        return internal_error(e)


@website.route('/contacttypes/<int:contactTypeID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_contact_type(contactTypeID):
    try:
        contactType = query.get_contact_type(contactTypeID)
        if contactType is not None:
            form = forms.ContactTypeLUTForm(request.form)
            if form.validate():
                if contactType.contactCode != form.contactCode.data:
                    contactType2 = query.get_contact_type_by_code(form.contactCode.data)
                    if contactType2:
                        form.contactCode.errors.append("Contact Code already exists in database.")
                    return missing_params(form.errors)
                if int(form.versionID.data) == contactType.versionID:
                    contactType.contactDefinition = form.contactDefinition.data
                    contactType.contactCode = form.contactCode.data
                    query.commit()
                    flash("Updated Contact Type")
                    return redirect_back('contacttypes/{}/'.format(contactTypeID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ContactTypeID {} not found".format(contactTypeID))
    except Exception as e:
        return internal_error(e)


@website.route('/contacttypes/', methods=['POST'])
@website.route('/contacttypes/<int:contactTypeID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_contact_type(contactTypeID=None):
    try:
        if contactTypeID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_contact_type(contactTypeID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_contact_type(contactTypeID)
            else:
                return invalid_method()
        else:
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
                flash("Created Contact Type")
                return redirect_back('contacttypes/{}/'.format(contactType.contactTypeID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/contacttypes/<int:contactTypeID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
@website.route('/contactinfosources/', methods=['GET'])
@website.route('/contactinfosources/<int:contactInfoSourceID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_contact_info_source(contactInfoSourceID=None):
    try:
        if contactInfoSourceID is None:
            form = {
                "contactInfoSources": query.get_contact_info_sources(),
                "add": True
            }
            return render_template("contact_info_sources.html", form=form)
        else:
            contactInfoSource = query.get_contact_info_source(contactInfoSourceID)
            if contactInfoSource is not None:
                form = {
                    "contactInfoSources": [contactInfoSource],
                    "add": False
                }
                return render_template('contact_info_sources.html', form=form)
            else:
                return item_not_found("ContactInfoSourceID {} not found".format(contactInfoSourceID))
    except Exception as e:
        return internal_error(e)


@website.route('/contactinfosources/<int:contactInfoSourceID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_contact_info_source(contactInfoSourceID):
    try:
        contactInfoSource = query.get_contact_info_source(contactInfoSourceID)
        if contactInfoSource is not None:
            form = forms.ContactInfoSourceForm(request.form)
            if form.validate():
                if int(form.versionID.data) == contactInfoSource.versionID:
                    contactInfoSource.contactInfoSource = form.contactInfoSource.data
                    query.commit()
                    flash("Updated Contact Info Source")
                    return redirect_back('contactinfosources/{}/'.format(contactInfoSourceID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ContactInfoSourceID {} not found".format(contactInfoSourceID))
    except Exception as e:
        return internal_error(e)


@website.route('/contactinfosources/', methods=['POST'])
@website.route('/contactinfosources/<int:contactInfoSourceID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_contact_info_source(contactInfoSourceID=None):
    try:
        if contactInfoSourceID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_contact_info_source(contactInfoSourceID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_contact_info_source(contactInfoSourceID)
            else:
                return invalid_method()
        else:
            form = forms.ContactInfoSourceForm(request.form)
            if form.validate():
                contactInfoSource = models.ContactInfoSourceLUT(
                    contactInfoSource=form.contactInfoSource.data,
                )
                query.add(contactInfoSource)
                flash("Created Contact Info Source")
                return redirect_back('contactinfosources/{}/'.format(contactInfoSource.contactInfoSourceID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/contactinfosources/<int:contactInfoSourceID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
@website.route('/contactinfostatuses/', methods=['GET'])
@website.route('/contactinfostatuses/<int:contactInfoStatusID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_contact_info_status(contactInfoStatusID=None):
    if contactInfoStatusID is None:
        form = {
            "contactInfoStatuses": query.get_contact_info_statuses(),
            "add": True
        }
        return render_template("contact_info_statuses.html", form=form)
    else:
        contactInfoStatus = query.get_contact_info_status(contactInfoStatusID)
        if contactInfoStatus is not None:
            form = {
                "contactInfoStatuses": [contactInfoStatus],
                "add": False
            }
            return render_template('contact_info_statuses.html', form=form)
        else:
            return item_not_found("ContactInfoStatusID {} not found".format(contactInfoStatusID))


@website.route('/contactinfostatuses/<int:contactInfoStatusID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_contact_info_status(contactInfoStatusID):
    try:
        contactInfoStatus = query.get_contact_info_status(contactInfoStatusID)
        if contactInfoStatus is not None:
            form = forms.ContactInfoStatusForm(request.form)
            if form.validate():
                if int(form.versionID.data) == contactInfoStatus.versionID:
                    contactInfoStatus.contactInfoStatus = form.contactInfoStatus.data
                    query.commit()
                    flash("Updated Contact Info Status")
                    return redirect_back('contactinfostatuses/{}/'.format(contactInfoStatusID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ContactInfoStatusID {} not found".format(contactInfoStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/contactinfostatuses/', methods=['POST'])
@website.route('/contactinfostatuses/<int:contactInfoStatusID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_contact_info_status(contactInfoStatusID=None):
    try:
        if contactInfoStatusID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_contact_info_status(contactInfoStatusID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_contact_info_status(contactInfoStatusID)
            else:
                return invalid_method()
        else:
            form = forms.ContactInfoStatusForm(request.form)
            if form.validate():
                contactInfoStatus = models.ContactInfoStatusLUT(
                    contactInfoStatus=form.contactInfoStatus.data,
                )
                query.add(contactInfoStatus)
                flash("Created Contact Info Status")
                return redirect_back('contactinfostatuses/{}/'.format(contactInfoStatus.contactInfoStatusID))
            else:
                missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/contactinfostatuses/<int:contactInfoStatusID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/ctcs/', methods = ['GET'])
@website.route('/ctcs/<int:ctcID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_ctc(ctcID=None):
    try:
        if ctcID is None:
            return jsonify(CTCs=[i.dict() for i in query.get_ctcs()])
        else:
            ctc = query.get_ctc(ctcID)
            if ctc is not None:
                form = {}
                form["states"] = query.get_states()
                form["ctcs"] = query.get_ctcs()
                form["facilities"] = query.get_facilities()
                form["physicians"] = query.get_physicians()
                return render_template('ctc_form.html', form=form, ctc=ctc)
            else:
                return item_not_found("CtcID {} not found".format(ctcID))
    except Exception as e:
        return internal_error(e)


@website.route('/ctcs/<int:ctcID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_ctc(ctcID):
    try:
        ctc = query.get_ctc(ctcID)
        if ctc is not None:
            form = forms.CTCForm(request.form)
            if form.validate():
                if int(form.versionID.data) == ctc.versionID:
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
                    ctc.ctcRecordNumber = form.ctcRecordNumber.data
                    ctc.dmsCtcID=form.dmsCtcID.data
                    query.commit()
                    flash("Updated CTC")
                    return redirect_back('ctcs/{}/'.format(ctcID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("CtcID {} not found".format(ctcID))
    except Exception as e:
        return internal_error(e)


@website.route('/ctcs/', methods=['POST'])
@website.route('/ctcs/<int:ctcID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_ctc(ctcID=None):
    try:
        if ctcID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_ctc(ctcID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_ctc(ctcID)
            else:
                return invalid_method()
        else:
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
                    recordID=form.recordID.data,
                    ctcRecordNumber = form.ctcRecordNumber.data,
                    dmsCtcID = form.dmsCtcID.data
                )
                query.add(ctc)
                flash("Created CTC")
                return redirect_back('ctcs/{}/'.format(ctc.ctcID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/ctcs/<int:ctcID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/ctcfacilities/', methods = ['GET'])
@website.route('/ctcfacilities/<int:CTCFacilityID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_ctc_facility(CTCFacilityID=None):
    try:
        if CTCFacilityID is None:
            return jsonify(CTCFacilities=[i.dict() for i in query.get_ctc_facilities()])
        else:
            ctcFacility = query.get_ctc_facility(CTCFacilityID)
            if ctcFacility is not None:
                form = {}
                form["ctcs"] = query.get_ctcs()
                form["facilities"] = query.get_facilities()
                return render_template("ctc_facility_form.html", form=form, ctcFacility=ctcFacility)
            else:
                return item_not_found("CTCFacilityID {} not found".format(CTCFacilityID))
    except Exception as e:
        return internal_error(e)


@website.route('/ctcfacilities/<int:CTCFacilityID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_ctc_facility(CTCFacilityID):
    try:
        ctcFacility = query.get_ctc_facility(CTCFacilityID)
        if ctcFacility is not None:
            form = forms.CTCFacilityForm(request.form)
            if form.validate():
                if int(form.versionID.data) == ctcFacility.versionID:
                    ctcFacility.ctcID = form.ctcID.data
                    ctcFacility.facilityID = form.facilityID.data
                    ctcFacility.coc = form.coc.data
                    query.commit()
                    flash("Updated CTC to Facility Link")
                    return redirect_back("ctcfacilities/{}/".format(CTCFacilityID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("CTCFacilityID {} not found".format(CTCFacilityID))
    except Exception as e:
        return internal_error(e)


@website.route('/ctcfacilities/', methods=['POST'])
@website.route('/ctcfacilities/<int:CTCFacilityID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_ctc_facility(CTCFacilityID=None):
    try:
        if CTCFacilityID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_ctc_facility(CTCFacilityID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_ctc_facility(CTCFacilityID)
            else:
                return invalid_method()
        else:
            form = forms.CTCFacilityForm(request.form)
            if form.validate():
                ctcFacility = models.CTCFacility(
                    ctcID=form.ctcID.data,
                    facilityID=form.facilityID.data,
                    coc=form.coc.data
                )
                query.add(ctcFacility)
                flash("Created CTC to Facility Link")
                return redirect_back("ctcfacilities/{}/".format(ctcFacility.CTCFacilityID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/ctcfacilities/<int:CTCFacilityID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# Departments LUT
##############################################################################
@website.route('/departments/', methods=['GET'])
@website.route('/departments/<int:departmentID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_department(departmentID=None):
    try:
        if departmentID is None:
            form = {
                "departments": query.get_departments(),
                "add": True
            }
            return render_template("departments.html", form=form)
        else:
            department = query.get_department(departmentID)
            if department is not None:
                form = {
                    "departments": [department],
                    "add": False
                }
                return render_template("departments.html", form=form)
            else:
                return item_not_found("DepartmentID {} not found".format(departmentID))
    except Exception as e:
        return internal_error(e)

@website.route('/departments/<int:departmentID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_department(departmentID):
    try:
        department = query.get_department(departmentID)
        if department is not None:
            form = forms.DepartmentLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == department.versionID:
                    department.department = form.department.data
                    query.commit()
                    flash("Updated Departments")
                    return redirect_back('departments/{}/'.format(departmentID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("DepartmentID {} not found".format(departmentID))
    except Exception as e:
        return internal_error(e)

@website.route('/departments/', methods=['POST'])
@website.route('/departments/<int:departmentID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_department(departmentID=None):
    try:
        if departmentID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_department(departmentID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_department(departmentID)
            else:
                return invalid_method()
        else:
            form = forms.DepartmentLUTForm(request.form)
            if form.validate():
                department = models.Department(
                    department=form.department.data
                )
                query.add(department)
                flash("Created Department")
                return redirect_back(
                    'departments/{}/'.format(department.departmentID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@website.route('/departments/<int:departmentID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def delete_department(departmentID):
    try:
        department = query.get_department(departmentID)
        if department is not None:
            deps = get_dependencies(department)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(department)
                return item_deleted("DepartmentID {} deleted".format(departmentID))
        else:
            return item_not_found("DepartmentID {} not found".format(departmentID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# ExternalStudyCode LUT
##############################################################################
@website.route('/externalstudycodes/', methods=['GET'])
@website.route('/externalstudycodes/<int:externalID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_external_study_code(externalID=None):
    try:
        if externalID is None:
            form = {
                "externals": query.get_external_study_codes(),
                "add": True
            }
            return render_template("externalstudycodes.html", form=form)
        else:
            externalStudyCode = query.get_external_study_code(externalID)
            if externalStudyCode is not None:
                form = {
                    "externals": [externalStudyCode],
                    "add": False
                }
                return render_template("externalstudycodes.html", form=form)
            else:
                return item_not_found("externalID {} not found".format(externalID))
    except Exception as e:
        return internal_error(e)

@website.route('/externalstudycodes/<int:externalID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_external_study_code(externalID):
    try:
        externalStudy = query.get_external_study_code(externalID)
        if externalStudy is not None:
            form = forms.ExternalStudyCodeLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == externalStudy.versionID:
                    externalStudy.externalStudyCode = form.externalStudyCode.data
                    query.commit()
                    flash("Updated External Study Code")
                    return redirect_back('externalstudycodes/{}/'.format(externalID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("externalID {} not found".format(externalID))
    except Exception as e:
        return internal_error(e)

@website.route('/externalstudycodes/', methods=['POST'])
@website.route('/externalstudycodes/<int:externalID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_external_study_code(externalID=None):
    try:
        if externalID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_external_study_code(externalID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_external_study_code(externalID)
            else:
                return invalid_method()
        else:
            form = forms.ExternalStudyCodeLUTForm(request.form)
            if form.validate():
                externalStudy = models.ExternalStudyCode(
                    externalID = form.externalID.data,
                    externalStudyCode=form.externalStudyCode.data
                )
                query.add(externalStudy)
                flash("Created External Code")
                return redirect_back(
                    'externalstudycodes/{}/'.format(externalStudy.externalID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@website.route('/externalstudycodes/<int:externalID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def delete_external_study_code(externalID):
    try:
        studycode = query.get_external_study_code(externalID)
        if studycode is not None:
            deps = get_dependencies(studycode)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(studycode)
                return item_deleted("ExternalCodeID {} deleted".format(externalID))
        else:
            return item_not_found("ExternalCodeID {} not found".format(externalID))
    except Exception as e:
        return internal_error(e)


##############################################################################
# Funding
##############################################################################
# @website.route('/fundings/', methods = ['GET'])
@website.route('/fundings/<int:fundingID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_funding(fundingID=None):
    try:
        if fundingID is None:
            return jsonify(Fundings=[i.dict() for i in query.get_fundings()])
        else:
            funding = query.get_funding(fundingID)
            if funding is not None:
                form = {}
                form["fundingSources"] = query.get_funding_sources()
                form["grantStatuses"] = query.get_grant_statuses()
                form["projects"] = query.get_projects()
                form["staff"] = query.get_staffs()
                return render_template("funding_form.html", form=form, funding=funding)
            else:
                return item_not_found("FundingID {} not found".format(fundingID))
    except Exception as e:
        return internal_error(e)


@website.route('/fundings/<int:fundingID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_funding(fundingID):
    try:
        funding = query.get_funding(fundingID)
        if funding is not None:
            form = forms.FundingForm(request.form)
            if form.validate():
                if int(form.versionID.data) == funding.versionID:
                    funding.grantStatusID = form.grantStatusID.data
                    funding.projectID = form.projectID.data
                    funding.fundingSourceID = form.fundingSourceID.data
                    funding.fundingNumber = form.fundingNumber.data
                    funding.grantTitle = form.grantTitle.data
                    funding.dateStatus = form.dateStatus.data
                    funding.grantPi = form.grantPi.data
                    funding.primaryChartfield = form.primaryChartfield.data
                    funding.secondaryChartfield = form.secondaryChartfield.data
                    funding.fundingNotes= form.fundingNotes.data
                    query.commit()
                    flash("Updated Funding")
                    return redirect_back('fundings/{}/'.format(fundingID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("FundingID {} not found".format(fundingID))
    except Exception as e:
        return internal_error(e)


@website.route('/fundings/', methods=['POST'])
@website.route('/fundings/<int:fundingID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_funding(fundingID=None):
    try:
        if fundingID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_funding(fundingID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_funding(fundingID)
            else:
                return invalid_method()
        else:
            form = forms.FundingForm(request.form)
            if form.validate():
                funding = models.Funding(
                    grantStatusID=form.grantStatusID.data,
                    projectID=form.projectID.data,
                    fundingSourceID=form.fundingSourceID.data,
                    fundingNumber=form.fundingNumber.data,
                    grantTitle=form.grantTitle.data,
                    dateStatus=form.dateStatus.data,
                    grantPi=form.grantPi.data,
                    primaryChartfield=form.primaryChartfield.data,
                    secondaryChartfield=form.secondaryChartfield.data,
                    fundingNotes=form.fundingNotes.data
                )
                query.add(funding)
                flash("Created Funding")
                return redirect_back('fundings/{}/'.format(funding.fundingID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/fundings/<int:fundingID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/facilityphones/', methods=['GET'])
@website.route('/facilityphones/<int:facilityPhoneID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_facility_phone(facilityPhoneID=None):
    try:
        if facilityPhoneID is None:
            return jsonify(FacilityPhones=[i.dict() for i in query.get_facility_phones()])
        else:
            facilityPhone = query.get_facility_phone(facilityPhoneID)
            if facilityPhone is not None:
                form = {}
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["phoneTypes"] = query.get_phone_types()
                return render_template("facility_phone_form.html", form=form, facilityPhone=facilityPhone)
            else:
                return item_not_found("FacilityPhoneID {} not found".format(facilityPhoneID))
    except Exception as e:
        return internal_error(e)


@website.route('/facilityphones/<int:facilityPhoneID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_facility_phone(facilityPhoneID):
    try:
        facilityPhone = query.get_facility_phone(facilityPhoneID)
        if facilityPhone is not None:
            form = forms.FacilityPhoneForm(request.form)
            if form.validate():
                if int(form.versionID.data) == facilityPhone.versionID:
                    facilityPhone.contactInfoSourceID = form.contactInfoSourceID.data
                    facilityPhone.facilityID = form.facilityID.data
                    facilityPhone.contactInfoStatusID = form.contactInfoStatusID.data
                    facilityPhone.clinicName = form.clinicName.data
                    facilityPhone.phoneTypeID = form.phoneTypeID.data
                    facilityPhone.phoneNumber = form.phoneNumber.data
                    facilityPhone.phoneStatusDate = form.phoneStatusDate.data
                    query.commit()
                    flash("Updated Facility Phone")
                    return redirect_back("facilityphones/{}/".format(facilityPhoneID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("FacilityPhoneID {} not found".format(facilityPhoneID))
    except Exception as e:
        return internal_error(e)


@website.route('/facilityphones/', methods=['POST'])
@website.route('/facilityphones/<int:facilityPhoneID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_facility_phone(facilityPhoneID=None):
    try:
        if facilityPhoneID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_facility_phone(facilityPhoneID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_facility_phone(facilityPhoneID)
            else:
                return invalid_method()
        else:
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
                flash("Created Facility Phone")
                return redirect_back("facilityphones/{}/".format(facilityPhone.facilityPhoneID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/facilityphones/<int:facilityPhoneID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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
@website.route('/facilities/', methods=['GET'])
@website.route('/facilities/<int:facilityID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_facility(facilityID=None):
    try:
        if facilityID is None:
            facilityName = None
            contactFirstName = None
            contactLastName = None
            facilityStatus = None
            form = {}
            form["queryParams"] = {}
            if "action" in request.args:
                if request.args["action"].lower() == "clear":
                    facilityName = contactFirstName = contactLastName = facilityStatus = None
                else:
                    if "facilityName" in request.args:
                        facilityName = value_or_none(request.args["facilityName"])
                        form["queryParams"]["facilityName"] = request.args["facilityName"]
                    if "contactFirstName" in request.args:
                        contactFirstName = value_or_none(request.args["contactFirstName"])
                        form["queryParams"]["contactFirstName"] = request.args["contactFirstName"]
                    if "contactLastName" in request.args:
                        contactLastName = value_or_none(request.args["contactLastName"])
                        form["queryParams"]["contactLastName"] = request.args["contactLastName"]
                    if "facilityStatus" in request.args:
                        facilityStatus = value_or_none(request.args["facilityStatus"])
                        form["queryParams"]["facilityStatus"] = request.args["facilityStatus"]

            facilities = query.query_facilities(facilityName=facilityName,
                                                contactFirstName=contactFirstName,
                                                contactLastName=contactLastName,
                                                facilityStatus=facilityStatus)

            return render_template("facility_table.html", form=form, facilities=facilities)
        else:
            facility = query.get_facility(facilityID)
            if facility is not None:
                form = {}
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["phoneTypes"] = query.get_phone_types()
                form["states"] = query.get_states()
                form["phoneTypes"] = query.get_phone_types()
                return render_template("facility_form.html", form=form, facility=facility)
            else:
                return item_not_found("FacilityID {} not found".format(facilityID))
    except Exception as e:
        return internal_error(e)


@website.route('/facilities/<int:facilityID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_facility(facilityID):
    try:
        facility = query.get_facility(facilityID)
        if facility is not None:
            form = forms.FacilityForm(request.form)
            if form.validate():
                if int(form.versionID.data) == facility.versionID:
                    facility.facilityName = form.facilityName.data
                    facility.contactFirstName = form.contactFirstName.data
                    facility.contactLastName = form.contactLastName.data
                    facility.facilityStatus = form.facilityStatus.data
                    facility.facilityStatusDate = form.facilityStatusDate.data
                    facility.contact2FirstName = form.contact2FirstName.data
                    facility.contact2LastName = form.contact2LastName.data
                    facility.displayID=form.displayID.data
                    query.commit()
                    flash("Updated Facility")
                    return redirect_back("facilties/{}/".format(facilityID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("FacilityID {} not found".format(facilityID))
    except Exception as e:
        return internal_error(e)


@website.route('/facilities/', methods=['POST'])
@website.route('/facilities/<int:facilityID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_facility(facilityID=None):
    try:
        if facilityID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_facility(facilityID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_facility(facilityID)
            else:
                return invalid_method()
        else:
            form = forms.FacilityForm(request.form)
            if form.validate():
                facility = models.Facility(
                    facilityName=form.facilityName.data,
                    contactFirstName=form.contactFirstName.data,
                    contactLastName=form.contactLastName.data,
                    facilityStatus=form.facilityStatus.data,
                    facilityStatusDate=form.facilityStatusDate.data,
                    contact2FirstName=form.contact2FirstName.data,
                    contact2LastName=form.contact2LastName.data,
                    displayID=form.displayID.data
                )
                ret = query.add(facility)
                flash("Created Facility")
                return redirect("facilities/{}/".format(facility.facilityID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/facilities/<int:facilityID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/facilityaddresses/', methods=['GET'])
@website.route('/facilityaddresses/<int:facilityAddressID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_facility_address(facilityAddressID=None):
    try:
        if facilityAddressID is None:
            return jsonify(FacilityAddresses=[i.dict() for i in query.get_facility_addresses()])
        else:
            facilityAddress = query.get_facility_address(facilityAddressID)
            if facilityAddress is not None:
                form = {}
                form["states"] = query.get_states()
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                form["contactInfoSources"] = query.get_contact_info_sources()
                return render_template("facility_address_form.html", form=form, facilityAddress=facilityAddress)
            else:
                return item_not_found("FacilityAddressID {} not found".format(facilityAddressID))
    except Exception as e:
        return internal_error(e)


@website.route('/facilityaddresses/<int:facilityAddressID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_facility_address(facilityAddressID):
    try:
        facilityAddress = query.get_facility_address(facilityAddressID)
        if facilityAddress is not None:
            form = forms.FacilityAddressForm(request.form)
            if form.validate():
                if int(form.versionID.data) == facilityAddress.versionID:
                    facilityAddress.contactInfoSourceID = form.contactInfoSourceID.data
                    facilityAddress.facilityID = form.facilityID.data
                    facilityAddress.contactInfoStatusID = form.contactInfoStatusID.data
                    facilityAddress.street = form.street.data
                    facilityAddress.street2 = form.street2.data
                    facilityAddress.city = form.city.data
                    if form.stateID.data is '':
                        facilityAddress.stateID = 'zz'
                    else:
                        facilityAddress.stateID = form.stateID.data
                    facilityAddress.zip = form.zip.data
                    facilityAddress.addressStatusDate = form.addressStatusDate.data
                    query.commit()
                    flash("Updated Facility Address")
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
            return redirect_back("facilityaddresses/{}/".format(facilityAddressID))
        else:
            return item_not_found("FacilityAddressID {} not found".format(facilityAddressID))
    except Exception as e:
        return internal_error(e)


@website.route('/facilityaddresses/', methods=['POST'])
@website.route('/facilityaddresses/<int:facilityAddressID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_facility_address(facilityAddressID=None):
    try:
        if facilityAddressID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_facility_address(facilityAddressID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_facility_address(facilityAddressID)
            else:
                return invalid_method()
        else:
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
                flash("Created Facility Address")
                return redirect_back("facilityaddresses/{}/".format(facilityAddressID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/facilityaddresses/<int:facilityAddressID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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


@website.route('/finalcodes/', methods=['GET'])
@website.route('/finalcodes/<int:finalCodeID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_final_code(finalCodeID=None):
    try:
        if finalCodeID is None:
            form = {
                "finalCodes": query.get_final_codes(),
                "add": True
            }
            return render_template("final_codes.html", form=form)
        else:
            finalCode = query.get_final_code(finalCodeID)
            if finalCode is not None:
                form = {
                    "finalCodes": [finalCode],
                    "add": False
                }
                return render_template("final_codes.html", form=form)
            else:
                return item_not_found("FinalCodeID {} not found".format(finalCodeID))
    except Exception as e:
        return internal_error(e)


@website.route('/finalcodes/<int:finalCodeID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
                    flash("Updated Final Code")
                    return redirect_back('finalcodes/{}/'.format(finalCodeID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("FinalCodeID {} not found".format(finalCodeID))
    except Exception as e:
        return internal_error(e)


@website.route('/finalcodes/', methods=['POST'])
@website.route('/finalcodes/<int:finalCodeID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_final_code(finalCodeID=None):
    try:
        if finalCodeID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_final_code(finalCodeID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_final_code(finalCodeID)
            else:
                return invalid_method()
        else:
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
                flash("Created Final Code")
                return redirect_back('finalcodes/{}/'.format(finalCode.finalCodeID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/finalcodes/<int:finalCodeID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# Field Divisions LUT
##############################################################################
@website.route('/fielddivisions/', methods=['GET'])
@website.route('/fielddivisions/<int:fielddivisionID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_fielddivision(fielddivisionID=None):
    try:
        if fielddivisionID is None:
            form = {
                "fieldDivisions": query.get_fieldDivisions(),
                "add": True
            }
            return render_template("fielddivisions.html", form=form)
        else:
            fieldDivision = query.get_fieldDivision(fielddivisionID)
            if fieldDivision is not None:
                form = {
                    "fieldDivisions": [fieldDivision],
                    "add": False
                }
                return render_template("fielddivisions.html", form=form)
            else:
                return item_not_found("Field Division ID {} not found".format(fielddivisionID))
    except Exception as e:
        return internal_error(e)

@website.route('/fielddivisions/<int:fielddivisionID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_fielddivision(fielddivisionID):
    try:
        fieldDivision = query.get_fieldDivision(fielddivisionID)
        if fieldDivision is not None:
            form = forms.FieldDivisionLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == fieldDivision.versionID:
                    fieldDivision.fieldDivision = form.fieldDivision.data
                    query.commit()
                    flash("Updated Field Divisions")
                    return redirect_back('fielddivisions/{}/'.format(fielddivisionID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("Field Division ID {} not found".format(fielddivisionID))
    except Exception as e:
        return internal_error(e)

@website.route('/fielddivisions/', methods=['POST'])
@website.route('/fielddivisions/<int:fielddivisionID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_fielddivision(fielddivisionID=None):
    try:
        if fielddivisionID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_fielddivision(fielddivisionID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_fielddivision(fielddivisionID)
            else:
                return invalid_method()
        else:
            form = forms.FieldDivisionLUTForm(request.form)
            if form.validate():
                fieldDivision = models.FieldDivision(
                    fieldDivision=form.fieldDivision.data
                )
                query.add(fieldDivision)
                flash("Created Field Division")
                return redirect_back(
                    'fielddivisions/{}/'.format(fieldDivision.fieldDivisionID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@website.route('/fielddivisions/<int:fielddivisionID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def delete_fielddivision(fielddivisionID):
    try:
        fieldDivision = query.get_fieldDivision(fielddivisionID)
        if fieldDivision is not None:
            deps = get_dependencies(fieldDivision)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(fieldDivision)
                return item_deleted("Field Division ID {} deleted".format(fielddivisionID))
        else:
            return item_not_found("Field Division ID {} not found".format(fielddivisionID))
    except Exception as e:
        return internal_error(e)


##############################################################################
# Funding Source LUT
##############################################################################
@website.route('/fundingsources/', methods=['GET'])
@website.route('/fundingsources/<int:fundingSourceID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_funding_source(fundingSourceID=None):
    try:
        if fundingSourceID is None:
            form = {
                "fundingSources": query.get_funding_sources(),
                "add": True
            }
            return render_template("funding_sources.html", form=form)
        else:
            fundingSource = query.get_funding_source(fundingSourceID)
            if fundingSource is not None:
                form = {
                    "fundingSources": [fundingSource],
                    "add": False
                }
                return render_template("funding_sources.html", form=form)
            else:
                return item_not_found("FundingSourceID {} not found".format(fundingSourceID))
    except Exception as e:
        return internal_error(e)


@website.route('/fundingsources/<int:fundingSourceID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_funding_source(fundingSourceID):
    try:
        fundingSource = query.get_funding_source(fundingSourceID)
        if fundingSource is not None:
            form = forms.FundingSourceLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == fundingSource.versionID:
                    fundingSource.fundingSource = form.fundingSource.data
                    query.commit()
                    flash("Updated Funding Source")
                    return redirect_back('fundingsources/{}/'.format(fundingSourceID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("FundingSourceID {} not found".format(fundingSourceID))
    except Exception as e:
        return internal_error(e)


@website.route('/fundingsources/', methods=['POST'])
@website.route('/fundingsources/<int:fundingSourceID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_funding_source(fundingSourceID=None):
    try:
        if fundingSourceID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_funding_source(fundingSourceID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_funding_source(fundingSourceID)
            else:
                return invalid_method()
        else:
            form = forms.FundingSourceLUTForm(request.form)
            if form.validate():
                fundingSource = models.FundingSourceLUT(
                    fundingSource=form.fundingSource.data
                )
                query.add(fundingSource)
                flash("Created Funding Source")
                return redirect_back('fundingsources/{}/'.format(fundingSource.fundingSourceID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/fundingsources/<int:fundingSourceID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
@website.route('/grantstatuses/', methods=['GET'])
@website.route('/grantstatuses/<int:grantStatusID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_grant_status(grantStatusID=None):
    try:
        if grantStatusID is None:
            form = {
                "grantStatuses": query.get_grant_statuses(),
                "add": True
            }
            return render_template("grant_statuses.html", form=form)
        else:
            grantStatus = query.get_grant_status(grantStatusID)
            if grantStatus is not None:
                form = {
                    "grantStatuses": [grantStatus],
                    "add": False
                }
                return render_template("grant_statuses.html", form=form)
            else:
                return item_not_found("GrantStatusID {} not found".format(grantStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/grantstatuses/<int:grantStatusID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_grant_status(grantStatusID):
    try:
        grantStatus = query.get_grant_status(grantStatusID)
        if grantStatus is not None:
            form = forms.GrantStatusLUTForm(request.form)
            if form.validate():
                if int(request.form['versionID']) == grantStatus.versionID:
                    grantStatus.grantStatus = form.grantStatus.data
                    flash("Updated Funding Source")
                    return redirect_back('grantstatuses/{}/'.format(grantStatusID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("GrantStatusID {} not found".format(grantStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/grantstatuses/', methods=['POST'])
@website.route('/grantstatuses/<int:grantStatusID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_grant_status(grantStatusID=None):
    try:
        if grantStatusID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_grant_status(grantStatusID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_grant_status(grantStatusID)
            else:
                return invalid_method()
        else:
            form = forms.GrantStatusLUTForm(request.form)
            if form.validate():
                grantStatus = models.GrantStatusLUT(
                    grantStatus=form.grantStatus.data
                )
                query.add(grantStatus)
                flash("Created Grant Status")
                return redirect_back('grantstatuses/{}/'.format(grantStatus.grantStatusID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/grantstatuses/<int:grantStatusID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
@website.route('/humansubjecttrainings/', methods=['GET'])
@website.route('/humansubjecttrainings/<int:humanSubjectTrainingID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_human_subject_training(humanSubjectTrainingID=None):
    try:
        if humanSubjectTrainingID is None:
            form = {
                "humanSubjectTrainings": query.get_human_subject_trainings(),
                "add": True
            }
            return render_template("human_subject_trainings.html", form=form)
        else:
            humanSubjectTraining = query.get_human_subject_training(humanSubjectTrainingID)
            if humanSubjectTraining is not None:
                form = {
                    "humanSubjectTrainings": [humanSubjectTraining],
                    "add": False
                }
                return render_template("human_subject_trainings.html", form=form)
            else:
                return item_not_found("HumanSubjectTrainingID {} not found".format(humanSubjectTrainingID))
    except Exception as e:
        return internal_error(e)


@website.route('/humansubjecttrainings/<int:humanSubjectTrainingID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_human_subject_training(humanSubjectTrainingID):
    try:
        humanSubjectTraining = query.get_human_subject_training(humanSubjectTrainingID)
        if humanSubjectTraining is not None:
            form = forms.HumanSubjectTrainingLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == humanSubjectTraining.versionID:
                    humanSubjectTraining.trainingType = form.trainingType.data
                    query.commit()
                    flash("Updated Human Subject Training")
                    return redirect_back('humansubjecttrainings/{}/'.format(humanSubjectTrainingID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("HumanSubjectTrainingID {} not found".format(humanSubjectTrainingID))
    except Exception as e:
        return internal_error(e)


@website.route('/humansubjecttrainings/', methods=['POST'])
@website.route('/humansubjecttrainings/<int:humanSubjectTrainingID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_human_subject_training(humanSubjectTrainingID=None):
    try:
        if humanSubjectTrainingID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_human_subject_training(humanSubjectTrainingID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_human_subject_training(humanSubjectTrainingID)
            else:
                return invalid_method()
        else:
            form = forms.HumanSubjectTrainingLUTForm(request.form)
            if form.validate():
                humanSubjectTraining = models.HumanSubjectTrainingLUT(
                    trainingType=form.trainingType.data
                )
                query.add(humanSubjectTraining)
                flash("Created Human Subject Training")
                return redirect_back('humansubjecttrainings/{}/'.format(humanSubjectTraining.humanSubjectTrainingID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/humansubjecttrainings/<int:humanSubjectTrainingID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/incentives/', methods = ['GET'])
@website.route('/incentives/<int:incentiveID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_incentive(incentiveID=None):
    try:
        if incentiveID is None:
            return jsonify(Incentives=[i.dict() for i in query.get_incentives()])
        else:
            incentive = query.get_incentive(incentiveID)
            if incentive is not None:
                form = {}
                form["projectPatients"] = query.get_project_patients()
                return render_template("incentive_form.html", form=form, incentive=incentive)
            else:
                return item_not_found("IncentiveID {} not found".format(incentiveID))
    except Exception as e:
        return internal_error(e)


@website.route('/incentives/<int:incentiveID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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
                    incentive.contactID = form.contactID.data
                    query.commit()
                    flash("Updated Incentive")
                    return redirect_back('incentives/{}/'.format(incentive.incentiveID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("IncentiveID {} not found".format(incentiveID))
    except Exception as e:
        return internal_error(e)


@website.route('/incentives/', methods=['POST'])
@website.route('/incentives/<int:incentiveID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_incentive(incentiveID=None):
    try:
        if incentiveID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_incentive(incentiveID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_incentive(incentiveID)
            else:
                return invalid_method()
        else:
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
                    dateGiven=form.dateGiven.data,
                    contactID=form.contactID.data
                )
                query.add(incentive)
                flash("Created Incentive")
                return redirect_back("incentives/{}/".format(incentive.incentiveID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/incentives/<int:incentiveID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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
# @website.route('/informants/', methods=['GET'])
@website.route('/informants/<int:informantID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_informant(informantID=None):
    try:
        if informantID is None:
            return jsonify(Informants=[i.dict() for i in query.get_informants()])
        else:
            informant = query.get_informant(informantID)
            if informant is not None:
                form = {}
                form["states"] = query.get_states()
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                form["phoneTypes"] = query.get_phone_types()
                form["informantRelationships"] = query.get_informant_relationships()
                return render_template("informant_form.html", form=form, informant=informant)
            else:
                return item_not_found("InformantID {} not found".format(informantID))
    except Exception as e:
        return internal_error(e)


@website.route('/informants/<int:informantID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_informant(informantID):
    try:
        informant = query.get_informant(informantID)
        if informant is not None:
            form = forms.InformantForm(request.form)
            if form.validate():
                if int(form.versionID.data) == informant.versionID:
                    informant.participantID = form.participantID.data
                    informant.firstName = form.firstName.data
                    informant.lastName = form.lastName.data
                    informant.middleName = form.middleName.data
                    informant.informantPrimary = form.informantPrimary.data
                    informant.informantRelationshipID = form.informantRelationshipID.data
                    informant.notes = form.notes.data
                    query.commit()
                    flash("Updated Informant")
                    return redirect_back('informants/{}/'.format(informantID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("InformantID {} not found".format(informantID))
    except Exception as e:
        return internal_error(e)


@website.route('/informants/', methods=['POST'])
@website.route('/informants/<int:informantID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_informant(informantID=None):
    try:
        if informantID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_informant(informantID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_informant(informantID)
            else:
                return invalid_method()
        else:
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
                flash("Created Informant")
                return redirect_back('informants/{}/'.format(informant.informantID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/informants/<int:informantID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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
# @website.route('/informantaddresses/', methods=['GET'])
@website.route('/informantaddresses/<int:informantAddressID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_informant_address(informantAddressID=None):
    try:
        if informantAddressID is None:
            return jsonify(InformantAddresses=[i.dict() for i in query.get_informant_addresses()])
        else:
            informantAddress = query.get_informant_address(informantAddressID)
            if informantAddress is not None:
                form = {}
                form["informantAddress"] = informantAddress
                form["states"] = query.get_states()
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                return render_template('informant_address_form.html', form=form)
            else:
                return item_not_found("InformantAddressID {} not found".format(informantAddressID))
    except Exception as e:
        return internal_error(e)


@website.route('/informantaddresses/<int:informantAddressID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_informant_address(informantAddressID):
    try:
        informantAddress = query.get_informant_address(informantAddressID)
        if informantAddress is not None:
            form = forms.InformantAddressForm(request.form)
            if form.validate():
                if int(form.versionID.data) == informantAddress.versionID:
                    informantAddress.contactInfoSourceID = form.contactInfoSourceID.data
                    informantAddress.informantID = form.informantID.data
                    informantAddress.contactInfoStatusID = form.contactInfoStatusID.data
                    informantAddress.street = form.street.data
                    informantAddress.street2 = form.street2.data
                    informantAddress.city = form.city.data
                    if form.stateID.data is not '':
                      informantAddress.stateID = form.stateID.data
                    else:
                      informantAddress.stateID = 'zz'
                    informantAddress.zip = form.zip.data
                    informantAddress.addressStatusDate = form.addressStatusDate.data
                    query.commit()
                    flash("Updated Informant Address")
                    return redirect_back('informantaddresses/{}/'.format(informantAddressID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("InformantAddressID {} not found".format(informantAddressID))
    except Exception as e:
        return internal_error(e)


@website.route('/informantaddresses/', methods=['POST'])
@website.route('/informantaddresses/<int:informantAddressID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_informant_address(informantAddressID=None):
    try:
        if informantAddressID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_informant_address(informantAddressID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_informant_address(informantAddressID)
            else:
                return invalid_method()
        else:
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
                flash("Created Informant Address")
                return redirect_back('informantaddresses/{}/'.format(informantAddress.informantAddressID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/informantaddresses/<int:informantAddressID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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
# @website.route('/informantphones/', methods=['GET'])
@website.route('/informantphones/<int:informantPhoneID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_informant_phone(informantPhoneID=None):
    try:
        if informantPhoneID is None:
            return jsonify(InformantPhones=[i.dict() for i in query.get_informant_phones()])
        else:
            informantPhone = query.get_informant_phone(informantPhoneID)
            if informantPhone is not None:
                form = {}
                form["states"] = query.get_states()
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                form["phoneTypes"] = query.get_phone_types()
                return render_template('informant_phone_form.html', form=form, informantPhone=informantPhone)
            else:
                return item_not_found("InformantPhoneID {} not found".format(informantPhoneID))
    except Exception as e:
        return internal_error(e)


@website.route('/informantphones/<int:informantPhoneID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_informant_phone(informantPhoneID):
    try:
        informantPhone = query.get_informant_phone(informantPhoneID)
        if informantPhone is not None:
            form = forms.InformantPhoneForm(request.form)
            if form.validate():
                if int(form.versionID.data) == informantPhone.versionID:
                    informantPhone.contactInfoSourceID = form.contactInfoSourceID.data
                    informantPhone.informantID = form.informantID.data
                    informantPhone.contactInfoStatusID = form.contactInfoStatusID.data
                    informantPhone.phoneTypeID = form.phoneTypeID.data
                    informantPhone.phoneNumber = form.phoneNumber.data
                    informantPhone.phoneStatusDate = form.phoneStatusDate.data
                    query.commit()
                    flash("Updated Informant Phone")
                    return redirect_back('informantphones/{}/'.format(informantPhoneID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("InformantPhoneID {} not found".format(informantPhoneID))
    except Exception as e:
        return internal_error(e)


@website.route('/informantphones/', methods=['POST'])
@website.route('/informantphones/<int:informantPhoneID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_informant_phone(informantPhoneID=None):
    try:
        if informantPhoneID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_informant_phone(informantPhoneID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_informant_phone(informantPhoneID)
            else:
                return invalid_method()
        else:
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
                flash("Created Informant Phone")
                return redirect_back('informantphones/{}/'.format(informantPhone.informantPhoneID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/informantphones/<int:informantPhoneID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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
# Institutions LUT
##############################################################################
@website.route('/institutions/', methods=['GET'])
@website.route('/institutions/<int:institutionID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_institution(institutionID=None):
    try:
        if institutionID is None:
            form = {
                "institutions": query.get_institutions(),
                "add": True
            }
            return render_template("institutions.html", form=form)
        else:
            institution = query.get_institution(institutionID)
            if institution is not None:
                form = {
                    "institutions": [institution],
                    "add": False
                }
                return render_template("institutions.html", form=form)
            else:
                return item_not_found("InstitutionID {} not found".format(institutionID))
    except Exception as e:
        return internal_error(e)

@website.route('/institutions/<int:institutionID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_institution(institutionID):
    try:
        institution = query.get_institution(institutionID)
        if institution is not None:
            form = forms.InstitutionLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == institution.versionID:
                    institution.institution = form.institution.data
                    query.commit()
                    flash("Updated Institutions")
                    return redirect_back('institutions/{}/'.format(institutionID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("InstitutionID {} not found".format(institutionID))
    except Exception as e:
        return internal_error(e)

@website.route('/institutions/', methods=['POST'])
@website.route('/institutions/<int:institutionID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_institution(institutionID=None):
    try:
        if institutionID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_institution(institutionID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_institution(institutionID)
            else:
                return invalid_method()
        else:
            form = forms.InstitutionLUTForm(request.form)
            if form.validate():
                institution = models.Institution(
                    institution=form.institution.data
                )
                query.add(institution)
                flash("Created Institution")
                return redirect_back(
                    'institutions/{}/'.format(institution.institutionID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@website.route('/institutions/<int:institutionID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def delete_institution(institutionID):
    try:
        institution = query.get_institution(institutionID)
        if institution is not None:
            deps = get_dependencies(institution)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(institution)
                return item_deleted("InstitutionID {} deleted".format(institutionID))
        else:
            return item_not_found("InstitutionID {} not found".format(institutionID))
    except Exception as e:
        return internal_error(e)


##############################################################################
# IRBHolderLUT
##############################################################################
@website.route('/irbholders/', methods=['GET'])
@website.route('/irbholders/<int:irbHolderID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_irb_holder(irbHolderID=None):
    try:
        if irbHolderID is None:
            form = {
                "irbHolders": query.get_irb_holders(),
                "add": True
            }
            return render_template("irb_holders.html", form=form)
        else:
            irb = query.get_irb_holder(irbHolderID)
            if irb is not None:
                form = {
                    "irbHolders": [irb],
                    "add": False
                }
                return render_template("irb_holders.html", form=form)
            else:
                return item_not_found("IrbHolderID {} not found".format(irbHolderID))
    except Exception as e:
        return internal_error(e)


@website.route('/irbholders/<int:irbHolderID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_irb_holder(irbHolderID):
    try:
        irb = query.get_irb_holder(irbHolderID)
        if irb is not None:
            form = forms.IRBHolderLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == irb.versionID:
                    irb.holder = form.holder.data
                    irb.holderDefinition = form.holderDefinition.data
                    query.commit()
                    flash("Updated IRB Holder")
                    return redirect_back('irbholders/{}/'.format(irbHolderID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("IrbHolderID {} not found".format(irbHolderID))
    except Exception as e:
        return internal_error(e)


@website.route('/irbholders/', methods=['POST'])
@website.route('/irbholders/<int:irbHolderID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_irb_holder(irbHolderID=None):
    try:
        if irbHolderID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_irb_holder(irbHolderID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_irb_holder(irbHolderID)
            else:
                return invalid_method()
        else:
            form = forms.IRBHolderLUTForm(request.form)
            if form.validate():
                irb = models.IRBHolderLUT(
                    holder=form.holder.data,
                    holderDefinition=form.holderDefinition.data
                )
                query.add(irb)
                flash("Created IRB Holder")
                return redirect_back('irbholders/{}/'.format(irb.irbHolderID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/irbholders/<int:irbHolderID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/logs/',methods=['GET'])
@website.route('/logs/<int:logID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_log(logID=None):
    try:
        if logID is None:
            return jsonify(Logs=[i.dict() for i in query.get_logs()])
        else:
            log = query.get_log(logID)
            if log is not None:
                form = {}
                form["projects"] = query.get_projects()
                form["staff"] = query.get_staffs()
                form["phaseStatuses"] = query.get_phase_statuses()
                form["logSubjects"] = query.get_log_subjects()
                return render_template("log_form.html", form=form, log=log)
            else:
                return item_not_found("LogID {} not found".format(logID))
    except Exception as e:
        internal_error(e)


@website.route('/logs/<int:logID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_log(logID):
    try:
        log = query.get_log(logID)
        if log is not None:
            form = forms.LogForm(request.form)
            if form.validate():
                if int(form.versionID.data) == log.versionID:
                    log.logSubjectID = form.logSubjectID.data
                    log.projectID = form.projectID.data
                    log.staffID = form.staffID.data
                    log.phaseStatusID = form.phaseStatusID.data
                    log.note = form.note.data
                    log.date = form.date.data
                    query.commit()
                    flash("Updated Log")
                    return redirect_back('logs/{}/'.format(logID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("LogID {} not found".format(logID))
    except Exception as e:
        return internal_error(e)


@website.route('/logs/', methods=['POST'])
@website.route('/logs/<int:logID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_log(logID=None):
    try:
        if logID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_log(logID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_log(logID)
            else:
                return invalid_method()
        else:
            form = forms.LogForm(request.form)
            if form.validate():
                log = models.Log(
                    logSubjectID=form.logSubjectID.data,
                    projectID=form.projectID.data,
                    staffID=form.staffID.data,
                    phaseStatusID=form.phaseStatusID.data,
                    note=form.note.data,
                    date=form.date.data
                )
                query.add(log)
                flash("Created Log")
                return redirect_back('logs/{}/'.format(log.logID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/logs/<int:logID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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
@website.route('/logsubjects/', methods=['GET'])
@website.route('/logsubjects/<int:logSubjectID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_log_subject(logSubjectID=None):
    try:
        if logSubjectID is None:
            form = {
                "logSubjects": query.get_log_subjects(),
                "add": True
            }
            return render_template("log_subjects.html", form=form)
        else:
            logSubject = query.get_log_subject(logSubjectID)
            if logSubject is not None:
                form = {
                    "irbHolders": query.get_log_subject(logSubjectID),
                    "add": True
                }
                return render_template("log_subjects.html", form=form)
            else:
                return item_not_found("LogSubjectID {} not found".format(logSubjectID))
    except Exception as e:
        return internal_error(e)


@website.route('/logsubjects/<int:logSubjectID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_log_subject(logSubjectID):
    try:
        logSubject = query.get_log_subject(logSubjectID)
        if logSubject is not None:
            form = forms.LogSubjectLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == logSubject.versionID:
                    logSubject.logSubject = form.logSubject.data
                    query.commit()
                    flash("Updated Log Subject")
                    return redirect_back('logsubjects/{}/'.format(logSubjectID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("logSubjectID {} not found".format(logSubjectID))
    except Exception as e:
        internal_error(e)


@website.route('/logsubjects/', methods=['POST'])
@website.route('/logsubjects/<int:logSubjectID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_log_subject(logSubjectID=None):
    try:
        if logSubjectID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_log_subject(logSubjectID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_log_subject(logSubjectID)
            else:
                return invalid_method()
        else:
            form = forms.LogSubjectLUTForm(request.form)
            if form.validate():
                logSubject = models.LogSubjectLUT(
                    logSubject=form.logSubject.data
                )
                query.add(logSubject)
                flash("Added Log Subject")
                return redirect_back('logsubjects/{}/'.format(logSubject.logSubjectID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/logsubjects/<int:logSubjectID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
@website.route('/patients/', methods=['GET'])
@website.route('/patients/<int:patAutoID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_patient(patAutoID=None):
    try:
        if patAutoID is None:
            form = {}
            firstName = None
            lastName = None
            patID = None
            recordID = None
            ucrDistID = None
            UPDBID = None
            phoneNumber = None
            form["queryParams"] = {}
            if "action" in request.args:
                if request.args["action"].lower() == "clear":
                    firstName = lastName = patID = ucrDistID = UPDBID = phoneNumber = None
                else:
                    if "firstName" in request.args:
                        firstName = value_or_none(request.args["firstName"])
                        form["queryParams"]["firstName"] = request.args["firstName"]
                    if "lastName" in request.args:
                        lastName = value_or_none(request.args["lastName"])
                        form["queryParams"]["lastName"] = request.args["lastName"]
                    if "patID" in request.args:
                        patID = value_or_none(request.args["patID"])
                        form["queryParams"]["patID"] = request.args["patID"]
                    if "ucrDistID" in request.args:
                        ucrDistID = value_or_none(request.args["ucrDistID"])
                        form["queryParams"]["ucrDistID"] = request.args["ucrDistID"]
                    if "UPDBID" in request.args:
                        UPDBID = value_or_none(request.args["UPDBID"])
                        form["queryParams"]["UPDBID"] = request.args["UPDBID"]
                    if "phoneNumber" in request.args:
                        phoneNumber = value_or_none(request.args["phoneNumber"])
                        form["queryParams"]["phoneNumber"] = request.args["phoneNumber"]

            patients = query.query_patients(firstName=firstName,
                                            lastName=lastName,
                                            patID=patID,
                                            ucrDistID=ucrDistID,
                                            UPDBID=UPDBID,
                                            phoneNumber=phoneNumber)
            form["patients"] = patients
            return render_template("patient_table.html", form=form)
        else:
            patient = query.get_patient(patAutoID)
            if patient is not None:
                form = {}
                form["patient"] = patient
                form["patientAddresses"] = patient.patientAddresses
                form["patientEmails"] = patient.patientEmails
                form["patientPhones"] = patient.patientPhones
                form["ctcs"] = patient.ctcs
                form["informants"] = patient.informants
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                form["races"] = query.get_races()
                form["ethnicities"] = query.get_ethnicities()
                form["sexes"] = query.get_sexes()
                form["states"] = query.get_states()
                form["phoneTypes"] = query.get_phone_types()
                return render_template("patient_form.html", form=form)
            else:
                return item_not_found("PatientID {} not found".format(patAutoID))
    except Exception as e:
        return internal_error(e)


@website.route('/patients/<int:patientID>/', methods=['PUT'])
def update_patient(patientID):
    try:
        patient = query.get_patient(patientID)
        if patient is not None:
            form = forms.PatientForm(request.form)
            if form.validate():
                if int(form.versionID.data) == patient.versionID:
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
                    patient.SSN = form.SSN.data
                    patient.sexID = form.sexID.data
                    patient.raceID = form.raceID.data
                    patient.ethnicityID = form.ethnicityID.data
                    patient.recordNumber=form.recordNumber.data
                    query.commit()
                    flash("Updated Patient")
                    return redirect_back("/patients/{}".format(patientID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PatientID {} not found".format(patientID))
    except Exception as e:
        return internal_error(e)


@website.route('/patients/', methods=['POST'])
@website.route('/patients/<int:patientID>/', methods=['POST'])
def create_patient(patientID=None):
    try:
        if patientID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_patient(patientID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_patient(patientID)
            else:
                return invalid_method()
        else:
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
                    SSN=form.SSN.data,
                    raceID=form.raceID.data,
                    sexID=form.sexID.data,
                    ethnicityID=form.ethnicityID.data,
                    recordNumber = form.recordNumber.data
                )
                query.add(patient)
                flash("Created Patient")
                return redirect_back("/patients/{}".format(patientID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/patients/<int:patientID>/', methods=['DELETE'])
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
# @website.route('/patientaddresses/', methods=['GET'])
@website.route('/patientaddresses/<int:patAddressID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_patient_address(patAddressID=None):
    try:
        if patAddressID is None:
            return jsonify(PatientAddresses=[i.dict() for i in query.get_patient_addresses()])
        else:
            patientAddress = query.get_patient_address(patAddressID)
            if patientAddress is not None:
                form = {}
                form["states"] = query.get_states()
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                return render_template('patient_address_form.html', form=form, patientAddress=patientAddress)
            else:
                return item_not_found("PatAddressID {} not found".format(patAddressID))
    except Exception as e:
        return internal_error(e)


@website.route('/patientaddresses/<int:patAddressID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_patient_address(patAddressID):
    try:
        patientAddress = query.get_patient_address(patAddressID)
        if patientAddress is not None:
            form = forms.PatientAddressForm(request.form)
            if form.validate():
                if int(form.versionID.data) == patientAddress.versionID:
                    patientAddress.contactInfoSourceID = form.contactInfoSourceID.data
                    patientAddress.participantID = form.participantID.data
                    patientAddress.contactInfoStatusID = form.contactInfoStatusID.data
                    patientAddress.street = form.street.data
                    patientAddress.street2 = form.street2.data
                    patientAddress.city = form.city.data
                    if form.stateID.data is not '':
                        patientAddress.stateID = form.stateID.data
                    else:
                        patientAddress.stateID = 'zz'
                    patientAddress.zip = form.zip.data
                    patientAddress.addressStatusDate = form.addressStatusDate.data
                    query.commit()
                    flash("Updated Patient Address")
                    return redirect_back('patientaddresses/{}/'.format(patAddressID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PatAddressID {} not found".format(patAddressID))
    except Exception as e:
        return internal_error(e)


@website.route('/patientaddresses/', methods=['POST'])
@website.route('/patientaddresses/<int:patAddressID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_patient_address(patAddressID=None):
    try:
        if patAddressID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_patient_address(patAddressID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_patient_address(patAddressID)
            else:
                return invalid_method()
        else:
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
                flash("Created Patient Address")
                return redirect_back('patientaddresses/{}/'.format(patientaddress.patAddressID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/patientaddresses/<int:patAddressID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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
# @website.route('/patientemails/', methods=['GET'])
@website.route('/patientemails/<int:emailID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_patient_email(emailID=None):
    try:
        if emailID is None:
            return jsonify(PatientEmails=[i.dict() for i in query.get_patient_emails()])
        else:
            patientEmail = query.get_patient_email(emailID)
            if patientEmail is not None:
                form = {}
                form["states"] = query.get_states()
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                return render_template('patient_email_form.html', form=form, patientEmail=patientEmail)
            else:
                return item_not_found("EmailID {} not found".format(emailID))
    except Exception as e:
        return internal_error(e)


@website.route('/patientemails/<int:emailID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_patient_email(emailID):
    try:
        patientEmail = query.get_patient_email(emailID)
        if patientEmail is not None:
            form = forms.PatientEmailForm(request.form)
            if form.validate():
                if int(form.versionID.data) == patientEmail.versionID:
                    patientEmail.contactInfoSourceID = form.contactInfoSourceID.data
                    patientEmail.participantID = form.participantID.data
                    patientEmail.contactInfoStatusID = form.contactInfoStatusID.data
                    patientEmail.email = form.email.data
                    patientEmail.emailStatusDate = form.emailStatusDate.data
                    query.commit()
                    flash("Updated Patient Email")
                    return redirect_back('patientemails/{}/'.format(emailID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("EmailID {} not found".format(emailID))
    except Exception as e:
        return internal_error(e)


@website.route('/patientemails/', methods=['POST'])
@website.route('/patientemails/<int:emailID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_patient_email(emailID=None):
    try:
        if emailID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_patient_email(emailID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_patient_email(emailID)
            else:
                return invalid_method()
        else:
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
                flash("Created Patient Email")
                return redirect_back('patientemails/{}/'.format(patientEmail.participantID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/patientemails/<int:emailID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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
# @website.route('/patientphones/', methods=['GET'])
@website.route('/patientphones/<int:patPhoneID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_patient_phone(patPhoneID=None):
    try:
        if patPhoneID is None:
            return jsonify(PatientPhones=[i.dict() for i in query.get_patient_phones()])
        else:
            patientPhone = query.get_patient_phone(patPhoneID)
            if patientPhone is not None:
                form = {}
                form["states"] = query.get_states()
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                form["phoneTypes"] = query.get_phone_types()
                return render_template('patient_phone_form.html', form=form, patientPhone=patientPhone)
            else:
                return item_not_found("PatPhoneID {} not found".format(patPhoneID))
    except Exception as e:
        return internal_error(e)


@website.route('/patientphones/<int:patPhoneID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_patient_phone(patPhoneID):
    try:
        patientPhone = query.get_patient_phone(patPhoneID)
        if patientPhone is not None:
            form = forms.PatientPhoneForm(request.form)
            if form.validate():
                if int(form.versionID.data) == patientPhone.versionID:
                    patientPhone.contactInfoSourceID = form.contactInfoSourceID.data
                    patientPhone.participantID = form.participantID.data
                    patientPhone.contactInfoStatusID = form.contactInfoStatusID.data
                    patientPhone.phoneTypeID = form.phoneTypeID.data
                    patientPhone.phoneNumber = form.phoneNumber.data
                    patientPhone.phoneStatusDate = form.phoneStatusDate.data
                    query.commit()
                    flash("Updated Patient Phone")
                    return redirect_back('patientphones/{}/'.format(patPhoneID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PatPhoneID {} not found".format(patPhoneID))
    except Exception as e:
        return internal_error(e)


@website.route('/patientphones/', methods=['POST'])
@website.route('/patientphones/<int:patPhoneID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_patient_phone(patPhoneID=None):
    try:
        if patPhoneID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_patient_phone(patPhoneID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_patient_phone(patPhoneID)
            else:
                return invalid_method()
        else:
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
                flash("Created Patient Phone")
                return redirect_back('patientphones/{}/'.format(patientPhone.participantID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/patientphones/<int:patPhoneID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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
# @website.route('/patientprojectstatuses/', methods = ['GET'])
@website.route('/patientprojectstatuses/<int:patientProjectStatusID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_patient_project_status(patientProjectStatusID=None):
    try:
        if patientProjectStatusID is None:
            return jsonify(PatientProjectStatuses=[i.dict() for i in query.get_patient_project_statuses()])
        else:
            patientProjectStatus = query.get_patient_project_status(patientProjectStatusID)
            if patientProjectStatus is not None:
                form = {}
                form["projectPatients"] = query.get_project_patients()
                form["patientProjectStatusTypes"] = query.get_patient_project_status_types()
                form["staffs"]=query.get_staffs()
                return render_template("patient_project_status_form.html", form=form,
                                       patientProjectStatus=patientProjectStatus)
            else:
                return item_not_found("PatientProjectStatusID {} not found".format(patientProjectStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/patientprojectstatuses/<int:patientProjectStatusID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_patient_project_status(patientProjectStatusID):
    try:
        patientProjectStatus = query.get_patient_project_status(patientProjectStatusID)
        if patientProjectStatus is not None:
            form = forms.PatientProjectStatusForm(request.form)
            if form.validate():
                if int(form.versionID.data) == patientProjectStatus.versionID:
                    patientProjectStatus.patientProjectStatusTypeID = form.patientProjectStatusTypeID.data
                    patientProjectStatus.participantID = form.participantID.data
                    patientProjectStatus.statusDate = form.statusDate.data
                    patientProjectStatus.staffID = form.staffID.data
                    query.commit()
                    flash("Updated Patient Project Status")
                    return redirect_back("patientprojectstatuses/{}/".format(patientProjectStatusID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PatientProjectStatusID {} not found".format(patientProjectStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/patientprojectstatuses/', methods=['POST'])
@website.route('/patientprojectstatuses/<int:patientProjectStatusID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager','Contact Staff'])
def create_patient_project_status(patientProjectStatusID=None):
    try:
        if patientProjectStatusID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_patient_project_status(patientProjectStatusID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_patient_project_status(patientProjectStatusID)
            else:
                return invalid_method()
        else:
            form = forms.PatientProjectStatusForm(request.form)
            if form.validate():
                patientProjectStatus = models.PatientProjectStatus(
                    patientProjectStatusTypeID=form.patientProjectStatusTypeID.data,
                    participantID=form.participantID.data,
                    statusDate = form.statusDate.data,
                    staffID = form.staffID.data
                )
                query.add(patientProjectStatus)
                flash("Created Patient Project Status")
                return redirect_back("patientprojectstatuses/{}/".format(patientProjectStatus.patientProjectStatusID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/patientprojectstatuses/<int:patientProjectStatusID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
@website.route('/patientprojectstatustypes/', methods=['GET'])
@website.route('/patientprojectstatustypes/<int:patientProjectStatusTypeID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_patient_project_status_type(patientProjectStatusTypeID=None):
    try:
        if patientProjectStatusTypeID is None:
            form = {
                "patientProjectStatuses": query.get_patient_project_status_types(),
                "add": True
            }
            return render_template("patient_project_status_types.html", form=form)
        else:
            patientProjectStatusType = query.get_patient_project_status_type(patientProjectStatusTypeID)
            if patientProjectStatusType is not None:
                form = {
                    "patientProjectStatuses": [patientProjectStatusType],
                    "add": False
                }
                return render_template("patient_project_status_types.html", form=form)
            else:
                return item_not_found("PatientProjectStatusTypeID {} not found".format(patientProjectStatusTypeID))
    except Exception as e:
        return internal_error(e)


@website.route('/patientprojectstatustypes/<int:patientProjectStatusTypeID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_patient_project_status_type(patientProjectStatusTypeID):
    try:
        patientProjectStatusType = query.get_patient_project_status_type(patientProjectStatusTypeID)
        if patientProjectStatusType is not None:
            form = forms.PatientProjectStatusLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == patientProjectStatusType.versionID:
                    patientProjectStatusType.statusDescription = form.statusDescription.data
                    query.commit()
                    flash("Updated Patient Project Status Type")
                    return redirect_back('patientprojectstatustypes/{}/'.format(patientProjectStatusTypeID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PatientProjectStatusTypeID {} not found".format(patientProjectStatusTypeID))
    except Exception as e:
        return internal_error(e)


@website.route('/patientprojectstatustypes/', methods=['POST'])
@website.route('/patientprojectstatustypes/<int:patientProjectStatusTypeID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_patient_project_status_type(patientProjectStatusTypeID=None):
    try:
        if patientProjectStatusTypeID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_patient_project_status_type(patientProjectStatusTypeID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_patient_project_status_type(patientProjectStatusTypeID)
            else:
                return invalid_method()
        else:
            form = forms.PatientProjectStatusLUTForm(request.form)
            if form.validate():
                patientProjectStatusType = models.PatientProjectStatusLUT(
                    statusDescription=form.statusDescription.data
                )
                query.add(patientProjectStatusType)
                flash("Created Patient Project Status Type")
                return redirect_back(
                    'patientprojectstatustypes/{}/'.format(patientProjectStatusType.patientProjectStatusTypeID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/patientprojectstatustypes/<int:patientProjectStatusTypeID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
@website.route('/phasestatuses/', methods=['GET'])
@website.route('/phasestatuses/<int:logPhaseID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_phase_status(logPhaseID=None):
    try:
        if logPhaseID is None:
            form = {
                "phaseStatuses": query.get_phase_statuses(),
                "add": True
            }
            return render_template("phase_statuses.html", form=form)
        else:
            phaseStatus = query.get_phase_status(logPhaseID)
            if phaseStatus is not None:
                form = {
                    "phaseStatuses": [phaseStatus],
                    "add": False
                }
                return render_template("phase_statuses.html", form=form)
            else:
                return item_not_found("LogPhaseID {} not found".format(logPhaseID))
    except Exception as e:
        return internal_error(e)


@website.route('/phasestatuses/<int:logPhaseID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_phase_status(logPhaseID):
    try:
        phaseStatus = query.get_phase_status(logPhaseID)
        if phaseStatus is not None:
            form = forms.PhaseStatusForm(request.form)
            if form.validate():
                if int(form.versionID.data) == phaseStatus.versionID:
                    phaseStatus.phaseStatus = form.phaseStatus.data
                    phaseStatus.phaseDescription = form.phaseDescription.data
                    query.commit()
                    flash("Updated Phase Status")
                    return redirect_back('phasestatuses/{}/'.format(logPhaseID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("LogPhaseID {} not found".format(logPhaseID))
    except Exception as e:
        return internal_error(e)


@website.route('/phasestatuses/', methods=['POST'])
@website.route('/phasestatuses/<int:logPhaseID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_phase_status(logPhaseID=None):
    try:
        if logPhaseID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_phase_status(logPhaseID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_phase_status(logPhaseID)
            else:
                return invalid_method()
        else:
            form = forms.PhaseStatusForm(request.form)
            if form.validate():
                phaseStatus = models.PhaseStatus(
                    phaseStatus=form.phaseStatus.data,
                    phaseDescription=form.phaseDescription.data
                )
                query.add(phaseStatus)
                flash("Created Phase Status")
                return redirect_back('patientprojectstatustypes/{}/'.format(phaseStatus.logPhaseID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/phasestatuses/<int:logPhaseID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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
@website.route('/phonetypes/', methods=['GET'])
@website.route('/phonetypes/<int:phoneTypeID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_phone_type(phoneTypeID=None):
    try:
        if phoneTypeID is None:
            form = {
                "phoneTypes": query.get_phone_types(),
                "add": True
            }
            return render_template("phone_types.html", form=form)
        else:
            phoneType = query.get_phone_type(phoneTypeID)
            if phoneType is not None:
                form = {
                    "phoneTypes": [phoneType],
                    "add": False
                }
                return render_template("phone_types.html", form=form)
            else:
                return item_not_found("PhoneTypeID {} not found".format(phoneTypeID))
    except Exception as e:
        return internal_error(e)


@website.route('/phonetypes/<int:phoneTypeID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_phone_type(phoneTypeID):
    try:
        phoneType = query.get_phone_type(phoneTypeID)
        if phoneType is not None:
            form = forms.PhoneTypeForm(request.form)
            if form.validate():
                if int(form.versionID.data) == phoneType.versionID:
                    phoneType.phoneType = form.phoneType.data
                    query.commit()
                    flash("Updated Phone Type")
                    return redirect_back('phonetypes/{}/'.format(phoneTypeID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhoneTypeID {} not found".format(phoneTypeID))
    except Exception as e:
        return internal_error(e)


@website.route('/phonetypes/', methods=['POST'])
@website.route('/phonetypes/<int:phoneTypeID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_phone_type(phoneTypeID=None):
    try:
        if phoneTypeID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_phone_type(phoneTypeID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_phone_type(phoneTypeID)
            else:
                return invalid_method()
        else:
            form = forms.PhoneTypeForm(request.form)
            if form.validate():
                phoneType = models.PhoneTypeLUT(
                    phoneType=form.phoneType.data
                )
                query.add(phoneType)
                flash("Created Phone Type")
                return redirect_back('phonetypes/{}/'.format(phoneType.phoneTypeID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/phonetypes/<int:phoneTypeID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
@website.route('/physicians/', methods=['GET'])
@website.route('/physicians/<int:physicianID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_physician(physicianID=None):
    try:
        if physicianID is None:
            form = {}
            firstName = None
            lastName = None
            specialty = None
            physicianStatusID = None
            form["queryParams"] = {}
            if "action" in request.args:
                if request.args["action"].lower() == "clear":
                    firstName = lastName = specialty = physicianStatusID = None
                else:
                    if "firstName" in request.args:
                        firstName = value_or_none(request.args["firstName"])
                        form["queryParams"]["firstName"] = request.args["firstName"]
                    if "lastName" in request.args:
                        lastName = value_or_none(request.args["lastName"])
                        form["queryParams"]["lastName"] = request.args["lastName"]
                    if "specialty" in request.args:
                        specialty = value_or_none(request.args["specialty"])
                        form["queryParams"]["specialty"] = request.args["specialty"]
                    if "physicianStatusID" in request.args:
                        physicianStatusID = value_or_none(request.args["physicianStatusID"])
                        form["queryParams"]["physicianStatusID"] = request.args["physicianStatusID"]

            physicians = query.query_physicians(firstName=firstName,
                                                lastName=lastName,
                                                specialty=specialty,
                                                physicianStatusID=physicianStatusID)
            form["physicianStatuses"] = query.get_physician_statuses()
            return render_template("physician_table.html", form=form, physicians=physicians)
        else:
            physician = query.get_physician(physicianID)
            if physician is not None:
                form = {}
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                form["states"] = query.get_states()
                form["phoneTypes"] = query.get_phone_types()
                form["physicians"] = query.get_physicians()
                form["facilities"] = query.get_facilities()
                form["physicianStatuses"] = query.get_physician_statuses()
                return render_template("physician_form.html", form=form, physician=physician)
            else:
                return item_not_found("PhysicianID {} not found".format(physicianID))
    except Exception as e:
        return internal_error(e)


@website.route('/physicians/<int:physicianID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_physician(physicianID):
    try:
        physician = query.get_physician(physicianID)
        if physician is not None:
            form = forms.PhysicianForm(request.form)
            if form.validate():
                if int(form.versionID.data) == physician.versionID:
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
                    physician.displayID=form.displayID.data
                    query.commit()
                    flash("Updated Physician")
                    return redirect_back("physicians/{}/".format(physicianID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysicianID {} not found".format(physicianID))
    except Exception as e:
        return internal_error(e)


@website.route('/physicians/', methods=['POST'])
@website.route('/physicians/<int:physicianID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_physician(physicianID=None):
    try:
        if physicianID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_physician(physicianID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_physician(physicianID)
            else:
                return invalid_method()
        else:
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
                    displayID = form.displayID.data
                )
                query.add(physician)
                flash("Created Physician")
                return redirect_back("physicians/{}/".format(physician.physicianID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/physicians/<int:physicianID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/physicianaddresses/', methods=['GET'])
@website.route('/physicianaddresses/<int:physicianAddressID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_physician_address(physicianAddressID=None):
    try:
        if physicianAddressID is None:
            return jsonify(PhysicianAddresses=[i.dict() for i in query.get_physician_addresses()])
        else:
            physicianAddress = query.get_physician_address(physicianAddressID)
            if physicianAddress is not None:
                form = {}
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["physicians"] = query.get_physicians()
                form["states"] = query.get_states()
                return render_template("physician_address_form.html", form=form, physicianAddress=physicianAddress)
            else:
                return item_not_found("PhysicianAddressID {} not found".format(physicianAddressID))
    except Exception as e:
        return internal_error(e)


@website.route('/physicianaddresses/<int:physicianAddressID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_physician_address(physicianAddressID):
    try:
        physicianAddress = query.get_physician_address(physicianAddressID)
        if physicianAddress is not None:
            form = forms.PhysicianAddressForm(request.form)
            if form.validate():
                if int(form.versionID.data) == physicianAddress.versionID:
                    physicianAddress.contactInfoSourceID = form.contactInfoSourceID.data
                    physicianAddress.physicianID = form.physicianID.data
                    physicianAddress.contactInfoStatusID = form.contactInfoStatusID.data
                    physicianAddress.street = form.street.data
                    physicianAddress.street2 = form.street2.data
                    physicianAddress.city = form.city.data
                    if form.stateID.data is not '':
                        physicianAddress.stateID = form.stateID.data
                    else:
                        physicianAddress.stateID = 'zz'
                    physicianAddress.zip = form.zip.data
                    physicianAddress.addressStatusDate = form.addressStatusDate.data
                    query.commit()
                    flash("Updated Physician Address")
                    return redirect_back("physicianaddresses/{}/".format(physicianAddressID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysicianAddressID {} not found".format(physicianAddressID))
    except Exception as e:
        return internal_error(e)


@website.route('/physicianaddresses/', methods=['POST'])
@website.route('/physicianaddresses/<int:physicianAddressID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_physician_address(physicianAddressID=None):
    try:
        if physicianAddressID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_physician_address(physicianAddressID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_physician_address(physicianAddressID)
            else:
                return invalid_method()
        else:
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
                flash("Created Physician Address")
                return redirect_back("physicianaddresses/{}/".format(physicianAddress.physicianAddressID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/physicianaddresses/<int:physicianAddressID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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
# @website.route('/physicianemails/', methods=['GET'])
@website.route('/physicianemails/<int:physicianEmailID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_physician_email(physicianEmailID=None):
    try:
        if physicianEmailID is None:
            return jsonify(PhysicianEmails=[i.dict() for i in query.get_physician_emails()])
        else:
            physicianEmail = query.get_physician_email(physicianEmailID)
            if physicianEmail is not None:
                form = {}
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["physicians"] = query.get_physicians()
                return render_template("physician_email_form.html", form=form, physicianEmail=physicianEmail)
            else:
                return item_not_found("PhysicianEmailID {} not found".format(physicianEmailID))
    except Exception as e:
        internal_error(e)


@website.route('/physicianemails/<int:physicianEmailID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_physician_email(physicianEmailID):
    try:
        physicianEmail = query.get_physician_email(physicianEmailID)
        if physicianEmail is not None:
            form = forms.PhysicianEmailForm(request.form)
            if form.validate():
                if int(form.versionID.data) == physicianEmail.versionID:
                    physicianEmail.contactInfoSourceID = form.contactInfoSourceID.data
                    physicianEmail.physicianID = form.physicianID.data
                    physicianEmail.contactInfoStatusID = form.contactInfoStatusID.data
                    physicianEmail.email = form.email.data
                    physicianEmail.emailStatusDate = form.emailStatusDate.data
                    query.commit()
                    flash("Updated Physician Email")
                    return redirect_back("physicianemails/{}/".format(physicianEmailID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysicianEmailID {} not found".format(physicianEmailID))
    except Exception as e:
        return internal_error(e)


@website.route('/physicianemails/', methods=['POST'])
@website.route('/physicianemails/<int:physicianEmailID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_physician_email(physicianEmailID=None):
    try:
        if physicianEmailID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_physician_email(physicianEmailID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_physician_email(physicianEmailID)
            else:
                return invalid_method()
        else:
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
                flash("Created Physician Email")
                return redirect_back("physicianemails/{}/".format(physicianEmail.physicianID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/physicianemails/<int:physicianEmailID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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
# @website.route('/physicianfacilities/', methods=['GET'])
@website.route('/physicianfacilities/<int:physFacilityID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_physician_facility(physFacilityID=None):
    try:
        if physFacilityID is None:
            return jsonify(PhysicianFacilities=[i.dict() for i in query.get_physician_facilities()])
        else:
            physicianFacility = query.get_physician_facility(physFacilityID)
            if physicianFacility is not None:
                form = {}
                form["facilities"] = query.get_facilities()
                form["physicians"] = query.get_physicians()
                return render_template("physician_facility_form.html", form=form, physicianFacility=physicianFacility)
            else:
                return item_not_found("PhysFacilityID {} not found".format(physFacilityID))
    except Exception as e:
        return internal_error(e)


@website.route('/physicianfacilities/<int:physFacilityID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_physician_facility(physFacilityID):
    try:
        physicianFacility = query.get_physician_facility(physFacilityID)
        if physicianFacility is not None:
            form = forms.PhysicianFacilityForm(request.form)
            if form.validate():
                if int(form.versionID.data) == physicianFacility.versionID:
                    physicianFacility.facilityID = form.facilityID.data
                    physicianFacility.physicianID = form.physicianID.data
                    physicianFacility.physFacilityStatusID = form.physFacilityStatusID.data
                    physicianFacility.physFacilityStatusDate = form.physFacilityStatusDate.data
                    query.commit()
                    flash("Updated Physician Facility Link")
                    return redirect_back("physicianfacilities/{}/".format(physFacilityID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysFacilityID {} not found".format(physFacilityID))
    except Exception as e:
        return internal_error(e)


@website.route('/physicianfacilities/', methods=['POST'])
@website.route('/physicianfacilities/<int:physFacilityID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_physician_facility(physFacilityID=None):
    try:
        if physFacilityID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_physician_facility(physFacilityID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_physician_facility(physFacilityID)
            else:
                return invalid_method()
        else:
            form = forms.PhysicianFacilityForm(request.form)
            if form.validate():
                physicianFacility = models.PhysicianFacility(
                    facilityID=form.facilityID.data,
                    physicianID=form.physicianID.data,
                    physFacilityStatusID=form.physFacilityStatusID.data,
                    physFacilityStatusDate=form.physFacilityStatusDate.data,
                )
                query.add(physicianFacility)
                flash("Created Physician Facility Link")
                return redirect_back("physicianfacilities/{}/".format(physicianFacility.physFacilityID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/physicianfacilities/<int:physFacilityID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/physicianphones/', methods=['GET'])
@website.route('/physicianphones/<int:physicianPhoneID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_physician_phone(physicianPhoneID=None):
    try:
        if physicianPhoneID is None:
            return jsonify(PhysicianPhones=[i.dict() for i in query.get_physician_phones()])
        else:
            physicianPhone = query.get_physician_phone(physicianPhoneID)
            if physicianPhone is not None:
                form = {}
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["physicians"] = query.get_physicians()
                form["phoneTypes"] = query.get_phone_types()
                return render_template("physician_phone_form.html", form=form, physicianPhone=physicianPhone)
            else:
                return item_not_found("PhysicianPhoneID {} not found".format(physicianPhoneID))
    except Exception as e:
        return internal_error(e)


@website.route('/physicianphones/<int:physicianPhoneID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_physician_phone(physicianPhoneID):
    try:
        physicianPhone = query.get_physician_phone(physicianPhoneID)
        if physicianPhone is not None:
            form = forms.PhysicianPhoneForm(request.form)
            if form.validate():
                if int(form.versionID.data) == physicianPhone.versionID:
                    physicianPhone.contactInfoSourceID = form.contactInfoSourceID.data
                    physicianPhone.physicianID = form.physicianID.data
                    physicianPhone.contactInfoStatusID = form.contactInfoStatusID.data
                    physicianPhone.phoneNumber = form.phoneNumber.data
                    physicianPhone.phoneTypeID = form.phoneTypeID.data
                    physicianPhone.phoneStatusDate = form.phoneStatusDate.data
                    query.commit()
                    flash("Updated Physician Phone")
                    return redirect_back("physicianphones/{}/".format(physicianPhoneID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysicianPhoneID {} not found".format(physicianPhoneID))
    except Exception as e:
        return internal_error(e)


@website.route('/physicianphones/', methods=['POST'])
@website.route('/physicianphones/<int:physicianPhoneID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_physician_phone(physicianPhoneID=None):
    try:
        if physicianPhoneID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_physician_phone(physicianPhoneID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_physician_phone(physicianPhoneID)
            else:
                return invalid_method()
        else:
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
                flash("Created Physician Phone")
                return redirect_back("physicianphones/{}/".format(physicianPhone.physicianPhoneID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/physicianphones/<int:physicianPhoneID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
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


@website.route('/physicianstatuses/', methods=['GET'])
@website.route('/physicianstatuses/<int:physicianStatusID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_physician_status(physicianStatusID=None):
    try:
        if physicianStatusID is None:
            form = {
                "physicianStatuses": query.get_physician_statuses(),
                "add": True
            }
            return render_template("physician_statuses.html", form=form)
        else:
            physicianStatus = query.get_physician_status(physicianStatusID)
            if physicianStatus is not None:
                form = {
                    "physicianStatuses": [physicianStatus],
                    "add": False
                }
                return render_template("physician_statuses.html", form=form)
            else:
                return item_not_found("PhysicianStatusID {} not found".format(physicianStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/physicianstatuses/<int:physicianStatusID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_physician_status(physicianStatusID):
    try:
        physicianStatus = query.get_physician_status(physicianStatusID)
        if physicianStatus is not None:
            form = forms.PhysicianStatusForm(request.form)
            if form.validate():
                if int(form.versionID.data) == physicianStatus.versionID:
                    physicianStatus.physicianStatus = form.physicianStatus.data
                    query.commit()
                    flash("Updated Physician Status")
                    return redirect_back('physicianstatuses/{}/'.format(physicianStatusID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysicianStatusID {} not found".format(physicianStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/physicianstatuses/', methods=['POST'])
@website.route('/physicianstatuses/<int:physicianStatusID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_physician_status(physicianStatusID=None):
    try:
        if physicianStatusID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_physician_status(physicianStatusID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_physician_status(physicianStatusID)
            else:
                return invalid_method()
        else:
            form = forms.PhysicianStatusForm(request.form)
            if form.validate():
                physicianStatus = models.PhysicianStatus(
                    physicianStatus=form.physicianStatus.data,
                )
                query.add(physicianStatus)
                flash("Created Physician Status")
                return redirect_back('physicianStatuses/{}/'.format(physicianStatus.physicianStatusID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/physicianstatuses/<int:physicianStatusID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/physiciantoctcs/', methods = ['GET'])
@website.route('/physiciantoctcs/<int:physicianCTCID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_physician_to_ctc(physicianCTCID=None):
    try:
        if physicianCTCID is None:
            return jsonify(PhysicianToCTCs=[i.dict() for i in query.get_physician_to_ctcs()])
        else:
            physicianToCTC = query.get_physician_to_ctc(physicianCTCID)
            if physicianToCTC is not None:
                form = {}
                form["physicians"] = query.get_physicians()
                form["ctcs"] = query.get_ctcs()
                return render_template("physician_to_ctc_form.html", form=form, physicianToCTC=physicianToCTC)
            else:
                return item_not_found("PhysicianCTCID {} not found".format(physicianCTCID))
    except Exception as e:
        return internal_error(e)


@website.route('/physiciantoctcs/<int:physicianCTCID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_physician_to_ctc(physicianCTCID):
    try:
        physicianToCTC = query.get_physician_to_ctc(physicianCTCID)
        if physicianToCTC is not None:
            form = forms.PhysicianToCTCForm(request.form)
            if form.validate():
                if int(form.versionID.data) == physicianToCTC.versionID:
                    physicianToCTC.physicianID = form.physicianID.data
                    physicianToCTC.ctcID = form.ctcID.data
                    query.commit()
                    flash("Updated Physician to CTC Link")
                    return redirect_back("physiciantoctcs/{}/".format(physicianCTCID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PhysicianCTCID {} not found".format(physicianCTCID))
    except Exception as e:
        return internal_error(e)


@website.route('/physiciantoctcs/', methods=['POST'])
@website.route('/physiciantoctcs/<int:physicianCTCID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_physician_to_ctc(physicianCTCID=None):
    try:
        if physicianCTCID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_physician_to_ctc(physicianCTCID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_physician_to_ctc(physicianCTCID)
            else:
                return invalid_method()
        else:
            form = forms.PhysicianToCTCForm(request.form)
            if form.validate():
                physicianToCTC = models.PhysicianToCTC(
                    physicianID=form.physicianID.data,
                    ctcID=form.ctcID.data
                )
                query.add(physicianToCTC)
                flash("Created Physician to CTC Link")
                return redirect_back("physiciantoctcs/{}/".format(physicianToCTC.physicianCTCID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/physiciantoctcs/<int:physicianCTCID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/preapplications/', methods = ['GET'])
@website.route('/preapplications/<int:preApplicationID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_pre_application(preApplicationID=None):
    try:
        if preApplicationID is None:
            return jsonify(PreApplications=[i.dict() for i in query.get_pre_applications()])
        else:
            preApplication = query.get_pre_application(preApplicationID)
            if preApplication is not None:
                form = {}
                form["projects"] = query.get_projects()
                form["institutions"] = query.get_institutions()
                return render_template("pre_application_form.html", form=form, preApplication=preApplication)
            else:
                return item_not_found("PreApplicationID {} not found".format(preApplicationID))
    except Exception as e:
        return internal_error(e)


@website.route('/preapplications/<int:preApplicationID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_pre_application(preApplicationID):
    try:
        preApplication = query.get_pre_application(preApplicationID)
        if preApplication is not None:
            form = forms.PreApplicationForm(request.form)
            if form.validate():
                if int(form.versionID.data) == preApplication.versionID:
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
                    flash("Updated Pre-Application")
                    return redirect_back("preapplications/{}/".format(preApplicationID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("PreApplicationID {} not found".format(preApplicationID))
    except Exception as e:
        return internal_error(e)


@website.route('/preapplications/', methods=['POST'])
@website.route('/preapplications/<int:preApplicationID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_pre_application(preApplicationID=None):
    try:
        if preApplicationID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_pre_application(preApplicationID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_pre_application(preApplicationID)
            else:
                return invalid_method()
        else:
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
                    irb0=form.irb0.data,
                    irb1=form.irb1.data,
                    irb2=form.irb2.data,
                    irb3=form.irb3.data,
                    irb4=form.irb4.data,
                    otherIrb=form.otherIrb.data,
                    updb=form.updb.data,
                    ptContact=form.ptContact.data,
                    startDate=form.startDate.data,
                    link=form.link.data,
                    deliveryDate=form.deliveryDate.data,
                    description=form.description.data
                )
                query.add(preApplication)
                flash("Created Pre-Application")
                return redirect_back("preapplications/{}/".format(preApplication.preApplicationID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/preapplications/<int:preApplicationID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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
@website.route('/createprojects/', methods=['GET'])
@authorization_required(roles=['Developer','Research Manager'])
def create_project_preapplication():
    form, projects = get_project(None,1)
    return render_template("project_table.html", form=form, projects=projects)

@website.route('/projects/', methods=['GET'])
@website.route('/projects/<int:projectID>/', methods=['GET'])
@website.route('/projects/<int:projectID>/<int:preApplication>', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_project(projectID=None,preApplication=None):
    try:
        if projectID is None:
            form = {}
            projectID = None
            shortTitle = None
            projectTypeID = None
            piLastName = None
            mostRecentProjectStatusTypeID = None
            form["queryParams"] = {}
            if "action" in request.args:
                if request.args["action"].lower() == "clear":
                    projectID = shortTitle = projectTypeID = piLastName = mostRecentProjectStatusTypeID =None
                else:
                    if "projectID" in request.args:
                        projectID = value_or_none(request.args["projectID"])
                        form["queryParams"]["projectID"] = request.args["projectID"]
                    if "shortTitle" in request.args:
                        shortTitle = value_or_none(request.args["shortTitle"])
                        form["queryParams"]["shortTitle"] = request.args["shortTitle"]
                    if "piLastName" in request.args:
                        piLastName = value_or_none(request.args["piLastName"])
                        form["queryParams"]["piLastName"] = request.args["piLastName"]
                    if "projectTypeID" in request.args:
                        projectTypeID = value_or_none(request.args["projectTypeID"])
                        form["queryParams"]["projectTypeID"] = request.args["projectTypeID"]
                    if "mostRecentProjectStatusTypeID" in request.args:
                        mostRecentProjectStatusTypeID = value_or_none(request.args["mostRecentProjectStatusTypeID"])
                        form["queryParams"]["mostRecentProjectStatusTypeID"] = request.args["mostRecentProjectStatusTypeID"]

            projects = query.query_projects(projectID=projectID,
                                            shortTitle=shortTitle,
                                            projectTypeID=projectTypeID,
                                            piLastName=piLastName,
                                            mostRecentProjectStatusTypeID=mostRecentProjectStatusTypeID)

            form["preApplication"] = preApplication
            form["projectTypes"] = query.get_project_types()
            form["projectStatusLUTs"] = query.get_project_status_luts()
            form["institutions"] = query.get_institutions()
            form["verifyDate"] = datetime.date(1,1,1);

            if preApplication == 1:
                projects = query.query_projects_in_preapplications()
                return form, projects
            return render_template("project_table.html", form=form, projects=projects)
        else:
            proj = ''
            if preApplication is None:
                proj = query.get_project(projectID)
            if proj is not None:
                form = {}
                if preApplication is None:
                    form["project"] = proj
                else:
                    form["project"] = query.get_pre_application(preApplication)
                form["projects"] = query.get_projects()
                form["irbHolders"] = query.get_irb_holders()
                form["projectTypes"] = query.get_project_types()
                if preApplication is None:
                    form["projectStatuses"] = proj.projectStatuses
                    form["preApplication"] = proj.preApplication
                form["staff"] = query.get_staffs()
                form["fundingSources"] = query.get_funding_sources()
                form["grantStatuses"] = query.get_grant_statuses()
                form["phaseStatuses"] = query.get_phase_statuses()
                form["logSubjects"] = query.get_log_subjects()
                form["projectStatusTypes"] = query.get_project_status_luts()
                form["reviewCommitteeStatuses"] = query.get_review_committee_statuses()
                form["reviewCommitteeLUTs"] = query.get_review_committee_luts()
                form["reportTypes"] = query.get_report_types()
                form["staffRoles"] = query.get_staff_roles()
                form["siteGroups"]=query.get_sites()
                form["institutions"] = query.get_institutions()
                form["preApplication"] = preApplication
                return render_template("project_form.html", form=form)
            else:
                return item_not_found("ProjectID {} not found".format(projectID))
    except Exception as e:
        return internal_error(e)


@website.route('/projects/<int:projectID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_project(projectID):
    try:
        proj = query.get_project(projectID)
        if proj is not None:
            form = forms.ProjectForm(request.form)
            if form.validate():
                if int(form.versionID.data) == proj.versionID:
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
                    proj.numberAbstractions=form.numberAbstractions.data
                    proj.sftpUsername=form.sftpUsername.data
                    proj.irbResearchManager=form.irbResearchManager.data
                    query.commit()
                    flash("Updated Project", 'message')
                    return redirect_back("projects/{}/".format(projectID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ProjectID {} not found".format(projectID))
    except Exception as e:
        return internal_error(e)


@website.route('/projects/', methods=['POST'])
@website.route('/projects/<int:projectID>/', methods=['POST'])
@website.route('/projects/<int:projectID>/<int:preApplication>', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_project(projectID=None,preApplication=None):
    try:
        if projectID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_project(projectID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_project(projectID)
            else:
                return invalid_method()
        if projectID is None or preApplication is not None:
            form = forms.ProjectForm(request.form)
            if preApplication is not None:
               form.dateAdded.data = datetime.datetime.now().date()
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
                    ongoingContact=form.ongoingContact.data,
                    activityStartDate=form.activityStartDate.data,
                    activityEndDate=form.activityEndDate.data,
                    numberAbstractions=form.numberAbstractions.data,
                    sftpUsername=form.sftpUsername.data,
                    irbResearchManager=form.irbResearchManager.data
                )
                query.add(proj)
                flash("Created Project")
                if preApplication is not None:
                    preApplications = query.get_pre_application(preApplication)
                    preApplications.projectID = proj.projectID
                    query.commit()
                    return redirect("/website/projects/{}/".format(proj.projectID))
                return redirect_back("projects/{}/".format(proj.projectID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/projects/<int:projectID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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

@website.route('/projectpatients/', methods=['GET'])
@website.route('/projectpatients/<int:participantID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_project_patient(participantID=None,project=0,patientProjectStatus=0):
    try:
        if participantID is None:
            form = {}
            firstName = None
            lastName = None
            batch = None
            siteGrpID = None
            projectID = None
            finalCodeID = None
            form["queryParams"] = {}
            if "action" in  request.args:
                if request.args["action"].lower() == "clear":
                    firstName = lastName = finalCodeID = batch = siteGrpID = projectID = None
                else:
                    if "firstName" in request.args:
                        firstName = value_or_none(request.args["firstName"])
                        form["queryParams"]["firstName"] = request.args["firstName"]
                    if "lastName" in request.args:
                        lastName = value_or_none(request.args["lastName"])
                        form["queryParams"]["lastName"] = request.args["lastName"]
                    if "finalCodeID" in request.args:
                        finalCodeID = value_or_none(request.args["finalCodeID"])
                        form["queryParams"]["finalCodeID"] = request.args["finalCodeID"]
                    if "batch" in request.args:
                        batch = value_or_none(request.args["batch"])
                        form["queryParams"]["batch"] = request.args["batch"]
                    if "siteGrpID" in request.args:
                        siteGrpID = value_or_none(request.args["siteGrpID"])
                        form["queryParams"]["siteGrpID"] = request.args["siteGrpID"]
                    if "projectID" in request.args:
                        projectID = value_or_none(request.args["projectID"])
                        form["queryParams"]["projectID"] = request.args["projectID"]
            if patientProjectStatus == 0:
                projectPatients = query.query_project_patients(firstName=firstName,
                                                           lastName=lastName,
                                                           finalCodeID=finalCodeID,
                                                           batch=batch,
                                                           siteGrpID=siteGrpID,
                                                           projectID=projectID)
            else:
                projectPatients = query.get_project_patient_worklist(projectID = project,patientProjectStatusTypeID=patientProjectStatus,firstName=firstName,
                                                           lastName=lastName,batch=batch,siteGrpID=siteGrpID)
            form["projects"] = query.get_projects()
            form["finalCodes"] = query.get_final_codes()
            form["siteGroups"] = query.get_sites()
            form["patientProjectStatus"] = patientProjectStatus
            form["staff"] = query.get_staffs()
            form["contactTypes"] = query.get_contact_types()
            if patientProjectStatus == 0:
                return render_template("project_patient_table.html", form=form, projectPatients=projectPatients)
            else:
                return form,projectPatients
        else:
            projectPatient = query.get_project_patient(participantID)
            if projectPatient is not None:
                form = {}
                form["projects"] = query.get_projects()
                form["staff"] = query.get_staffs()
                form["states"] = query.get_states()
                form["staff"] = query.get_staffs()
                form["ctcs"] = query.get_ctcs()
                form["contactTypes"] = query.get_contact_types()
                form["projectPatients"] = query.get_project_patients()
                form["informants"] = projectPatient.ctc.patient.informants
                form["informantPhones"] = []
                for informant in form["informants"]:
                    form["informantPhones"].extend(informant.informantPhones)
                form["facilities"] = [x.facility for x in projectPatient.ctc.ctcFacilities]
                form["facilityPhones"] = []
                for facility in form["facilities"]:
                    form["facilityPhones"].extend(facility.facilityPhones)
                form["physicians"] = [x.physician for x in projectPatient.ctc.physicianToCTC]
                form["physicianPhones"] = []
                for physician in form["physicians"]:
                    form["physicianPhones"].extend(physician.physicianPhones)
                form["patientPhones"] = projectPatient.ctc.patient.patientPhones
                form["phoneTypes"] = query.get_phone_types()
                form["contactInfoStatuses"] = query.get_contact_info_statuses()
                form["contactInfoSources"] = query.get_contact_info_sources()
                form["patientProjectStatusTypes"] = query.get_patient_project_status_types()
                form["tracingSources"] = query.get_tracing_sources()
                form["finalCodes"] = query.get_final_codes()
                form["abstractStatuses"] = query.get_abstract_statuses()
                form["vitalStatuses"] = query.get_vital_statues()
                form["externalstudycodes"] = query.get_external_study_codes()
                form["siteGroups"]=query.get_sites()
                if projectPatient.dayOfLastConsent == '':
                    form["dayOfLastConsent"]=''
                else:
                    form["dayOfLastConsent"]=projectPatient.dayOfLastConsent
                if projectPatient.monthOfLastConsent == '':
                    form["monthOfLastConsent"]=''
                else:
                    form["monthOfLastConsent"] = projectPatient.monthOfLastConsent
                if projectPatient.yearOfLastConsent == '':
                    form["yearOfLastConsent"] = ''
                else:
                    form["yearOfLastConsent"] = projectPatient.yearOfLastConsent

                return render_template("project_patient_form.html", form=form, projectPatient=projectPatient)
            else:
                return item_not_found("ParticipantID {} not found".format(participantID))
    except Exception as e:
        return internal_error(e)


@website.route('/projectpatients/<int:participantID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_project_patient(participantID):
    try:
        projectPatient = query.get_project_patient(participantID)
        if projectPatient is not None:
            form = forms.ProjectPatientForm(request.form)
            if form.validate():
                if int(form.versionID.data) == projectPatient.versionID:
                    projectPatient.projectID = form.projectID.data
                    projectPatient.ctcID = form.ctcID.data
                    projectPatient.finalCodeID = form.finalCodeID.data
                    projectPatient.finalCodeDate = form.finalCodeDate.data
                    projectPatient.consentSigned = form.consentSigned.data
                    projectPatient.enrollmentDate = form.enrollmentDate.data
                    projectPatient.dateCoordSigned = form.dateCoordSigned.data
                    projectPatient.externalID = form.externalID.data
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
                    projectPatient.surveyReturned = form.surveyReturned.data
                    projectPatient.surveyToResearcher = form.surveyToResearcher.data
                    projectPatient.surveyToResearcherStaffID = form.surveyToResearcherStaffID.data
                    projectPatient.qualityControl = form.qualityControl.data
                    projectPatient.vitalStatusID = form.vitalStatusID.data
                    query.commit()
                    flash("Updated Project Patient")
                    return redirect_back("projectpatients/{}/".format(participantID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ParticipantID {} not found".format(participantID))
    except Exception as e:
        return internal_error(e)


@website.route('/projectpatients/', methods=['POST'])
@website.route('/projectpatients/<int:participantID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_project_patient(participantID=None):
    try:
        if participantID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_project_patient(participantID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_project_patient(participantID)
            else:
                return invalid_method()
        else:
            form = forms.ProjectPatientForm(request.form)
            if form.validate():
                projectPatient = models.ProjectPatient(
                    projectID=form.projectID.data,
                    ctcID=form.ctcID.data,
                    consentSigned = form.consentSigned.data,
                    finalCodeID=form.finalCodeID.data,
                    finalCodeDate=form.finalCodeDate.data,
                    enrollmentDate=form.enrollmentDate.data,
                    dateCoordSigned=form.dateCoordSigned.data,
                    externalID = form.externalID.data,
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
                    medRecordReleaseSigned=form.medRecordReleaseSigned.data,
                    medRecordReleaseLink=form.medRecordReleaseLink.data,
                    medRecordReleaseStaffID=form.medRecordReleaseStaffID.data,
                    medRecordReleaseDate=form.medRecordReleaseDate.data,
                    surveyReturned = form.surveyReturned.data,
                    surveyToResearcher=form.surveyToResearcher.data,
                    surveyToResearcherStaffID=form.surveyToResearcherStaffID.data,
                    qualityControl=form.qualityControl.data,
                    vitalStatusID=form.vitalStatusID.data
                )
                query.add(projectPatient)
                flash("Created Project Patient")
                return redirect_back("projectPatients/{}/".format(projectPatient.participantID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/projectpatients/<int:participantID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/projectstaff/', methods = ['GET'])
@website.route('/projectstaff/<int:projectStaffID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_project_staff(projectStaffID=None):
    try:
        if projectStaffID is None:
            return jsonify(ProjectStaff=[i.dict() for i in query.get_project_staffs()])
        else:
            projectStaff = query.get_project_staff(projectStaffID)
            if projectStaff is not None:
                form = {}
                form["staff"] = query.get_staffs()
                form["projects"] = query.get_projects()
                form["staffRoles"] = query.get_staff_roles()
                return render_template("project_staff_form.html", form=form, projectStaff=projectStaff)
            else:
                return item_not_found("ProjectStaffID {} not found".format(projectStaffID))
    except Exception as e:
        internal_error(e)


@website.route('/projectstaff/<int:projectStaffID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_project_staff(projectStaffID):
    try:
        projectStaff = query.get_project_staff(projectStaffID)
        if projectStaff is not None:
            form = forms.ProjectStaffForm(request.form)
            if form.validate():
                if int(form.versionID.data) == projectStaff.versionID:
                    projectStaff.staffRoleID = form.staffRoleID.data
                    projectStaff.projectID = form.projectID.data
                    projectStaff.staffID = form.staffID.data
                    projectStaff.datePledge = form.datePledge.data
                    projectStaff.dateRevoked = form.dateRevoked.data
                    projectStaff.contactID = form.contactID.data
                    projectStaff.inactive = form.inactive.data
                    projectStaff.primaryPI = form.primaryPI.data
                    query.commit()
                    flash("Updated Project-Staff Link")
                    return redirect_back("projectstaff/{}/".format(projectStaffID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ProjectStaffID {} not found".format(projectStaffID))
    except Exception as e:
        return internal_error(e)


@website.route('/projectstaff/', methods=['POST'])
@website.route('/projectstaff/<int:projectStaffID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_project_staff(projectStaffID=None):
    try:
        if projectStaffID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_project_staff(projectStaffID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_project_staff(projectStaffID)
            else:
                return invalid_method()
        else:
            form = forms.ProjectStaffForm(request.form)
            if form.validate():
                projectStaff = models.ProjectStaff(
                    staffRoleID=form.staffRoleID.data,
                    projectID=form.projectID.data,
                    staffID=form.staffID.data,
                    datePledge=form.datePledge.data,
                    dateRevoked=form.dateRevoked.data,
                    contactID=form.contactID.data,
                    inactive=form.inactive.data,
                    primaryPI=form.primaryPI.data
                )
                query.add(projectStaff)
                flash("Created Project-Staff Link")
                return redirect_back("projectstaff/{}/".format(projectStaff.projectStaffID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/projectstaff/<int:projectStaffID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/projectstatuses/', methods = ['GET'])
@website.route('/projectstatuses/<int:projectStatusID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_project_status(projectStatusID=None):
    try:
        if projectStatusID is None:
            return jsonify(ProjectStatuses=[i.dict() for i in query.get_project_statuses()])
        else:
            projectStatus = query.get_project_status(projectStatusID)
            if projectStatus is not None:
                form = {}
                form["staff"] = query.get_staffs()
                form["projectStatusTypes"] = query.get_project_status_luts()
                form["projects"] = query.get_projects()
                return render_template("project_status_form.html", form=form, projectStatus=projectStatus)
            else:
                return item_not_found("ProjectStatusID {} not found".format(projectStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/projectstatuses/<int:projectStatusID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_project_status(projectStatusID):
    try:
        projectStatus = query.get_project_status(projectStatusID)
        if projectStatus is not None:
            form = forms.ProjectStatusForm(request.form)
            if form.validate():
                if int(form.versionID.data) == projectStatus.versionID:
                    projectStatus.projectStatusTypeID = form.projectStatusTypeID.data
                    projectStatus.projectID = form.projectID.data
                    projectStatus.staffID = form.staffID.data
                    projectStatus.statusDate = form.statusDate.data
                    projectStatus.statusNotes = form.statusNotes.data
                    query.commit()
                    flash("Updated Project Status")
                    return redirect_back('projectstatuses/{}/'.format(projectStatus.projectStatusID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ProjectStatusID {} not found".format(projectStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/projectstatuses/', methods=['POST'])
@website.route('/projectstatuses/<int:projectStatusID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_project_status(projectStatusID=None):
    try:
        if projectStatusID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_project_status(projectStatusID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_project_status(projectStatusID)
            else:
                return invalid_method()
        else:
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
                flash("Created Project Status")
                return redirect_back('projectstatuses/{}/'.format(projectStatusID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/projectstatuses/<int:projectStatusID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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
@website.route('/projectstatustypes/', methods=['GET'])
@website.route('/projectstatustypes/<int:projectStatusTypeID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_project_status_lut(projectStatusTypeID=None):
    try:
        if projectStatusTypeID is None:
            form = {
                "projectStatusTypes": query.get_project_status_luts(),
                "add": True
            }
            return render_template("project_status_types.html", form=form)
        else:
            projectStatusType = query.get_project_status_lut(projectStatusTypeID)
            if projectStatusType is not None:
                form = {
                    "projectStatusTypes": [projectStatusType],
                    "add": False
                }
                return render_template("project_status_types.html", form=form)
            else:
                return item_not_found("ProjectStatusTypeID {} not found".format(projectStatusTypeID))
    except Exception as e:
        return internal_error(e)


@website.route('/projectstatustypes/<int:projectStatusTypeID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_project_status_lut(projectStatusTypeID):
    try:
        projectStatusType = query.get_project_status_lut(projectStatusTypeID)
        if projectStatusType is not None:
            form = forms.ProjectStatusLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == projectStatusType.versionID:
                    projectStatusType.projectStatus = form.projectStatus.data
                    projectStatusType.projectStatusDefinition = form.projectStatusDefinition.data
                    query.commit()
                    flash("Updated Project Status Type")
                    return redirect_back('projectstatustypes/{}/'.format(projectStatusTypeID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ProjectStatusTypeID {} not found".format(projectStatusTypeID))
    except Exception as e:
        return internal_error(e)


@website.route('/projectstatustypes/', methods=['POST'])
@website.route('/projectstatustypes/<int:projectStatusTypeID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_project_status_lut(projectStatusTypeID=None):
    try:
        if projectStatusTypeID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_project_status_lut(projectStatusTypeID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_project_status(projectStatusTypeID)
            else:
                return invalid_method()
        else:
            form = forms.ProjectStatusLUTForm(request.form)
            if form.validate():
                projectStatusType = models.ProjectStatusLUT(
                    projectStatus=form.projectStatus.data,
                    projectStatusDefinition=form.projectStatusDefinition.data
                )
                query.add(projectStatusType)
                flash("Created Project Status Type")
                return redirect_back('patientprojectstatustypes/{}/'.format(projectStatusType.projectStatusTypeID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/projectstatustypes/<int:projectStatusTypeID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
@website.route('/projecttypes/', methods=['GET'])
@website.route('/projecttypes/<int:projectTypeID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_project_type(projectTypeID=None):
    try:
        if projectTypeID is None:
            form = {
                "projectTypes": query.get_project_types(),
                "add": True
            }
            return render_template("project_types.html", form=form)
        else:
            projectType = query.get_project_type(projectTypeID)
            if projectType is not None:
                form = {
                    "projectTypes": [projectType],
                    "add": False
                }
                return render_template("project_types.html", form=form)
            else:
                return item_not_found("ProjectTypeID {} not found".format(projectTypeID))
    except Exception as e:
        return internal_error(e)


@website.route('/projecttypes/<int:projectTypeID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_project_type(projectTypeID):
    try:
        projectType = query.get_project_type(projectTypeID)
        if projectType is not None:
            form = forms.ProjectTypeForm(request.form)
            if form.validate():
                if int(form.versionID.data) == projectType.versionID:
                    projectType.projectType = form.projectType.data
                    projectType.projectTypeDefinition = form.projectTypeDefinition.data
                    query.commit()
                    flash("Updated Project Type")
                    return redirect_back('projecttypes/{}/'.format(projectTypeID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ProjectTypeID {} not found".format(projectTypeID))
    except Exception as e:
        return internal_error(e)


@website.route('/projecttypes/', methods=['POST'])
@website.route('/projecttypes/<int:projectTypeID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_project_type(projectTypeID=None):
    try:
        if projectTypeID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_project_type(projectTypeID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_project_type(projectTypeID)
            else:
                return invalid_method()
        else:
            form = forms.ProjectTypeForm(request.form)
            if form.validate():
                projectType = models.ProjectType(
                    projectType=form.projectType.data,
                    projectTypeDefinition=form.projectTypeDefinition.data
                )
                query.add(projectType)
                flash("Created Project Type")
                return redirect_back('projecttypes/{}/'.format(projectType.projectTypeID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/projecttypes/<int:projectTypeID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
@website.route('/reviewcommitteestatuses/', methods=['GET'])
@website.route('/reviewcommitteestatuses/<int:reviewCommitteeStatusID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_rc_status_list(reviewCommitteeStatusID=None):
    try:
        if reviewCommitteeStatusID is None:
            form = {
                "reviewCommitteeStatuses": query.get_review_committee_statuses(),
                "add": True
            }
            return render_template("review_committee_statuses.html", form=form)
        else:
            rcStatus = query.get_review_committee_status(reviewCommitteeStatusID)
            if rcStatus is not None:
                form = {
                    "reviewCommitteeStatuses": [rcStatus],
                    "add": False
                }
                return render_template("review_committee_statuses.html", form=form)
            else:
                return item_not_found("ReviewCommitteeStatusID {} not found".format(reviewCommitteeStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/reviewcommitteestatuses/<int:reviewCommitteeStatusID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_rc_status_list(reviewCommitteeStatusID):
    try:
        rcStatus = query.get_review_committee_status(reviewCommitteeStatusID)
        if rcStatus is not None:
            form = forms.ReviewCommitteeStatusLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == rcStatus.versionID:
                    rcStatus.reviewCommitteeStatus = form.reviewCommitteeStatus.data
                    rcStatus.reviewCommitteeStatusDefinition = form.reviewCommitteeStatusDefinition.data
                    query.commit()
                    flash("Updated Review Committee Status")
                    return redirect_back('reviewcommitteestatuses/{}/'.format(reviewCommitteeStatusID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ReviewCommitteeStatusID {} not found".format(reviewCommitteeStatusID))
    except Exception as e:
        return internal_error(e)


@website.route('/reviewcommitteestatuses/', methods=['POST'])
@website.route('/reviewcommitteestatuses/<int:reviewCommitteeStatusID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_rc_status_list(reviewCommitteeStatusID=None):
    try:
        if reviewCommitteeStatusID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_rc_status_list(reviewCommitteeStatusID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_rc_status_list(reviewCommitteeStatusID)
            else:
                return invalid_method()
        else:
            form = forms.ReviewCommitteeStatusLUTForm(request.form)
            if form.validate():
                rcStatus = models.ReviewCommitteeStatusLUT(
                    reviewCommitteeStatus=form.reviewCommitteeStatus.data,
                    reviewCommitteeStatusDefinition=form.reviewCommitteeStatusDefinition.data
                )
                query.add(rcStatus)
                flash("Created Review Committee Status")
                return redirect_back('reviewcommitteestatuses/{}/'.format(rcStatus.reviewCommitteeStatusID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/reviewcommitteestatuses/<int:reviewCommitteeStatusID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/reviewcommittees/', methods = ['GET'])
@website.route('/reviewcommittees/<int:reviewCommitteeID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_review_committee(reviewCommitteeID=None):
    try:
        if reviewCommitteeID is None:
            return jsonify(reviewCommittees=[i.dict() for i in query.get_review_committees()])
        else:
            reviewCommittee = query.get_review_committee(reviewCommitteeID)
            if reviewCommittee is not None:
                form = {}
                form["projects"] = query.get_projects()
                form["reviewCommitteeStatuses"] = query.get_review_committee_statuses()
                form["reviewCommitteeLUTs"] = query.get_review_committee_luts()
                return render_template("review_committee_form.html", form=form, reviewCommittee=reviewCommittee)
            else:
                return item_not_found("ReviewCommitteeID {} not found".format(reviewCommitteeID))
    except Exception as e:
        return internal_error(e)


@website.route('/reviewcommittees/<int:reviewCommitteeID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_review_committee(reviewCommitteeID):
    try:
        rc = query.get_review_committee(reviewCommitteeID)
        if rc is not None:
            form = forms.ReviewCommitteeForm(request.form)
            if form.validate():
                if int(form.versionID.data) == rc.versionID:
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
                    flash("Updated Review Committee")
                    return redirect_back("reviewcommittees/{}/".format(reviewCommitteeID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ReviewCommitteeID {} not found".format(reviewCommitteeID))
    except Exception as e:
        return internal_error(e)


@website.route('/reviewcommittees/', methods=['POST'])
@website.route('/reviewcommittees/<int:reviewCommitteeID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_review_committee(reviewCommitteeID=None):
    try:
        if reviewCommitteeID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_review_committee(reviewCommitteeID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_review_committee(reviewCommitteeID)
            else:
                return invalid_method()
        else:
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
                flash("Created Review Committee")
                return redirect_back("reviewcommittees/{}/".format(rc.reviewCommitteeID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/reviewcommittees/<int:reviewCommitteeID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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
@website.route('/reviewcommitteelist/', methods=['GET'])
@website.route('/reviewcommitteelist/<int:reviewCommitteeID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_review_committee_list(reviewCommitteeID=None):
    try:
        if reviewCommitteeID is None:
            form = {
                "reviewCommittees": query.get_review_committee_luts(),
                "add": True
            }
            return render_template("review_committee_lists.html", form=form)
        else:
            review_committee_list = query.get_review_committee_lut(reviewCommitteeID)
            if review_committee_list is not None:
                form = {
                    "reviewCommittees": [review_committee_list],
                    "add": False
                }
                return render_template("review_committee_lists.html", form=form)
            else:
                return item_not_found("ReviewCommitteeID {} not found".format(reviewCommitteeID))
    except Exception as e:
        return internal_error(e)


@website.route('/reviewcommitteelist/<int:reviewCommitteeID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_review_committee_list(reviewCommitteeID):
    try:
        rcList = query.get_review_committee_lut(reviewCommitteeID)
        if rcList is not None:
            form = forms.ReviewCommitteeLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == rcList.versionID:
                    rcList.reviewCommittee = form.reviewCommittee.data
                    rcList.reviewCommitteeDescription = form.reviewCommitteeDescription.data
                    query.commit()
                    flash("Updated Review Committee")
                    return redirect_back('reviewcommitteelist/{}/'.format(reviewCommitteeID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ReviewCommitteeID {} not found".format(reviewCommitteeID))
    except Exception as e:
        return internal_error(e)


@website.route('/reviewcommitteelist/', methods=['POST'])
@website.route('/reviewcommitteelist/<int:reviewCommitteeID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_review_committee_list(reviewCommitteeID=None):
    try:
        if reviewCommitteeID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_review_committee_list(reviewCommitteeID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_review_committee_list(reviewCommitteeID)
            else:
                return invalid_method()
        else:
            form = forms.ReviewCommitteeLUTForm(request.form)
            if form.validate():
                reviewCommitteeList = models.ReviewCommitteeLUT(
                    reviewCommittee=form.reviewCommittee.data,
                    reviewCommitteeDescription=form.reviewCommitteeDescription.data
                )
                query.add(reviewCommitteeList)
                flash("Created Review Committee")
                return redirect_back('reviewcommitteelist/{}/'.format(reviewCommitteeID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/reviewcommitteelist/<int:reviewCommitteeID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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
# Run Sql Queries
##############################################################################
@website.route('/queries/', methods = ['GET'])
@website.route('/queries/<int:queryID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_sql_queries(queryID=None):
    try:
        if len(request.args) == 0:
            form = {}
            form['queries'] = query.get_queries()
            form["results"] = None
            return render_template("run_queries.html", form=form)
        else:
            type = query.get_query(request.args['reportTypes'])
            sqlQuery = type.query
            form = {}
            form['queries'] = query.get_queries()
            form['selectedQuery'] = int(request.args['reportTypes'])
            form["results"] = query.get_sql_query(sqlQuery)
            form["projectid"] =0
            for column in form['results'].cursor.description:
                regex = re.compile('[^a-zA-Z]')
                temp = regex.sub('',column[0])
                if "projectid" == temp.lower():
                    form["projectid"] = 1
                    form["projectid_name"] = column[0]
                    break

            return render_template("run_queries.html", form=form)

    except Exception as e:
        return internal_error(e)

@website.route('/downloadReport/', methods = ['GET'])
@website.route('/downloadReport/<int:queryID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_download(queryID=None):
    try:
        # Create the HttpResponse object with the appropriate CSV header.
        type = query.get_query(queryID)
        sqlQuery = type.query
        results = query.get_sql_query(sqlQuery)
        si = StringIO()
        writer = csv.writer(si)
        row = []
        for column in results.cursor.description:
             row.append(column[0])
        writer.writerow(row)
        for row in results:
            writer.writerow(row)
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename="+type.queryName+".csv"
        output.headers["Content-type"] = "text/csv"
        return output

    except Exception as e:
        return internal_error(e)

@website.route('/editqueries/', methods = ['GET'])
@website.route('/editqueries/<int:queryID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_edit_sql_queries(queryID=None):
    try:
        if queryID is None:
            form = {}
            form['queries'] = query.get_queries()
            form['query'] = {}
            form['selectedQuery'] = 0
            return render_template("edit_queries.html", form=form)
        else:
            form = {}
            form['queries'] = query.get_queries()
            form['query'] = query.get_query(queryID)
            form['selectedQuery'] = int(queryID)
            return render_template("edit_queries.html", form=form)

    except Exception as e:
        return internal_error(e)

@website.route('/queries/<int:queryID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_sql_query(queryID):
    try:
        sqlQuery = query.get_query(queryID)
        if queryID is not None:
            form = forms.SqlQueryForm(request.form)
            if int(form.versionID.data) == sqlQuery.versionID:
                sqlQuery.query = form.query.data
                sqlQuery.queryName = form.queryName.data
                sqlQuery.director = form.director.data
                sqlQuery.contactStaff = form.contactStaff.data
                sqlQuery.informaticsStaff = form.informaticsStaff.data
                sqlQuery.researchManager = form.researchManager.data
                query.add(sqlQuery)
                query.flush()
                query.commit()
                flash("Updated Report")
                return redirect_back('editqueries/{}/'.format(queryID))
            else:
                return out_of_date_error()
        else:
            return item_not_found("Report ID {} not found".format(queryID))
    except Exception as e:
        return internal_error(e)

@website.route('/editqueries/', methods=['POST'])
@website.route('/editqueries/<int:queryID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_sql_query(queryID=None):
    try:
        if request.form["action"].lower() == "editquery":
            return update_sql_query(queryID)
        if request.form["action"].lower() == "removequery":
            return delete_sql_query(queryID)
        else:
            form = forms.SqlQueryForm(request.form)
            sqlQuery = models.SqlQuery(
                    query=form.query.data,
                    queryName=form.queryName.data,
                    director=form.director.data,
                    contactStaff=form.contactStaff.data,
                    informaticsStaff=form.informaticsStaff.data,
                    researchManager=form.researchManager.data
                )
            query.add(sqlQuery)
            flash("Created New Report")
            return redirect_back('editqueries/')
    except Exception as e:
        return internal_error(e)

@website.route('/queries/<int:queryID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def delete_sql_query(queryID):
    try:
        sqlQuery = query.get_query(queryID)
        if sqlQuery is not None:
            deps = get_dependencies(sqlQuery)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(sqlQuery)
                flash("Deleted Report {}".format(queryID))
                return redirect_back('editqueries/')
        else:
            return item_not_found("ReportID {} not found".format(queryID))
    except Exception as e:
        return internal_error(e)


##############################################################################
   # Worklists
##############################################################################
@website.route('/tasks/', methods=['GET'])
@website.route('/tasks/<int:projectID>/<typeID>', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_tasks(projectID=None,typeID=None):
    try:
            patientprojectStatusID = 0
            type = typeID.split('-')[0].strip().lower()
            if type.find('edit')>=0:
                patientprojectStatusID = 2
            elif type.find('tracing')>=0:
                patientprojectStatusID = 3
            elif type.find('quality')>=0:
                patientprojectStatusID = 4
            elif type.find('mailing')>=0:
                patientprojectStatusID = 20+int(type[8])
            elif type.find('call')>=0:
                patientprojectStatusID = 50+int(type[12:])

            if patientprojectStatusID != 0:
                form, projectPatients = get_project_patient(None,projectID,patientprojectStatusID)

            if "action" in  request.args:
                if request.args["action"].lower() == "mailing":
                    sqlQuery = """SELECT p.patid, p.record_num,p.first_name, p.middle_name, p.last_name,concat(p.dob_month,'/',p.dob_day,'/',p.dob_year) as DOB,
pp.batch,pp.final_code,pp.vital_statusID,pa.street,pa.street2,pa.city,pa.stateID,pa.zip,pa.contactInfoStatusID,pa.address_status_date
FROM [ucr].[dbo].[Patient] p inner join [ucr].[dbo].[PatientAddress] pa on p.participantID = pa.participantID inner join [ucr].[dbo].[CTC] c on pa.participantID = c.participantID
inner join [ucr].[dbo].[ProjectPatient] pp on c.ctcID = pp.ctcID WHERE pa.contactInfoStatusID = 1 and pp.final_code =1  and """
                    temp = "("
                    for projectPatient in projectPatients:
                        temp = temp +"pp.participantID = "+str(projectPatient.participantID)+" or "
                    temp = temp[:-3]+")"
                    sqlQuery = sqlQuery + temp
                    results = query.get_sql_query(sqlQuery)
                    si = StringIO()
                    writer = csv.writer(si)
                    row = []
                    for column in results.cursor.description:
                        row.append(column[0])
                    writer.writerow(row)
                    for row in results:
                        writer.writerow(row)
                    output = make_response(si.getvalue())
                    output.headers["Content-Disposition"] = "attachment; filename=Patient Addresses-"+str(datetime.datetime.now())+".csv"
                    output.headers["Content-type"] = "text/csv"
                    return output
                if request.args["action"].lower() == "contact":
                    for projectPatient in projectPatients:
                        contact = models.Contact(
                            contactTypeLUTID=request.args["contactType"],
                            participantID=projectPatient.participantID,
                            staffID=request.args["staffID"],
                            contactDate=request.args["contactDate"]
                        )
                        query.add(contact)
                    flash("Created Contacts")

            return render_template("project_patient_table.html", form=form, projectPatients=projectPatients)
    except Exception as e:
        return internal_error(e)


@website.route('/worklist/', methods=['GET'])
@website.route('/worklist/<int:projectID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_worklist(projectID=None):
    try:
        if projectID is None:
          if len(request.args) == 0 :
            form = {}
            form['projects'] = query.get_projects_worklists()
            form['project'] = {}
            form['selectedProject'] = 0
            return render_template("worklist.html", form=form)
          else:
              form = {}
              form['projects'] = query.get_projects_worklists()
              form['project'] = query.get_query(request.args['projectID'])
              form['selectedProject'] = int(request.args['projectID'])
              PatientProjectStatuses = query.get_project_worklists(int(request.args['projectID']))
              map = {2:0,3:0,4:0,21:0,22:0,23:0,24:0,25:0,26:0,27:0,28:0,29:0,51:0,52:0,53:0,54:0,55:0,56:0,
                     57:0,58:0,59:0,60:0,61:0,62:0,63:0,64:0,65:0,66:0,67:0,68:0,69:0}
              for PatientProjectStatus in PatientProjectStatuses:
                  if PatientProjectStatus.patientProjectStatusTypeID in map:
                      map[PatientProjectStatus.patientProjectStatusTypeID] = map[PatientProjectStatus.patientProjectStatusTypeID]+1
              buttons = []
              for k,v in map.items():
                  if v != 0:
                    if k== 2:
                       buttons.append("Edit - "+str(v))
                    if k == 3:
                       buttons.append("Tracing - "+str(v))
                    if k == 4:
                       buttons.append("Quality Control - "+str(v))
                    if k>=21 and k<=29:
                       buttons.append("Mailing "+str(k-20)+" - "   +str(v))
                    if k>=51 and k<=69:
                       buttons.append("Call Window "+str(k-50)+" - "   +str(v))
              form['buttons'] = buttons
              return render_template("worklist.html", form=form)
        else:
            if projectID == 0:
                execute_workflow()
                flash("Refreshed Successfully")
                return redirect_back('worklist/')
    except Exception as e:
        return internal_error(e)

def execute_workflow():
    patientProjectStatuses = query.get_patient_project_statuses()
    for patientProjectStatus in patientProjectStatuses:
        patient = patientProjectStatus.projectPatient.ctc.patient
        currentAddress = False
        currentPhone = False
        for patientAddress in patient.patientAddresses:
            if patientAddress.contactInfoStatusID == 1:
                currentAddress = True
                break
        if currentAddress == False:
            for informant in patient.informants:
                for informantAddress in informant.informantAddresses:
                    if informantAddress.contactInfoStatusID == 1:
                        currentAddress = True
                        break
        for patientPhone in patient.patientPhones:
            if patientPhone.contactInfoStatusID == 1:
                currentPhone = True
                break
        if currentPhone == False:
            for informant in patient.informants:
                for informantPhone in informant.informantPhones:
                    if informantPhone.contactInfoStatusID == 1:
                        currentPhone = True
                        break
        compareTypeSet = set([100, 101, 102, 103, 104, 150, 151, 152, 153, 154, 300, 301, 302, 303, 304, 305, 306, 350,
                             351, 352, 353, 354, 355, 356, 380, 381, 382, 383, 384, 385, 386, 390, 391, 392, 393, 394,
                             395, 396])
        finalCode = patientProjectStatus.projectPatient.finalCodeID
        isChanged = True
        old_value = patientProjectStatus.patientProjectStatusTypeID

        if patientProjectStatus.patientProjectStatusTypeID == 2:   #Edit case
            if currentAddress and currentPhone and len(patientProjectStatus.projectPatient.contacts) == 0 and finalCode == 1:
               patientProjectStatus.patientProjectStatusTypeID = 21
            elif currentAddress and not currentPhone and len(patientProjectStatus.projectPatient.contacts) == 0 and finalCode == 1:
               patientProjectStatus.patientProjectStatusTypeID = 21
            elif not currentAddress and currentPhone and len(patientProjectStatus.projectPatient.contacts) == 0 and finalCode == 1:
               patientProjectStatus.patientProjectStatusTypeID = 3
            elif not currentAddress and not currentPhone and len(patientProjectStatus.projectPatient.contacts) == 0 and finalCode == 1:
               patientProjectStatus.patientProjectStatusTypeID = 3
            elif finalCode >1:
               patientProjectStatus.patientProjectStatusTypeID = 4
            else:
               isChanged = False

        elif patientProjectStatus.patientProjectStatusTypeID == 3:  # Tracing case
            contactType = []
            for contact in patientProjectStatus.projectPatient.contacts:
                contactType.append(contact.contactTypeLUTID)
            contactTypeSet = set(contactType)
            if currentAddress and currentPhone and len(contactTypeSet & compareTypeSet) ==0 and finalCode == 1:
               patientProjectStatus.patientProjectStatusTypeID = 21
            elif currentAddress and not currentPhone and len(contactTypeSet & compareTypeSet) ==0 and finalCode == 1:
                patientProjectStatus.patientProjectStatusTypeID = 21
            elif finalCode >1:
               patientProjectStatus.patientProjectStatusTypeID = 4
            else:
               isChanged = False

        elif patientProjectStatus.patientProjectStatusTypeID >= 21 and patientProjectStatus.patientProjectStatusTypeID <=29:  # Mailing 1-N case
            projectProtocol = query.get_project_protocol(patientProjectStatus.projectPatient.projectID)
            if projectProtocol is not None:
                protocol = projectProtocol.dict()
                daysBetweenSteps = protocol['daysBetweenSteps']
                del protocol['daysBetweenSteps']
                del protocol['projectID']
                del protocol['callsPerWindow']
                del protocol['createdDate']
                del protocol['modifiedDate']
                del protocol['versionID']
                contactType = False
                contactType2 = False
                for contact in patientProjectStatus.projectPatient.contacts:
                    difference = datetime.datetime.now().date() - contact.contactDate
                    if contact.contactTypeLUTID in compareTypeSet and difference.days >= daysBetweenSteps:
                        contactType = True
                    if contact.contactTypeLUTID in set([121,171,321,371]):
                        contactType2 = True

                if currentAddress and currentPhone and contactType and finalCode == 1:
                    present_value = protocol['mailing_'+str(patientProjectStatus.patientProjectStatusTypeID-20)]
                    next_value = ''
                    for k, v in protocol.items():
                        if v == present_value+1:
                            next_value =k
                            break
                    difference = datetime.datetime.now().date() - patientProjectStatus.statusDate
                    if next_value.find('mailing') >= 0 and difference.days >= daysBetweenSteps:
                        patientProjectStatus.patientProjectStatusTypeID = 20+int(next_value[8:])
                    elif next_value.find('call') >= 0 and difference.days >= daysBetweenSteps:
                        patientProjectStatus.patientProjectStatusTypeID = 50 + int(next_value[11:])
                elif currentAddress and not currentPhone and contactType and finalCode == 1:
                    present_value = protocol['mailing_' + str(patientProjectStatus.patientProjectStatusTypeID - 20)]
                    next_value = ''
                    for k, v in protocol.items():
                        if v == present_value + 1:
                            next_value = k
                            break
                    if next_value.find('mailing') >= 0:
                        patientProjectStatus.patientProjectStatusTypeID = 20 + int(next_value[8:])
                    elif next_value.find('call') >= 0:
                        patientProjectStatus.patientProjectStatusTypeID = 3
                elif currentAddress and currentPhone and contactType2 and finalCode == 1:
                    patientProjectStatus.patientProjectStatusTypeID = 3
                    localAddress = False
                    for patientAddress in patient.patientAddresses:
                        if patientAddress.contactInfoStatusID == 1:
                            patientAddress.contactInfoStatusID = 3
                            localAddress = True
                            patientAddress.addressStatusDate = datetime.datetime.now().date()
                            break
                    if localAddress == False:
                        for informant in patient.informants:
                            for informantAddress in informant.informantAddresses:
                                if informantAddress.contactInfoStatusID == 1:
                                    currentAddress = True
                                    break
                elif currentAddress and not currentPhone and contactType2 and finalCode == 1:
                    patientProjectStatus.patientProjectStatusTypeID = 3
                    localAddress = False
                    for patientAddress in patient.patientAddresses:
                        if patientAddress.contactInfoStatusID == 1:
                            patientAddress.contactInfoStatusID = 3
                            localAddress = True
                            patientAddress.addressStatusDate = datetime.datetime.now().date()
                            break
                    if localAddress == False:
                        for informant in patient.informants:
                            for informantAddress in informant.informantAddresses:
                                if informantAddress.contactInfoStatusID == 1:
                                    informantAddress.contactInfoStatusID = 3
                                    informantAddress.addressStatusDate = datetime.datetime.now().date()
                                    break
                elif finalCode>1:
                    patientProjectStatus.patientProjectStatusTypeID = 4
                else:
                    isChanged = False
            else:
                return item_not_found(" {} not found in ProjectProtocol table".format(patientProjectStatus.projectPatient.projectID))

        elif patientProjectStatus.patientProjectStatusTypeID >= 51 and patientProjectStatus.patientProjectStatusTypeID <= 69:  # CallWindow 1-N case
            contactType = False
            for contact in patientProjectStatus.projectPatient.contacts:
                if contact.contactTypeLUTID in set([205,255]):
                    contactType = True
            if currentAddress and currentPhone and contactType and finalCode == 1:
                localPhone = False
                for patientPhone in patient.patientPhones:
                    if patientPhone.contactInfoStatusID == 1:
                        patientPhone.contactInfoStatusID = 3
                        localPhone = True
                        patientPhone.phoneStatusDate = datetime.datetime.now().date()
                        break
                if localPhone == False:
                    for informant in patient.informants:
                        for informantPhone in informant.informantPhones:
                            if informantPhone.contactInfoStatusID == 1:
                                informantPhone.contactInfoStatusID = 3
                                informantPhone.phoneStatusDate = datetime.datetime.now().date()
                                break
                patientProjectStatus.patientProjectStatusTypeID = 3
            elif finalCode>1:
                patientProjectStatus.patientProjectStatusTypeID = 4
            else:
                isChanged = False

        if isChanged and patientProjectStatus.patientProjectStatusTypeID != old_value:
           patientProjectStatus.staffID = 250
           patientProjectStatus.statusDate = datetime.datetime.now().date()
           query.commit()
    flash("Refreshed Successfully")


@website.route('/queries/<int:queryID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_sqal_query(queryID):
    try:
        sqlQuery = query.get_query(queryID)
        if queryID is not None:
            form = forms.SqlQueryForm(request.form)
            if int(form.versionID.data) == sqlQuery.versionID:
                sqlQuery.query = form.query.data
                sqlQuery.queryName = form.queryName.data
                sqlQuery.director = form.director.data
                sqlQuery.contactStaff = form.contactStaff.data
                sqlQuery.informaticsStaff = form.informaticsStaff.data
                sqlQuery.researchManager = form.researchManager.data
                query.add(sqlQuery)
                query.flush()
                query.commit()
                flash("Updated Report")
                return redirect_back('editqueries/{}/'.format(queryID))
            else:
                return out_of_date_error()
        else:
            return item_not_found("Report ID {} not found".format(queryID))
    except Exception as e:
        return internal_error(e)

@website.route('/editqueries/', methods=['POST'])
@website.route('/editqueries/<int:queryID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_sqal_query(queryID=None):
    try:
        if queryID != 0:
            if request.form["action"].lower() == "editquery":
                return update_sqal_query(queryID)
            elif request.form["action"].lower() == "removequery":
                return delete_sqal_query(queryID)
            else:
                return invalid_method()
        else:
            form = forms.SqlQueryForm(request.form)
            sqlQuery = models.SqlQuery(
                query=form.query.data,
                queryName=form.queryName.data,
                director=form.director.data,
                contactStaff=form.contactStaff.data,
                informaticsStaff=form.informaticsStaff.data,
                researchManager=form.researchManager.data
            )
            query.add(sqlQuery)
            flash("Created New Report")
            return redirect_back('editqueries/')
    except Exception as e:
        return internal_error(e)

@website.route('/queries/<int:queryID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def delete_sqal_query(queryID):
    try:
        sqlQuery = query.get_query(queryID)
        if sqlQuery is not None:
            deps = get_dependencies(sqlQuery)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(sqlQuery)
                flash("Deleted Report {}".format(queryID))
                return redirect_back('editqueries/')
        else:
            return item_not_found("ReportID {} not found".format(queryID))
    except Exception as e:
        return internal_error(e)


##############################################################################
    # Site Groups
##############################################################################
@website.route('/sitegroups/<int:projectSiteGroupID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_site_groups(projectSiteGroupID=None):
    try:
        if projectSiteGroupID is None:
            return jsonify(projectSiteGroupID=[i.dict() for i in query.get_project_site_groups()])
        else:
            siteGroups = query.get_project_site_group(projectSiteGroupID)
            if siteGroups is not None:
                form = {}
                form["staff"] = query.get_staffs()
                form["siteGroups"] = query.get_sites()
                form["projects"] = query.get_projects()
                return render_template("site_groups_form.html", form=form, siteGroups=siteGroups)
            else:
                return item_not_found("SiteGroupID {} not found".format(projectSiteGroupID))
    except Exception as e:
        return internal_error(e)

# @website.route('/sitegroups/', methods = ['POST'])
@website.route('/sitegroups/', methods=['POST'])
@website.route('/sitegroups/<int:projectSiteGroupID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_site_groups(projectSiteGroupID=None):
    try:
        if projectSiteGroupID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_site_group(projectSiteGroupID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_site_groups(projectSiteGroupID)
            else:
                return invalid_method()
        else:
            form = forms.SiteGroupsForm(request.form)
            if form.validate():
                projectSiteGroups = models.ProjectSiteGroups(
                    projectID=form.projectID.data,
                    siteGroupID=form.siteGroupID.data
                )
                query.add(projectSiteGroups)
                flash("Created Project Site Group")
                return redirect_back('sitegroups/{}/'.format(projectSiteGroupID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@website.route('/sitegroups/<int:projectSiteGroupID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_site_group(projectSiteGroupID):
    try:
        projectSiteGroup = query.get_project_site_group(projectSiteGroupID)
        if projectSiteGroup is not None:
            form = forms.SiteGroupsForm(request.form)
            if form.validate():
                if int(form.versionID.data) == projectSiteGroup.versionID:
                    projectSiteGroup.projectID = form.projectID.data
                    projectSiteGroup.siteGroupID = form.siteGroupID.data
                    query.commit()
                    flash("Updated Site Groups")
                    return redirect_back('sitegroups/{}/'.format(projectSiteGroup.projectSiteGroupID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("ProjectSiteGroupID {} not found".format(projectSiteGroupID))
    except Exception as e:
        return internal_error(e)

@website.route('/sitegroups/<int:projectSiteGroupID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def delete_site_groups(projectSiteGroupID):
    try:
        projectSiteGroup = query.get_project_site_group(projectSiteGroupID)
        if projectSiteGroup is not None:
            deps = get_dependencies(projectSiteGroup)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(projectSiteGroup)
                return item_deleted("ProjectSiteGroupID {} deleted".format(projectSiteGroupID))
        else:
            return item_not_found("ProjectSiteGroupID {} not found".format(projectSiteGroupID))
    except Exception as e:
        return internal_error(e)

##############################################################################
# Staff
##############################################################################
@website.route('/addstaff/', methods=['GET'])
@authorization_required(roles=['Developer','Informatics Staff', 'Research Manager'])
def add_staff():
    try:
        form = {}
        form["states"] = query.get_states()
        form["humanSubjectTrainings"] = query.get_human_subject_trainings()
        form["staff"] = query.get_staffs()
        form["projects"] = query.get_projects()
        form["staffRoles"] = query.get_staff_roles()
        form["ucrRoles"] = query.get_ucr_roles()
        form["institutions"] = query.get_institutions()
        form["departments"] = query.get_departments()
        form["fieldDivisions"] = query.get_fieldDivisions()
        return render_template("staff_form.html", form=form, staff=None)

    except Exception as e:
     internal_error(e)

@website.route('/staff/', methods=['GET'])
@website.route('/staff/<int:staffID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_staff(staffID=None):
    try:
        if staffID is None:
            form = {}
            firstName = None
            lastName = None
            staffID = None
            phoneNumber = None
            email = None
            institutionID = None
            departmentID = None
            ucrRoleID = None
            form["queryParams"] = {}
            if "action" in request.args:
                if request.args["action"].lower() == "clear":
                    firstName = lastName = staffID = phoneNumber = email = institutionID = departmentID = ucrRoleID= None
                else:
                    if "firstName" in request.args:
                        firstName = value_or_none(request.args["firstName"])
                        form["queryParams"]["firstName"] = request.args["firstName"]
                    if "lastName" in request.args:
                        lastName = value_or_none(request.args["lastName"])
                        form["queryParams"]["lastName"] = request.args["lastName"]
                    if "staffID" in request.args:
                        staffID = value_or_none(request.args["staffID"])
                        form["queryParams"]["staffID"] = request.args["staffID"]
                    if "phoneNumber" in request.args:
                        phoneNumber = value_or_none(request.args["phoneNumber"])
                        form["queryParams"]["phoneNumber"] = request.args["phoneNumber"]
                    if "email" in request.args:
                        email = value_or_none(request.args["email"])
                        form["queryParams"]["email"] = request.args["email"]
                    if "institutionID" in request.args:
                        institutionID = value_or_none(request.args["institutionID"])
                        form["queryParams"]["institutionID"] = request.args["institutionID"]
                    if "departmentID" in request.args:
                        departmentID = value_or_none(request.args["departmentID"])
                        form["queryParams"]["departmentID"] = request.args["departmentID"]
                    if "ucrRoleID" in request.args:
                        ucrRoleID = value_or_none(request.args["ucrRoleID"])
                        form["queryParams"]["ucrRoleID"] = request.args["ucrRoleID"]

            staffs = query.query_staffs(firstName=firstName,
                                        lastName=lastName,
                                        staffID=staffID,
                                        phoneNumber=phoneNumber,
                                        email=email,
                                        institutionID=institutionID,
                                        departmentID=departmentID,
                                        ucrRoleID=ucrRoleID)
            form["ucrRoles"] = query.get_ucr_roles()
            form["institutions"] = query.get_institutions()
            form["departments"] = query.get_departments()
            return render_template("staff_table.html", form=form, staffs=staffs)
        else:
            staff = query.get_staff(staffID)
            if staff is not None:
                form = {}
                form["states"] = query.get_states()
                form["humanSubjectTrainings"] = query.get_human_subject_trainings()
                form["staff"] = query.get_staffs()
                form["projects"] = query.get_projects()
                form["staffRoles"] = query.get_staff_roles()
                form["ucrRoles"] = query.get_ucr_roles()
                form["institutions"] = query.get_institutions()
                form["departments"] = query.get_departments()
                form["fieldDivisions"] = query.get_fieldDivisions()
                return render_template("staff_form.html", form=form, staff=staff)
            else:
                return item_not_found("StaffID {} not found".format(staffID))
    except Exception as e:
        internal_error(e)


@website.route('/staff/<int:staffID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_staff(staffID):
    try:
        staff = query.get_staff(staffID)
        if staff is not None:
            form = forms.StaffForm(request.form)
            if form.validate():
                if int(form.versionID.data) == staff.versionID:
                    staff.firstName = form.firstName.data
                    staff.lastName = form.lastName.data
                    staff.middleName = form.middleName.data
                    staff.email = form.email.data
                    staff.phoneNumber = form.phoneNumber.data
                    staff.phoneComment = form.phoneComment.data
                    staff.institutionID = form.institutionID.data
                    staff.departmentID = form.departmentID.data
                    staff.position = form.position.data
                    staff.credentials = form.credentials.data
                    staff.street = form.street.data
                    staff.city = form.city.data
                    staff.zipcode=form.zipcode.data
                    if form.stateID.data is '':
                     staff.stateID = 'zz'
                    else:
                     staff.stateID = form.stateID.data
                    staff.ucrRoleID = form.ucrRoleID.data
                    staff.hci = form.hci.data
                    staff.ucr = form.ucr.data
                    staff.external = form.external.data
                    staff.fieldDivisionID=form.fieldDivisionID.data
                    # Don't allow updates to userID
                    #staff.userID = form.userID.data
                    query.commit()
                    flash("Updated Staff")
                    return redirect_back("staff/{}/".format(staffID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("StaffID {} not found".format(staffID))
    except Exception as e:
        internal_error(e)


@website.route('/staff/', methods=['POST'])
@website.route('/staff/<int:staffID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_staff(staffID=None):
    try:
        if staffID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_staff(staffID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_staff(staffID)
            else:
                return invalid_method()
        else:
            form = forms.StaffForm(request.form)
            if form.validate():
                staff = models.Staff(
                    firstName=form.firstName.data,
                    lastName=form.lastName.data,
                    middleName=form.middleName.data,
                    email=form.email.data,
                    phoneNumber=form.phoneNumber.data,
                    phoneComment=form.phoneComment.data,
                    institutionID=form.institutionID.data,
                    departmentID=form.departmentID.data,
                    position=form.position.data,
                    credentials=form.credentials.data,
                    street=form.street.data,
                    zipcode=form.zipcode.data,
                    city=form.city.data,
                    stateID=None if form.stateID.data == "" else form.stateID.data ,
                    ucrRoleID=form.ucrRoleID.data,
                    userID=form.userID.data,
                    hci=form.hci.data,
                    ucr=form.ucr.data,
                    external=form.external.data,
                    fieldDivisionID = form.fieldDivisionID.data
                )
                query.add(staff)
                flash("Created Staff")
                return redirect("/website/staff/{}/".format(staff.staffID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/staff/<int:staffID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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
@website.route('/staffroles/', methods=['GET'])
@website.route('/staffroles/<int:staffRoleID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_staff_role(staffRoleID=None):
    try:
        if staffRoleID is None:
            form = {
                "staffRoles": query.get_staff_roles(),
                "add": True
            }
            return render_template("staff_roles.html", form=form)
        else:
            staffRole = query.get_staff_role(staffRoleID)
            if staffRole is not None:
                form = {
                    "staffRoles": [staffRole],
                    "add": False
                }
                return render_template("staff_roles.html", form=form)
            else:
                return item_not_found("StaffRoleID {} not found".format(staffRoleID))
    except Exception as e:
        return internal_error(e)


@website.route('/staffroles/<int:staffRoleID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_staff_role(staffRoleID):
    try:
        staffRole = query.get_staff_role(staffRoleID)
        if staffRole is not None:
            form = forms.StaffRoleLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == staffRole.versionID:
                    staffRole.staffRole = form.staffRole.data
                    staffRole.staffRoleDescription = form.staffRoleDescription.data
                    query.commit()
                    flash("Updated Staff Role")
                    return redirect_back('staffroles/{}/'.format(staffRoleID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("StaffRoleID {} not found".format(staffRoleID))
    except Exception as e:
        return internal_error(e)


@website.route('/staffroles/', methods=['POST'])
@website.route('/staffroles/<int:staffRoleID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_staff_role(staffRoleID=None):
    try:
        if staffRoleID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_staff_role(staffRoleID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_staff_role(staffRoleID)
            else:
                return invalid_method()
        else:
            form = forms.StaffRoleLUTForm(request.form)
            if form.validate():
                staffRole = models.StaffRoleLUT(
                    staffRole=form.staffRole.data,
                    staffRoleDescription=form.staffRoleDescription.data,
                )
                query.add(staffRole)
                flash("Created Staff Role")
                return redirect_back('staffroles/{}/'.format(staffRoleID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/staffroles/<int:staffRoleID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/stafftrainings/', methods = ['GET'])
@website.route('/stafftrainings/<int:staffTrainingID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_staff_training(staffTrainingID=None):
    try:
        if staffTrainingID is None:
            return jsonify(StaffTrainings=[i.dict() for i in query.get_staff_trainings()])
        else:
            stafftraining = query.get_staff_training(staffTrainingID)
            if stafftraining is not None:
                form = {}
                form["humanSubjectTrainings"] = query.get_human_subject_trainings()
                form["staff"] = query.get_staffs()
                return render_template("staff_training_form.html", form=form, staffTraining=stafftraining)
            else:
                return item_not_found("StaffTrainingID {} not found".format(staffTrainingID))
    except Exception as e:
        return internal_error(e)


@website.route('/stafftrainings/<int:staffTrainingID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_staff_training(staffTrainingID):
    try:
        stafftraining = query.get_staff_training(staffTrainingID)
        if stafftraining is not None:
            form = forms.StaffTrainingForm(request.form)
            if form.validate():
                if int(form.versionID.data) == stafftraining.versionID:
                    stafftraining.staffID = form.staffID.data
                    stafftraining.humanSubjectTrainingID = form.humanSubjectTrainingID.data
                    stafftraining.dateTaken = form.dateTaken.data
                    stafftraining.dateExpires = form.dateExpires.data
                    query.commit()
                    flash("Updated Staff Training")
                    return redirect_back("stafftrainings/{}/".format(staffTrainingID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("StaffTrainingID {} not found".format(staffTrainingID))
    except Exception as e:
        return internal_error(e)


@website.route('/stafftrainings/', methods=['POST'])
@website.route('/stafftrainings/<int:staffTrainingID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_staff_training(staffTrainingID=None):
    try:
        if staffTrainingID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_staff_training(staffTrainingID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_staff_training(staffTrainingID)
        else:
            form = forms.StaffTrainingForm(request.form)
            if form.validate():
                stafftraining = models.StaffTraining(
                    staffID=form.staffID.data,
                    humanSubjectTrainingID=form.humanSubjectTrainingID.data,
                    dateTaken=form.dateTaken.data,
                    dateExpires=form.dateExpires.data
                )
                query.add(stafftraining)
                flash("Created Staff Training")
                return redirect_back("stafftrainings/{}/".format(stafftraining.staffTrainingID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/stafftrainings/<int:staffTrainingID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/tracings/', methods = ['GET'])
@website.route('/tracings/<int:tracingID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def get_tracing(tracingID=None):
    try:
        if tracingID is None:
            return jsonify(Tracings=[i.dict() for i in query.get_tracings()])
        else:
            tracing = query.get_tracing(tracingID)
            if tracing is not None:
                form = {}
                form["tracingSources"] = query.get_tracing_sources()
                form["projectPatients"] = query.get_project_patients()
                form["staff"] = query.get_staffs()
                return render_template("tracing_form.html", form=form, tracing=tracing)
            else:
                return item_not_found("TracingID {} not found".format(tracingID))
    except Exception as e:
        return internal_error(e)


@website.route('/tracings/<int:tracingID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def update_tracing(tracingID):
    try:
        tracing = query.get_tracing(tracingID)
        if tracing is not None:
            form = forms.TracingForm(request.form)
            if form.validate():
                if int(form.versionID.data) == tracing.versionID:
                    tracing.tracingSourceID = form.tracingSourceID.data
                    tracing.participantID = form.participantID.data
                    tracing.date = form.date.data
                    tracing.staffID = form.staffID.data
                    tracing.notes = form.notes.data
                    query.commit()
                    flash("Updated Tracing")
                    return redirect_back("tracings/{}/".format(tracingID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("TracingID {} not found".format(tracingID))
    except Exception as e:
        return internal_error(e)


@website.route('/tracings/', methods=['POST'])
@website.route('/tracings/<int:tracingID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager', 'Contact Staff'])
def create_tracing(tracingID=None):
    try:
        if tracingID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_tracing(tracingID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_tracing(tracingID)
            else:
                return invalid_method()
        else:
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
                flash("Created Tracing")
                return redirect_back("tracings/{}/".format(tracing.tracingID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/tracings/<int:tracingID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
@website.route('/tracingsources/', methods=['GET'])
@website.route('/tracingsources/<int:tracingSourceID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_tracing_source(tracingSourceID=None):
    try:
        if tracingSourceID is None:
            form = {
                "tracingSources": query.get_tracing_sources(),
                "add": True
            }
            return render_template("tracing_sources.html", form=form)
        else:
            tracing = query.get_tracing_source(tracingSourceID)
            if tracing is not None:
                form = {
                    "tracingSources": [tracing],
                    "add": False
                }
                return render_template("tracing_sources.html", form=form)
            else:
                return item_not_found("TracingSourceID {} not found".format(tracingSourceID))
    except Exception as e:
        return internal_error(e)


@website.route('/tracingsources/<int:tracingSourceID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_tracing_source(tracingSourceID):
    try:
        tracingSource = query.get_tracing_source(tracingSourceID)
        if tracingSource is not None:
            form = forms.TracingSourceLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == tracingSource.versionID:
                    tracingSource.description = form.description.data
                    query.commit()
                    flash("Updated Tracing Source")
                    return redirect_back('tracingsources/{}/'.format(tracingSourceID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("TracingSourceID {} not found".format(tracingSourceID))
    except Exception as e:
        return internal_error(e)


@website.route('/tracingsources/', methods=['POST'])
@website.route('/tracingsources/<int:tracingSourceID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_tracing_source(tracingSourceID=None):
    try:
        if tracingSourceID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_tracing_source(tracingSourceID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_tracing_source(tracingSourceID)
            else:
                return invalid_method()
        else:
            form = forms.TracingSourceLUTForm(request.form)
            if form.validate():
                tracingSource = models.TracingSourceLUT(
                    description=form.description.data
                )
                ret = query.add(tracingSource)
                flash("Created Tracing Source")
                return redirect_back('tracingsources/{}/'.format(tracingSourceID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/tracingsources/<int:tracingSourceID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
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
# @website.route('/ucrreports/', methods = ['GET'])
@website.route('/ucrreports/<int:ucrReportID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_ucr_report(ucrReportID=None):
    try:
        if ucrReportID is None:
            return jsonify(ucrReports=[i.dict() for i in query.get_ucr_reports()])
        else:
            ucr = query.get_ucr_report(ucrReportID)
            if ucr is not None:
                form = {}
                form["projects"] = query.get_projects()
                form["reportTypes"] = query.get_report_types()
                return render_template("ucr_report_form.html", form=form, ucrReport=ucr)
            else:
                return item_not_found("UcrReportID {} not found".format(ucrReportID))
    except Exception as e:
        internal_error(e)


@website.route('/ucrreports/<int:ucrReportID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_ucr_report(ucrReportID):
    try:
        ucr = query.get_ucr_report(ucrReportID)
        if ucr is not None:
            form = forms.UCRReportForm(request.form)
            if form.validate():
                if int(form.versionID.data) == ucr.versionID:
                    ucr.projectID = form.projectID.data
                    ucr.reportTypeID = form.reportTypeID.data
                    ucr.reportSubmitted = form.reportSubmitted.data
                    ucr.reportDue = form.reportDue.data
                    ucr.reportDoc = form.reportDoc.data
                    ucr.statusNotes=form.statusNotes.data
                    query.commit()
                    flash("Updated UCR Report")
                    return redirect_back("ucrreports/{}/".format(ucrReportID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("UcrReportID {} not found.".format(ucrReportID))
    except Exception as e:
        return internal_error(e)


@website.route('/ucrreports/', methods=['POST'])
@website.route('/ucrreports/<int:ucrReportID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_ucr_report(ucrReportID=None):
    try:
        if ucrReportID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_ucr_report(ucrReportID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_ucr_report(ucrReportID)
            else:
                return invalid_method()
        else:
            form = forms.UCRReportForm(request.form)
            if form.validate():
                ucr = models.UCRReport(
                    projectID=form.projectID.data,
                    reportTypeID=form.reportTypeID.data,
                    reportSubmitted=form.reportSubmitted.data,
                    reportDue=form.reportDue.data,
                    reportDoc=form.reportDoc.data,
                    statusNotes=form.statusNotes.data
                )
                query.add(ucr)
                flash("Created UCR Report")
                return redirect_back("ucrreports/{}/".format(ucr.ucrReportID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/ucrreports/<int:ucrReportID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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


@website.route('/ucrroles/', methods=['GET'])
@website.route('/ucrroles/<int:ucrRoleID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def get_ucr_role(ucrRoleID=None):
    try:
        if ucrRoleID is None:
            form = {
                "ucrRoles": query.get_ucr_roles(),
                "add": True
            }
            return render_template("ucr_roles.html", form=form)
        else:
            ucrRole = query.get_ucr_role(ucrRoleID)
            if ucrRole is not None:
                form = {
                    "ucrRoles": [ucrRole],
                    "add": False
                }
                return render_template("ucr_roles.html", form=form)
            else:
                return item_not_found("UCRRoleID {} not found".format(ucrRoleID))
    except Exception as e:
        return internal_error(e)


@website.route('/ucrroles/<int:ucrRoleID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def update_ucr_role(ucrRoleID):
    try:
        ucrRole = query.get_ucr_role(ucrRoleID)
        if ucrRole is not None:
            form = forms.UCRRoleForm(request.form)
            if form.validate():
                if int(form.versionID.data) == ucrRole.versionID:
                    ucrRole.ucrRole = form.ucrRole.data
                    query.commit()
                    flash("Updated UCR Role")
                    return redirect_back('ucrroles/{}/'.format(ucrRoleID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("UCRRoleID {} not found".format(ucrRoleID))
    except Exception as e:
        return internal_error(e)


@website.route('/ucrroles/', methods=['POST'])
@website.route('/ucrroles/<int:ucrRoleID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
def create_ucr_role(ucrRoleID=None):
    try:
        if ucrRoleID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_ucr_role(ucrRoleID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_ucr_role(ucrRoleID)
            else:
                return invalid_method()
        else:
            form = forms.UCRRoleForm(request.form)
            if form.validate():
                ucrRole = models.UCRRole(
                    ucrRole=form.ucrRole.data,
                )
                query.add(ucrRole)
                flash("Created UCR Role")
                return redirect_back('ucrroles/{}/'.format(ucrRole.ucrRoleID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)


@website.route('/ucrroles/<int:ucrRoleID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Director', 'Informatics Staff', 'Research Manager'])
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

##############################################################################
# Ucr Report Type LUT
##############################################################################
@website.route('/ucrreporttypes/', methods=['GET'])
@website.route('/ucrreporttypes/<int:ucrreporttypesID>/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_ucrreporttype(ucrreporttypesID=None):
    try:
        if ucrreporttypesID is None:
            form = {
                "ucrReports": query.get_report_types(),
                "add": True
            }
            return render_template("ucr_reports.html", form=form)
        else:
            ucrReport = query.get_report_type(ucrreporttypesID)
            if ucrReport is not None:
                form = {
                    "ucrReports": [ucrReport],
                    "add": False
                }
                return render_template("ucr_reports.html", form=form)
            else:
                return item_not_found("UcrReportID {} not found".format(ucrreporttypesID))
    except Exception as e:
        return internal_error(e)

@website.route('/ucrreporttypes/<int:ucrreporttypesID>/', methods=['PUT'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def update_ucrreporttype(ucrreporttypesID):
    try:
        ucrReport = query.get_report_type(ucrreporttypesID)
        if ucrReport is not None:
            form = forms.UcrReportLUTForm(request.form)
            if form.validate():
                if int(form.versionID.data) == ucrReport.versionID:
                    ucrReport.ucrReportType = form.ucrReportType.data
                    query.commit()
                    flash("Updated UCR Report")
                    return redirect_back('ucrreporttypes/{}/'.format(ucrreporttypesID))
                else:
                    return out_of_date_error()
            else:
                return missing_params(form.errors)
        else:
            return item_not_found("UcrReportID {} not found".format(ucrreporttypesID))
    except Exception as e:
        return internal_error(e)

@website.route('/ucrreporttypes/', methods=['POST'])
@website.route('/ucrreporttypes/<int:ucrreporttypesID>/', methods=['POST'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def create_ucrreporttype(ucrreporttypesID=None):
    try:
        if ucrreporttypesID:
            if "_method" in request.form and request.form["_method"].lower() == "put":
                return update_ucrreporttype(ucrreporttypesID)
            elif "_method" in request.form and request.form["_method"].lower() == "delete":
                return delete_ucrreporttype(ucrreporttypesID)
            else:
                return invalid_method()
        else:
            form = forms.UcrReportLUTForm(request.form)
            if form.validate():
                ucrReport = models.UCRReportType(
                    ucrReportType=form.ucrReportType.data
                )
                ret = query.add(ucrReport)
                flash("Created Ucr Report Type ")
                return redirect_back('ucrreporttypes/{}/'.format(ucrreporttypesID))
            else:
                return missing_params(form.errors)
    except Exception as e:
        return internal_error(e)

@website.route('/ucrreporttypes/<int:ucrreporttypesID>/', methods=['DELETE'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def delete_ucrreporttype(ucrreporttypesID):
    try:
        ucrReport = query.get_report_type(ucrreporttypesID)
        if ucrReport is not None:
            deps = get_dependencies(ucrReport)
            if deps:
                return dependency_detected(deps)
            else:
                query.delete(ucrReport)
                return item_deleted("UcrReportTypesID {} deleted".format(ucrreporttypesID))
        else:
            return item_not_found("UcrReportTypesID {} not found".format(ucrreporttypesID))
    except Exception as e:
        return internal_error(e)


##############################################################################
# Lookup Table
##############################################################################
@website.route('/lookuptables/', methods=['GET'])
@authorization_required(roles=['Developer', 'Informatics Staff', 'Research Manager'])
def get_lookup_tables():
    form = {"tables": []}

    abstractStatuses = query.get_abstract_statuses()
    form["tables"].append({
        "name": "Abstract Statuses",
        "count": len(abstractStatuses),
        "values": [abst.abstractStatus for abst in abstractStatuses],
        "endpoint": "abstractstatuses"
    })

    contactInfoSources = query.get_contact_info_sources()
    form["tables"].append({
        "name": "Contact Info Sources",
        "count": len(contactInfoSources),
        "values": [cis.contactInfoSource for cis in contactInfoSources],
        "endpoint": "contactinfosources"
    })

    contactInfoStatuses = query.get_contact_info_statuses()
    form["tables"].append({
        "name": "Contact Info Statuses",
        "count": len(contactInfoStatuses),
        "values": [cis.contactInfoStatus for cis in contactInfoStatuses],
        "endpoint": "contactinfostatuses"
    })

    contactTypes = query.get_contact_types()
    form["tables"].append({
        "name": "Contact Types",
        "count": len(contactTypes),
        "values": [ct.contactDefinition for ct in contactTypes],
        "endpoint": "contacttypes"
    })

    departments = query.get_departments()
    form["tables"].append({
        "name": "Departments",
        "count": len(departments),
        "values": [department.department for department in departments],
        "endpoint": "departments"
    })

    fieldDivisions = query.get_fieldDivisions()
    form["tables"].append({
        "name": "Divisions",
        "count": len(fieldDivisions),
        "values": [fieldDivision.fieldDivision for fieldDivision in fieldDivisions],
        "endpoint": "fielddivisions"
    })

    externalStudyCodes = query.get_external_study_codes()
    form["tables"].append({
        "name": "External Study Codes",
        "count": len(externalStudyCodes),
        "values": [externalStudyCode.externalStudyCode for externalStudyCode in externalStudyCodes],
        "endpoint": "externalstudycodes"
    })

    finalCodes = query.get_final_codes()
    form["tables"].append({
        "name": "Final Codes",
        "count": len(finalCodes),
        "values": [fc.finalCode for fc in finalCodes],
        "endpoint": "finalcodes"
    })

    fundingSources = query.get_funding_sources()
    form["tables"].append({
        "name": "Funding Sources",
        "count": len(fundingSources),
        "values": [fs.fundingSource for fs in fundingSources],
        "endpoint": "fundingsources"
    })

    grantStatuses = query.get_grant_statuses()
    form["tables"].append({
        "name": "Grant Statuses",
        "count": len(grantStatuses),
        "values": [gs.grantStatus for gs in grantStatuses],
        "endpoint": "grantstatuses"
    })

    humanSubjectTrainings = query.get_human_subject_trainings()
    form["tables"].append({
        "name": "Human Subject Trainings",
        "count": len(humanSubjectTrainings),
        "values": [hst.trainingType for hst in humanSubjectTrainings],
        "endpoint": "humansubjecttrainings"
    })

    institutions = query.get_institutions()
    form["tables"].append({
        "name": "Institutions",
        "count": len(institutions),
        "values": [institution.institution for institution in institutions],
        "endpoint": "institutions"
    })

    irbHolders = query.get_irb_holders()
    form["tables"].append({
        "name": "IRB Holders",
        "count": len(irbHolders),
        "values": [irb.holder for irb in irbHolders],
        "endpoint": "irbholders"
    })

    logSubjects = query.get_log_subjects()
    form["tables"].append({
        "name": "Log Subjects",
        "count": len(logSubjects),
        "values": [ls.logSubject for ls in logSubjects],
        "endpoint": "logsubjects"
    })

    phaseStatuses = query.get_phase_statuses()
    form["tables"].append({
        "name": "Phase Status",
        "count": len(phaseStatuses),
        "values": [ps.phaseStatus for ps in phaseStatuses],
        "endpoint": "phasestatuses"
    })

    phoneTypes = query.get_phone_types()
    form["tables"].append({
        "name": "Phone Types",
        "count": len(phoneTypes),
        "values": [pt.phoneType for pt in phoneTypes],
        "endpoint": "phonetypes"
    })

    projectStatuses = query.get_project_status_luts()
    form["tables"].append({
        "name": "Project Statuses",
        "count": len(projectStatuses),
        "values": [ps.projectStatus for ps in projectStatuses],
        "endpoint": "projectstatustypes"
    })

    projectTypes = query.get_project_types()
    form["tables"].append({
        "name": "Project Types",
        "count": len(projectTypes),
        "values": [pt.projectType for pt in projectTypes],
        "endpoint": "projecttypes"
    })

    reviewCommittees = query.get_review_committee_luts()
    form["tables"].append({
        "name": "Review Committees",
        "count": len(reviewCommittees),
        "values": [rc.reviewCommittee for rc in reviewCommittees],
        "endpoint": "reviewcommitteelist"
    })

    reviewCommitteeStatuses = query.get_review_committee_statuses()
    form["tables"].append({
        "name": "Review Committee Statuses",
        "count": len(reviewCommitteeStatuses),
        "values": [rcs.reviewCommitteeStatus for rcs in reviewCommitteeStatuses],
        "endpoint": "reviewcommitteestatuses"
    })

    staffRoles = query.get_staff_roles()
    form["tables"].append({
        "name": "Staff Roles",
        "count": len(staffRoles),
        "values": [sr.staffRole for sr in staffRoles],
        "endpoint": "staffroles"
    })

    tracingSources = query.get_tracing_sources()
    form["tables"].append({
        "name": "Tracing Sources",
        "count": len(tracingSources),
        "values": [ts.description for ts in tracingSources],
        "endpoint": "tracingsources"
    })

    ucrReportTypes = query.get_report_types()
    form["tables"].append({
        "name": "UCR Report Types",
        "count": len(ucrReportTypes),
        "values": [ut.ucrReportType for ut in ucrReportTypes],
        "endpoint": "ucrreporttypes"
    })

    return render_template("lookup_tables_table.html", form=form)
