import json
import datetime
from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from app.database import db
from app.helpers import DateTimeEncoder

STATES = db.Enum("AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "DC",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY"
            )
RACES = db.Enum("white", "black")
ETHNICITIES = db.Enum("hispanic", "non-hispanic")
PHONE_SOURCES = db.Enum("s1", "s2")
SEXES = db.Enum("male", "female")
VITAL_STATUSES = db.Enum("v1","v2")
CONTACTS = db.Enum("yes","no")
INACTIVES = db.Enum("yes", "no")
ADDRESS_STATUS_SOURCE = db.Enum("s1", "s2")

            
"""
    A base class that all models derive from
"""
class CustomModel(db.Model):
    __abstract__ = True
    #def __init__(self):
    #    super(CustomModel,self).__init__()
        
    def dict(self):
        items = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return items
    
    def json(self):
        return jsonify(self.dict())
            
##############################################################################
# Models
##############################################################################  

class ArcReview(CustomModel):
    __tablename__ = 'arcReview'

    arcReviewID = db.Column(db.Integer, primary_key=True)
    projectID = db.Column(db.Integer, db.ForeignKey('project.projectID'))
    review_type = db.Column(db.Integer)
    date_sent_to_reviewer = db.Column(db.Date)
    reviewer1 = db.Column(db.Integer)
    reviewer1_rec = db.Column(db.Integer)
    reviewer1_sig_date = db.Column(db.Date)
    reviewer1_comments = db.Column(db.String)
    reviewer2 = db.Column(db.Integer)
    reviewer2_rec = db.Column(db.Integer)
    reviewer2_sig_date = db.Column(db.Date)
    reviewer2_comments = db.Column(db.String)
    research = db.Column(db.Integer)
    contact = db.Column(db.Boolean)
    lnkage = db.Column(db.Boolean)
    engaged = db.Column(db.Boolean)
    non_public_data = db.Column(db.Boolean)
    
    # Relationships
    # 1-1
    project = db.relationship('Project', back_populates='arcReview')
    
    def __repr__(self):
        return "<ArcReview(\
        arcReviewID = {},\
        projectID = {},\
        review_type = {},\
        date_sent_to_reviewer = {},\
        reviewer1 = {},\
        reviewer1_rec = {},\
        reviewer1_sig_date = {},\
        reviewer1_comments = {},\
        reviewer2 = {},\
        reviewer2_rec = {},\
        reviewer2_sig_date = {},\
        reviewer2_comments = {},\
        research = {},\
        contact = {},\
        lnkage = {},\
        engaged = {},\
        non_public_date = {})>".format(
        self.arcReviewID,
        self.projectID,
        self.review_type,
        self.date_sent_to_reviewer,
        self.reviewer1,
        self.reviewer1_rec,
        self.reviewer1_sig_date,
        self.reviewer1_comments,
        self.reviewer2,
        self.reviewer2_rec,
        self.reviewer2_sig_date,
        self.reviewer2_comments,
        self.research,
        self.contact,
        self.lnkage,
        self.engaged,
        self.non_public_data)
    
class Budget(CustomModel):
    __tablename__ = "budget"
    
    budgetID = db.Column(db.Integer, primary_key=True)
    projectID = db.Column(db.Integer,db.ForeignKey('project.projectID'))
    numPeriods = db.Column(db.Integer)
    periodStart = db.Column(db.Date)
    periodEnd = db.Column(db.Date)
    periodTotal = db.Column(db.Float)
    periodComment = db.Column(db.String)
    
    # Relationships
    # 1 - M, 1 project, many budgets
    project = db.relationship("Project",back_populates="budgets")
    
    def __repr__(self):
        return "<Budget(\
            budgetID = {},\
            projectID = {},\
            numPeriods = {},\
            periodStart = {},\
            periodEnd = {},\
            periodTotal = {},\
            periodComment = {})>".format(
            self.budgetID,
            self.projectID,
            self.numPeriods,
            self.periodStart,
            self.periodEnd,
            self.periodTotal,
            self.periodComment)

class Contact(CustomModel):
    __tablename__ = 'contact'
    
    contactID = db.Column(db.Integer, primary_key=True)
    contactTypeLUTID = db.Column(db.Integer, db.ForeignKey("contactTypeLUT.contactTypeLUTID"))
    projectPatientID = db.Column(db.Integer, db.ForeignKey("projectPatient.participantID"))
    staffID = db.Column(db.Integer, db.ForeignKey("staff.staffID"))
    informantID = db.Column(db.Integer, db.ForeignKey("informant.informantID"))
    facilityID = db.Column(db.Integer, db.ForeignKey("facility.facilityID"))
    physicianID = db.Column(db.Integer, db.ForeignKey("physician.physicianID"))
    description = db.Column(db.String)
    contact_date = db.Column(db.Date)
    initials = db.Column(db.String)
    notes = db.Column(db.String)
    
    # Relastionships
    # M - 1, many contacts can have the same type
    contactType = db.relationship("ContactTypeLUT", back_populates="contacts")
    # M - 1, many contacts may have the same patient
    projectPatient = db.relationship("ProjectPatient",back_populates = "contacts")
    # M - 1 many contacts can have the same staff
    staff = db.relationship("Staff", back_populates="contacts")
    # M - 1, many contacts can have the same informant
    informant = db.relationship("Informant",back_populates="contacts")
    # M - 1, many contacts may have the same facility
    facility = db.relationship("Facility",back_populates="contacts")
    # M - 1, many contacts may have the same facility
    physician = db.relationship("Physician", back_populates="contacts")
    
    def __repr__(self):
        return "<Contact(\
        contactID = {},\
        contactTypeLUTID = {},\
        projectPatientID = {},\
        staffID = {},\
        informantID = {},\
        facilityID = {},\
        physicianID = {},\
        description = {},\
        contact_date = {},\
        initials = {},\
        notes = {})>".format(
        
        contactID,
        contactTypeLUTID,
        projectPatientID,
        staffID,
        informantID,
        facilityID,
        physicianID,
        description,
        contact_date,
        initials,
        notes)
            
class ContactInfoSourceLUT(CustomModel):
    __tablename__ = "contactInfoSourceLUT"
    
    contactInfoSourceLUTID = db.Column(db.Integer, primary_key=True)
    contact_info_source = db.Column(db.String)
    
    def __repr__(self):
        return "<ContactInfoSourceLUT(\
        contactInfoSourceLUTID = {},\
        contact_info_source = {})>".format(
        self.contactInfoSourceLUTID,
        self.contact_info_source)
            
class ContactInfoStatusLUT(CustomModel):
    __tablename__ = "contactInfoStatusLUT"
    
    contactInfoStatusID = db.Column(db.Integer, primary_key=True)
    contact_info_status = db.Column(db.String)
    
    def __repr__(self):
        return "<ContactInfoStatus(\
        contactInfoStatusID = {},\
        contact_info_status = {})>".format(
        self.contactInfoStatusID,
        self.contact_info_status)

class ContactTypeLUT(CustomModel):
    __tablename__ = "contactTypeLUT"
    
    contactTypeLUTID = db.Column(db.Integer, primary_key=True)
    contact_definition = db.Column(db.String)
    
    # Relationships
    # M - 1, many contacts can have the same type
    contacts = db.relationship("Contact",back_populates="contactType")
    
    def __repr__(self):
        return "<ContactTypeLUT(\
        contactTypeLUTID = {},\
        contact_definition = {})>".format(
        self.contactTypeLUTID,
        self.contact_definition)
        
class CTC(CustomModel):
    __tablename__ = 'ctc'
    
    ctcID = db.Column(db.Integer, primary_key=True)
    patientID = db.Column(db.Integer, db.ForeignKey('patient.patAutoID'))
    dx_date = db.Column(db.Date)
    site = db.Column(db.Integer)
    histology = db.Column(db.String)
    behavior = db.Column(db.String)
    ctc_sequence = db.Column(db.String)
    stage = db.Column(db.String)
    dx_age = db.Column(db.Integer)
    dx_street1 = db.Column(db.String)
    dx_street2 = db.Column(db.String)
    dx_city = db.Column(db.String)
    cx_state = db.Column(db.String)
    dx_zip = db.Column(db.Integer)
    dx_county = db.Column(db.String)
    dnc = db.Column(db.String)
    dnc_reason = db.Column(db.String)
    
    # Relationship
    # 1 - 1, one ctc per projectPatient
    projectPatient = db.relationship("ProjectPatient",back_populates="ctc")
    #TODO Guessing 1-1 but can't tell
    patient = db.relationship('Patient', back_populates='ctc')
    # M - 1
    ctcFacility = db.relationship("CTCFacility",back_populates="ctc")
    # 
    physicianToCTC = db.relationship("PhysicianToCTC",back_populates="ctc")
    
    def __repr__(self):
        return "<CTC(\
        ctcID = {},\
        patientID = {},\
        dx_date = {},\
        site = = {},\
        histology = = {},\
        behavior = = {},\
        ctc_sequence = = {},\
        stage = = {},\
        dx_age = = {},\
        dx_street1 = = {},\
        dx_street2 = = {},\
        dx_city = = {},\
        cx_state = = {},\
        dx_zip = = {},\
        dx_county = = {},\
        dnc = = {},\
        dnc_reason = {})>".format(
        self.ctcID,
        self.patientID,
        self.dx_date,
        self.site,
        self.histology, 
        self.behavior, 
        self.ctc_sequence, 
        self.stage,
        self.dx_age,
        self.dx_street1,
        self.dx_street2,
        self.dx_city,
        self.cx_state, 
        self.dx_zip,
        self.dx_county, 
        self.dnc,
        self.dnc_reason)

class CTCFacility(CustomModel):
    __tablename__ = 'CTCFacility'
    
    CTCFacilityID = db.Column(db.Integer,primary_key=True)
    ctcID = db.Column(db.Integer, db.ForeignKey('ctc.ctcID'))
    facilityID = db.Column(db.Integer, db.ForeignKey('facility.facilityID'))
    
    # Relationships
    # 1 - M, one facilty may have many CTCFacilities
    facility = db.relationship("Facility",back_populates="ctcFacilities")
    # M - 1,many ctc to one ctcfacility
    ctc = db.relationship("CTC",back_populates="ctcFacility")
    
    def __repr__(self):
        return "<CTCFacility(\
        CTCFacilityID = {},\
        ctcID = {},\
        facilityID = {})>".format(
        self.CTCFacilityID,
        self.ctcID,
        self.facilityID)
        
class Facility(CustomModel):
    __tablename__ = "facility"
    
    facilityID = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String)
    contact_fname = db.Column(db.String)
    contact_lname = db.Column(db.String)
    facility_status = db.Column(db.Integer)
    facility_status_date = db.Column(db.Date)
    contact2_fname = db.Column(db.String)
    contact2_lname = db.Column(db.String)
    
    # Relationships
    # M - 1, many facilities can have the same phone
    facilityPhone = db.relationship("FacilityPhone", back_populates = "facilities")
    facilityAddress = db.relationship("FacilityAddress", back_populates = "facilities")
    # M - 1, many contacts may have the same facility
    contacts = db.relationship('Contact',back_populates="facility")
    # 1 - M, one facility may have many CTCFacility
    ctcFacilities = db.relationship("CTCFacility",back_populates="facility")
    # M - 1
    physicianFacility = db.relationship("PhysicianFacility",back_populates="facilities")
    
    def __repr__(self):
        return "<Facility(\
        facilityID = {},\
        facility_name = {},\
        contact_fname = {},\
        contact_lname = {},\
        facility_status = {},\
        facility_status_date = {},\
        contact2_fname = {},\
        contact2_lname = {})>".format(
        self.facilityID,
        self.facility_name,
        self.contact_fname,
        self.contact_lname,
        self.facility_status,
        self.facility_status_date,
        self.contact2_fname,
        self.contact2_lname)

class FacilityAddress(CustomModel):
    __tablename__ = 'facilityAddress'
    
    facilityAddressID = db.Column(db.Integer, primary_key=True)
    contactInfoSourceLUTID = db.Column(db.Integer, db.ForeignKey("contactInfoSourceLUT.contactInfoSourceLUTID"))
    facilityID = db.Column(db.Integer, db.ForeignKey("facility.facilityID"))
    contactInfoStatusLUTID = db.Column(db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    street = db.Column(db.String)
    street2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.Integer)
    addresss_status = db.Column(db.Integer)
    address_status_date = db.Column(db.Date)
    address_status_source = db.Column(ADDRESS_STATUS_SOURCE)
    
    # Relationships
    # M - 1, many facilities can be at the same address
    facilities = db.relationship("Facility",back_populates="facilityAddress")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "FacilityAddress(\
        facilityAddressID = {},\
        contactInfoSourceLUTID  = {},\
        facilityID = {},\
        contactInfoStatusLUTID = {},\
        street = {},\
        street2  = {},\
        city = {},\
        state = {},\
        zip = {},\
        addresss_status = {},\
        address_status_date = {},\
        address_status_source = {})>".format(
        self.facilityAddressID,
        self.contactInfoSourceLUTID ,
        self.facilityID,
        self.contactInfoStatusLUTID,
        self.street,
        self.street2 ,
        self.city,
        self.state,
        self.zip,
        self.addresss_status,
        self.address_status_date,
        self.address_status_source)
        
class FacilityPhone(CustomModel):
    __tablename__ = 'facilityPhone'
    
    facilityPhoneID = db.Column(db.Integer, primary_key=True)
    contactInfoSourcelUTID = db.Column(db.Integer, db.ForeignKey('contactInfoSourceLUT.contactInfoSourceLUTID'))
    contactInfoStatusLUTID = db.Column(db.Integer, db.ForeignKey('contactInfoStatusLUT.contactInfoStatusID'))
    facilityID = db.Column(db.Integer, db.ForeignKey('facility.facilityID'))
    facility_phone = db.Column(db.Integer)
    facility_name = db.Column(db.String)
    clinic_name = db.Column(db.String)
    facility_phone_type = db.Column(db.String)
    facility_phone_status = db.Column(db.Integer)
    facility_phone_source = db.Column(db.Integer)
    facility_phone_status_date = db.Column(db.Date)
    
    # Relationships
    # M - 1, many patients can be at the same phone
    facilities = db.relationship("Facility", back_populates = "facilityPhone")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "<FacilityPhone(\
        facilityPhoneID = {},\
        contactInfoSourcelUTID = {},\
        contactInfoStatusLUTID = {},\
        facilityID = {},\
        facility_phone = {},\
        facility_name = {},\
        clinic_name = {},\
        facility_phone_type = {},\
        facility_phone_status = {},\
        facility_phone_source = {},\
        facility_phone_status_date = {})>".format(
        facilityPhoneID,
        contactInfoSourcelUTID,
        contactInfoStatusLUTID,
        facilityID,
        facility_phone,
        facility_name,
        clinic_name,
        facility_phone_type,
        facility_phone_status,
        facility_phone_source,
        facility_phone_status_date)
    
class Funding(CustomModel):
    __tablename__ = "funding"
    
    fundingID = db.Column(db.Integer, primary_key=True)
    grantStatusLUTID = db.Column(db.Integer, db.ForeignKey('grantStatusLUT.grantStatusLUTID'))
    projectID = db.Column(db.Integer,db.ForeignKey('project.projectID'))
    fundingSourceLUTID = db.Column(db.Integer,db.ForeignKey('fundingSourceLUT.fundingSourceLUTID'))
    primary_funding_source = db.Column(db.String)
    secondary_funding_source = db.Column(db.String)
    funding_number = db.Column(db.String)
    grant_title = db.Column(db.String)
    grantStatusID = db.Column(db.Integer)
    date_status = db.Column(db.Date)
    grant_pi = db.Column(db.Integer)
    primary_chartfield = db.Column(db.String)
    secondary_chartfield = db.Column(db.String)
    
    # Relationships
    # M - 1, many fundings with the same source
    fundingSource = db.relationship("FundingSourceLUT", foreign_keys=[fundingSourceLUTID],back_populates="fundings")
    # M - 1, many fundings with the same grant status
    grantStatus = db.relationship("GrantStatusLUT",foreign_keys=[grantStatusLUTID],back_populates="fundings")
    # 1 - M, one project with many fundings
    project = db.relationship("Project",back_populates="fundings")

    def __repr__(self):
        return "<Funding(\
            fundingID = {},\
            grantStatusLUTID = {},\
            projectID = {},\
            fundingSourceLUTID = {},\
            primary_funding_source = {},\
            secondary_funding_source = {},\
            funding_number = {},\
            grant_title = {},\
            grantStatusID = {},\
            date_status = {},\
            grant_pi = {},\
            primary_chartfield = {},\
            secondary_chartfield = {})>".format(
            self.fundingID,
            self.grantStatusLUTID,
            self.projectID,
            self.fundingSourceLUTID,
            self.primary_funding_source,
            self.secondary_funding_source,
            self.funding_number,
            self.grant_title,
            self.grantStatusID,
            self.date_status,
            self.grant_pi,
            self.primary_chartfield,
            self.secondary_chartfield)
            
class FundingSourceLUT(CustomModel):
    __tablename__ = 'fundingSourceLUT'
    
    fundingSourceLUTID = db.Column(db.Integer,primary_key=True)
    fundingSource = db.Column(db.String)
    
    # Relationships
    # M - 1, many fundings with the same source
    fundings = db.relationship("Funding",back_populates="fundingSource")
    
    def __repr__(self):
        return "<FundingSourceLUT(\
        fundingSourceLUTID = {},\
        fundingSource = {})>".format(
        self.fundingSourceLUTID,
        self.fundingSource)
            
class GrantStatusLUT(CustomModel):
    __tablename__ = 'grantStatusLUT'
    
    grantStatusLUTID = db.Column(db.Integer, primary_key=True)
    grant_status = db.Column(db.String)
    
    # Relationships
    # M - 1, many fundings with the same grant status
    fundings = db.relationship("Funding",back_populates="grantStatus")
    
    def __repr__(self):
        return "<GrantStatusLUT(\
            grantStatusLUTID = {}\
            grant_status = {})>".format(
            self.grantStatusLUTID,
            self.grant_status)
            
class HumanSubjectTrainingLUT(CustomModel):
    __tablename__ = 'humanSubjectTrainingLUT'
    
    human_sub_type_id = db.Column(db.Integer, primary_key=True)
    training_type = db.Column(db.String)
    
    # Relationships
    # M - 1, many staff trainings with the same HST
    staffTrainings = db.relationship('StaffTraining',back_populates="humanSubjectTraining")
    
    def __repr__(self):
        return "<HumanSubjectTrainginLUT(\
        human_sub_type_id = {},\
        training_type = {})>".format(
        self.human_sub_type_id,
        self.training_type)
            
class IRBHolderLUT(CustomModel):
    __tablename__ = 'IRBHolderLUT'
    
    irbHolderID = db.Column(db.Integer,primary_key=True)
    irb_holder = db.Column(db.String)
    irb_holder_definition = db.Column(db.String)
    
    # Relationships
    # M - 1, Many projects with the same IRB
    projects = db.relationship("Project",back_populates="irbHolder")
    
    def __repr__(self):
        return "<IRBHolderLUT(\
            irbHolderID = {},\
            irb_holder = {},\
            irb_holder_definition = {})>".format(
            self.irbHolderID,
            self.irb_holder,
            self.irb_holder_definition)

class Informant(CustomModel):
    __tablename__ = "informant"
    
    informantID = db.Column(db.Integer, primary_key=True)
    patAutoID = db.Column(db.Integer, db.ForeignKey("patient.patAutoID"))
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    middle_name = db.Column(db.String)
    informant_primary = db.Column(db.String)
    informant_relationship = db.Column(db.String)
    notes = db.Column(db.String)
    
    # Relationships
    # 1 - M, one patient may have multiple informants
    patients = db.relationship("Patient",back_populates= "informant")
    # 1 - M, one informant may have muleple addresses/phones
    informantAddresses = db.relationship("InformantAddress")
    informantPhones = db.relationship("InformantPhone")
    # M - 1, many contacts can have the same informant
    contacts = db.relationship("Contact",back_populates="informant")
    
    
    def __repr__(self):
        return "<Informant(\
        informantID = {},\
        patientID = {},\
        fname = {},\
        lname = {},\
        middle_name = {},\
        informant_primary = {},\
        informant_relationship = {},\
        notes = {})>".format(
        self.informantID,
        self.patientID,
        self.fname,
        self.lname,
        self.middle_name,
        self.informant_primary,
        self.informant_relationship,
        self.notes)

class InformantAddress(CustomModel):
    __tablename__ = 'informantAddress'
    
    informantAddressID = db.Column(db.Integer, primary_key=True)
    contactInfoSourceLUTID = db.Column(db.Integer, db.ForeignKey('contactInfoSourceLUT.contactInfoSourceLUTID'))
    contactInfoStatusID = db.Column(db.Integer, db.ForeignKey('contactInfoStatusLUT.contactInfoStatusID'))
    informantID = db.Column(db.Integer, db.ForeignKey('informant.informantID'))
    street = db.Column(db.String)
    street2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
    address_status = db.Column(db.Integer)
    address_status_date = db.Column(db.Date)
    address_status_source = db.Column(ADDRESS_STATUS_SOURCE)
    
    # Relationships
    # 1 - M, one informant may have multiple addresses
    informant = db.relationship("Informant", back_populates = "informantAddresses")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "<InformantAddress(\
        informantAddressID = {},\
        contactInfoSourceLUTID = {},\
        contactInfoStatusID = {},\
        informantID = {},\
        street = {},\
        street2 = {},\
        city = {},\
        state = {}.\
        zip = {},\
        address_status = {},\
        address_status_date = {},\
        address_status_source = {})>".format(
        self.informantAddressID,
        self.contactInfoSourceLUTID,
        self.contactInfoStatusID,
        self.informantID,
        self.street,
        self.street2,
        self.city,
        self.state,
        self.zip,
        self.address_status,
        self.address_status_date,
        self.address_status_source)

class InformantPhone(CustomModel):
    __tablename__ = 'informantPhone'
    
    informantPhoneID = db.Column(db.Integer, primary_key=True)
    contactInfoSourceLUTID = db.Column(db.Integer, db.ForeignKey("contactInfoSourceLUT"))
    informantID = db.Column(db.Integer,db.ForeignKey("informant.informantID"))
    contactInfoStatusID = db.Column(db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    phone = db.Column(db.String)
    phone_source = db.Column(PHONE_SOURCES)
    phone_status = db.Column(db.Integer)
    phone_status_date = db.Column(db.Date)
    
    # Relationships
    # 1 - M, one informant may have multiple phones
    informant = db.relationship("Informant",back_populates="informantPhones")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "<InformantPhone(\
        informantPhoneID = {},\
        contactInfoSourceLUTID = {},\
        informantID = {},\
        contactInfoStatusID = {},\
        phone = {},\
        phone_source = {},\
        phone_status = {},\
        phone_status_date = {})>".format(
        self.informantPhoneID,
        self.contactInfoSource,
        self.informantID,
        self.contactInfoStatusID,
        self.phone,
        self.phone_source,
        self.phone_status,
        self.phoen_status_date)
        
class Log(CustomModel):
    __tablename__ = 'log'
    
    logID = db.Column(db.Integer, primary_key=True)
    logSubjectLUTID = db.Column(db.Integer, db.ForeignKey('logSubjectLUT.logSubjectLUTID'))
    projectID = db.Column(db.Integer, db.ForeignKey('project.projectID'))
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    phaseStatusID = db.Column(db.Integer, db.ForeignKey('phaseStatus.logPhaseID'))
    note = db.Column(db.String)
    date = db.Column(db.Date)
    
    # Relationships
    # M - 1, many logs with the same subject
    logSubject = db.relationship("LogSubjectLUT", back_populates="logs")
    # M - 1, many logs with the same subject
    phaseStatus = db.relationship("PhaseStatus", back_populates="logs")
    # 1 - M, one staff with many logs
    staff = db.relationship("Staff", back_populates="logs")
    # 1 - M, one project with many logs
    project = db.relationship("Project",back_populates="logs")
    
    def __repr__(self):
        return "<Log<(\
        logID = {},\
        logSubjectLUTID = {},\
        projectID = {},\
        staffID = {},\
        phaseStatus = {},\
        note = {},\
        date = {})>".format(
        self.logID,
        self.logSubjectLUTID,
        self.projectID,
        self.staffID,
        self.phaseStatusID,
        self.note,
        self.date)
        
class LogSubjectLUT(CustomModel):
    __tablename__ = 'logSubjectLUT'
    
    logSubjectLUTID = db.Column(db.Integer, primary_key=True)
    log_subject = db.Column(db.String)
    
    # Relationships
    # M - 1, many logs with the same subject
    logs = db.relationship("Log",back_populates="logSubject")
    
    def __repr(self):
        return "<LogSubject(\
        logSubjectLUTID = {},\
        log_subject = {})>".format(
        self.logSubjectLUTID,
        self.log_subject)
 
class Patient(CustomModel):
    __tablename__ = 'patient'
    
    patAutoID = db.Column(db.Integer, primary_key=True)
    patID = db.Column(db.String)
    recordID = db.Column(db.Integer)
    ucrDistID = db.Column(db.Integer)
    UPDBID = db.Column(db.Integer)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    middle_name = db.Column(db.String)
    maiden_name = db.Column(db.String)
    alias_fname = db.Column(db.String)
    alias_lname = db.Column(db.String)
    alias_middle_name = db.Column(db.String)
    dob = db.Column(db.Date)
    SSN = db.Column(db.Integer)
    sex = db.Column(SEXES)
    race = db.Column(RACES)
    ethnicity = db.Column(ETHNICITIES)
    vital_status = db.Column(VITAL_STATUSES)
    
    # Relationships
    # M - 1, many patients can be at the same address
    patientAddress = db.relationship('PatientAddress',back_populates="patients")
    #TODO 1 - 1 Guess? can't tell from schematic 
    ctc = db.relationship('CTC',uselist=False,back_populates="patient")
    # M - 1, many patients can be at the same email
    patientEmail = db.relationship('PatientEmail',back_populates="patients")
    # M - 1, many patients can be at the same phone
    patientPhone = db.relationship('PatientPhone',back_populates="patients")
    # M - 1, many informants may have multiple patients
    informant = db.relationship('Informant',back_populates="patients")
    
    def __repr__(self):
        return "<Patient(\
        patAutoID = {},\
        patID = {},\
        recordID = {},\
        ucrDistID = {},\
        UPDBID = {},\
        fname = {},\
        lname = {},\
        middle_name = {},\
        maiden_name = {},\
        alias_fname = {},\
        alias_lname = {},\
        alias_middle_name = {},\
        dob = {},\
        SSN = {},\
        sex = {},\
        race = {},\
        ethnicity = {},\
        vital_status = {})>".format(
        self.patAutoID,
        self.patID,
        self.recordID,
        self.ucrDistID,
        self.UPDBID,
        self.fname,
        self.lname,
        self.middle_name,
        self.maiden_name,
        self.alias_fname,
        self.alias_lname,
        self.alias_middle_name,
        self.dob,
        self.SSN,
        self.sex,
        self.race,
        self.ethnicity,
        self.vital_status)

class PatientAddress(CustomModel):
    __tablename__  = "patientAddress"
    
    patAddressID = db.Column(db.Integer, primary_key=True)
    contactInfoSourceLUTID = db.Column(db.Integer, db.ForeignKey("contactInfoSourceLUT.contactInfoSourceLUTID"))
    patientID = db.Column(db.Integer, db.ForeignKey("patient.patAutoID"))
    contactInfoStatusLUTID = db.Column(db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    street = db.Column(db.String)
    street2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.Integer)
    address_status = db.Column(db.Integer)
    address_status_date = db.Column(db.Date)
    address_status_source = db.Column(ADDRESS_STATUS_SOURCE)
    
    # Relationships
    patients = db.relationship("Patient",back_populates="patientAddress")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "PatientAddress(\
        patAddressID = {},\
        contactInfoSourceLUTID  = {},\
        patientID = {},\
        contactInfoStatusLUTID = {},\
        street = {},\
        street2  = {},\
        city = {},\
        state = {},\
        zip = {},\
        addresss_status = {},\
        address_status_date = {},\
        address_status_source = {})>".format(
        self.patAddressID,
        self.contactInfoSourceLUTID ,
        self.patientID,
        self.contactInfoStatusLUTID,
        self.street,
        self.street2 ,
        self.city,
        self.state,
        self.zip,
        self.addresss_status,
        self.address_status_date,
        self.address_status_source)
        
class PatientEmail(CustomModel):
    __tablename__ = 'patientEmail'
    
    emailID = db.Column(db.Integer,primary_key=True)
    contactInfoSourceLUTID = db.Column(db.Integer, db.ForeignKey("contactInfoSourceLUT.contactInfoSourceLUTID"))
    patientID = db.Column(db.Integer, db.ForeignKey("patient.patAutoID"))
    contactInfoStatusID = db.Column(db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    email = db.Column(db.String)
    email_status = db.Column(db.Integer)
    email_source = db.Column(db.Integer)
    email_status_date = db.Column(db.Date)
    
    # Relationships
    # 1 - M, one patient may have multiple emails
    patients = db.relationship("Patient",back_populates="patientEmail")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "<PatientEmail(\
        emailID = {},\
        contactInfoSourceLUTID = {},\
        patientID = {},\
        contactInfoStatusID = {},\
        email = {},\
        email_status = {},\
        email_source = {},\
        email_status_date = {})>".format(
        self.emailID,
        self.contactInfoSourceLUTID,
        self.patientID,
        self.contactInfoStatus,
        self.email,
        self.email_status,
        self.email_source,
        self.email_status_date)

class PatientPhone(CustomModel):
    __tablename__ = 'patientPhone'
    
    patPhoneID = db.Column(db.Integer, primary_key=True)
    contactInfoSourceLUTID = db.Column(db.Integer, db.ForeignKey("contactInfoSourceLUT"))
    patientID = db.Column(db.Integer,db.ForeignKey("patient.patAutoID"))
    contactInfoStatusID = db.Column(db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    phone = db.Column(db.String)
    phone_source = db.Column(PHONE_SOURCES)
    phone_status = db.Column(db.Integer)
    phone_status_date = db.Column(db.Date)
    
    # Relationships
    # M - 1, many patients can be at the same phone
    patients = db.relationship("Patient",back_populates="patientPhone")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "<PatientPhone(\
        patPhoneID = {},\
        contactInfoSourceLUTID = {},\
        patientID = {},\
        contactInfoStatusID = {},\
        phone = {},\
        phone_source = {},\
        phone_status = {},\
        phone_status_date = {})>".format(
        self.patPhoneID,
        self.contactInfoSource,
        self.patientID,
        self.contactInfoStatusID,
        self.phone,
        self.phone_source,
        self.phone_status,
        self.phoen_status_date)

class PatientProjectStatus(CustomModel):
    __tablename__ = 'patientProjectStatus'
    
    patientProjectStatusID = db.Column(db.Integer, primary_key=True)
    patientProjectStatusLUTID = db.Column(db.Integer, db.ForeignKey('patientProjectStatusLUT.idpatientProjectStatusLUT'))
    projectPatientID = db.Column(db.Integer, db.ForeignKey('projectPatient.participantID'))
    
    # Relationships
    # M - 1, many patientProjectStatuses with same ppsLUT
    patientProjectStatus = db.relationship("PatientProjectStatusLUT", back_populates = "patientProjectStatuses")
    # 1 - M, one project Patient has many statuses
    projectPatient = db.relationship("ProjectPatient", back_populates ="patientProjectStatuses")
    
    def __repr__(self):
        return "<PatientProjectStatus(\
        patientProjectStatusID = {},\
        patientProjectStatusLUTID = {},\
        projectPatientID = {})>".format(
        self.patientProjectStatusID,
        self.patientProjectStatusLUTID,
        self.projectPatientID)
        
class PatientProjectStatusLUT(CustomModel):
    __tablename__ = 'patientProjectStatusLUT'
    
    idpatientProjectStatusLUT = db.Column(db.Integer, primary_key=True)
    status_description = db.Column(db.String)
    
    # Relationships
    # M - 1, many pps with same ppsLUT
    patientProjectStatuses = db.relationship("PatientProjectStatus",back_populates="patientProjectStatus")
    
    def __repr__(self):
        return "<PatientProjectStatusLUT(\
        idpatientProjectStatusLUT = {}\
        status_description = {})>".format(
        idpatientProjectStatusLUT,
        status_description)
    
class PhaseStatus(CustomModel):
    __tablename__ = 'phaseStatus'
    
    logPhaseID = db.Column(db.Integer, primary_key=True)
    phase_status = db.Column(db.String)
    phase_description = db.Column(db.String)
    
    # Relationships
    # M - 1, many logs with the same phase
    logs = db.relationship("Log",back_populates="phaseStatus")
    
    def __repr__(self):
        return "<PhaseStatus(\
        logPhaseID = {},\
        phase_status = {},\
        phase_description = {})>".format(
        self.logPhaseID,
        self.phase_status,
        self.phase_description)

class Physician(CustomModel):
    __tablename__ = "physician"
    
    physicianID = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    middle_name = db.Column(db.String)
    credentials = db.Column(db.String)
    specialty = db.Column(db.String)
    alias_fname = db.Column(db.String)
    alias_lname = db.Column(db.String)
    alias_middle_name = db.Column(db.String)
    physician_status = db.Column(db.Integer)
    physician_status_date = db.Column(db.Date)
    email = db.Column(db.String)
    
    # Relationships
    # M - 1, many physicians can be at the same address
    physicianAddress = db.relationship("PhysicianAddress",back_populates="physicians")
    # M - 1, many physicians can have the same phone
    physicianPhone = db.relationship("PhysicianPhone",back_populates="physicians")
    # M - 1, many phys at same facility
    physicianFacility = db.relationship("PhysicianFacility", back_populates="physicians")
    # M - 1
    physicianToCTC = db.relationship("PhysicianToCTC", back_populates="physicians")
    # M - 1, many contacts may have the same facility
    contacts = db.relationship("Contact",back_populates="physician")
    
    
    def __repr__(self):
        return "<Physician(\
        physicianID = {},\
        fname = {},\
        lname = {},\
        middle_name = {},\
        credentials = {},\
        specialty = {},\
        alias_fname = {},\
        alias_lname = {},\
        alias_middle_name = {},\
        physician_status = {},\
        physician_status_date = {},\
        email = {})>".format(
        physicianID,
        fname,
        lname,
        middle_name,
        credentials,
        specialty,
        alias_fname,
        alias_lname,
        alias_middle_name,
        physician_status,
        physician_status_date,
        email)

class PhysicianAddress(CustomModel):
    __tablename__ = "physicianAddress"
    
    physicianAddressID = db.Column(db.Integer, primary_key=True)
    contactInfoSourceLUTID = db.Column(db.Integer, db.ForeignKey("contactInfoSourceLUT.contactInfoSourceLUTID"))
    physicianID = db.Column(db.Integer, db.ForeignKey("physician.physicianID"))
    contactInfoStatusLUTID = db.Column(db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    street = db.Column(db.String)
    street2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.Integer)
    addresss_status = db.Column(db.Integer)
    address_status_date = db.Column(db.Date)
    address_status_source = db.Column(ADDRESS_STATUS_SOURCE)
    
    # Relationship
    # M - 1, many physicians can be at the same address
    physicians = db.relationship("Physician",back_populates="physicianAddress")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "PhysicianAddress(\
        physicianAddressID = {},\
        contactInfoSourceLUTID  = {},\
        physicianID = {},\
        contactInfoStatusLUTID = {},\
        street = {},\
        street2  = {},\
        city = {},\
        state = {},\
        zip = {},\
        addresss_status = {},\
        address_status_date = {},\
        address_status_source = {})>".format(
        self.physicianAddressID,
        self.contactInfoSourceLUTID ,
        self.physicianID,
        self.contactInfoStatusLUTID,
        self.street,
        self.street2 ,
        self.city,
        self.state,
        self.zip,
        self.addresss_status,
        self.address_status_date,
        self.address_status_source)

class PhysicianFacility(CustomModel):
    __tablename__ = 'physicianFacility'
    
    physFacilityID = db.Column(db.Integer, primary_key=True)
    facilityID = db.Column(db.Integer, db.ForeignKey('facility.facilityID'))
    physicianID = db.Column(db.Integer, db.ForeignKey('physician.physicianID'))
    phys_facility_status = db.Column(db.Integer)
    phys_facility_status_date = db.Column(db.Date)
    
    # Relationships
    # M - 1 many physicians at the same physician facility
    physicians = db.relationship("Physician",back_populates="physicianFacility")
    # M - 1
    facilities = db.relationship("Facility",back_populates = "physicianFacility")
    
    def __repr__(self):
        return "<PhysicianFacility(\
        physFacilityID = {},\
        facilityID = {},\
        physicianID = {},\
        phys_facility_status = {},\
        phys_facility_status_date = {})>".format(
        self.physFacilityID,
        self.facilityID,
        self.physicianID,
        self.phys_facility_status,
        self.phys_facility_status_date)      
        
class PhysicianPhone(CustomModel):
    __tablename__ = "physicianPhone"
    
    physicianPhoneID = db.Column(db.Integer, primary_key=True)
    contactInfoSourceLUTID = db.Column(db.Integer, db.ForeignKey("contactInfoSourceLUT.contactInfoSourceLUTID"))
    physicianID = db.Column(db.Integer,db.ForeignKey("physician.physicianID"))
    contactInfoStatusID = db.Column(db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    phone = db.Column(db.String)
    phone_source = db.Column(PHONE_SOURCES)
    phone_status = db.Column(db.Integer)
    phone_status_date = db.Column(db.Date)
    
    # Relationship
    # M - 1, many physicians can be at the same phone
    physicians = db.relationship("Physician",back_populates="physicianPhone")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "<PhysicianPhone(\
        physicianPhoneID = {},\
        contactInfoSourceLUTID = {},\
        physicianID = {},\
        contactInfoStatusID = {},\
        phone = {},\
        phone_source = {},\
        phone_status = {},\
        phone_status_date = {})>".format(
        self.physicianPhoneID,
        self.contactInfoSource,
        self.physicianID,
        self.contactInfoStatusID,
        self.phone,
        self.phone_source,
        self.phone_status,
        self.phoen_status_date)
       
class PhysicianToCTC(CustomModel):
    __tablename__ = "physicianToCTC"
    
    physicianCTCID = db.Column(db.Integer, primary_key=True)
    physicianID = db.Column(db.Integer, db.ForeignKey('physician.physicianID'))
    ctcID = db.Column(db.Integer, db.ForeignKey('ctc.ctcID'))
    
    # Relationships
    # M - 1
    physicians = db.relationship("Physician",back_populates="physicianToCTC")
    # M - 1
    ctc = db.relationship("CTC",back_populates="physicianToCTC")
    
    def __repr__(self):
        return "<PhysicianToCTC(\
        physicianCTCID = {},\
        physicianID = {},\
        ctcID = {})>".format(
        self.physicianCTCID,
        self.physicianID,
        self.ctcID)
        
class PreApplication(CustomModel):
    __tablename__ = 'preApplication'
    
    preApplicationID = db.Column(db.Integer, primary_key=True)
    projectID = db.Column(db.Integer, db.ForeignKey('project.projectID'))
    pi_fname = db.Column(db.String)
    pi_lname = db.Column(db.String)
    pi_phone = db.Column(db.String)
    pi_email = db.Column(db.String)
    contact_fname = db.Column(db.String)
    contact_lname = db.Column(db.String)
    contact_phone = db.Column(db.String)
    contact_email = db.Column(db.String)
    institution = db.Column(db.String)
    institution2 = db.Column(db.String)
    uid = db.Column(db.String)
    udoh = db.Column(db.Integer)
    project_title = db.Column(db.String)
    purpose = db.Column(db.String)
    irb0 = db.Column(db.Boolean)
    irb1 = db.Column(db.Boolean)
    irb2 = db.Column(db.Boolean)
    irb3 = db.Column(db.Boolean)
    irb4 = db.Column(db.Boolean)
    other_irb = db.Column(db.String)
    updb = db.Column(db.Boolean)
    pt_contact = db.Column(db.Boolean)
    start_date = db.Column(db.Date)
    link = db.Column(db.Boolean)
    delivery_date = db.Column(db.Date)
    description = db.Column(db.String)
    
    # Relationships
    # 1-1 one project, one preApp
    project = db.relationship('Project',back_populates='preApplication')
    
    def __repr__(self):
        return "<(PreApplication(\
        preApplicationID = {},\
        projectID = {},\
        projectID = {},\
        pi_fname = {},\
        pi_lname = {},\
        pi_phone = {},\
        pi_email = {},\
        contact_fname = {},\
        contact_lname = {},\
        contact_phone = {},\
        contact_email = {},\
        institution = {},\
        institution2 = {},\
        uid = {},\
        udoh = ={},\
        project_title = {},\
        purpose = = {},\
        irb0 = {},\
        irb1 = {},\
        irb2 = {},\
        irb3 = {},\
        irb4 = {},\
        other_irb = {},\
        updb = {},\
        pt_contact = {},\
        start_date = {},\
        link = {},\
        delivery_date = {},\
        description = {})>".format(
        preApplicationID,
        projectID,
        pi_fname,
        pi_lname,
        pi_phone,
        pi_email,
        contact_fname,
        contact_lname,
        contact_phone,
        contact_email,
        institution,
        institution2,
        uid,
        udoh,
        project_title,
        purpose,
        irb0,
        irb1,
        irb2,
        irb3,
        irb4,
        other_irb,
        updb,
        pt_contact,
        start_date,
        link,
        delivery_date,
        description)
    
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
    
    # M - 1, Many projects with same IRB Holder
    irbHolder = db.relationship("IRBHolderLUT", back_populates="projects")
    # M - 1, Many projects with same type
    projectType = db.relationship("ProjectType",back_populates="projects")
    # 1-1
    arcReview = db.relationship("ArcReview", uselist=False, back_populates="project")
    # 1-M one project, many budgets
    budgets = db.relationship("Budget",back_populates="project")
    # 1-M, one project many review Committees
    reviewCommittees = db.relationship("ReviewCommittee",back_populates="project")
    # 1 - M, one project, many ucrReports
    ucrReports = db.relationship("UCRReport",back_populates="project")
    # 1 - M, one project many project statuses
    projectStatuses = db.relationship("ProjectStatus",back_populates="project")
    # 1 - 1, one project, one preApp
    preApplication = db.relationship("PreApplication",uselist=False,back_populates = "project")
    # 1 - M, one project, many logs
    logs = db.relationship("Log",back_populates="project")
    # 1 - M, one project, many fundings
    fundings = db.relationship("Funding",back_populates="project")
    # M - 1, many project staff can have the same project
    projectStaff = db.relationship("ProjectStaff",back_populates="project")
    # M - 2, many project patients can have the same project
    projectPatient = db.relationship("ProjectPatient", back_populates="project")
    # 1 - M, one project, many statuses
    projectStatus = db.relationship("ProjectStatus",back_populates="project")
    
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
        
class ProjectPatient(CustomModel):
    __tablename__ = 'projectPatient'
    
    participantID = db.Column(db.Integer, primary_key=True)
    projectID = db.Column(db.Integer, db.ForeignKey('project.projectID'))
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    ctcID = db.Column(db.Integer, db.ForeignKey('ctc.ctcID'))
    current_age = db.Column(db.Integer)
    batch = db.Column(db.Integer)
    sitegrp = db.Column(db.Integer)
    final_code = db.Column(db.Integer)
    final_code_date = db.Column(db.Date)
    enrollment_date = db.Column(db.Date)
    date_coord_signed = db.Column(db.Date)
    import_date = db.Column(db.Date)
    final_code_staff = db.Column(db.Integer) # FK?
    enrollment_staff = db.Column(db.Integer) #FK?
    date_coord_signed_staff = db.Column(db.Date)
    abstract_status = db.Column(db.Integer)
    abstract_status_date = db.Column(db.Date)
    abstract_status_staff = db.Column(db.Integer) # FK?
    sent_to_abstractor = db.Column(db.Date)
    sent_to_abstractor_staff = db.Column(db.Integer) # FK
    abstracted_date = db.Column(db.Date)
    abstractor_initials = db.Column(db.String)
    researcher_date = db.Column(db.Date)
    researcher_staff = db.Column(db.Integer) # FK
    consent_link = db.Column(db.String)
    tracing_status = db.Column(db.Integer)
    med_record_release_signed = db.Column(db.Boolean)
    med_record_release_link = db.Column(db.String)
    med_record_release_staff = db.Column(db.Integer) # FK
    med_record_release_date = db.Column(db.Date)
    survey_to_researcher = db.Column(db.Date)
    survey_to_researcher_staff = db.Column(db.Integer) # FK
    
    # Relationships
    # 1 - M, one PP with many PPStatuses
    patientProjectStatuses = db.relationship('PatientProjectStatus',back_populates="projectPatient")
    # 1 - M, one PP with many tracings
    tracings = db.relationship('Tracing', back_populates="projectPatient")
    # M -1 many projectPatient can have the same project
    project = db.relationship('Project',back_populates='projectPatient')
    # 1 - 1 one PP with one CTC
    ctc = db.relationship('CTC',back_populates="projectPatient")
    # 1 - M, on PP with many staff
    staff = db.relationship("Staff", back_populates="projectPatient")
    # M - 1, many contacts may have the same facility
    contacts = db.relationship("Contact",back_populates="projectPatient")
    
    def __repr__(self):
        return "<ProjectPatient(\
        participantID = {},\
        projectID = {},\
        staffID = {},\
        ctcID = {},\
        current_age = {},\
        batch = {},\
        sitegrp = {},\
        final_code = {},\
        final_code_date = {},\
        enrollment_date = {},\
        date_coord_signed = {},\
        import_date = {},\
        final_code_staff = {},\
        enrollment_staff = {},\
        date_coord_signed_staff = {},\
        abstract_status = {},\
        abstarct_status_date = {},\
        abstract_status_staff = {},\
        sent_to_abstractor = {},\
        sent_to_abstractor_staff = {},\
        abstracted_date = {},\
        abstractor_initials = {},\
        researcher_date = {},\
        researcher_staff = {},\
        consent_link = {},\
        tracing_status = {},\
        med_record_release_signed = {},\
        med_record_relase_link = {},\
        med_record_release_staff = {},\
        med_record_release_date = {},\
        survey_to_researcher = {},\
        survey_to_researcher_staff = {})>".format(
        self.participantID,
        self.projectID,
        self.staffID,
        self.ctcID,
        self.current_age,
        self.batch,
        self.sitegrp,
        self.final_code,
        self.final_code_date,
        self.enrollment_date,
        self.date_coord_signed,
        self.import_date,
        self.final_code_staff,
        self.enrollment_staff,
        self.date_coord_signed_staff,
        self.abstract_status,
        self.abstarct_status_date,
        self.abstract_status_staff,
        self.sent_to_abstractor,
        self.sent_to_abstractor_staff,
        self.abstracted_date,
        self.abstractor_initials,
        self.researcher_date,
        self.researcher_staff,
        self.consent_link,
        self.tracing_status,
        self.med_record_release_signed,
        self.med_record_relase_link,
        self.med_record_release_staff,
        self.med_record_release_date,
        self.survey_to_researcher,
        self.survey_to_researcher_staff)
        
class ProjectStaff(CustomModel):
    __tablename__ =  'projectStaff'
    
    projectStaffID = db.Column(db.Integer, primary_key=True)
    staffRoleLUTID = db.Column(db.Integer, db.ForeignKey('staffRoleLUT.staffRoleLUTID'))
    projectID = db.Column(db.Integer, db.ForeignKey('project.projectID'))
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    role = db.Column(db.Integer)
    date_pledge = db.Column(db.Date)
    date_revoked = db.Column(db.Date)
    contact = db.Column(CONTACTS)
    inactive = db.Column(INACTIVES)
    human_sub_training_exp = db.Column(db.Date)
    human_sub_type_id = db.Column(db.Integer)
    study_role = db.Column(db.Integer)
    
    # Relationships
    # M - 1, Many projectStaff with the same role
    staffRole = db.relationship("StaffRoleLUT", back_populates="projectStaff")
    # M - 1, many projectStaff with the same project
    project = db.relationship("Project", back_populates="projectStaff")
    # 1  M one staff can have multiple project staff
    staff = db.relationship("Staff", back_populates="projectStaff")
    
    def __repr__(self):
        return "<ProjectStaff(\
        projectStaffID = {},\
        staffRoleLUTID = {},\
        projectID = {},\
        staffID = {},\
        role = {},\
        date_pledge = {},\
        date_revoked = {},\
        contact = {},\
        inactive = {},\
        human_sub_training_exp = {},\
        human_sub_type_id = {},\
        study_role = {})>".format(
        self.projectStaffID,
        self.staffRoleLUTID,
        self.projectID,
        self.staffID,
        self.role,
        self.date_pledge,
        self.date_revoked,
        self.contact,
        self.inactive,
        self.human_sub_training_exp,
        self.human_sub_type_id,
        self.study_role)
        
class ProjectStatus(CustomModel):
    __tablename__ = 'projectStatus'

    projectStatusID = db.Column(db.Integer, primary_key=True)
    projectStatusLUTID = db.Column(db.Integer, db.ForeignKey('projectStatusLUT.projectStatusTypeID'))
    projectID = db.Column(db.Integer, db.ForeignKey('project.projectID'))
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    status_date = db.Column(db.Date)
    status_notes = db.Column(db.String)
    
    # Relationships
    # M -1 , many projectStatuses per projectStatusLUT
    projectStatus = db.relationship("ProjectStatusLUT", back_populates="projectStatuses")
    
    # 1 - M, one project, many statuses
    project = db.relationship("Project", back_populates="projectStatuses")
    # 1 - M, many statuses per staff
    staff = db.relationship("Staff", back_populates="projectStatuses")
    
    def __repr__(self):
        return "<ProjectStatus(\
        projectStatusID = {},\
        projectStatusLUTID = {},\
        projectID = {},\
        staffID = {},\
        status_date = {},\
        status_notes = {})>".format(
        self.projectStatusID,
        self.projectStatusLUTID,
        self.projectID,
        self.staffID,
        self.status_date,
        self.status_notes)
    
class ProjectStatusLUT(CustomModel):
    __tablename__ = 'projectStatusLUT'
    
    projectStatusTypeID = db.Column(db.Integer, primary_key=True)
    project_status = db.Column(db.String)
    status_definition = db.Column(db.String)
    
    # Relationships
    # M - 1, many ProjectStatuses per projectStatusLUT
    projectStatuses = db.relationship("ProjectStatus",back_populates="projectStatus")
    
    def __repr__(self):
        return "<ProjectStatusLUT(\
        projectStatusTypeID = {},\
        project_status = {},\
        status_definition = {})>".format(
        self.projectStatusTypeID,
        self.project_status,
        self.status_definition)
          
class ProjectType(CustomModel):
    __tablename__ = 'projectType'
    
    projectTypeID = db.Column(db.Integer,primary_key=True)
    project_type = db.Column(db.String)
    project_type_definition = db.Column(db.String)
    
    # Relationships
    # M - 1 Many projects with same project type
    projects = db.relationship("Project", back_populates="projectType")
    
    def __repr__(self):
        return "<ProjectType(\
        projectTypeID={},\
        project_type={},\
        project_type_definition={})>".format(
        self.projectTypeID,
        self,project_type,
        self.project_type_definition)
    
class RCStatusList(CustomModel):
    __tablename__ = 'RCStatusList'
    
    rcStatusID = db.Column(db.Integer, primary_key=True)
    rc_status = db.Column(db.String)
    rc_status_definition = db.Column(db.String)
    
    # Relationships
    reviewCommittees = db.relationship("ReviewCommittee", back_populates="RCStatusList")
    
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
    
    # Relationships
    # 1- M, one project many review committees
    project = db.relationship("Project",foreign_keys=[project_projectID],back_populates="reviewCommittees")
    # M - 1, Many review committees per rcStatus
    RCStatusList = db.relationship("RCStatusList", foreign_keys=[RCStatusList_rc_StatusID], back_populates="reviewCommittees")
    # M - 1, Many review committees per rcList
    reviewCommitteeList = db.relationship("ReviewCommitteeList",foreign_keys=[reviewCommitteeList_rcListID],back_populates="reviewCommittees")
        
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
    
    # Relationships
    # M - 1 Many reviewCommittess per reviewCommitteeList
    reviewCommittees = db.relationship("ReviewCommittee",back_populates="reviewCommitteeList")
    
    def __repr__(self):
        return "<ReviewCommitteeList(\
        rcListID={},\
        reviewCommittee={},\
        rc_description={})>".format(
        self.rcListID,
        self.reviewComittee,
        self.rc_description)
        
class Staff(CustomModel):
    __tablename__ = 'staff'
    
    staffID = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    middle_name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    phoneComment = db.Column(db.String)
    institution = db.Column(db.String)
    department = db.Column(db.String)
    position = db.Column(db.String)
    credentials = db.Column(db.String)
    street = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    human_sub_training_exp = db.Column(db.Date)
    UCR_role = db.Column(db.Integer)
    
    # Relationships
    # 1 - M, one staff with many statuses
    projectStatuses = db.relationship("ProjectStatus",back_populates="staff")
    # 1 - M, one staff with many lgos
    logs = db.relationship("Log",back_populates="staff")
    # 1 - M, one staff with many trainings
    staffTraining = db.relationship('StaffTraining', back_populates="staff")
    # M - 1, many projectStaff to staff (people can be working on multiple projects)
    projectStaff = db.relationship('ProjectStaff',back_populates="staff")
    # M - 1 many contacts can have the same staff
    contacts = db.relationship("Contact",back_populates="staff")
    # 1 - M, one study/projectPatient can have many staff
    projectPatient = db.relationship("ProjectPatient",back_populates="staff")

    
    def __repr__(self):
        return "<Staff(\
        staffID = {},\
        fname = {},\
        lname = {},\
        middle_name = {},\
        email = {},\
        phone = {},\
        phoneComment = {},\
        institution = {},\
        department = {},\
        position = {},\
        credentials = {},\
        street = {},\
        city = {},\
        state = {},\
        human_sub_training_exp = {},\
        UCR_role = {})>".format(
        self.staffID,
        self.fname,
        self.lname,
        self.middle_name,
        self.email,
        self.phone,
        self.phoneComment,
        self.institution,
        self.department,
        self.position,
        self.credentials,
        self.street,
        self.city,
        self.state,
        self.human_sub_training_exp,
        self.UCR_role)
        
class StaffRoleLUT(CustomModel):
    __tablename__ = 'staffRoleLUT'
    
    staffRoleLUTID = db.Column(db.Integer,primary_key=True)
    staffRole = db.Column(db.String)
    staffRoleDescription = db.Column(db.String)
    
    # Relationships
    # M - 1, many projectStaff with the same role
    projectStaff = db.relationship("ProjectStaff",back_populates="staffRole")
    
    def __repr__(self):
        return "<StaffRoleLUT(\
        staffRoleLUTID = {},\
        staffRole = {},\
        staffRoleDescription = {})>".format(
        self.staffRoleLUTID,
        self.staffRole,
        self.staffRoleDescription)
        
class StaffTraining(CustomModel):
    __tablename__ = 'staffTraining'
    
    staffTrainingID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    humanSubjectTrainingLUTID = db.Column(db.Integer,db.ForeignKey('humanSubjectTrainingLUT.human_sub_type_id'))
    date_taken = db.Column(db.Date)
    exp_date = db.Column(db.Date)
    
    # Relationships
    # M - 1, many staffTrainings with the same HST
    humanSubjectTraining = db.relationship('HumanSubjectTrainingLUT',back_populates="staffTrainings")
    # 1 - M, one staff with many trainings
    staff = db.relationship('Staff',back_populates='staffTraining')

    def __repr__(self):
        return "<StaffTraining(\
        staffTrainingID = {},\
        staffID = {},\
        humanSubjectTrainingLUTID = {},\
        date_taken = {},\
        exp_date = {})>".format(
        self.staffTrainingID,
        self.staffID,
        self.humanSubjectTrainingLUTID,
        self.date_taken,
        self.exp_date)

class Tracing(CustomModel):
    __tablename__ = "tracing"
    
    tracingID = db.Column(db.Integer, primary_key=True)
    tracingSourceLUTID = db.Column(db.Integer, db.ForeignKey('tracingSourceLUT.tracingSourceLUTID'))
    projectPatientID = db.Column(db.Integer, db.ForeignKey('projectPatient.participantID'))
    date = db.Column(db.Date)
    staff = db.Column(db.Integer)
    notes = db.Column(db.String)
    
    # Relationships
    # M - 1, many trancings can have the same tracingSource
    tracingSource = db.relationship('TracingSourceLUT',back_populates="tracings")
    # 1 - M, one project patient with many tracings
    projectPatient = db.relationship('ProjectPatient', back_populates="tracings")
    
    def __repr__(self):
        return "<Tracing(\
        tracingID = {},\
        tracingSourceLUTID = {},\
        projectPatientID = {},\
        date = {},\
        staff = {},\
        notes = {})>".format(
        self.tracingID,
        self.tracingSourceLUTID,
        self.projectPatientID,
        self.date,
        self.staff,
        self.notes)

class TracingSourceLUT(CustomModel):
    __tablename__ = "tracingSourceLUT"
    
    tracingSourceLUTID = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    
    # Relationships
    tracings = db.relationship('Tracing',back_populates="tracingSource")
    
    def __repr__(self):
        return "<TracingSourceLUT(\
        tracingSourceLUTID = {},\
        description = {})>".format(
        tracingSourceLUTID,
        description)
        
class UCRReport(CustomModel):
    __tablename__ = 'ucrReport'
    
    ucrReportID = db.Column(db.Integer, primary_key=True)
    projectID = db.Column(db.Integer, db.ForeignKey('project.projectID'))
    report_type = db.Column(db.Integer)
    report_submitted = db.Column(db.Date)
    report_due = db.Column(db.Date)
    report_doc = db.Column(db.String)
    
    # Relationships
    # 1 - M, one project, many reports
    project = db.relationship("Project", back_populates="ucrReports")
    
    def __repr__(self):
        return "<UCRReport(\
        ucrReportID = {},\
        projectID = {},\
        report_type = {},\
        report_submitted = {},\
        report_due = {},\
        report_doc = {})>".format(
        self.ucrReportID,
        self.projectID,
        self.report_type,
        self.report_submitted,
        self.report_due,
        self.report_doc)
    