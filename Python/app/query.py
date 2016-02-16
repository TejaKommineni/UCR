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

def get_contacts():
    return db.session.query(Contact).all()
    
def get_contact(id):
    return db.session.query(Contact).filter_by(contactID = id).first()
    
def get_contact_types():
    return db.session.query(ContactTypeLUT).all()
    
def get_contact_type(id):
    return db.session.query(ContactTypeLUT).filter_by(contactTypeLUTID = id).first()
    
def get_contact_info_sources():
    return db.session.query(ContactInfoSourceLUT).all()
    
def get_contact_info_source(id):
    return db.session.query(ContactInfoSourceLUT).filter_by(contactInfoSourceLUTID = id).first()    
    
def get_contact_info_statuses():
    return db.session.query(ContactInfoStatusLUT).all()
    
def get_contact_info_status(id):
    return db.session.query(ContactInfoStatusLUT).filter_by(contactInfoStatusID = id).first()

def get_ctcs():
    return db.session.query(CTC).all()

def get_ctc(id):
    return db.session.query(CTC).filter_by(ctcID = id).first()

def get_ctc_facilities():
    return db.session.query(CTCFacility).all()
    
def get_ctc_facility(id):
    return db.session.query(CTCFacility).filter_by(CTCFacilityID = id).first()
    
def get_facilities():
    return db.session.query(Facility).all()
    
def get_facility(id):
    return db.session.query(Facility).filter_by(facilityID= id).first()
    
def get_facility_phones():
    return db.session.query(FacilityPhone).all()
    
def get_facility_phone(id):
    return db.session.query(FacilityPhone).filter_by(facilityPhoneID = id).first()
    
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

def get_human_subject_trainings():
    return db.session.query(HumanSubjectTrainingLUT).all()
    
def get_human_subject_training(id):
    return db.session.query(HumanSubjectTrainingLUT).filter_by(humanSubjectTrainingID = id).first()
    
def get_informants():
    return db.session.query(Informant).all()
    
def get_informant(id):
    return db.session.query(Informant).filter_by(informantID = id).first()
    
def get_informant_addresses():
    return db.session.query(InformantAddress).all()
    
def get_informant_address(id):
    return db.session.query(InformantAddress).filter_by(informantAddressID = id).first()    
    
def get_informant_phones():
    return db.session.query(InformantPhone).all()
    
def get_informant_phone(id):
    return db.session.query(InformantPhone).filter_by(informantPhoneID = id).first()
    
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
    return db.session.query(LogSubjectLUT).filter_by(logSubjectLUTID = id).first()
    
def get_patients():
    return db.session.query(Patient).all()
    
def get_patient(id):
    return db.session.query(Patient).filter_by(patAutoID = id).first()

def get_patient_addresses():
    return db.session.query(PatientAddress).all()
    
def get_patient_address(id):
    return db.session.query(PatientAddress).filter_by(patAddressID = id).first()

def get_patient_emails():
    return db.session.query(PatientEmail).all()
    
def get_patient_email(id):
    return db.session.query(PatientEmail).filter_by(emailID = id).first()

def get_patient_phones():
    return db.session.query(PatientPhone).all()
    
def get_patient_phone(id):
    return db.session.query(PatientPhone).filter_by(patPhoneID = id).first()

def get_patient_project_statuses():
    return db.session.query(PatientProjectStatus).all()
    
def get_patient_project_status(id):
    return db.session.query(PatientProjectStatus).filter_by(patientProjectStatusID = id).first()

def get_patient_project_status_types():
    return db.session.query(PatientProjectStatusLUT).all()
    
def get_patient_project_status_type(id):
    return db.session.query(PatientProjectStatusLUT).filter_by(patientProjectStatusTypeID=id).first()
    
def get_phase_statuses():
    return db.session.query(PhaseStatus).all()
    
def get_phase_status(id):
    return db.session.query(PhaseStatus).filter_by(logPhaseID=id).first()

def get_physicians():
    return db.session.query(Physician).all()
    
def get_physician(id):
    return db.session.query(Physician).filter_by(physicianID = id).first()
    
def get_physician_to_ctcs():
    return db.session.query(PhysicianToCTC).all()
    
def get_physician_to_ctc(id):
    return db.session.query(PhysicianToCTC).filter_by(physicianCTCID = id).first()
    
def get_pre_applications():
    return db.session.query(PreApplication).all()
    
def get_pre_application(id):
    return db.session.query(PreApplication).filter_by(preApplicationID=id).first()
    
def get_project(id):
    return Project.query.filter_by(projectID=id).first()
    
def get_projects():
    return db.session.query(Project).all()

def get_project_patients():
    return db.session.query(ProjectPatient).all()
    
def get_project_patient(id):
    return db.session.query(ProjectPatient).filter_by(participantID = id).first()

def get_project_staffs():
    return db.session.query(ProjectStaff).all()
    
def get_project_staff(id):
    return db.session.query(ProjectStaff).filter_by(projectStaffID = id).first()
    
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

def get_staffs():
    return db.session.query(Staff).all()
    
def get_staff(id):
    return db.session.query(Staff).filter_by(staffID = id).first()

def get_staff_roles():
    return db.session.query(StaffRoleLUT).all()
    
def get_staff_role(id):
    return db.session.query(StaffRoleLUT).filter_by(staffRoleLUTID = id).first()
    
def get_staff_trainings():
    return db.session.query(StaffTraining).all()
    
def get_staff_training(id):
    return db.session.query(StaffTraining).filter_by(staffTrainingID = id).first()
    
def get_tracings():
    return db.session.query(Tracing).all()
    
def get_tracing(id):
    return db.session.query(Tracing).filter_by(tracingID = id).first()
    
def get_tracing_sources():
    return db.session.query(TracingSourceLUT).all()
    
def get_tracing_source(id):
    return db.session.query(TracingSourceLUT).filter_by(tracingSourceLUTID = id).first()
     
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