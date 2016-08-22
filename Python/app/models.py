import json
import datetime
from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from app.database import db
from app.helpers import DateTimeEncoder
from sqlalchemy.orm import class_mapper
from sqlalchemy.ext.declarative import declared_attr

"""
    A base class that all models derive from
"""


class CustomModel(db.Model):
    __abstract__ = True
    # def __init__(self):
    #    super(CustomModel,self).__init__()

    createdDate = db.Column(db.DateTime, server_default=db.func.now())
    modifiedDate = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    versionID = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        "version_id_col": versionID
    }

    def dict(self):
        result = {}
        for prop in class_mapper(self.__class__).iterate_properties:
            if isinstance(prop, sqlalchemy.orm.ColumnProperty):
                result[prop.key] = getattr(self, prop.key)
        return result

    def json(self):
        return jsonify(self.dict())


class AbstractStatus(CustomModel):
    __tablename__ = "AbstractStatusLUT"

    abstractStatusID = db.Column('abstractStatusID', db.Integer, primary_key=True)
    abstractStatus = db.Column('abstract_status', db.String)

    projectPatients = db.relationship("ProjectPatient", back_populates="abstractStatus")


class ArcReview(CustomModel):
    __tablename__ = 'ArcReview'

    arcReviewID = db.Column('arcReviewID', db.Integer, primary_key=True)
    projectID = db.Column('projectID', db.Integer, db.ForeignKey('Project.projectID'), nullable=False)
    reviewType = db.Column('review_type', db.Integer)
    dateSentToReviewer = db.Column('date_sent_to_reviewer', db.Date)
    reviewer1 = db.Column('reviewer1', db.Integer)
    reviewer1Rec = db.Column('reviewer1_rec', db.Integer)
    reviewer1SigDate = db.Column('reviewer1_sig_date', db.Date)
    reviewer1Comments = db.Column('reviewer1_comments', db.String)
    reviewer2 = db.Column('reviewer2', db.Integer)
    reviewer2Rec = db.Column('reviewer2_rec', db.Integer)
    reviewer2SigDate = db.Column('reviewer2_sig_date', db.Date)
    reviewer2Comments = db.Column('reviewer2_comments', db.String)
    research = db.Column('research', db.Integer)
    contact = db.Column('contact', db.Boolean)
    linkage = db.Column('linkage', db.Boolean)
    engaged = db.Column('engaged', db.Boolean)
    nonPublicData = db.Column('non_public_data', db.Boolean)

    # Relationships
    # 1-1
    project = db.relationship('Project', back_populates='arcReviews')

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
    __tablename__ = "Budget"

    budgetID = db.Column('budgetID', db.Integer, primary_key=True)
    projectID = db.Column('projectID', db.Integer, db.ForeignKey('Project.projectID'), nullable=False)
    numPeriods = db.Column('num_periods', db.Integer)
    periodStart = db.Column('period_start', db.Date)
    periodEnd = db.Column('period_end', db.Date)
    periodTotal = db.Column('period_total', db.Float)
    periodComment = db.Column('period_comment', db.String)

    # Relationships
    # 1 - M, 1 project, many budgets
    project = db.relationship("Project", back_populates="budgets")

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
    __tablename__ = 'Contact'

    contactID = db.Column('contactID', db.Integer, primary_key=True)
    contactTypeLUTID = db.Column('contactTypeLUTID', db.Integer, db.ForeignKey("ContactTypeLUT.contactTypeLUTID"), nullable=False)
    projectPatientID = db.Column('particpantID', db.Integer, db.ForeignKey("ProjectPatient.participantID"), nullable=False)
    staffID = db.Column('staffID', db.Integer, db.ForeignKey("Staff.staffID"), nullable=False)
    informantID = db.Column('informantID', db.Integer, db.ForeignKey("Informant.informantID"))
    facilityID = db.Column('facilityID', db.Integer, db.ForeignKey("Facility.facilityID"))
    physicianID = db.Column('physicianID', db.Integer, db.ForeignKey("Physician.physicianID"))
    description = db.Column('description', db.String)
    contactDate = db.Column('contact_date', db.Date, nullable=False)
    initials = db.Column('initials', db.String)
    notes = db.Column('notes', db.String)

    # Relastionships
    # M - 1, many contacts can have the same type
    contactType = db.relationship("ContactTypeLUT", back_populates="contacts")
    # M - 1, many contacts may have the same patient
    projectPatient = db.relationship("ProjectPatient", back_populates="contacts")
    # M - 1 many contacts can have the same staff
    staff = db.relationship("Staff", foreign_keys=[staffID], back_populates="contacts")
    # M - 1, many contacts can have the same informant
    informant = db.relationship("Informant", back_populates="contacts")
    # M - 1, many contacts may have the same facility
    facility = db.relationship("Facility", back_populates="contacts")
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


class Contacts(CustomModel):
    __tablename__ = "ContactsLUT"
    contactID = db.Column('contactID', db.Integer, primary_key=True)
    contact = db.Column('contact', db.String)


class ContactInfoSourceLUT(CustomModel):
    __tablename__ = "ContactInfoSourceLUT"

    contactInfoSourceID = db.Column('contactInfoSourceID', db.Integer, primary_key=True)
    contactInfoSource = db.Column('contact_info_source', db.String)

    def __repr__(self):
        return "<ContactInfoSourceLUT(\
        contactInfoSourceID = {},\
        contactInfoSource = {})>".format(
            self.contactInfoSourceID,
            self.contactInfoSource)


class ContactInfoStatusLUT(CustomModel):
    __tablename__ = "ContactInfoStatusLUT"

    contactInfoStatusID = db.Column('contactInfoStatusID', db.Integer, primary_key=True)
    contactInfoStatus = db.Column('contact_info_status', db.String)

    def __repr__(self):
        return "<ContactInfoStatus(\
        contactInfoStatusID = {},\
        contactInfoStatus = {})>".format(
            self.contactInfoStatusID,
            self.contactInfoStatus)


class ContactTypeLUT(CustomModel):
    __tablename__ = "ContactTypeLUT"

    contactTypeID = db.Column('contactTypeLUTID', db.Integer, primary_key=True)
    contactDefinition = db.Column('contact_definition', db.String)

    # Relationships
    # M - 1, many contacts can have the same type
    contacts = db.relationship("Contact", back_populates="contactType")

    def __repr__(self):
        return "<ContactTypeLUT(\
        contactTypeID = {},\
        contactDefinition = {})>".format(
            self.contactTypeID,
            self.contactDefinition)


class CTC(CustomModel):
    __tablename__ = 'CTC'

    ctcID = db.Column('ctcID', db.Integer, primary_key=True)
    participantID = db.Column('participantID', db.Integer, db.ForeignKey('Patient.participantID'), nullable=False)
    dxDate = db.Column('dx_date', db.Date)
    site = db.Column('site', db.Integer)
    histology = db.Column('histology', db.String)
    behavior = db.Column('behavior', db.String)
    ctcSequence = db.Column('ctc_sequence', db.String)
    stage = db.Column('stage', db.String)
    dxAge = db.Column('dx_age', db.Integer)
    dxStreet1 = db.Column('dx_street1', db.String)
    dxStreet2 = db.Column('dx_street2', db.String)
    dxCity = db.Column('dx_city', db.String)
    dxStateID = db.Column('dx_stateID', db.Integer, db.ForeignKey("StateLUT.stateID"))
    dxZip = db.Column('dx_zip', db.String)
    dxCounty = db.Column('dx_county', db.String)
    dnc = db.Column('dnc', db.String)
    dncReason = db.Column('dnc_reason', db.String)

    # Relationship
    # 1 - 1, one ctc per projectPatient
    projectPatient = db.relationship("ProjectPatient", uselist=False, back_populates="ctc")
    # many ctcs to one patient
    patient = db.relationship('Patient', uselist=False, back_populates='ctcs')
    # M - 1
    ctcFacilities = db.relationship("CTCFacility", back_populates="ctc")
    #
    dxState = db.relationship("State")
    physicianToCTC = db.relationship("PhysicianToCTC", back_populates="ctc")

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

    CTCFacilityID = db.Column('CTCFacilityID', db.Integer, primary_key=True)
    ctcID = db.Column('ctcID', db.Integer, db.ForeignKey('CTC.ctcID'), nullable=False)
    facilityID = db.Column('facilityID', db.Integer, db.ForeignKey('Facility.facilityID'), nullable=False)

    # Relationships
    # 1 - M, one facilty may have many CTCFacilities
    facility = db.relationship("Facility", back_populates="ctcFacilities")
    # M - 1,many ctc to one ctcfacility
    ctc = db.relationship("CTC", back_populates="ctcFacilities")

    def __repr__(self):
        return "<CTCFacility(\
        CTCFacilityID = {},\
        ctcID = {},\
        facilityID = {})>".format(
            self.CTCFacilityID,
            self.ctcID,
            self.facilityID)


class Ethnicity(CustomModel):
    __tablename__ = "EthnicityLUT"
    ethnicityID = db.Column('ethnicityID', db.Integer, primary_key=True)
    ethnicity = db.Column('ethnicity', db.String)


class Facility(CustomModel):
    __tablename__ = "Facility"

    facilityID = db.Column('facilityID', db.Integer, primary_key=True)
    facilityName = db.Column('facility_name', db.String)
    contactFirstName = db.Column('contact_first_name', db.String)
    contactLastName = db.Column('contact_last_name', db.String)
    facilityStatus = db.Column('facility_status', db.Integer)
    facilityStatusDate = db.Column('facility_status_date', db.Date)
    contact2FirstName = db.Column('contact2_first_name', db.String)
    contact2LastName = db.Column('contact2_last_name', db.String)

    # Relationships
    # M - 1, many facilities can have the same phone
    facilityPhones = db.relationship("FacilityPhone", back_populates="facilities")
    facilityAddresses = db.relationship("FacilityAddress", back_populates="facilities")
    # M - 1, many contacts may have the same facility
    contacts = db.relationship('Contact', back_populates="facility")
    # 1 - M, one facility may have many CTCFacility
    ctcFacilities = db.relationship("CTCFacility", back_populates="facility")
    # M - 1
    physicianFacilities = db.relationship("PhysicianFacility", back_populates="facility")

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
    __tablename__ = 'FacilityAddress'

    facilityAddressID = db.Column('facilityAddressID', db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID', db.Integer,
                                    db.ForeignKey("ContactInfoSourceLUT.contactInfoSourceID"))
    facilityID = db.Column('facilityID', db.Integer, db.ForeignKey("Facility.facilityID"), nullable=False)
    contactInfoStatusID = db.Column('contactInfoStatusLUTID', db.Integer,
                                    db.ForeignKey("ContactInfoStatusLUT.contactInfoStatusID"))
    street = db.Column('street', db.String)
    street2 = db.Column('street2', db.String)
    city = db.Column('city', db.String)
    stateID = db.Column('stateID', db.Integer, db.ForeignKey("StateLUT.stateID"))
    zip = db.Column('zip', db.String)
    addressStatusDate = db.Column('facility_address_status_date', db.Date)

    # Relationships
    # M - 1, many facilities can be at the same address
    state = db.relationship("State")
    facilities = db.relationship("Facility", back_populates="facilityAddresses")
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
            self.contactInfoSourceID,
            self.facilityID,
            self.contactInfoStatusID,
            self.street,
            self.street2,
            self.city,
            self.state,
            self.zip,
            self.addressStatus,
            self.addressStatusDate,
            self.addressStatusSource)


class FacilityPhone(CustomModel):
    __tablename__ = 'FacilityPhone'

    facilityPhoneID = db.Column('facilityPhoneID', db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceID', db.Integer,
                                    db.ForeignKey('ContactInfoSourceLUT.contactInfoSourceID'))
    contactInfoStatusID = db.Column('contactInfoStatusID', db.Integer,
                                    db.ForeignKey('ContactInfoStatusLUT.contactInfoStatusID'))
    facilityID = db.Column('facilityID', db.Integer, db.ForeignKey('Facility.facilityID'), nullable=False)
    phoneTypeID = db.Column('phoneTypeLUTID', db.Integer, db.ForeignKey('PhoneTypeLUT.phoneTypeLUTID'))
    phoneNumber = db.Column('facility_phone', db.String)
    clinicName = db.Column('clinic_name', db.String)
    phoneStatusDate = db.Column('facility_phone_status_date', db.Date)

    # Relationships
    # M - 1, many patients can be at the same phone
    facilities = db.relationship("Facility", back_populates="facilityPhones")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    phoneType = db.relationship("PhoneTypeLUT")

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


class FinalCode(CustomModel):
    __tablename__ = "FinalCode"

    finalCodeID = db.Column('finalCodeID', db.Integer, primary_key=True)
    finalCode = db.Column('final_code', db.String)

    projectPatients = db.relationship("ProjectPatient", back_populates="finalCode")


class Funding(CustomModel):
    __tablename__ = "Funding"

    fundingID = db.Column('fundingID', db.Integer, primary_key=True)
    grantStatusID = db.Column('grantStatusLUTID', db.Integer, db.ForeignKey('GrantStatusLUT.grantStatusID'))
    projectID = db.Column('projectID', db.Integer, db.ForeignKey('Project.projectID'), nullable=False)
    fundingSourceID = db.Column('fundingSourceID', db.Integer, db.ForeignKey('FundingSourceLUT.fundingSourceID'))
    primaryFundingSource = db.Column('primary_funding_source', db.String)
    secondaryFundingSource = db.Column('secondary_funding_source', db.String)
    fundingNumber = db.Column('funding_number', db.String)
    grantTitle = db.Column('grant_title', db.String)
    dateStatus = db.Column('date_status', db.Date)
    grantPi = db.Column('grant_pi', db.Integer)
    primaryChartfield = db.Column('primary_chartfield', db.String)
    secondaryChartfield = db.Column('secondary_chartfield', db.String)

    # Relationships
    # M - 1, many fundings with the same source
    fundingSource = db.relationship("FundingSourceLUT", foreign_keys=[fundingSourceID], back_populates="fundings")
    # M - 1, many fundings with the same grant status
    grantStatus = db.relationship("GrantStatusLUT", foreign_keys=[grantStatusID], back_populates="fundings")
    # 1 - M, one project with many fundings
    project = db.relationship("Project", back_populates="fundings")

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
    __tablename__ = 'FundingSourceLUT'

    fundingSourceID = db.Column('fundingSourceID', db.Integer, primary_key=True)
    fundingSource = db.Column('funding_source', db.String)

    # Relationships
    # M - 1, many fundings with the same source
    fundings = db.relationship("Funding", back_populates="fundingSource")

    def __repr__(self):
        return "<FundingSourceLUT(\
        fundingSourceID = {},\
        fundingSource = {})>".format(
            self.fundingSourceLUTID,
            self.fundingSource)


class GrantStatusLUT(CustomModel):
    __tablename__ = 'GrantStatusLUT'

    grantStatusID = db.Column('grantStatusID', db.Integer, primary_key=True)
    grantStatus = db.Column('grant_status', db.String)

    # Relationships
    # M - 1, many fundings with the same grant status
    fundings = db.relationship("Funding", back_populates="grantStatus")

    def __repr__(self):
        return "<GrantStatusLUT(\
            grantStatusID = {}\
            grantStatus = {})>".format(
            self.grantStatusID,
            self.grantStatus)


class HumanSubjectTrainingLUT(CustomModel):
    __tablename__ = 'HumanSubjectTrainingLUT'

    humanSubjectTrainingID = db.Column('humanSubjectTrainingID', db.Integer, primary_key=True)
    trainingType = db.Column('training_type', db.String)

    # Relationships
    # M - 1, many staff trainings with the same HST
    staffTrainings = db.relationship('StaffTraining', back_populates="humanSubjectTraining")

    def __repr__(self):
        return "<HumanSubjectTrainginLUT(\
        human_sub_type_id = {},\
        trainingType = {})>".format(
            self.humanSubjectTrainingID,
            self.trainingType)


class IRBHolderLUT(CustomModel):
    __tablename__ = 'IRBHolderLUT'

    irbHolderID = db.Column('irbHolderID', db.Integer, primary_key=True)
    holder = db.Column('irb_holder', db.String)
    holderDefinition = db.Column('irb_holder_definition', db.String)

    # Relationships
    # M - 1, Many projects with the same IRB
    projects = db.relationship("Project", back_populates="irbHolder")

    def __repr__(self):
        return "<IRBHolderLUT(\
            irbHolderID = {},\
            holder = {},\
            holderDefinition = {})>".format(
            self.irbHolderID,
            self.holder,
            self.holderDefinition)


class Inactive(CustomModel):
    __tablename__ = "InactiveLUT"
    inactiveID = db.Column('inactiveID', db.Integer, primary_key=True)
    inactive = db.Column('inactive', db.String)


class Incentive(CustomModel):
    __tablename__ = "Incentive"

    incentiveID = db.Column('incentiveID', db.Integer, primary_key=True)
    contactID = db.Column('contactID', db.Integer, db.ForeignKey("Contact.contactID"))
    participantID = db.Column('participantID', db.Integer, db.ForeignKey("ProjectPatient.participantID"), nullable=False)
    incentiveDescription = db.Column('incentive_desc', db.String)
    barcode = db.Column('barcode', db.String)

    contact = db.relationship("Contact")
    projectPatient = db.relationship("ProjectPatient", back_populates="incentives")

    def __repr__(self):
        return "<Incentive(\
        incentiveID = {}\
        projectPatientID = {}\
        incentiveDescription = {}\
        incentiveDate = {})>"


class Informant(CustomModel):
    __tablename__ = "Informant"

    informantID = db.Column('informantID', db.Integer, primary_key=True)
    participantID = db.Column('participantID', db.Integer, db.ForeignKey("Patient.participantID"), nullable=False)
    firstName = db.Column('first_name', db.String)
    lastName = db.Column('last_name', db.String)
    middleName = db.Column('middle_name', db.String)
    informantPrimary = db.Column('informant_primary', db.String)
    informantRelationship = db.Column('informant_relationship', db.String)
    notes = db.Column('notes', db.String)

    # Relationships
    # 1 - M, one patient may have multiple informants
    patients = db.relationship("Patient", back_populates="informants")
    # 1 - M, one informant may have muleple addresses/phones
    informantAddresses = db.relationship("InformantAddress")
    informantPhones = db.relationship("InformantPhone")
    # M - 1, many contacts can have the same informant
    contacts = db.relationship("Contact", back_populates="informant")

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
    __tablename__ = 'InformantAddress'

    informantAddressID = db.Column('informantAddressID', db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID', db.Integer,
                                    db.ForeignKey('ContactInfoSourceLUT.contactInfoSourceID'))
    contactInfoStatusID = db.Column('contactInfoStatusID', db.Integer,
                                    db.ForeignKey('ContactInfoStatusLUT.contactInfoStatusID'))
    informantID = db.Column('informantID', db.Integer, db.ForeignKey('Informant.informantID'), nullable=False)
    street = db.Column('street', db.String)
    street2 = db.Column('street2', db.String)
    city = db.Column('city', db.String)
    stateID = db.Column('stateID', db.Integer, db.ForeignKey("StateLUT.stateID"))
    zip = db.Column('zip', db.String)
    addressStatusDate = db.Column('address_status_date', db.Date)

    # Relationships
    # 1 - M, one informant may have multiple addresses
    state = db.relationship("State")
    informant = db.relationship("Informant", back_populates="informantAddresses")
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
    __tablename__ = 'InformantPhone'

    informantPhoneID = db.Column('informantPhoneID', db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID', db.Integer,
                                    db.ForeignKey("ContactInfoSourceLUT.contactInfoSourceID"))
    informantID = db.Column('informantId', db.Integer, db.ForeignKey("Informant.informantID"), nullable=False)
    contactInfoStatusID = db.Column('contactInfoStatusID', db.Integer,
                                    db.ForeignKey("ContactInfoStatusLUT.contactInfoStatusID"))
    phoneTypeID = db.Column('phoneTypeLUTID', db.Integer, db.ForeignKey("PhoneTypeLUT.phoneTypeLUTID"))
    phoneNumber = db.Column('phone', db.String)
    phoneStatusDate = db.Column('phone_status_date', db.Date)

    # Relationships
    # 1 - M, one informant may have multiple phones
    informant = db.relationship("Informant", back_populates="informantPhones")
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
    __tablename__ = 'Log3'

    logID = db.Column('logID', db.Integer, primary_key=True)
    logSubjectID = db.Column('logSubjectLUTID', db.Integer, db.ForeignKey('LogSubjectLUT.logSubjectLUTID'))
    projectID = db.Column('projectID', db.Integer, db.ForeignKey('Project.projectID'), nullable=False)
    staffID = db.Column('staffID', db.Integer, db.ForeignKey('Staff.staffID'), nullable=False)
    phaseStatusID = db.Column('logPhaseID', db.Integer, db.ForeignKey('PhaseStatus.logPhaseID'))
    note = db.Column('note', db.String)
    date = db.Column('date', db.Date)

    # Relationships
    # M - 1, many logs with the same subject
    logSubject = db.relationship("LogSubjectLUT", back_populates="logs")
    # M - 1, many logs with the same subject
    phaseStatus = db.relationship("PhaseStatus", back_populates="logs")
    # 1 - M, one staff with many logs
    staff = db.relationship("Staff", foreign_keys=[staffID], back_populates="logs")
    # 1 - M, one project with many logs
    project = db.relationship("Project", back_populates="logs")

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
    __tablename__ = 'LogSubjectLUT'

    logSubjectID = db.Column('logSubjectLUTID', db.Integer, primary_key=True)
    logSubject = db.Column('log_subject', db.String)

    # Relationships
    # M - 1, many logs with the same subject
    logs = db.relationship("Log", back_populates="logSubject")

    def __repr(self):
        return "<LogSubject(\
        logSubjectID = {},\
        logSubject = {})>".format(
            self.logSubjectID,
            self.logSubject)


class Patient(CustomModel):
    __tablename__ = 'Patient'

    participantID = db.Column('participantID', db.Integer, primary_key=True)
    patID = db.Column('patID', db.String)
    recordID = db.Column('recordID', db.Integer)
    ucrDistID = db.Column('ucrDistID', db.Integer)
    UPDBID = db.Column('UPDBID', db.Integer)
    firstName = db.Column('first_name', db.String)
    lastName = db.Column('last_name', db.String)
    middleName = db.Column('middle_name', db.String)
    maidenName = db.Column('maiden_name', db.String)
    aliasFirstName = db.Column('alias_first_name', db.String)
    aliasLastName = db.Column('alias_last_name', db.String)
    aliasMiddleName = db.Column('alias_middle_name', db.String)
    dob = db.Column('dob', db.Date)
    SSN = db.Column('SSN', db.Integer)
    sexID = db.Column('sexID', db.Integer, db.ForeignKey("SexLUT.sexID"))
    raceID = db.Column('raceID', db.Integer, db.ForeignKey("RaceLUT.raceID"))
    ethnicityID = db.Column('ethnicityID', db.Integer, db.ForeignKey("EthnicityLUT.ethnicityID"))
    vitalStatusID = db.Column('vital_statusID', db.Integer, db.ForeignKey("VitalStatusLUT.vitalStatusID"))

    # Relationships
    # M - 1, many patients can be at the same address
    patientAddresses = db.relationship('PatientAddress', back_populates="patients")
    # many to one
    ctcs = db.relationship('CTC', back_populates="patient")
    # M - 1, many patients can be at the same email
    patientEmails = db.relationship('PatientEmail', back_populates="patients")
    # M - 1, many patients can be at the same phone
    patientPhones = db.relationship('PatientPhone', back_populates="patients")
    # M - 1, many informants may have multiple patients
    informants = db.relationship('Informant', back_populates="patients")
    sex = db.relationship('Sex')
    race = db.relationship('Race')
    ethnicity = db.relationship('Ethnicity')
    vitalStatus = db.relationship('VitalStatus')

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
    __tablename__ = "PatientAddress"

    patAddressID = db.Column('patAddressID', db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID', db.Integer,
                                    db.ForeignKey("ContactInfoSourceLUT.contactInfoSourceID"))
    participantID = db.Column('participantID', db.Integer, db.ForeignKey("Patient.participantID"), nullable=False)
    contactInfoStatusID = db.Column('contactInfoStatusID', db.Integer,
                                    db.ForeignKey("ContactInfoStatusLUT.contactInfoStatusID"))
    street = db.Column('street', db.String)
    street2 = db.Column('street2', db.String)
    city = db.Column('city', db.String)
    stateID = db.Column('stateID', db.Integer, db.ForeignKey("StateLUT.stateID"))
    zip = db.Column('zip', db.String)
    addressStatusDate = db.Column('address_status_date', db.Date)

    # Relationships
    state = db.relationship("State")
    patients = db.relationship("Patient", back_populates="patientAddresses")
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
            self.contactInfoSourceID,
            self.patientID,
            self.contactInfoStatusLUTID,
            self.street,
            self.street2,
            self.city,
            self.state,
            self.zip,
            self.addressStatus,
            self.addressStatusDate,
            self.addressStatusSource)


class PatientEmail(CustomModel):
    __tablename__ = 'PatientEmail'

    emailID = db.Column('emailID', db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID', db.Integer,
                                    db.ForeignKey("ContactInfoSourceLUT.contactInfoSourceID"))
    participantID = db.Column('participantID', db.Integer, db.ForeignKey("Patient.participantID"), nullable=False)
    contactInfoStatusID = db.Column('contactInfoStatusID', db.Integer,
                                    db.ForeignKey("ContactInfoStatusLUT.contactInfoStatusID"))
    email = db.Column('email', db.String)
    emailStatusDate = db.Column('email_status_date', db.Date)

    # Relationships
    # 1 - M, one patient may have multiple emails
    patients = db.relationship("Patient", back_populates="patientEmails")
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
    __tablename__ = 'PatientPhone'

    patPhoneID = db.Column('patPhoneID', db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID', db.Integer,
                                    db.ForeignKey("ContactInfoSourceLUT.contactInfoSourceID"))
    participantID = db.Column('patientID', db.Integer, db.ForeignKey("Patient.participantID"), nullable=False)
    contactInfoStatusID = db.Column('contactInfoStatusID', db.Integer,
                                    db.ForeignKey("ContactInfoStatusLUT.contactInfoStatusID"))
    phoneTypeID = db.Column('phoneTypeLUTID', db.Integer, db.ForeignKey('PhoneTypeLUT.phoneTypeLUTID'))
    phoneNumber = db.Column('phone', db.String)
    phoneStatusDate = db.Column('phone_status_date', db.Date)

    # Relationships
    # M - 1, many patients can be at the same phone
    patients = db.relationship("Patient", back_populates="patientPhones")
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
    __tablename__ = 'PatientProjectStatus'

    patientProjectStatusID = db.Column('patientProjectStatusID', db.Integer, primary_key=True)
    patientProjectStatusTypeID = db.Column('patientProjectStatusLUTID', db.Integer,
                                           db.ForeignKey('PatientProjectStatusLUT.patientProjectStatusLUTID'))
    participantID = db.Column('participantID', db.Integer, db.ForeignKey('ProjectPatient.participantID'), nullable=False)

    # Relationships
    # M - 1, many patientProjectStatuses with same ppsLUT
    patientProjectStatus = db.relationship("PatientProjectStatusLUT", back_populates="patientProjectStatuses")
    # 1 - M, one project Patient has many statuses
    projectPatient = db.relationship("ProjectPatient", back_populates="patientProjectStatuses")

    def __repr__(self):
        return "<PatientProjectStatus(\
        patientProjectStatusID = {},\
        patientProjectStatusTypeID = {},\
        projectPatientID = {})>".format(
            self.patientProjectStatusID,
            self.patientProjectStatusTypeID,
            self.projectPatientID)


class PatientProjectStatusLUT(CustomModel):
    __tablename__ = 'PatientProjectStatusLUT'

    patientProjectStatusTypeID = db.Column('patientProjectStatusLUTID', db.Integer, primary_key=True)
    statusDescription = db.Column('status_description', db.String)

    # Relationships
    # M - 1, many pps with same ppsLUT
    patientProjectStatuses = db.relationship("PatientProjectStatus", back_populates="patientProjectStatus")

    def __repr__(self):
        return "<PatientProjectStatusLUT(\
        patientProjectStatusTypeID = {}\
        status_description = {})>".format(
            patientProjectStatusTypeID,
            status_description)


class PhaseStatus(CustomModel):
    __tablename__ = 'PhaseStatus'

    logPhaseID = db.Column('logPhaseID', db.Integer, primary_key=True)
    phaseStatus = db.Column('phase_status', db.String)
    phaseDescription = db.Column('phase_description', db.String)

    # Relationships
    # M - 1, many logs with the same phase
    logs = db.relationship("Log", back_populates="phaseStatus")

    def __repr__(self):
        return "<PhaseStatus(\
        logPhaseID = {},\
        phase_status = {},\
        phase_description = {})>".format(
            self.logPhaseID,
            self.phase_status,
            self.phase_description)


class PhoneTypeLUT(CustomModel):
    __tablename__ = 'PhoneTypeLUT'

    phoneTypeID = db.Column('phoneTypeLUTID', db.Integer, primary_key=True)
    phoneType = db.Column('phone_type', db.String)

    def __repr__self(self):
        return "<PhoneTypeLUT(\
        phoneTypeID = {},\
        phoneType = {}>".format(
            self.phoneTypeID,
            self.phoneType)


class Physician(CustomModel):
    __tablename__ = "Physician"

    physicianID = db.Column('physicianID', db.Integer, primary_key=True)
    firstName = db.Column('first_name', db.String)
    lastName = db.Column('last_name', db.String)
    middleName = db.Column('middle_name', db.String)
    credentials = db.Column('credentials', db.String)
    specialty = db.Column('specialty', db.String)
    aliasFirstName = db.Column('alias_first_name', db.String)
    aliasLastName = db.Column('alias_last_name', db.String)
    aliasMiddleName = db.Column('alias_middle_name', db.String)
    physicianStatusID = db.Column('physician_status', db.Integer, db.ForeignKey("PhysicianStatusLUT.physicianStatusID"))
    physicianStatusDate = db.Column('physician_status_date', db.Date)

    # Relationships
    # M - 1, many physicians can be at the same address
    physicianAddresses = db.relationship("PhysicianAddress", back_populates="physicians")
    # M - 1, many physicians can have the same phone
    physicianPhones = db.relationship("PhysicianPhone", back_populates="physicians")

    physicianEmails = db.relationship("PhysicianEmail", back_populates="physicians")
    # M - 1, many phys at same facility
    physicianFacilities = db.relationship("PhysicianFacility", back_populates="physician")
    # M - 1
    physicianToCTC = db.relationship("PhysicianToCTC", back_populates="physician")
    # M - 1, many contacts may have the same facility
    contacts = db.relationship("Contact", back_populates="physician")

    physicianStatus = db.relationship("PhysicianStatus", back_populates="physicians")

    def __repr__(self):
        return "<Physician(\
        physicianID = {},\
        firstName = {},\
        lastName = {},\
        middleName = {},\
        credentials = {},\
        specialty = {},\
        aliasFirstName = {},\
        aliasLastName = {},\
        aliasMiddleName = {},\
        physicianStatus = {},\
        physicianStatusDate = {},\
        email = {})>".format(
            self.physicianID,
            self.firstName,
            self.lastName,
            self.middleName,
            self.credentials,
            self.specialty,
            self.aliasLastName,
            self.aliasLastName,
            self.aliasMiddleName,
            self.physicianStatus,
            self.physicianStatusDate,
            self.email)


class PhysicianAddress(CustomModel):
    __tablename__ = "PhysicianAddress"

    physicianAddressID = db.Column('physicianAddressID', db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID', db.Integer,
                                    db.ForeignKey("ContactInfoSourceLUT.contactInfoSourceID"))
    physicianID = db.Column('physicianID', db.Integer, db.ForeignKey("Physician.physicianID"), nullable=False)
    contactInfoStatusID = db.Column('contactInfoSourceID', db.Integer,
                                    db.ForeignKey("ContactInfoStatusLUT.contactInfoStatusID"))
    street = db.Column('physician_street', db.String)
    street2 = db.Column('physician_street2', db.String)
    city = db.Column('physician_city', db.String)
    stateID = db.Column('physician_stateID', db.Integer, db.ForeignKey("StateLUT.stateID"))
    zip = db.Column('physician_zip', db.String)
    addressStatusDate = db.Column('physician_address_status_date', db.Date)

    # Relationship
    # M - 1, many physicians can be at the same address
    state = db.relationship("State")
    physicians = db.relationship("Physician", back_populates="physicianAddresses")
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
            self.contactInfoSourceID,
            self.physicianID,
            self.contactInfoStatusLUTID,
            self.street,
            self.street2,
            self.city,
            self.state,
            self.zip,
            self.addressStatus,
            self.addressStatusDate,
            self.addressStatusSource)


class PhysicianEmail(CustomModel):
    __tablename__ = "PhysicianEmail"

    physicianEmailID = db.Column('physicianEmailID', db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceLUTID', db.Integer,
                                    db.ForeignKey("ContactInfoSourceLUT.contactInfoSourceID"))
    physicianID = db.Column('physicianID', db.Integer, db.ForeignKey("Physician.physicianID"), nullable=False)
    contactInfoStatusID = db.Column('contactInfoSourceID', db.Integer,
                                    db.ForeignKey("ContactInfoStatusLUT.contactInfoStatusID"))
    email = db.Column('email', db.String)
    emailStatusDate = db.Column('email_status_date', db.Date)

    physicians = db.relationship("Physician", back_populates="physicianEmails")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")

    def __repr__(self):
        return "<PhysicianEmail(\
            physicianEmailID = {}\
            contactInfoSourceID = {}\
            contactInfoStatusID = {}\
            physicianID ={}\
            email = {}\
            emailStatusDate = {})>".format(
            self.physicianEmailID,
            self.contactInfoSourceID,
            self.contactInfoStatusID,
            self.physicianID,
            self.email,
            self.emailStatusDate)


class PhysicianFacility(CustomModel):
    __tablename__ = 'PhysicianFacility'

    physFacilityID = db.Column('physicianFacilityID', db.Integer, primary_key=True)
    facilityID = db.Column('facilityID', db.Integer, db.ForeignKey('Facility.facilityID'), nullable=False)
    physicianID = db.Column('physicianID', db.Integer, db.ForeignKey('Physician.physicianID'), nullable=False)
    physFacilityStatusID = db.Column('physician_facility_status', db.Integer,
                                     db.ForeignKey('PhysicianFacilityStatusLUT.physicianFacilityStatusID'))
    physFacilityStatusDate = db.Column('physician_facility_date', db.Date)

    physFacilityStatus = db.relationship("PhysicianFacilityStatus")
    # Relationships
    # M - 1 many physicians at the same physician facility
    physician = db.relationship("Physician", back_populates="physicianFacilities")
    # M - 1
    facility = db.relationship("Facility", back_populates="physicianFacilities")

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
            self.physFacilityStatus,
            self.physFacilityStatusDate)


class PhysicianFacilityStatus(CustomModel):
    __tablename__ = "PhysicianFacilityStatusLUT"
    physicianFacilityStatusID = db.Column('physicianFacilityStatusID', db.Integer, primary_key=True)
    physicianFacilityStatus = db.Column('physicianFacilityStatus', db.String)


class PhysicianPhone(CustomModel):
    __tablename__ = "PhysicianPhone"

    physicianPhoneID = db.Column('physicianPhoneID', db.Integer, primary_key=True)
    contactInfoSourceID = db.Column('contactInfoSourceID', db.Integer,
                                    db.ForeignKey("ContactInfoSourceLUT.contactInfoSourceID"))
    physicianID = db.Column('physicianID', db.Integer, db.ForeignKey("Physician.physicianID"), nullable=False)
    contactInfoStatusID = db.Column('contactInfoStatus', db.Integer,
                                    db.ForeignKey("ContactInfoStatusLUT.contactInfoStatusID"))
    phoneTypeID = db.Column('phoneTypeID', db.Integer, db.ForeignKey("PhoneTypeLUT.phoneTypeLUTID"))
    phoneNumber = db.Column('physician_phone', db.String)
    phoneStatusDate = db.Column('phoneStatusDate', db.Date)

    # Relationship
    # M - 1, many physicians can be at the same phone
    physicians = db.relationship("Physician", back_populates="physicianPhones")
    contactInfoStatus = db.relationship("ContactInfoStatusLUT")
    contactInfoSourceLUT = db.relationship("ContactInfoSourceLUT")
    phoneType = db.relationship("PhoneTypeLUT")

    def __repr__(self):
        return "<PhysicianPhone(\
        physicianPhoneID = {},\
        contactInfoSourceID = {},\
        physicianID = {},\
        contactInfoStatusID = {},\
        phone = {},\
        phoneType = {}, \
        phone_source = {},\
        phone_status = {},\
        phone_status_date = {})>".format(
            self.physicianPhoneID,
            self.contactInfoSource,
            self.physicianID,
            self.contactInfoStatusID,
            self.phoneNumber,
            self.phoneType,
            self.phoneSource,
            self.phoneStatus,
            self.phoneStatusDate)


class PhysicianStatus(CustomModel):
    __tablename__ = "PhysicianStatusLUT"

    physicianStatusID = db.Column('physicianStatusID', db.Integer, primary_key=True)
    physicianStatus = db.Column('physicianStatus', db.String)

    physicians = db.relationship("Physician", back_populates="physicianStatus")


class PhysicianToCTC(CustomModel):
    __tablename__ = "PhysicianToCTC"

    physicianCTCID = db.Column('physicianCTCID', db.Integer, primary_key=True)
    physicianID = db.Column('physicianID', db.Integer, db.ForeignKey('Physician.physicianID'), nullable=False)
    ctcID = db.Column('ctcID', db.Integer, db.ForeignKey('CTC.ctcID'), nullable=False)

    # Relationships
    # M - 1
    physician = db.relationship("Physician", uselist=False, back_populates="physicianToCTC")
    # M - 1
    ctc = db.relationship("CTC", uselist=False, back_populates="physicianToCTC")

    def __repr__(self):
        return "<PhysicianToCTC(\
        physicianCTCID = {},\
        physicianID = {},\
        ctcID = {})>".format(
            self.physicianCTCID,
            self.physicianID,
            self.ctcID)


class PreApplication(CustomModel):
    __tablename__ = 'PreApplication'

    preApplicationID = db.Column('preApplication', db.Integer, primary_key=True)
    projectID = db.Column('projectID', db.Integer, db.ForeignKey('Project.projectID'), nullable=False)
    piFirstName = db.Column('pi_first_name', db.String)
    piLastName = db.Column('pi_last_name', db.String)
    piPhone = db.Column('pi_phone', db.String)
    piEmail = db.Column('pi_email', db.String)
    contactFirstName = db.Column('contact_first_name', db.String)
    contactLastName = db.Column('contact_last_name', db.String)
    contactPhone = db.Column('contact_phone', db.String)
    contactEmail = db.Column('contact_email', db.String)
    institution = db.Column('institution', db.String)
    institution2 = db.Column('institution2', db.String)
    uid = db.Column('uid', db.String)
    udoh = db.Column('udoh', db.Integer)
    projectTitle = db.Column('project_title', db.String)
    purpose = db.Column('purpose', db.String)
    irb0 = db.Column('irb0', db.Boolean)
    irb1 = db.Column('irb1', db.Boolean)
    irb2 = db.Column('irb2', db.Boolean)
    irb3 = db.Column('irb3', db.Boolean)
    irb4 = db.Column('irb4', db.Boolean)
    otherIrb = db.Column('other_irb', db.String)
    updb = db.Column('updb', db.Boolean)
    ptContact = db.Column('pt_contact', db.Boolean)
    startDate = db.Column('start_date', db.Date)
    link = db.Column('link', db.Boolean)
    deliveryDate = db.Column('delivery_date', db.Date)
    description = db.Column('description', db.String)

    # Relationships
    # 1-1 one project, one preApp
    project = db.relationship('Project', back_populates='preApplication')

    def __repr__(self):
        return "<(PreApplication(\
        preApplicationID = {},\
        projectID = {},\
        projectID = {},\
        piFirstName = {},\
        piLastName = {},\
        piPhone = {},\
        piEmail = {},\
        contactFirstName = {},\
        contactLastName = {},\
        contactPhone = {},\
        contactEmail = {},\
        institution = {},\
        institution2 = {},\
        uid = {},\
        udoh = ={},\
        projectTitle = {},\
        purpose = = {},\
        irb0 = {},\
        irb1 = {},\
        irb2 = {},\
        irb3 = {},\
        irb4 = {},\
        otherIrb = {},\
        updb = {},\
        ptContact = {},\
        startDate = {},\
        link = {},\
        deliveryDate = {},\
        description = {})>".format(
            self.preApplicationID,
            self.projectID,
            self.piFirstName,
            self.piLastName,
            self.piPhone,
            self.piEmail,
            self.contactFirstName,
            self.contactLastName,
            self.contactPhone,
            self.contactEmail,
            self.institution,
            self.institution2,
            self.uid,
            self.udoh,
            self.projectTitle,
            self.purpose,
            self.irb0,
            self.irb1,
            self.irb2,
            self.irb3,
            self.irb4,
            self.otherIrb,
            self.updb,
            self.ptContact,
            self.startDate,
            self.link,
            self.deliveryDate,
            self.description)


class Project(CustomModel):
    __tablename__ = 'Project'

    projectID = db.Column('projectID', db.Integer, primary_key=True)
    projectTypeID = db.Column('projectTypeID', db.Integer, db.ForeignKey('ProjectType.projectTypeID'))
    irbHolderID = db.Column('irbHolderID', db.Integer, db.ForeignKey('IRBHolderLUT.irbHolderID'))
    projectTitle = db.Column('project_title', db.String)
    shortTitle = db.Column('short_title', db.String)
    projectSummary = db.Column('project_summary', db.String)
    sop = db.Column('sop', db.String)
    ucrProposal = db.Column('UCR_proposal', db.String)
    budgetDoc = db.Column('budget_doc', db.String)
    ucrFee = db.Column('UCR_fee', db.String)
    ucrNoFee = db.Column('UCR_no_fee', db.String)
    previousShortTitle = db.Column('previous_short_title', db.String)
    dateAdded = db.Column('date_added', db.Date)
    finalRecruitmentReport = db.Column('final_recruitment_report', db.String)
    ongoingContact = db.Column('ongoing_contact', db.Boolean)
    activityStartDate = db.Column('activity_start_date', db.Date)
    activityEndDate = db.Column('activity_end_date', db.Date)

    # M - 1, Many projects with same IRB Holder
    irbHolder = db.relationship("IRBHolderLUT", back_populates="projects")
    # M - 1, Many projects with same type
    projectType = db.relationship("ProjectType", back_populates="projects")
    # 1-1
    arcReviews = db.relationship("ArcReview", back_populates="project")
    # 1-M one project, many budgets
    budgets = db.relationship("Budget", back_populates="project")
    # 1-M, one project many review Committees
    reviewCommittees = db.relationship("ReviewCommittee", back_populates="project")
    # 1 - M, one project, many ucrReports
    ucrReports = db.relationship("UCRReport", back_populates="project")
    # 1 - M, one project many project statuses
    projectStatuses = db.relationship("ProjectStatus", back_populates="project")
    # 1 - 1, one project, one preApp
    preApplication = db.relationship("PreApplication", uselist=False, back_populates="project")
    # 1 - M, one project, many logs
    logs = db.relationship("Log", back_populates="project")
    # 1 - M, one project, many fundings
    fundings = db.relationship("Funding", back_populates="project")
    # M - 1, many project staff can have the same project
    projectStaff = db.relationship("ProjectStaff", back_populates="project")
    # M - 2, many project patients can have the same project
    projectPatients = db.relationship("ProjectPatient", back_populates="project")

    def __repr__(self):
        return "<Project(\
        projectID={},\
        projectTypeID={},\
        irbHolderID={},\
        projectName={},\
        shortTitle={},\
        projectSummary={},\
        sop={},\
        ucrProposal={},\
        budgetDoc={},\
        ucrFee={},\
        ucrNoFee={},\
        budgetEndDate={},\
        previousShortTitle={},\
        dateAdded={},\
        finalRecruitmentReport={})>".format(
            self.projectID,
            self.projectTypeID,
            self.irbHolderID,
            self.projectName,
            self.shortTitle,
            self.projectSummary,
            self.sop,
            self.ucrProposal,
            self.budgetDoc,
            self.ucrFee,
            self.ucrNoFee,
            self.budgetEndDate,
            self.previousShortTitle,
            self.dateAdded,
            self.finalRecruitmentReport)


class ProjectPatient(CustomModel):
    __tablename__ = 'ProjectPatient'

    participantID = db.Column('participantID', db.Integer, primary_key=True)
    projectID = db.Column('projectID', db.Integer, db.ForeignKey('Project.projectID'), nullable=False)
    staffID = db.Column('staffID', db.Integer, db.ForeignKey('Staff.staffID'), nullable=False)
    ctcID = db.Column('ctcID', db.Integer, db.ForeignKey('CTC.ctcID'))
    currentAge = db.Column('current_age', db.Integer)
    batch = db.Column('batch', db.Integer)
    siteGrp = db.Column('sitegrp', db.Integer)
    finalCodeID = db.Column('final_code', db.Integer, db.ForeignKey('FinalCode.finalCodeID'), nullable=False)
    finalCodeDate = db.Column('final_code_date', db.Date)
    finalCodeStaffID = db.Column('final_code_staff', db.Integer, db.ForeignKey('Staff.staffID'))  # FK?
    enrollmentDate = db.Column('enrollment_date', db.Date)
    enrollmentStaffID = db.Column('enrollment_staff', db.Integer, db.ForeignKey('Staff.staffID'))  # FK?
    dateCoordSigned = db.Column('date_coord_signed', db.Date)
    dateCoordSignedStaffID = db.Column('date_coord_signed_staff', db.Integer, db.ForeignKey('Staff.staffID'))
    importDate = db.Column('import_date', db.Date, nullable=False)
    abstractStatusID = db.Column('abstract_status', db.Integer, db.ForeignKey('AbstractStatusLUT.abstractStatusID'))
    abstractStatusDate = db.Column('abstract_status_date', db.Date)
    abstractStatusStaffID = db.Column('abstract_status_staff', db.Integer, db.ForeignKey('Staff.staffID'))  # FK?
    sentToAbstractorDate = db.Column('sent_to_abstractor', db.Date)
    sentToAbstractorStaffID = db.Column('sent_to_abstractor_staff', db.Integer, db.ForeignKey('Staff.staffID'))  # FK
    abstractedDate = db.Column('abstracted_date', db.Date)
    abstractorStaffID = db.Column('abstractor_staff', db.Integer, db.ForeignKey('Staff.staffID'))
    researcherDate = db.Column('researcher_date', db.Date)
    researcherStaffID = db.Column('researcher_staff', db.Integer, db.ForeignKey('Staff.staffID'))  # FK
    consentLink = db.Column('consent_link', db.String)
    medRecordReleaseSigned = db.Column('med_record_release_signed', db.Boolean)
    medRecordReleaseLink = db.Column('med_record_release_link', db.String)
    medRecordReleaseStaffID = db.Column('med_record_release_staff', db.Integer, db.ForeignKey('Staff.staffID'))  # FK
    medRecordReleaseDate = db.Column('med_record_release_date', db.Date)
    surveyToResearcher = db.Column('survey_to_researcher', db.Date)
    surveyToResearcherStaffID = db.Column('survey_to_researcher_staff', db.Integer,
                                          db.ForeignKey('Staff.staffID'))  # FK

    incentives = db.relationship('Incentive', back_populates='projectPatient')
    # Relationships
    # 1 - M, one PP with many PPStatuses
    patientProjectStatuses = db.relationship('PatientProjectStatus', back_populates="projectPatient")
    # 1 - M, one PP with many tracings
    tracings = db.relationship('Tracing', back_populates="projectPatient")
    # M -1 many projectPatient can have the same project
    project = db.relationship('Project', foreign_keys=[projectID], back_populates='projectPatients')
    # 1 - 1 one PP with one CTC
    ctc = db.relationship('CTC', foreign_keys=[ctcID], back_populates="projectPatient")
    # 1 - M, on PP with many staff
    staff = db.relationship("Staff", foreign_keys=[staffID])  # , back_populates="projectPatient")
    # M - 1, many contacts may have the same facility
    contacts = db.relationship("Contact", back_populates="projectPatient", order_by="desc(Contact.contactDate)")

    abstractStatus = db.relationship("AbstractStatus", back_populates="projectPatients")
    finalCode = db.relationship("FinalCode", back_populates="projectPatients")
    finalCodeStaff = db.relationship("Staff", foreign_keys=[finalCodeStaffID])
    enrollmentStaff = db.relationship("Staff", foreign_keys=[enrollmentStaffID])
    dateCoordSignedStaff = db.relationship("Staff", foreign_keys=[dateCoordSignedStaffID])
    abstractStatusStaff = db.relationship("Staff", foreign_keys=[abstractStatusStaffID])
    sentToAbstractorStaff = db.relationship("Staff", foreign_keys=[sentToAbstractorStaffID])
    researcherStaff = db.relationship("Staff", foreign_keys=[researcherStaffID])
    medRecordReleaseStaff = db.relationship("Staff", foreign_keys=[medRecordReleaseStaffID])
    surveyToResearcherStaff = db.relationship("Staff", foreign_keys=[surveyToResearcherStaffID])

    def __repr__(self):
        return "<ProjectPatient(\
        participantID = {},\
        projectID = {},\
        staffID = {},\
        ctcID = {},\
        currentAge = {},\
        batch = {},\
        siteGrp = {},\
        finalCode = {},\
        finalCodeDate = {},\
        enrollmentDate = {},\
        dateCoordSigned = {},\
        importDate = {},\
        finalCodeStaff = {},\
        enrollmentStaff = {},\
        dateCoordSignedStaff = {},\
        abstractStatus = {},\
        abstractStatusDate = {},\
        abstractStatusStaff = {},\
        sentToAbstractorDate = {},\
        sentToAbstractorStaff = {},\
        abstractedDate = {},\
        abstractorInitials = {},\
        researcherDate = {},\
        researcherStaff = {},\
        consentLink = {},\
        tracingStatus = {},\
        medRecordReleaseSigned = {},\
        medRecordRelaseLink = {},\
        medRecordReleaseStaff = {},\
        medRecordReleaseDate = {},\
        surveyToResearcher = {},\
        surveyToResearcherStaff = {})>".format(
            self.participantID,
            self.projectID,
            self.staffID,
            self.ctcID,
            self.currentAge,
            self.batch,
            self.siteGrp,
            self.finalCode,
            self.finalCodeDate,
            self.enrollmentDate,
            self.dateCoordSigned,
            self.importDate,
            self.finalCodeStaff,
            self.enrollmentStaff,
            self.dateCoordSignedStaff,
            self.abstractStatus,
            self.abstractedDate,
            self.abstractStatusStaff,
            self.sentToAbstractorDate,
            self.sentToAbstractorStaffe,
            self.abstractedDate,
            self.abstractorInitials,
            self.researcherDate,
            self.researcherStaff,
            self.consentLink,
            self.tracingStatus,
            self.medRecordReleaseSigned,
            self.medRecordReleaseLink,
            self.medRecordReleaseStaff,
            self.medRecordReleaseDate,
            self.surveyToResearcher,
            self.surveyToResearcherStaff)


class ProjectStaff(CustomModel):
    __tablename__ = 'ProjectStaff'

    projectStaffID = db.Column('projectStaffID', db.Integer, primary_key=True)
    staffRoleID = db.Column('staffRoleLUTID', db.Integer, db.ForeignKey('StaffRoleLUT.staffRoleLUTID'))
    projectID = db.Column('projectID', db.Integer, db.ForeignKey('Project.projectID'), nullable=False)
    staffID = db.Column('staffID', db.Integer, db.ForeignKey('Staff.staffID'), nullable=False)
    datePledge = db.Column('date_pledge', db.Date)
    dateRevoked = db.Column('date_revoked', db.Date)
    contactID = db.Column('contactID', db.Integer, db.ForeignKey('ContactsLUT.contactID'))
    inactiveID = db.Column('inactiveID', db.Integer, db.ForeignKey('InactiveLUT.inactiveID'))

    contact = db.relationship("Contacts")
    inactive = db.relationship("Inactive")
    # Relationships
    # M - 1, Many projectStaff with the same role
    staffRole = db.relationship("StaffRoleLUT", back_populates="projectStaff")
    # M - 1, many projectStaff with the same project
    project = db.relationship("Project", back_populates="projectStaff")
    # 1  M one staff can have multiple project staff
    staff = db.relationship("Staff", foreign_keys=[staffID], back_populates="projectStaff")

    def __repr__(self):
        return "<ProjectStaff(\
        projectStaffID = {},\
        staffRoleID = {},\
        projectID = {},\
        staffID = {},\
        role = {},\
        datePledge = {},\
        dateRevoked = {},\
        contact = {},\
        inactive = {},\
        humanSubjectTrainingExp = {},\
        humanSubjectTrainingTypeID = {},\
        studyRole = {})>".format(
            self.projectStaffID,
            self.staffRoleID,
            self.projectID,
            self.staffID,
            self.role,
            self.datePledge,
            self.dateRevoked,
            self.contact,
            self.inactive,
            self.humanSubjectTrainingExp,
            self.humanSubjectTrainingTypeID,
            self.studyRole)


class ProjectStatus(CustomModel):
    __tablename__ = 'ProjectStatus'

    projectStatusID = db.Column('projectStatusID', db.Integer, primary_key=True)
    projectStatusTypeID = db.Column('projectStatusTypeID', db.Integer,
                                    db.ForeignKey('ProjectStatusLUT.projectStatusTypeID'))
    projectID = db.Column('projectID', db.Integer, db.ForeignKey('Project.projectID'), nullable=False)
    staffID = db.Column('staffID', db.Integer, db.ForeignKey('Staff.staffID'), nullable=False)
    statusDate = db.Column('statusDate', db.Date)
    statusNotes = db.Column('statusNotes', db.String)

    # Relationships
    # M -1 , many projectStatuses per projectStatusLUT
    projectStatus = db.relationship("ProjectStatusLUT", foreign_keys=[projectStatusTypeID],
                                    back_populates="projectStatuses")

    # 1 - M, one project, many statuses
    project = db.relationship("Project", foreign_keys=[projectID], back_populates="projectStatuses")
    # 1 - M, many statuses per staff
    staff = db.relationship("Staff", foreign_keys=[staffID], back_populates="projectStatuses")

    def __repr__(self):
        return "<ProjectStatus(\
        projectStatusID = {},\
        projectStatusTypeID = {},\
        projectID = {},\
        staffID = {},\
        statusDate = {},\
        statusNotes = {})>".format(
            self.projectStatusID,
            self.projectStatusTypeID,
            self.projectID,
            self.staffID,
            self.statusDate,
            self.statusNotes)


class ProjectStatusLUT(CustomModel):
    __tablename__ = 'ProjectStatusLUT'

    projectStatusTypeID = db.Column('projectStatusTypeID', db.Integer, primary_key=True)
    projectStatus = db.Column('project_status', db.String)
    projectStatusDefinition = db.Column('status_definition', db.String)

    # Relationships
    # M - 1, many ProjectStatuses per projectStatusLUT
    projectStatuses = db.relationship("ProjectStatus", back_populates="projectStatus")

    def __repr__(self):
        return "<ProjectStatusLUT(\
        projectStatusTypeID = {},\
        projectStatus = {},\
        projectStatusDefinition = {})>".format(
            self.projectStatusTypeID,
            self.projectStatus,
            self.projectStatusDefinition)


class ProjectType(CustomModel):
    __tablename__ = 'ProjectType'

    projectTypeID = db.Column('projectTypeID', db.Integer, primary_key=True)
    projectType = db.Column('project_type', db.String)
    projectTypeDefinition = db.Column('project_type_defintion', db.String)

    # Relationships
    # M - 1 Many projects with same project type
    projects = db.relationship("Project", back_populates="projectType")

    def __repr__(self):
        return "<ProjectType(\
        projectTypeID={},\
        project_type={},\
        project_type_definition={})>".format(
            self.projectTypeID,
            self.projectType,
            self.projectTypeDefinition)


class Race(CustomModel):
    __tablename__ = "RaceLUT"
    raceID = db.Column('raceID', db.Integer, primary_key=True)
    race = db.Column('race', db.String)


class ReviewCommitteeStatusLUT(CustomModel):
    __tablename__ = 'ReviewCommitteeStatusLUT'

    reviewCommitteeStatusID = db.Column('reviewCommitteeStatusLUTID', db.Integer, primary_key=True)
    reviewCommitteeStatus = db.Column('review_committee_status', db.String)
    reviewCommitteeStatusDefinition = db.Column('review_committee_status_definition', db.String)

    # Relationships
    reviewCommittees = db.relationship("ReviewCommittee", back_populates="reviewCommitteeStatusLUT")

    def __repr__(self):
        return "<RCStatusList(\
            rcStatusID = {},\
            rc_status = {},\
            rc_status_definition = {})>".format(
            self.rcStatusID,
            self.reviewCommitteeStatus,
            self.reviewCommitteeStatusDefinition)


class ReviewCommittee(CustomModel):
    __tablename__ = 'ReviewCommittee'

    reviewCommitteeID = db.Column('reviewCommitteeID', db.Integer, primary_key=True)
    projectID = db.Column('projectID', db.Integer, db.ForeignKey('Project.projectID'), nullable=False)
    reviewCommitteeStatusID = db.Column('reviewCommitteeStatusLUTID', db.Integer,
                                        db.ForeignKey('ReviewCommitteeStatusLUT.reviewCommitteeStatusLUTID'))
    reviewCommitteeLUTID = db.Column('reviewCommitteeLUT', db.Integer,
                                     db.ForeignKey('ReviewCommitteeLUT.reviewCommitteeLUTID'))
    reviewCommitteeNumber = db.Column('review_committe_number', db.String)
    dateInitialReview = db.Column('date_initial_review', db.Date)
    dateExpires = db.Column('date_expires', db.Date)
    rcNote = db.Column('review_committee_note', db.String)
    rcProtocol = db.Column('review_committee_protocol', db.String)
    rcApproval = db.Column('review_committee_approval', db.String)

    # Relationships
    # 1- M, one project many review committees
    project = db.relationship("Project", foreign_keys=[projectID], back_populates="reviewCommittees")
    # M - 1, Many review committees per rcStatus
    reviewCommitteeStatusLUT = db.relationship("ReviewCommitteeStatusLUT", foreign_keys=[reviewCommitteeStatusID],
                                               back_populates="reviewCommittees")
    # M - 1, Many review committees per rcList
    reviewCommitteeLUT = db.relationship("ReviewCommitteeLUT", foreign_keys=[reviewCommitteeLUTID],
                                         back_populates="reviewCommittees")

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
            self.projectID,
            self.rcStatusID,
            self.rcListID,
            self.reviewCommitteeNumber,
            self.dateInitialReview,
            self.dateExpires,
            self.rcNote,
            self.rcProtocol,
            self.rcApproval)


class ReviewCommitteeLUT(CustomModel):
    __tablename__ = 'ReviewCommitteeLUT'

    reviewCommitteeID = db.Column('reviewCommitteeLUTID', db.Integer, primary_key=True)
    reviewCommittee = db.Column('review_committee', db.String)
    reviewCommitteeDescription = db.Column('review_committee_description', db.String)

    # Relationships
    # M - 1 Many reviewCommittess per reviewCommitteeList
    reviewCommittees = db.relationship("ReviewCommittee", back_populates="reviewCommitteeLUT")

    def __repr__(self):
        return "<ReviewCommitteeList(\
        rcListID={},\
        reviewCommittee={},\
        rcDescription={})>".format(
            self.rcListID,
            self.reviewComittee,
            self.rcDescription)


class Sex(CustomModel):
    __tablename__ = "SexLUT"
    sexID = db.Column('sexID', db.Integer, primary_key=True)
    sex = db.Column('sex', db.String)


class Staff(CustomModel):
    __tablename__ = 'Staff'

    staffID = db.Column('staffID', db.Integer, primary_key=True)
    firstName = db.Column('first_name', db.String)
    lastName = db.Column('last_name', db.String)
    middleName = db.Column('middle_name', db.String)
    email = db.Column('email', db.String)
    phoneNumber = db.Column('phone', db.String)
    phoneComment = db.Column('phone_comment', db.String)
    institution = db.Column('institution', db.String)
    department = db.Column('department', db.String)
    position = db.Column('position', db.String)
    credentials = db.Column('credentials', db.String)
    street = db.Column('street', db.String)
    city = db.Column('city', db.String)
    stateID = db.Column('stateID', db.Integer, db.ForeignKey("StateLUT.stateID"))
    humanSubjectTrainingExp = db.Column('human_sub_training_exp', db.Date)
    ucrRoleID = db.Column('UCR_role', db.Integer, db.ForeignKey("UCRRole.ucrRoleID"))

    # Relationships
    # 1 - M, one staff with many statuses
    projectStatuses = db.relationship("ProjectStatus", back_populates="staff")
    # 1 - M, one staff with many lgos
    logs = db.relationship("Log", back_populates="staff")
    # 1 - M, one staff with many trainings
    staffTraining = db.relationship('StaffTraining', back_populates="staff")
    # M - 1, many projectStaff to staff (people can be working on multiple projects)
    projectStaff = db.relationship('ProjectStaff', back_populates="staff")
    # M - 1 many contacts can have the same staff
    contacts = db.relationship("Contact", back_populates="staff")
    # 1 - M, one study/projectPatient can have many staff
    # projectPatient = db.relationship("ProjectPatient",back_populates="staff")
    tracings = db.relationship("Tracing", back_populates="staff")
    state = db.relationship("State")
    ucrRole = db.relationship("UCRRole", back_populates="staff")

    def __repr__(self):
        return "<Staff(\
        staffID = {},\
        firstName = {},\
        lastName = {},\
        middleName = {},\
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
        humanSubjectTrainingExp = {},\
        ucrRole = {})>".format(
            self.staffID,
            self.firstName,
            self.lastName,
            self.middleName,
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
            self.humanSubjectTrainingExp,
            self.ucrRole)


class StaffRoleLUT(CustomModel):
    __tablename__ = 'StaffRoleLUT'

    staffRoleID = db.Column('staffRoleLUTID', db.Integer, primary_key=True)
    staffRole = db.Column('staff_role', db.String)
    staffRoleDescription = db.Column('staff_role_description', db.String)

    # Relationships
    # M - 1, many projectStaff with the same role
    projectStaff = db.relationship("ProjectStaff", back_populates="staffRole")

    def __repr__(self):
        return "<StaffRoleLUT(\
        staffRoleID = {},\
        staffRole = {},\
        staffRoleDescription = {})>".format(
            self.staffRoleLUTID,
            self.staffRole,
            self.staffRoleDescription)


class StaffTraining(CustomModel):
    __tablename__ = 'StaffTraining'

    staffTrainingID = db.Column('staffTrainingID', db.Integer, primary_key=True)
    staffID = db.Column('staffID', db.Integer, db.ForeignKey('Staff.staffID'), nullable=False)
    humanSubjectTrainingID = db.Column('humanSubjectTrainingID', db.Integer,
                                       db.ForeignKey('HumanSubjectTrainingLUT.humanSubjectTrainingID'))
    dateTaken = db.Column('date_taken', db.Date)
    dateExpires = db.Column('exp_date', db.Date)

    # Relationships
    # M - 1, many staffTrainings with the same HST
    humanSubjectTraining = db.relationship('HumanSubjectTrainingLUT', back_populates="staffTrainings")
    # 1 - M, one staff with many trainings
    staff = db.relationship('Staff', foreign_keys=[staffID], back_populates='staffTraining')

    def __repr__(self):
        return "<StaffTraining(\
        staffTrainingID = {},\
        staffID = {},\
        humanSubjectTrainingID = {},\
        dateTaken = {},\
        dateExpires = {})>".format(
            self.staffTrainingID,
            self.staffID,
            self.humanSubjectTrainingID,
            self.dateTaken,
            self.dateExpires)


class State(CustomModel):
    __tablename__ = "StateLUT"
    stateID = db.Column('stateID', db.Integer, primary_key=True)
    state = db.Column('state', db.String)


class Tracing(CustomModel):
    __tablename__ = "Tracing"

    tracingID = db.Column('tracingID', db.Integer, primary_key=True)
    tracingSourceID = db.Column('tracingSourceLUTID', db.Integer, db.ForeignKey('TracingSourceLUT.tracingSourceLUTID'))
    participantID = db.Column('participantID', db.Integer, db.ForeignKey('ProjectPatient.participantID'), nullable=False)
    date = db.Column('date', db.Date)
    staffID = db.Column('staffID', db.Integer, db.ForeignKey('Staff.staffID'), nullable=False)
    notes = db.Column('notes', db.String)

    # Relationships
    # M - 1, many trancings can have the same tracingSource
    tracingSource = db.relationship('TracingSourceLUT', back_populates="tracings")
    # 1 - M, one project patient with many tracings
    projectPatient = db.relationship('ProjectPatient', back_populates="tracings")

    staff = db.relationship('Staff', uselist=False, back_populates="tracings")

    def __repr__(self):
        return "<Tracing(\
        tracingID = {},\
        tracingSourceID = {},\
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
    __tablename__ = "TracingSourceLUT"

    tracingSourceID = db.Column('tracingSourceLUTID', db.Integer, primary_key=True)
    description = db.Column('tracing_source_description', db.String)

    # Relationships
    tracings = db.relationship('Tracing', back_populates="tracingSource")

    def __repr__(self):
        return "<TracingSourceLUT(\
        tracingSourceLUTID = {},\
        description = {})>".format(
            tracingSourceLUTID,
            description)


class UCRReport(CustomModel):
    __tablename__ = 'UcrReport'

    ucrReportID = db.Column('ucrReportID', db.Integer, primary_key=True)
    projectID = db.Column('projectID', db.Integer, db.ForeignKey('Project.projectID'), nullable=False)
    reportTypeID = db.Column('report_typeID', db.Integer, db.ForeignKey('UCRReportTypeLUT.ucrReportTypeID'))
    reportSubmitted = db.Column('report_submitted', db.Date)
    reportDue = db.Column('report_due', db.Date)
    reportDoc = db.Column('report_doc', db.String)

    # Relationships
    # 1 - M, one project, many reports
    reportType = db.relationship("UCRReportType")
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


class UCRReportType(CustomModel):
    __tablename__ = "UCRReportTypeLUT"
    ucrReportTypeID = db.Column('ucrReportTypeID', db.Integer, primary_key=True)
    ucrReportType = db.Column('ucrReportType', db.String)


class UCRRole(CustomModel):
    __tablename__ = "UCRRole"

    ucrRoleID = db.Column("ucrRoleID", db.Integer, primary_key=True)
    ucrRole = db.Column("ucrRole", db.String)

    staff = db.relationship("Staff", back_populates="ucrRole")


class VitalStatus(CustomModel):
    __tablename__ = "VitalStatusLUT"
    vitalStatusID = db.Column('vitalStatusID', db.Integer, primary_key=True)
    vitalStatus = db.Column('vitalStatus', db.String)
