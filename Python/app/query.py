import json
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.database import db
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import aliased
from app.models import *


def summary(projectTitle=None, mostRecentProjectStatusTypeID=None):
    """
    Generates a dictionary that summarizes each project over the last 30 days
    :return:
    """
    summary_dict = {"projects":[]}
    # subq = db.session.query(ProjectPatient.projectID, ProjectPatient.finalCodeID, func.count(ProjectPatient.finalCodeID)).group_by(ProjectPatient.finalCodeID, ProjectPatient.projectID).subquery()
    # subq_alias1 = aliased(subq)
    # qry = db.session.query(Project.projectTitle, Project.activityStartDate, Project.projectID, subq_alias1). \
    #     join(subq_alias1, and_(Project.projectID==subq_alias1.c.projectID))
    # for result in qry.all():
    #     summary_dict[result[2]] = {
    #         "title": result[0],
    #         "activityStarteDate": result[1],
    #         "lettersSent": lettersSent,
    #         "phoneCalls": phoneCalls,
    #         "avgDaysToFinalize": avgDaysToFinalize,
    #         "avgNumberOfContactsPerPerson": avgNumberOfContactsPerPerson
    #     }
    # db.session.query(func.count(Contact.contactID)).join(Contact.projectPatient).join(ProjectPatient.project).filter(Project.projectID==1)
    # res = db.session.query(Project.projectID, Project.projectTitle, Project.activityStartDate, Project.projectTypeID).all()

    # some complex query to filter by the most recent projectStatusTypeID
    filters = []
    if projectTitle:
        filters.append(Project.projectTitle.like('%{}%'.format(projectTitle)))
    if mostRecentProjectStatusTypeID:
        filters.append(ProjectStatus.projectStatusTypeID == mostRecentProjectStatusTypeID)
    res = db.session.query(Project.projectID, Project.projectTitle, Project.activityStartDate, Project.projectTypeID).outerjoin(ProjectStatus.project).filter(ProjectStatus.statusDate == db.session.query(
        func.max(ProjectStatus.statusDate)).filter(ProjectStatus.projectID==Project.projectID).correlate(Project).as_scalar()).filter(and_(*filters)).order_by(Project.projectTitle).all()
    for result in res:
        summary_info = {
            "projectID": result[0],
            "projectTitle": result[1],
            "activityStartDate": result[2],
            "numberOfLettersSent": get_number_of_contact_types(projectID=result[0],
                                                               startDate=datetime.datetime.today() - datetime.timedelta(
                                                                   days=30), contact_type_ids=[1, 2, 3, 4, 5, 6])[0],
            "numberOfPhoneCalls": get_number_of_contact_types(projectID=result[0],
                                                              startDate=datetime.datetime.today() - datetime.timedelta(
                                                                  days=30),
                                                              contact_type_ids=[10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                                                                20, 21, 22, 23, 24, 25, 26, 27])[0],
            "numberOfConsentsOrPermissions": get_number_of_final_code_types(projectID=result[0],
                                                              min_final_code=100, max_final_code=199)[0],
        }
        try:
            summary_info["avgNumberOfContactsPerPerson"]= float(get_number_of_contact_types(projectID=result[0],
                                                                              startDate=datetime.datetime.today() - datetime.timedelta(
                                                                                  days=30))[0]) / float(
                len(query_project_patients(projectID=result[0])))
        except ZeroDivisionError:
            summary_info["avgNumberOfContactsPerPerson"] = "inf"
        summary_dict["projects"].append(summary_info)
    return summary_dict


def get_number_of_contact_types(projectID=None, startDate=None, endDate=None, contact_type_ids=None, contact_codes=None, min_contact_code=None, max_contact_code=None):
    filters = []
    if projectID:
        filters.append(Project.projectID == projectID)
    if startDate:
        filters.append(Contact.contactDate >= startDate)
    if endDate:
        filters.append(Contact.contactDate <= endDate)
    if contact_type_ids:
        filters.append(Contact.contactTypeLUTID.in_(contact_type_ids))
    if contact_codes:
        filters.append(Contact.contactCode.in_(contact_codes))
    if  min_contact_code:
        filters.append(Contact.contactCode >= min_contact_code)
    if max_contact_code:
        filters.append(Contact.contactCode <= max_contact_code)
    res = db.session.query(func.count(Contact.contactID), func.count(ProjectPatient.participantID)).join(Contact.projectPatient).join(ProjectPatient.project). \
        filter(and_(*filters)).first()
    return res


def get_number_of_final_code_types(projectID=None, final_code_type_ids=None, min_final_code=None, max_final_code=None):
    filters = []
    if projectID:
        filters.append(Project.projectID == projectID)
    if final_code_type_ids:
        filters.append(FinalCode.finalCodeID.in_(final_code_type_ids))
    if min_final_code:
        filters.append(FinalCode.finalCode >= min_final_code)
    if max_final_code:
        filters.append(FinalCode.finalCode <= max_final_code)
    res = db.session.query(func.count(FinalCode.finalCodeID)).join(FinalCode.projectPatients).join(ProjectPatient.project). \
        filter(and_(*filters)).first()
    return res


def create_all():
    db.create_all()


def add(obj):
    db.session.add(obj)


def flush():
    db.session.flush()


def get_abstract_statuses():
    return db.session.query(AbstractStatus).all()


def get_abstract_status(id):
    return db.session.query(AbstractStatus).filter_by(abstractStatusID=id).first()


def get_arc_reviews():
    return db.session.query(ArcReview).all()


def get_arc_review(id):
    return db.session.query(ArcReview).filter_by(arcReviewID=id).first()


def get_booleans():
    return db.session.query(Boolean).all()


def get_boolean(id):
    return db.session.query(Boolean).filter_by(booleanID=id).first()


def get_budgets():
    return db.session.query(Budget).all()


def get_budget(id):
    return db.session.query(Budget).filter_by(budgetID=id).first()


def get_contacts():
    return db.session.query(Contact).order_by(Contact.contactDate.desc()).all()


def get_contact(id):
    return db.session.query(Contact).filter_by(contactID=id).first()


def get_contact_enum(id):
    return db.session.query(Contacts).filter_by(contactID=id).first()


def get_contact_enums():
    return db.session.query(Contacts).all()


def get_contact_types():
    return db.session.query(ContactTypeLUT).all()


def get_contact_type(id):
    return db.session.query(ContactTypeLUT).filter_by(contactTypeID=id).first()


def get_contact_type_by_code(code):
    return db.session.query(ContactTypeLUT).filter_by(contactCode=code).first()


def get_contact_info_sources():
    return db.session.query(ContactInfoSourceLUT).all()


def get_contact_info_source(id):
    return db.session.query(ContactInfoSourceLUT).filter_by(contactInfoSourceID=id).first()


def get_contact_info_statuses():
    return db.session.query(ContactInfoStatusLUT).all()


def get_contact_info_status(id):
    return db.session.query(ContactInfoStatusLUT).filter_by(contactInfoStatusID=id).first()


def get_ctcs():
    return db.session.query(CTC).all()


def get_ctc(id):
    return db.session.query(CTC).filter_by(ctcID=id).first()


def get_ethnicity(id):
    return db.session.query(Ethnicity).filter_by(ethnicityID=id).first()


def get_ethnicities():
    return db.session.query(Ethnicity).all()


def get_ctc_facilities():
    return db.session.query(CTCFacility).all()


def get_ctc_facility(id):
    return db.session.query(CTCFacility).filter_by(CTCFacilityID=id).first()


def get_facilities():
    return db.session.query(Facility).all()


def query_facilities(facilityName=None, contactFirstName=None, contactLastName=None, facilityStatus=None):
    filters = []
    if facilityName:
        filters.append(Facility.facilityName.like('%{}%'.format(facilityName)))
    if contactFirstName:
        filters.append(Facility.contactFirstName.like('%{}%'.format(contactFirstName)))
    if contactLastName:
        filters.append(Facility.contactLastName.like('%{}%'.format(contactLastName)))
    if facilityStatus:
        filters.append(Facility.facilityStatus == facilityStatus)
    return db.session.query(Facility).filter(or_(*filters)).all()


def get_facility(id):
    return db.session.query(Facility).filter_by(facilityID=id).first()


def get_facility_phones():
    return db.session.query(FacilityPhone).all()


def get_facility_phone(id):
    return db.session.query(FacilityPhone).filter_by(facilityPhoneID=id).first()


def get_facility_addresses():
    return db.session.query(FacilityAddress).all()


def get_facility_address(id):
    return db.session.query(FacilityAddress).filter_by(facilityAddressID=id).first()


def get_final_codes():
    return db.session.query(FinalCode).all()


def get_final_code(id):
    return db.session.query(FinalCode).filter_by(finalCodeID=id).first()


def get_final_code_by_code(code):
    return db.session.query(FinalCode).filter_by(finalCode=code).first()


def get_fundings():
    return db.session.query(Funding).all()


def get_funding(id):
    return db.session.query(Funding).filter_by(fundingID=id).first()


def get_funding_sources():
    return db.session.query(FundingSourceLUT).all()


def get_funding_source(id):
    return db.session.query(FundingSourceLUT).filter_by(fundingSourceID=id).first()


def get_gift_cards():
    return db.session.query(GiftCard).all()


def get_gift_card(id):
    return db.session.query(GiftCard).filter_by(giftCardID=id).first()

def get_gift_card_by_barcode(barcode):
    return db.session.query(GiftCard).filter_by(barcode=barcode).first()


def get_grant_statuses():
    return db.session.query(GrantStatusLUT).all()


def get_grant_status(id):
    return db.session.query(GrantStatusLUT).filter_by(grantStatusID=id).first()


def get_human_subject_trainings():
    return db.session.query(HumanSubjectTrainingLUT).all()


def get_human_subject_training(id):
    return db.session.query(HumanSubjectTrainingLUT).filter_by(humanSubjectTrainingID=id).first()


def get_inactive_enum(id):
    return db.session.query(Inactive).filter_by(inactiveID=id).first()


def get_inactive_enums():
    return db.session.query(Inactive).all()


def get_incentives():
    return db.session.query(Incentive).order_by(Incentive.dateGiven.desc()).all()


def get_incentive(id):
    return db.session.query(Incentive).filter_by(incentiveID=id).first()


def get_incentive_by_barcode(barcode):
    return db.session.query(Incentive).filter_by(barcode=barcode).first()


def get_informants():
    return db.session.query(Informant).all()


def get_informant(id):
    return db.session.query(Informant).filter_by(informantID=id).first()


def get_informant_addresses():
    return db.session.query(InformantAddress).all()


def get_informant_address(id):
    return db.session.query(InformantAddress).filter_by(informantAddressID=id).first()


def get_informant_phones():
    return db.session.query(InformantPhone).all()


def get_informant_phone(id):
    return db.session.query(InformantPhone).filter_by(informantPhoneID=id).first()


def get_irb_holders():
    return db.session.query(IRBHolderLUT).all()


def get_irb_holder(id):
    return db.session.query(IRBHolderLUT).filter_by(irbHolderID=id).first()


def get_logs():
    return db.session.query(Log).all()


def get_log(id):
    return db.session.query(Log).filter_by(logID=id).first()


def get_log_subjects():
    return db.session.query(LogSubjectLUT).all()


def get_log_subject(id):
    return db.session.query(LogSubjectLUT).filter_by(logSubjectID=id).first()


def get_patients():
    return db.session.query(Patient).all()


def query_patients(firstName=None, lastName=None, patID=None, UPDBID=None, ucrDistID=None,
                   phoneNumber=None):
    filters = []
    if firstName:
        filters.append(Patient.firstName.like('%{}%'.format(firstName)))
    if lastName:
        filters.append(Patient.lastName.like('%{}%'.format(lastName)))
    if patID:
        filters.append(Patient.patID.like('%{}%'.format(patID)))
    if UPDBID:
        filters.append(Patient.UPDBID == UPDBID)
    if ucrDistID:
        filters.append(Patient.ucrDistID == ucrDistID)
    if phoneNumber:
        filters.append(PatientPhone.phoneNumber == phoneNumber)
    return db.session.query(Patient).outerjoin(PatientPhone).filter(or_(*filters)).all()


def get_patient(id):
    return db.session.query(Patient).filter_by(participantID=id).first()


def get_patient_addresses():
    return db.session.query(PatientAddress).all()


def get_patient_address(id):
    return db.session.query(PatientAddress).filter_by(patAddressID=id).first()


def get_patient_emails():
    return db.session.query(PatientEmail).all()


def get_patient_email(id):
    return db.session.query(PatientEmail).filter_by(emailID=id).first()


def get_patient_phones():
    return db.session.query(PatientPhone).all()


def get_patient_phone(id):
    return db.session.query(PatientPhone).filter_by(patPhoneID=id).first()


def get_patient_project_statuses():
    return db.session.query(PatientProjectStatus).all()


def get_patient_project_status(id):
    return db.session.query(PatientProjectStatus).filter_by(patientProjectStatusID=id).first()


def get_patient_project_status_types():
    return db.session.query(PatientProjectStatusLUT).all()


def get_patient_project_status_type(id):
    return db.session.query(PatientProjectStatusLUT).filter_by(patientProjectStatusTypeID=id).first()


def get_phase_statuses():
    return db.session.query(PhaseStatus).all()


def get_phase_status(id):
    return db.session.query(PhaseStatus).filter_by(logPhaseID=id).first()


def get_phone_types():
    return db.session.query(PhoneTypeLUT).all()


def get_phone_type(id):
    return db.session.query(PhoneTypeLUT).filter_by(phoneTypeID=id).first()


def get_physicians():
    return db.session.query(Physician).all()


def query_physicians(firstName=None, lastName=None, specialty=None, physicianStatusID=None):
    filters = []
    if firstName:
        filters.append(Physician.firstName.like('%{}%'.format(firstName)))
    if lastName:
        filters.append(Physician.lastName.like('%{}%'.format(lastName)))
    if specialty:
        filters.append(Physician.specialty.like('%{}%'.format(specialty)))
    if physicianStatusID:
        filters.append(Physician.physicianStatusID == physicianStatusID)
    return db.session.query(Physician).filter(or_(*filters)).all()


def get_physician(id):
    return db.session.query(Physician).filter_by(physicianID=id).first()


def get_physician_addresses():
    return db.session.query(PhysicianAddress).all()


def get_physician_address(id):
    return db.session.query(PhysicianAddress).filter_by(physicianAddressID=id).first()


def get_physician_emails():
    return db.session.query(PhysicianEmail).all()


def get_physician_email(id):
    return db.session.query(PhysicianEmail).filter_by(physicianEmailID=id).first()


def get_physician_facilities():
    return db.session.query(PhysicianFacility).all()


def get_physician_facility(id):
    return db.session.query(PhysicianFacility).filter_by(physFacilityID=id).first()


def get_physician_facility_status(id):
    return db.session.query(PhysicianFacilityStatus).filter_by(physicianFacilityStatusID=id).first()


def get_physician_facility_statuses():
    return db.session.query(PhysicianFacilityStatus).all()


def get_physician_phones():
    return db.session.query(PhysicianPhone).all()


def get_physician_phone(id):
    return db.session.query(PhysicianPhone).filter_by(physicianPhoneID=id).first()


def get_physician_statuses():
    return db.session.query(PhysicianStatus).all()


def get_physician_status(id):
    return db.session.query(PhysicianStatus).filter_by(physicianStatusID=id).first()


def get_physician_to_ctcs():
    return db.session.query(PhysicianToCTC).all()


def get_physician_to_ctc(id):
    return db.session.query(PhysicianToCTC).filter_by(physicianCTCID=id).first()


def get_pre_applications():
    return db.session.query(PreApplication).all()


def get_pre_application(id):
    return db.session.query(PreApplication).filter_by(preApplicationID=id).first()


def get_project(id):
    return Project.query.filter_by(projectID=id).first()


def get_projects():
    return db.session.query(Project).all()


def query_projects(projectID=None, shortTitle=None, projectTypeID=None, piLastName=None, mostRecentProjectStatusTypeID=None):
    filters = []
    if projectID:
        filters.append(Project.projectID == projectID)
    if shortTitle:
        filters.append(Project.shortTitle.like('%{}%'.format(shortTitle)))
    if projectTypeID:
        filters.append(Project.projectTypeID == projectTypeID)
    if piLastName:
        filters.append(PreApplication.piLastName.like('%{}%'.format(piLastName)))
    if mostRecentProjectStatusTypeID:
        filters.append(ProjectStatus.projectStatusTypeID == mostRecentProjectStatusTypeID)

    res = db.session.query(Project).outerjoin(ProjectStatus.project).filter(ProjectStatus.statusDate == db.session.query(
        func.max(ProjectStatus.statusDate)).filter(ProjectStatus.projectID==Project.projectID).correlate(Project).as_scalar()).filter(and_(*filters)).order_by(Project.projectTitle).all()
    return res


def get_project_patients():
    return db.session.query(ProjectPatient).all()


def query_project_patients(firstName=None, lastName=None,
                           finalCodeID=None, batch=None,
                           siteGrp=None, projectID=None):
    filters = []
    if firstName:
        filters.append(Patient.firstName.like('%{}%'.format(firstName)))
    if lastName:
        filters.append(Patient.lastName.like('%{}%'.format(lastName)))
    if finalCodeID:
        filters.append(ProjectPatient.finalCodeID == finalCodeID)
    if batch:
        filters.append(ProjectPatient.batch == batch)
    if siteGrp:
        filters.append(ProjectPatient.siteGrp == siteGrp)
    if projectID:
        filters.append(Project.projectID == projectID)
    return db.session.query(ProjectPatient).outerjoin(Project).outerjoin(CTC).outerjoin(Patient).filter(
        or_(*filters)).all()


def get_project_patient(id):
    return db.session.query(ProjectPatient).filter_by(participantID=id).first()


def get_project_staffs():
    return db.session.query(ProjectStaff).all()


def query_staffs(firstName=None, lastName=None, staffID=None, phoneNumber=None, email=None, institution=None,
                 department=None, ucrRoleID=None):
    filters = []
    if firstName:
        filters.append(Staff.firstName.like('%{}%'.format(firstName)))
    if lastName:
        filters.append(Staff.lastName.like('%{}%'.format(lastName)))
    if staffID:
        filters.append(Staff.staffID == staffID)
    if phoneNumber:
        filters.append(Staff.phoneNumber == phoneNumber)
    if email:
        filters.append(Staff.email == email)
    if institution:
        filters.append(Staff.institution == institution)
    if department:
        filters.append(Staff.department == department)
    if ucrRoleID:
        filters.append(Staff.ucrRoleID == ucrRoleID)
    return db.session.query(Staff).filter(or_(*filters)).all()


def get_project_staff(id):
    return db.session.query(ProjectStaff).filter_by(projectStaffID=id).first()


def get_project_statuses():
    return db.session.query(ProjectStatus).all()


def get_project_status(id):
    return db.session.query(ProjectStatus).filter_by(projectStatusID=id).first()


def get_project_status_luts():
    return db.session.query(ProjectStatusLUT).all()


def get_project_status_lut(id):
    return db.session.query(ProjectStatusLUT).filter_by(projectStatusTypeID=id).first()


def get_project_types():
    return db.session.query(ProjectType).all()


def get_project_type(id):
    return db.session.query(ProjectType).filter_by(projectTypeID=id).first()


def get_race(id):
    return db.session.query(Race).filter_by(raceID=id).first()


def get_races():
    return db.session.query(Race).all()


def get_review_committee_status(id):
    return db.session.query(ReviewCommitteeStatusLUT).filter_by(reviewCommitteeStatusID=id).first()


def get_review_committee_statuses():
    return db.session.query(ReviewCommitteeStatusLUT).all()


def get_review_committees():
    return db.session.query(ReviewCommittee).all()


def get_review_committee(id):
    return db.session.query(ReviewCommittee).filter_by(reviewCommitteeID=id).first()


def get_review_committee_lut(id):
    return db.session.query(ReviewCommitteeLUT).filter_by(reviewCommitteeID=id).first()


def get_review_committee_luts():
    return db.session.query(ReviewCommitteeLUT).all()


def get_roles():
    return db.session.query(Role).all()


def get_role(id):
    return db.session.query(Role).filter_by(roleID=id).first()


def get_sex(id):
    return db.session.query(Sex).filter_by(sexID=id).first()


def get_sexes():
    return db.session.query(Sex).all()


def get_staffs():
    return db.session.query(Staff).all()


def get_staff(id):
    return db.session.query(Staff).filter_by(staffID=id).first()


def get_staff_roles():
    return db.session.query(StaffRoleLUT).all()


def get_staff_role(id):
    return db.session.query(StaffRoleLUT).filter_by(staffRoleID=id).first()


def get_staff_trainings():
    return db.session.query(StaffTraining).all()


def get_staff_training(id):
    return db.session.query(StaffTraining).filter_by(staffTrainingID=id).first()


def get_state(id):
    return db.session.query(State).filter_by(stateID=id).first()


def get_states():
    return db.session.query(State).all()


def get_tracings():
    return db.session.query(Tracing).all()


def get_tracing(id):
    return db.session.query(Tracing).filter_by(tracingID=id).first()


def get_tracing_sources():
    return db.session.query(TracingSourceLUT).all()


def get_tracing_source(id):
    return db.session.query(TracingSourceLUT).filter_by(tracingSourceID=id).first()


def get_ucr_reports():
    return db.session.query(UCRReport).all()


def get_ucr_report(id):
    return db.session.query(UCRReport).filter_by(ucrReportID=id).first()


def get_report_type(id):
    return db.session.query(UCRReportType).filter_by(ucrReportTypeID=id).first()


def get_report_types():
    return db.session.query(UCRReportType).all()


def get_ucr_roles():
    return db.session.query(UCRRole).all()


def get_ucr_role(id):
    return db.session.query(UCRRole).filter_by(ucrRoleID=id).first()


def get_user(id):
    return db.session.query(User).filter_by(userID=id).first()


def get_users():
    return db.session.query(User).all()


def get_user_by_username(username):
    return db.session.query(User).filter_by(uID=username).first()


def get_vital_status(id):
    return db.session.query(VitalStatus).filter_by(vitalStatusID=id).first()


def get_vital_statues():
    return db.session.query(VitalStatus).all()


def commit():
    return db.session.commit()


def add(obj):
    db.session.add(obj)
    return db.session.commit()


def delete(obj):
    db.session.delete(obj)
    return db.session.commit()
