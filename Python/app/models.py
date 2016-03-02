import json
import datetime
from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from app.database import db
from app.helpers import DateTimeEncoder
from sqlalchemy.orm import class_mapper

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
        result = {}
        for prop in class_mapper(self.__class__).iterate_properties:
            if isinstance(prop, sqlalchemy.orm.ColumnProperty):
                result[prop.key] = getattr(self, prop.key)
        return result
    
    def json(self):
        return jsonify(self.dict())
            
##############################################################################
# Models
##############################################################################  

class ArcReview(CustomModel):
    __tablename__ = 'arcReview'

    arcReviewID = db.Column(db.Integer, primary_key=True)
    projectID = db.Column(db.Integer, db.ForeignKey('project.projectID'))
    reviewType = db.Column('review_type',db.Integer)
    dateSentToReviewer = db.Column('date_sent_to_reviewer',db.Date)
    reviewer1 = db.Column('reviewer1',db.Integer)
    reviewer1Rec = db.Column('reviewer1_rec',db.Integer)
    reviewer1SigDate = db.Column('reviewer1_sig_date',db.Date)
    reviewer1Comments = db.Column('reviewer1_comments',db.String)
    reviewer2 = db.Column('reviewer2',db.Integer)
    reviewer2Rec = db.Column('reviewer2_rec',db.Integer)
    reviewer2SigDate = db.Column('reviewer2_sig_date',db.Date)
    reviewer2Comments = db.Column('reviewer2_comments',db.String)
    research = db.Column('research',db.Integer)
    contact = db.Column('contact',db.Boolean)
    lnkage = db.Column('lnkage',db.Boolean)
    engaged = db.Column('engaged',db.Boolean)
    nonPublicData = db.Column('non_public_data',db.Boolean)
    
    # Relationships
    # 1-1
    project = db.relationship('Project', back_populates='arcReview')
    
    def __repr__(self):
        return "<ArcReview(\
        arcReviewID = {},\
        projectID = {},\
        reviewType = {},\
        dateSentToReviewer = {},\
        reviewer1 = {},\
        reviewer1Rec = {},\
        reviewer1SigDate = {},\
        reviewer1Comments = {},\
        reviewer2 = {},\
        reviewer2Rec = {},\
        reviewer2SigDate = {},\
        reviewer2Comments = {},\
        research = {},\
        contact = {},\
        lnkage = {},\
        engaged = {},\
        nonPublicDate = {})>".format(
        self.arcReviewID,
        self.projectID,
        self.reviewType,
        self.dateSentToReviewer,
        self.reviewer1,
        self.reviewer1Rec,
        self.reviewer1SigDate,
        self.reviewer1Comments,
        self.reviewer2,
        self.reviewer2Rec,
        self.reviewer2SigDate,
        self.reviewer2Comments,
        self.research,
        self.contact,
        self.lnkage,
        self.engaged,
        self.nonPublicData)
    
class Budget(CustomModel):
    __tablename__ = "budget"
    
    budgetID = db.Column('budgetID',db.Integer, primary_key=True)
    projectID = db.Column('projectID',db.Integer,db.ForeignKey('project.projectID'))
    numPeriods = db.Column('numPeriods',db.Integer)
    periodStart = db.Column('periodStart',db.Date)
    periodEnd = db.Column('periodEnd',db.Date)
    periodTotal = db.Column('periodTotal',db.Float)
    periodComment = db.Column('periodComment',db.String)
    
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
    
    contactID = db.Column('contactID',db.Integer, primary_key=True)
    contactTypeLUTID = db.Column('contactTypeLUTID',db.Integer, db.ForeignKey("contactTypeLUT.contactTypeLUTID"))
    projectPatientID = db.Column('projectPatientID',db.Integer, db.ForeignKey("projectPatient.participantID"))
    staffID = db.Column('staffID',db.Integer, db.ForeignKey("staff.staffID"))
    informantID = db.Column('informantID',db.Integer, db.ForeignKey("informant.informantID"))
    facilityID = db.Column('facilityID',db.Integer, db.ForeignKey("facility.facilityID"))
    physicianID = db.Column('physician',db.Integer, db.ForeignKey("physician.physicianID"))
    description = db.Column('description',db.String)
    contactDate = db.Column('contact_date',db.Date)
    initials = db.Column('initials',db.String)
    notes = db.Column('notes',db.String)
    
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
        contactDate = {},\
        initials = {},\
        notes = {})>".format(
        
        self.contactID,
        self.contactTypeLUTID,
        self.projectPatientID,
        self.staffID,
        self.informantID,
        self.facilityID,
        self.physicianID,
        self.description,
        self.contactDate,
        self.initials,
        self.notes)
            
class ContactInfoSourceLUT(CustomModel):
    __tablename__ = "contactInfoSourceLUT"
    
    contactInfoSourceID = db.Column('contactInfoSourceID',db.Integer, primary_key=True)
    contactInfoSource = db.Column('contact_info_source',db.String)
    
    def __repr__(self):
        return "<ContactInfoSourceLUT(\
        contactInfoSourceID = {},\
        contactInfoSource = {})>".format(
        self.contactInfoSourceID,
        self.contactInfoSource)
            
class ContactInfoStatusLUT(CustomModel):
    __tablename__ = "contactInfoStatusLUT"
    
    contactInfoStatusID = db.Column('contactInfoStatusID',db.Integer, primary_key=True)
    contactInfoStatus = db.Column('contact_info_status',db.String)
    
    def __repr__(self):
        return "<ContactInfoStatus(\
        contactInfoStatusID = {},\
        contactInfoStatus = {})>".format(
        self.contactInfoStatusID,
        self.contactInfoStatus)

class ContactTypeLUT(CustomModel):
    __tablename__ = "contactTypeLUT"
    
    contactTypeLUTID = db.Column('contactTypeLUTID',db.Integer, primary_key=True)
    contactDefinition = db.Column('contact_definition',db.String)
    
    # Relationships
    # M - 1, many contacts can have the same type
    contacts = db.relationship("Contact",back_populates="contactType")
    
    def __repr__(self):
        return "<ContactTypeLUT(\
        contactTypeLUTID = {},\
        contactDefinition = {})>".format(
        self.contactTypeLUTID,
        self.contactDefinition)
        
class CTC(CustomModel):
    __tablename__ = 'ctc'
    
    ctcID = db.Column('ctcID',db.Integer, primary_key=True)
    patientID = db.Column('patientID',db.Integer, db.ForeignKey('patient.patAutoID'))
    dxDate = db.Column('dx_date',db.Date)
    site = db.Column('site',db.Integer)
    histology = db.Column('histology',db.String)
    behavior = db.Column('behavior',db.String)
    ctcSequence = db.Column('ctc_sequence',db.String)
    stage = db.Column('stage',db.String)
    dxAge = db.Column('dx_age',db.Integer)
    dxStreet1 = db.Column('dx_street1',db.String)
    dxStreet2 = db.Column('dx_street2',db.String)
    dxCity = db.Column('dx_city',db.String)
    dxState = db.Column('dx_state',db.String)
    dxZip = db.Column('dx_zip',db.Integer)
    dxCounty = db.Column('dx_county',db.String)
    dnc = db.Column('dnc',db.String)
    dncReason = db.Column('dnc_reason',db.String)
    
    # Relationship
    # 1 - 1, one ctc per projectPatient
    projectPatient = db.relationship("ProjectPatient",back_populates="ctc")
    # many ctcs to one patient
    patient = db.relationship('Patient',uselist=False, back_populates='ctcs')
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
        ctcSequence = = {},\
        stage = = {},\
        dxAge = = {},\
        dxStreet1 = = {},\
        dxStreet2 = = {},\
        dxCity = = {},\
        dxState = = {},\
        dxZip = = {},\
        dxCounty = = {},\
        dnc = = {},\
        dncReason = {})>".format(
        self.ctcID,
        self.patientID,
        self.dxDate,
        self.site,
        self.histology, 
        self.behavior, 
        self.ctcSequence,
        self.stage,
        self.dxAge,
        self.dxStreet1,
        self.dxStreet2,
        self.dxCity,
        self.dxState,
        self.dxZip,
        self.dxCounty,
        self.dnc,
        self.dncReason)

class CTCFacility(CustomModel):
    __tablename__ = 'CTCFacility'
    
    CTCFacilityID = db.Column('CTCFacilityID',db.Integer,primary_key=True)
    ctcID = db.Column('ctcID',db.Integer, db.ForeignKey('ctc.ctcID'))
    facilityID = db.Column('facilityID',db.Integer, db.ForeignKey('facility.facilityID'))
    
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
    
    facilityID = db.Column('facilityID',db.Integer, primary_key=True)
    facilityName = db.Column('facility_name',db.String)
    contactFirstName = db.Column('contact_fname',db.String)
    contactLastName = db.Column('contact_lname',db.String)
    facilityStatus = db.Column('facility_status',db.Integer)
    facilityStatusDate = db.Column('facility_status_date',db.Date)
    contact2FirstName = db.Column('contact2_fname',db.String)
    contact2LastName = db.Column('contact2_lname',db.String)
    
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
        facilityName = {},\
        contactFirstName = {},\
        contactLastName = {},\
        facilityStatus = {},\
        facilityStatusDate = {},\
        contact2FirstName = {},\
        contact2LastName = {})>".format(
        self.facilityID,
        self.facilityName,
        self.contactFirstName,
        self.contactLastName,
        self.facilityStatus,
        self.facilityStatusDate,
        self.contact2FirstName,
        self.contact2LastName)

class FacilityAddress(CustomModel):
    __tablename__ = 'facilityAddress'
    
    facilityAddressID = db.Column('facilityAddressID',db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceID',db.Integer, db.ForeignKey("contactInfoSourceLUT.contactInfoSourceID"))
    facilityID = db.Column('facilityID',db.Integer, db.ForeignKey("facility.facilityID"))
    contactInfoStatusID = db.Column('contactInfoStatusLUTID',db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    street = db.Column('street',db.String)
    street2 = db.Column('street2',db.String)
    city = db.Column('city',db.String)
    state = db.Column('state',db.String)
    zip = db.Column('zip',db.Integer)
    addressStatus = db.Column('facility_address_status',db.Integer)
    addressStatusDate = db.Column('facility_address_status_date',db.Date)
    addressStatusSource = db.Column('facility_address_status_source',ADDRESS_STATUS_SOURCE)
    
    # Relationships
    # M - 1, many facilities can be at the same address
    facilities = db.relationship("Facility",back_populates="facilityAddress")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "FacilityAddress(\
        facilityAddressID = {},\
        contactInfoSourceID  = {},\
        facilityID = {},\
        contactInfoStatusID = {},\
        street = {},\
        street2  = {},\
        city = {},\
        state = {},\
        zip = {},\
        facilityAddressStatus = {},\
        facilityAddressStatusDate = {},\
        facilityAddressStatusSource = {})>".format(
        self.facilityAddressID,
        self.contactInfoSourceID ,
        self.facilityID,
        self.contactInfoStatusID,
        self.street,
        self.street2 ,
        self.city,
        self.state,
        self.zip,
        self.addressStatus,
        self.addressStatusDate,
        self.addressStatusSource)
        
class FacilityPhone(CustomModel):
    __tablename__ = 'facilityPhone'
    
    facilityPhoneID = db.Column('facilityPhoneID',db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceID',db.Integer, db.ForeignKey('contactInfoSourceLUT.contactInfoSourceID'))
    contactInfoStatusID = db.Column('contactInfoStatusID',db.Integer, db.ForeignKey('contactInfoStatusLUT.contactInfoStatusID'))
    facilityID = db.Column('facilityID',db.Integer, db.ForeignKey('facility.facilityID'))
    phoneNumber = db.Column('facility_phone',db.String)
    clinicName = db.Column('clinic_name',db.String)
    phoneType = db.Column('phone_type',db.String)
    phoneStatus = db.Column('phone_status',db.Integer)
    phoneSource = db.Column('phone_source',db.Integer)
    phoneStatusDate = db.Column('phone_status_date',db.Date)
    
    # Relationships
    # M - 1, many patients can be at the same phone
    facilities = db.relationship("Facility", back_populates = "facilityPhone")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "<FacilityPhone(\
        facilityPhoneID = {},\
        contactInfoSourceID = {},\
        contactInfoStatusID = {},\
        facilityID = {},\
        phoneNumber = {},\
        clinicName = {},\
        phoneType = {},\
        phoneStatus = {},\
        phoneSource = {},\
        phoneStatusDate = {})>".format(
        self.facilityPhoneID,
        self.contactInfoSourceID,
        self.contactInfoStatusID,
        self.facilityID,
        self.phoneNumber,
        self.clinicName,
        self.phoneType,
        self.phoneStatus,
        self.phoneSource,
        self.phoneStatusDate)
    
class Funding(CustomModel):
    __tablename__ = "funding"
    
    fundingID = db.Column('fundingID',db.Integer, primary_key=True)
    grantStatusID = db.Column('grantStatusLUTID',db.Integer, db.ForeignKey('grantStatusLUT.grantStatusID'))
    projectID = db.Column('projectID',db.Integer,db.ForeignKey('project.projectID'))
    fundingSourceID = db.Column('fundingSourceID',db.Integer,db.ForeignKey('fundingSourceLUT.fundingSourceID'))
    primaryFundingSource = db.Column('primary_funding_source',db.String)
    secondaryFundingSource = db.Column('secondary_funding_source',db.String)
    fundingNumber = db.Column('funding_number',db.String)
    grantTitle = db.Column('grant_title',db.String)
    dateStatus = db.Column('date_status',db.Date)
    grantPi = db.Column('grant_pi',db.Integer)
    primaryChartfield = db.Column('primary_chartfield',db.String)
    secondaryChartfield = db.Column('secondary_chartfield',db.String)

    # Relationships
    # M - 1, many fundings with the same source
    fundingSource = db.relationship("FundingSourceLUT", foreign_keys=[fundingSourceID],back_populates="fundings")
    # M - 1, many fundings with the same grant status
    grantStatus = db.relationship("GrantStatusLUT",foreign_keys=[grantStatusID],back_populates="fundings")
    # 1 - M, one project with many fundings
    project = db.relationship("Project",back_populates="fundings")

    def __repr__(self):
        return "<Funding(\
            fundingID = {},\
            grantStatusID = {},\
            projectID = {},\
            fundingSourceID = {},\
            primaryFundingSource = {},\
            secondaryFundingSource = {},\
            fundingNumber = {},\
            grantTitle = {},\
            grantStatusID = {},\
            dateStatus = {},\
            grantPi = {},\
            primaryChartfield = {},\
            secondaryChartfield = {})>".format(
            self.fundingID,
            self.grantStatusID,
            self.projectID,
            self.fundingSourceID,
            self.primaryFundingSource,
            self.secondaryFundingSource,
            self.fundingNumber,
            self.grantTitle,
            self.grantStatusID,
            self.dateStatus,
            self.grantPi,
            self.primaryChartfield,
            self.secondaryChartfield)
            
class FundingSourceLUT(CustomModel):
    __tablename__ = 'fundingSourceLUT'
    
    fundingSourceID = db.Column('fundingSourceID',db.Integer,primary_key=True)
    fundingSource = db.Column('fundingSource',db.String)
    
    # Relationships
    # M - 1, many fundings with the same source
    fundings = db.relationship("Funding",back_populates="fundingSource")
    
    def __repr__(self):
        return "<FundingSourceLUT(\
        fundingSourceID = {},\
        fundingSource = {})>".format(
        self.fundingSourceLUTID,
        self.fundingSource)
            
class GrantStatusLUT(CustomModel):
    __tablename__ = 'grantStatusLUT'
    
    grantStatusID = db.Column('grantStatusID',db.Integer, primary_key=True)
    grantStatus = db.Column('grant_status',db.String)
    
    # Relationships
    # M - 1, many fundings with the same grant status
    fundings = db.relationship("Funding",back_populates="grantStatus")
    
    def __repr__(self):
        return "<GrantStatusLUT(\
            grantStatusID = {}\
            grantStatus = {})>".format(
            self.grantStatusID,
            self.grantStatus)
            
class HumanSubjectTrainingLUT(CustomModel):
    __tablename__ = 'humanSubjectTrainingLUT'
    
    humanSubjectTrainingID = db.Column('humanSubjectTrainingID',db.Integer, primary_key=True)
    trainingType = db.Column('training_type',db.String)
    
    # Relationships
    # M - 1, many staff trainings with the same HST
    staffTrainings = db.relationship('StaffTraining',back_populates="humanSubjectTraining")
    
    def __repr__(self):
        return "<HumanSubjectTrainginLUT(\
        human_sub_type_id = {},\
        trainingType = {})>".format(
        self.humanSubjectTrainingID,
        self.trainingType)
            
class IRBHolderLUT(CustomModel):
    __tablename__ = 'IRBHolderLUT'
    
    irbHolderID = db.Column('irbHolderID',db.Integer,primary_key=True)
    holder = db.Column('irb_holder',db.String)
    holderDefinition = db.Column('irb_holder_definition',db.String)
    
    # Relationships
    # M - 1, Many projects with the same IRB
    projects = db.relationship("Project",back_populates="irbHolder")
    
    def __repr__(self):
        return "<IRBHolderLUT(\
            irbHolderID = {},\
            holder = {},\
            holderDefinition = {})>".format(
            self.irbHolderID,
            self.holder,
            self.holderDefinition)

class Informant(CustomModel):
    __tablename__ = "informant"
    
    informantID = db.Column('informantID',db.Integer, primary_key=True)
    patientID = db.Column('patAutoID',db.Integer, db.ForeignKey("patient.patAutoID"))
    firstName = db.Column('fname',db.String)
    lastName = db.Column('lname',db.String)
    middleName = db.Column('middle_name',db.String)
    informantPrimary = db.Column('informant_primary',db.String)
    informantRelationship = db.Column('informant_relationship',db.String)
    notes = db.Column('notes',db.String)
    
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
        firstName = {},\
        lastName = {},\
        middleName = {},\
        informantPrimary = {},\
        informantRelationship = {},\
        notes = {})>".format(
        self.informantID,
        self.patientID,
        self.firstName,
        self.lastName,
        self.middleName,
        self.informantPrimary,
        self.informantRelationship,
        self.notes)

class InformantAddress(CustomModel):
    __tablename__ = 'informantAddress'
    
    informantAddressID = db.Column('informantAddressID',db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID',db.Integer, db.ForeignKey('contactInfoSourceLUT.contactInfoSourceID'))
    contactInfoStatusID = db.Column('contactInfoStatusID',db.Integer, db.ForeignKey('contactInfoStatusLUT.contactInfoStatusID'))
    informantID = db.Column('informantID',db.Integer, db.ForeignKey('informant.informantID'))
    street = db.Column('street',db.String)
    street2 = db.Column('street2',db.String)
    city = db.Column('city',db.String)
    state = db.Column('state',db.String)
    zip = db.Column('zip',db.String)
    addressStatus = db.Column('addressStatus',db.Integer)
    addressStatusDate = db.Column('addressStatusDate',db.Date)
    addressStatusSource = db.Column('addressStatusSource',ADDRESS_STATUS_SOURCE)
    
    # Relationships
    # 1 - M, one informant may have multiple addresses
    informant = db.relationship("Informant", back_populates = "informantAddresses")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSource = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "<InformantAddress(\
        informantAddressID = {},\
        contactInfoSourceID = {},\
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
        self.contactInfoSourceID,
        self.contactInfoStatusID,
        self.informantID,
        self.street,
        self.street2,
        self.city,
        self.state,
        self.zip,
        self.addressStatus,
        self.addressStatusDate,
        self.addressStatusSource)

class InformantPhone(CustomModel):
    __tablename__ = 'informantPhone'
    
    informantPhoneID = db.Column('informantPhoneID',db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID',db.Integer, db.ForeignKey("contactInfoSourceLUT.contactInfoSourceID"))
    informantID = db.Column('informantId',db.Integer,db.ForeignKey("informant.informantID"))
    contactInfoStatusID = db.Column('contactInfoStatusID',db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    phoneNumber = db.Column('phone',db.String)
    phoneSource = db.Column('phone_source',PHONE_SOURCES)
    phoneStatus = db.Column('phone_status',db.Integer)
    phoneStatusDate = db.Column('phone_status_date',db.Date)
    
    # Relationships
    # 1 - M, one informant may have multiple phones
    informant = db.relationship("Informant",back_populates="informantPhones")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSource = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "<InformantPhone(\
        informantPhoneID = {},\
        contactInfoSourceID = {},\
        informantID = {},\
        contactInfoStatusID = {},\
        phoneNumber = {},\
        phone_source = {},\
        phone_status = {},\
        phone_status_date = {})>".format(
        self.informantPhoneID,
        self.contactInfoSource,
        self.informantID,
        self.contactInfoStatusID,
        self.phoneNumber,
        self.phoneSource,
        self.phoneStatus,
        self.phoneStatusDate)
        
class Log(CustomModel):
    __tablename__ = 'log'
    
    logID = db.Column('logID',db.Integer, primary_key=True)
    logSubjectID = db.Column('logSubjectID',db.Integer, db.ForeignKey('logSubjectLUT.logSubjectID'))
    projectID = db.Column('projectID',db.Integer, db.ForeignKey('project.projectID'))
    staffID = db.Column('staffID',db.Integer, db.ForeignKey('staff.staffID'))
    phaseStatusID = db.Column('phaseStatusID',db.Integer, db.ForeignKey('phaseStatus.logPhaseID'))
    note = db.Column('note',db.String)
    date = db.Column('date',db.Date)
    
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
        logSubjectID = {},\
        projectID = {},\
        staffID = {},\
        phaseStatus = {},\
        note = {},\
        date = {})>".format(
        self.logID,
        self.logSubjectID,
        self.projectID,
        self.staffID,
        self.phaseStatusID,
        self.note,
        self.date)
        
class LogSubjectLUT(CustomModel):
    __tablename__ = 'logSubjectLUT'
    
    logSubjectID = db.Column('logSubjectID',db.Integer, primary_key=True)
    logSubject = db.Column('log_subject',db.String)
    
    # Relationships
    # M - 1, many logs with the same subject
    logs = db.relationship("Log",back_populates="logSubject")
    
    def __repr(self):
        return "<LogSubject(\
        logSubjectID = {},\
        logSubject = {})>".format(
        self.logSubjectID,
        self.logSubject)
 
class Patient(CustomModel):
    __tablename__ = 'patient'
    
    patientID = db.Column('patAutoID',db.Integer, primary_key=True)
    patID = db.Column('patID',db.String)
    recordID = db.Column('recordID',db.Integer)
    ucrDistID = db.Column('ucrDistID',db.Integer)
    UPDBID = db.Column('UPDBID',db.Integer)
    firstName = db.Column('fname',db.String)
    lastName = db.Column('lname',db.String)
    middleName = db.Column('middle_name',db.String)
    maidenName = db.Column('maiden_name',db.String)
    aliasFirstName = db.Column('alias_fname',db.String)
    aliasLastName = db.Column('alias_lname',db.String)
    aliasMiddleName = db.Column('alias_middle_name',db.String)
    dob = db.Column('dob',db.Date)
    SSN = db.Column('SSN',db.Integer)
    sex = db.Column('sex',SEXES)
    race = db.Column('race',RACES)
    ethnicity = db.Column('ethnicity',ETHNICITIES)
    vitalStatus = db.Column('viral_status',VITAL_STATUSES)
    
    # Relationships
    # M - 1, many patients can be at the same address
    patientAddress = db.relationship('PatientAddress',back_populates="patients")
    # many to one
    ctcs = db.relationship('CTC',back_populates="patient")
    # M - 1, many patients can be at the same email
    patientEmail = db.relationship('PatientEmail',back_populates="patients")
    # M - 1, many patients can be at the same phone
    patientPhone = db.relationship('PatientPhone',back_populates="patients")
    # M - 1, many informants may have multiple patients
    informant = db.relationship('Informant',back_populates="patients")
    
    def __repr__(self):
        return "<Patient(\
        patientID = {},\
        patID = {},\
        recordID = {},\
        ucrDistID = {},\
        UPDBID = {},\
        firstName = {},\
        lastname = {},\
        middleName = {},\
        maidenName = {},\
        aliasFirstName = {},\
        aliasLastName = {},\
        aliasMiddleName = {},\
        dob = {},\
        SSN = {},\
        sex = {},\
        race = {},\
        ethnicity = {},\
        vitalStatus = {})>".format(
        self.patientID,
        self.patID,
        self.recordID,
        self.ucrDistID,
        self.UPDBID,
        self.firstName,
        self.lastName,
        self.middleName,
        self.maidenName,
        self.aliasFirstNamee,
        self.aliasLastName,
        self.aliasMiddleName,
        self.dob,
        self.SSN,
        self.sex,
        self.race,
        self.ethnicity,
        self.vitalStatus)

class PatientAddress(CustomModel):
    __tablename__  = "patientAddress"
    
    patAddressID = db.Column('patAddressID',db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID',db.Integer, db.ForeignKey("contactInfoSourceLUT.contactInfoSourceID"))
    patientID = db.Column('patientId',db.Integer, db.ForeignKey("patient.patAutoID"))
    contactInfoStatusID = db.Column('contactInfoStatusID',db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    street = db.Column('street',db.String)
    street2 = db.Column('street2',db.String)
    city = db.Column('city',db.String)
    state = db.Column('state',db.String)
    zip = db.Column('zip',db.Integer)
    addressStatus = db.Column('address_status',db.Integer)
    addressStatusDate = db.Column('address_status_date',db.Date)
    addressStatusSource = db.Column('address_status_source',ADDRESS_STATUS_SOURCE)
    
    # Relationships
    patients = db.relationship("Patient",back_populates="patientAddress")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "PatientAddress(\
        patAddressID = {},\
        contactInfoSourceID  = {},\
        patientID = {},\
        contactInfoStatusID = {},\
        street = {},\
        street2  = {},\
        city = {},\
        state = {},\
        zip = {},\
        addressStatus = {},\
        addressStatusDate = {},\
        addressStatusSource = {})>".format(
        self.patAddressID,
        self.contactInfoSourceID ,
        self.patientID,
        self.contactInfoStatusLUTID,
        self.street,
        self.street2 ,
        self.city,
        self.state,
        self.zip,
        self.addressStatus,
        self.addressStatusDate,
        self.addressStatusSource)
        
class PatientEmail(CustomModel):
    __tablename__ = 'patientEmail'
    
    emailID = db.Column('emailID',db.Integer,primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID',db.Integer, db.ForeignKey("contactInfoSourceLUT.contactInfoSourceID"))
    patientID = db.Column('patientID',db.Integer, db.ForeignKey("patient.patAutoID"))
    contactInfoStatusID = db.Column('contactInfoStatusID',db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    email = db.Column('email',db.String)
    emailStatus = db.Column('email_status',db.Integer)
    emailSource = db.Column('email_source',db.Integer)
    emailStatusDate = db.Column('email_status_date',db.Date)
    
    # Relationships
    # 1 - M, one patient may have multiple emails
    patients = db.relationship("Patient",back_populates="patientEmail")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSource = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "<PatientEmail(\
        emailID = {},\
        contactInfoSourceID = {},\
        patientID = {},\
        contactInfoStatusID = {},\
        email = {},\
        email_status = {},\
        email_source = {},\
        email_status_date = {})>".format(
        self.emailID,
        self.contactInfoSourceID,
        self.patientID,
        self.contactInfoStatusID,
        self.email,
        self.emailStatus,
        self.emailSource,
        self.emailStatusDate)

class PatientPhone(CustomModel):
    __tablename__ = 'patientPhone'
    
    patPhoneID = db.Column('patPhoneID',db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID',db.Integer, db.ForeignKey("contactInfoSourceLUT.contactInfoSourceID"))
    patientID = db.Column('patientID',db.Integer, db.ForeignKey("patient.patAutoID"))
    contactInfoStatusID = db.Column('contactInfoStatusID',db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    phoneNumber = db.Column('phone',db.String)
    phoneSource = db.Column('phone_source',PHONE_SOURCES)
    phoneStatus = db.Column('phone_status',db.Integer)
    phoneStatusDate = db.Column('phone_status_date',db.Date)
    
    # Relationships
    # M - 1, many patients can be at the same phone
    patients = db.relationship("Patient",back_populates="patientPhone")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSource = db.relationship("ContactInfoSourceLUT")
    
    def __repr__(self):
        return "<PatientPhone(\
        patPhoneID = {},\
        contactInfoSourceID = {},\
        patientID = {},\
        contactInfoStatusID = {},\
        phoneNumber = {},\
        phoneSource = {},\
        phoneStatus = {},\
        phoneStatusDate = {})>".format(
        self.patPhoneID,
        self.contactInfoSource,
        self.patientID,
        self.contactInfoStatusID,
        self.phoneNumber,
        self.phoneSource,
        self.phoneStatus,
        self.phoneStatusDate)

class PatientProjectStatus(CustomModel):
    __tablename__ = 'patientProjectStatus'
    
    patientProjectStatusID = db.Column(db.Integer, primary_key=True)
    patientProjectStatusTypeID = db.Column(db.Integer, db.ForeignKey('patientProjectStatusLUT.patientProjectStatusTypeID'))
    projectPatientID = db.Column(db.Integer, db.ForeignKey('projectPatient.participantID'))
    
    # Relationships
    # M - 1, many patientProjectStatuses with same ppsLUT
    patientProjectStatus = db.relationship("PatientProjectStatusLUT", back_populates = "patientProjectStatuses")
    # 1 - M, one project Patient has many statuses
    projectPatient = db.relationship("ProjectPatient", back_populates ="patientProjectStatuses")
    
    def __repr__(self):
        return "<PatientProjectStatus(\
        patientProjectStatusID = {},\
        patientProjectStatusTypeID = {},\
        projectPatientID = {})>".format(
        self.patientProjectStatusID,
        self.patientProjectStatusTypeID,
        self.projectPatientID)
        
class PatientProjectStatusLUT(CustomModel):
    __tablename__ = 'patientProjectStatusLUT'
    
    patientProjectStatusTypeID = db.Column(db.Integer, primary_key=True)
    statusDescription = db.Column(db.String)
    
    # Relationships
    # M - 1, many pps with same ppsLUT
    patientProjectStatuses = db.relationship("PatientProjectStatus",back_populates="patientProjectStatus")
    
    def __repr__(self):
        return "<PatientProjectStatusLUT(\
        patientProjectStatusTypeID = {}\
        status_description = {})>".format(
        patientProjectStatusTypeID,
        status_description)
    
class PhaseStatus(CustomModel):
    __tablename__ = 'phaseStatus'
    
    logPhaseID = db.Column('logPhaseID',db.Integer, primary_key=True)
    phaseStatus = db.Column('phase_status',db.String)
    phaseDescription = db.Column('phase_description',db.String)
    
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
    contactInfoSourceID = db.Column(db.Integer, db.ForeignKey("contactInfoSourceLUT.contactInfoSourceID"))
    physicianID = db.Column(db.Integer, db.ForeignKey("physician.physicianID"))
    contactInfoStatusLUTID = db.Column(db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    street = db.Column(db.String)
    street2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.Integer)
    address_status = db.Column(db.Integer)
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
        contactInfoSourceID  = {},\
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
        self.contactInfoSourceID ,
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
    contactInfoSourceID = db.Column(db.Integer, db.ForeignKey("contactInfoSourceLUT.contactInfoSourceID"))
    physicianID = db.Column(db.Integer,db.ForeignKey("physician.physicianID"))
    contactInfoStatusID = db.Column(db.Integer, db.ForeignKey("contactInfoStatusLUT.contactInfoStatusID"))
    phone = db.Column(db.String)
    phone_type = db.Column(db.String)
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
        contactInfoSourceID = {},\
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
    review_committee = db.Column(db.String)
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
    humanSubjectTrainingLUTID = db.Column(db.Integer,db.ForeignKey('humanSubjectTrainingLUT.humanSubjectTrainingID'))
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
    