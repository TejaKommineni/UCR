from wtforms import Form, BooleanField, StringField, IntegerField, DateField, FloatField, BooleanField, validators
import query

COMMON_STRING_VALIDATORS = [
        validators.InputRequired(),
        validators.Length(min=1)]

COMMON_INTEGER_VALIDATORS = [
    validators.input_required(),
    validators.number_range(min=0)]

COMMON_DATE_VALIDATORS = [
    validators.input_required()
]

COMMON_FLOAT_VALIDATORS = [
    validators.input_required()
]

COMMON_BOOL_VALIDATORS = [
    validators.input_required()
]

DATE_FORMAT = "%Y-%m-%d"

class BaseForm(Form):
    versionID = IntegerField('versionID',
        []+COMMON_INTEGER_VALIDATORS)

class ArcReviewForm(BaseForm):
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    reviewType = IntegerField('reviewType',
        []+COMMON_INTEGER_VALIDATORS)
    dateSentToReviewer = DateField('dateSentToReviewer',
        []+COMMON_DATE_VALIDATORS,
        format=DATE_FORMAT)
    reviewer1 = IntegerField('reviewer1',
        []+COMMON_INTEGER_VALIDATORS)
    reviewer1Rec = IntegerField('reviewer1Rec',
        []+COMMON_INTEGER_VALIDATORS)
    reviewer1SigDate = DateField('reviewer1SigDate',
        []+COMMON_DATE_VALIDATORS)
    reviewer1Comments = StringField('reviewer1Comments',
        []+COMMON_STRING_VALIDATORS)
    reviewer2 = IntegerField('reviewer2',
        []+COMMON_INTEGER_VALIDATORS)
    reviewer2Rec = IntegerField('reviewer2Rec',
        []+COMMON_INTEGER_VALIDATORS)
    reviewer2SigDate = DateField('reviewer2SigDate',
        []+COMMON_DATE_VALIDATORS)
    reviewer2Comments = StringField('reviewer2Comments',
        []+COMMON_STRING_VALIDATORS)
    research = StringField('research',
        []+COMMON_STRING_VALIDATORS)
    contact = BooleanField('contact',
        []+COMMON_BOOL_VALIDATORS)
    lnkage = BooleanField('lnkage',
        []+COMMON_BOOL_VALIDATORS)
    engaged = BooleanField('engaged',
        []+COMMON_BOOL_VALIDATORS)
    nonPublicData = BooleanField('nonPublicData',
        []+COMMON_BOOL_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False
        if not f:
            hasErrors = True

        # Check to make sure the project FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors =  True
        return not hasErrors

class BudgetForm(BaseForm):
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    numPeriods = IntegerField('numPeriods',
        []+COMMON_INTEGER_VALIDATORS)
    periodStart = DateField('periodStart',
        []+COMMON_DATE_VALIDATORS,
        format=DATE_FORMAT)
    periodEnd = DateField('periodEnd',
        []+COMMON_DATE_VALIDATORS,
        format=DATE_FORMAT)
    periodTotal = FloatField('periodTotal',
        []+COMMON_FLOAT_VALIDATORS)
    periodComment = StringField('periodComment',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors =  True
        return not hasErrors

class ContactForm(BaseForm):
    contactTypeLUTID = IntegerField('contactTypeLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    projectPatientID = IntegerField('projectPatientID',
        []+COMMON_INTEGER_VALIDATORS)
    staffID = IntegerField('staffID',
        []+COMMON_INTEGER_VALIDATORS)
    informantID = IntegerField('informantID',
        []+COMMON_INTEGER_VALIDATORS)
    facilityID = IntegerField('facilityID',
        []+COMMON_INTEGER_VALIDATORS)
    physicianID = IntegerField('physicianID',
        []+COMMON_INTEGER_VALIDATORS)
    description = StringField('description',
        []+COMMON_STRING_VALIDATORS)
    contactDate = DateField('contactDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    initials = StringField('initials',
        []+COMMON_STRING_VALIDATORS)
    notes = StringField('notes',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project FK exists
        projectPatient = query.get_project_patient(self.projectPatientID.data)
        if projectPatient is None:
            self.projectPatientID.errors.append("ID not found")
            hasErrors =  True

        contactType = query.get_contact_type(self.contactTypeLUTID.data)
        if contactType is None:
            self.contactTypeLUTID.errors.append("ID not found")
            hasErrors =  True

        staff = query.get_staff(self.staffID.data)
        if staff is None:
            self.staffID.errors.append("ID not found")
            hasErrors =  True

        informant = query.get_informant(self.informantID.data)
        if informant is None:
            self.informantID.errors.append("ID not found")
            hasErrors =  True

        facility = query.get_project_patient(self.facilityID.data)
        if facility is None:
            self.facilityID.errors.append("ID not found")
            hasErrors =  True

        physician = query.get_physician(self.physicianID.data)
        if physician is None:
            self.physicianID.errors.append("ID not found")
            hasErrors =  True
        return not hasErrors

class ContactInfoSourceForm(BaseForm):
    contactInfoSource = StringField('contactInfoSource',
        []+COMMON_STRING_VALIDATORS)

class ContactInfoStatusForm(BaseForm):
    contactInfoStatus = StringField('contactInfoStatus',
        []+COMMON_STRING_VALIDATORS)

class ContactTypeLUTForm(BaseForm):
    contactDefinition = StringField('contactDefinition',
        []+COMMON_STRING_VALIDATORS)

class CTCFacilityForm(BaseForm):
    ctcID = IntegerField('ctcID',
        []+COMMON_INTEGER_VALIDATORS)
    facilityID = IntegerField('facilityID',
        []+COMMON_INTEGER_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project FK exists
        ctc = query.get_ctc(self.ctcID.data)
        if ctc is None:
            self.ctcID.errors.append("ID not found")
            hasErrors =  True

        facility = query.get_facility(self.facilityID.data)
        if facility is None:
            self.facilityID.errors.append("ID not found")
            hasErrors =  True
        return not hasErrors

class CTCForm(BaseForm):
    patientID = IntegerField('patientID',
        []+COMMON_INTEGER_VALIDATORS)
    dxDate = DateField('dxDate',
        []+COMMON_DATE_VALIDATORS,
        format= DATE_FORMAT)
    site = IntegerField('site',
        []+COMMON_INTEGER_VALIDATORS)
    histology = StringField('histology',
        []+COMMON_STRING_VALIDATORS)
    behavior = StringField('behavior',
        []+COMMON_STRING_VALIDATORS)
    ctcSequence = StringField('ctcSequence',
        []+COMMON_STRING_VALIDATORS)
    stage = StringField('stage',
        []+COMMON_STRING_VALIDATORS)
    dxAge = IntegerField('dxAge',
        []+COMMON_INTEGER_VALIDATORS)
    dxStreet1 = StringField('dxStreet1',
        []+COMMON_STRING_VALIDATORS)
    dxStreet2 = StringField('dxStreet2',
        []+COMMON_STRING_VALIDATORS)
    dxCity = StringField('dxCity',
        []+COMMON_STRING_VALIDATORS)
    dxState = StringField('dxState',
        []+COMMON_STRING_VALIDATORS)
    dxZip = IntegerField('dxZip',
        []+COMMON_INTEGER_VALIDATORS)
    dxCounty = StringField('dxCounty',
        []+COMMON_STRING_VALIDATORS)
    dnc = StringField('dnc',
        []+COMMON_STRING_VALIDATORS)
    dncReason = StringField('dncReason',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project FK exists
        patient = query.get_patient(self.patientID.data)
        if patient is None:
            self.projectID.errors.append("ID not found")
            hasErrors =  True

        return not hasErrors

class FacilityForm(BaseForm):
    facilityName = StringField('facilityName',
        []+COMMON_STRING_VALIDATORS)
    contactFirstName = StringField('contactFirstName',
        []+COMMON_STRING_VALIDATORS)
    contactLastName = StringField('contactLastName',
        []+COMMON_STRING_VALIDATORS)
    facilityStatus = IntegerField('facilityStatus',
        []+COMMON_INTEGER_VALIDATORS)
    facilityStatusDate = DateField('facilityStatusDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    contact2FirstName = StringField('contact2FirstName',
        []+COMMON_STRING_VALIDATORS)
    contact2LastName = StringField('contact2LastName',
        []+COMMON_STRING_VALIDATORS)

class FacilityAddressForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
        []+COMMON_INTEGER_VALIDATORS)
    facilityID = IntegerField('facilityID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    street = StringField('street',
        []+COMMON_STRING_VALIDATORS)
    street2 = StringField('street2',
        []+COMMON_STRING_VALIDATORS)
    city = StringField('city',
        []+COMMON_STRING_VALIDATORS)
    state = StringField('state',
        []+COMMON_STRING_VALIDATORS)
    zip = StringField('zip',
        []+COMMON_STRING_VALIDATORS)
    addressStatus = IntegerField('addressStatus',
        []+COMMON_INTEGER_VALIDATORS)
    addressStatusDate = DateField('addressStatusDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    addressStatusSource = StringField('addressStatusSource',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
        if contactSource is None:
            self.contactInfoSourceID.errors.append("ID not found")
            hasErrors = True

        facility = query.get_facility(self.facilityID.data)
        if facility is None:
            self.facilityID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
        if contactStatus is None:
            self.contactInfoStatusID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class FacilityPhoneForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
        []+COMMON_INTEGER_VALIDATORS)
    facilityID = IntegerField('facilityID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    phoneNumber = StringField('phoneNumber',
        []+COMMON_STRING_VALIDATORS)
    clinicName = StringField('clinicName',
        []+COMMON_STRING_VALIDATORS)
    phoneType = StringField('phoneType',
        []+COMMON_STRING_VALIDATORS)
    phoneSource = StringField('phoneSource',
        []+COMMON_STRING_VALIDATORS)
    phoneStatus = StringField('phoneStatus',
        []+COMMON_STRING_VALIDATORS)
    phoneStatusDate = DateField('phoneStatusDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
        if contactSource is None:
            self.contactInfoSourceID.errors.append("ID not found")
            hasErrors = True

        facility = query.get_facility(self.facilityID.data)
        if facility is None:
            self.facilityID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
        if contactStatus is None:
            self.contactInfoStatusID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class FundingForm(BaseForm):
    grantStatusID = IntegerField('grantStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    fundingSourceID = IntegerField('fundingSourceID',
        []+COMMON_INTEGER_VALIDATORS)
    primaryFundingSource = StringField('primaryFundingSource',
        []+COMMON_STRING_VALIDATORS)
    secondaryFundingSource = StringField('secondaryFundingSource',
        []+COMMON_STRING_VALIDATORS)
    fundingNumber = StringField('fundingNumber',
        []+COMMON_STRING_VALIDATORS)
    grantTitle = StringField('grantTitle',
        []+COMMON_STRING_VALIDATORS)
    dateStatus = DateField('dateStatus',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    grantPi = IntegerField('grantPi',
        []+COMMON_INTEGER_VALIDATORS)
    primaryChartfield = StringField('primaryChartfield',
        []+COMMON_STRING_VALIDATORS)
    secondaryChartfield = StringField('secondaryChartfield',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors =  True

        grantStatus = query.get_grant_status(self.grantStatusID.data)
        if grantStatus is None:
            self.grantStatusID.errors.append("ID not found")
            hasErrors = True

        fundingSource = query.get_funding_source(self.fundingSourceID.data)
        if fundingSource is None:
            self.fundingSourceID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class FundingSourceLUTForm(BaseForm):
    fundingSource = StringField('fundingSource',
        []+COMMON_STRING_VALIDATORS)

class GrantStatusLUTForm(BaseForm):
    grantStatus = StringField('grantStatus',
        []+COMMON_STRING_VALIDATORS)

class HumanSubjectTrainingLUTForm(BaseForm):
    trainingType = StringField('trainingType',
        []+COMMON_STRING_VALIDATORS)

class IRBHolderLUTForm(BaseForm):
    holder = StringField('holder',
        []+COMMON_STRING_VALIDATORS)
    holderDefinition = StringField('holderDefinition',
        []+COMMON_STRING_VALIDATORS)

class InformantForm(BaseForm):
    patientID = IntegerField('patientID',
        []+COMMON_INTEGER_VALIDATORS)
    firstName = StringField('firstName',
        []+COMMON_STRING_VALIDATORS)
    lastName = StringField('lastName',
        []+COMMON_STRING_VALIDATORS)
    middleName = StringField('middleName',
        []+COMMON_STRING_VALIDATORS)
    informantPrimary = StringField('informantPrimary',
        []+COMMON_STRING_VALIDATORS)
    informantRelationship = StringField('informantRelationship',
        []+COMMON_STRING_VALIDATORS)
    notes = StringField('notes',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)
        patient = query.get_patient(self.patientID.data)
        if patient is None:
            self.patientID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class InformantAddressForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
        []+COMMON_INTEGER_VALIDATORS)
    informantID = IntegerField('informantID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    street = StringField('street',
        []+COMMON_STRING_VALIDATORS)
    street2 = StringField('street2',
        []+COMMON_STRING_VALIDATORS)
    city = StringField('city',
        []+COMMON_STRING_VALIDATORS)
    state = StringField('state',
        []+COMMON_STRING_VALIDATORS)
    zip = StringField('zip',
        []+COMMON_STRING_VALIDATORS)
    addressStatus = IntegerField('addressStatus',
        []+COMMON_INTEGER_VALIDATORS)
    addressStatusDate = DateField('addressStatusDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    addressStatusSource = StringField('addressStatusSource',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
        if contactSource is None:
            self.contactInfoSourceID.errors.append("ID not found")
            hasErrors = True

        informant = query.get_informant(self.informantID.data)
        if informant is None:
            self.informantID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
        if contactStatus is None:
            self.contactInfoStatusID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class InformantPhoneForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
        []+COMMON_INTEGER_VALIDATORS)
    informantID = IntegerField('informantID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    phoneNumber = StringField('phoneNumber',
        []+COMMON_STRING_VALIDATORS)
    phoneSource = StringField('phoneSource',
        []+COMMON_STRING_VALIDATORS)
    phoneStatus = StringField('phoneStatus',
        []+COMMON_STRING_VALIDATORS)
    phoneStatusDate = DateField('phoneStatusDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
        if contactSource is None:
            self.contactInfoSourceID.errors.append("ID not found")
            hasErrors = True

        informant = query.get_informant(self.informantID.data)
        if informant is None:
            self.informantID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
        if contactStatus is None:
            self.contactInfoStatusID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class LogForm(BaseForm):
    logSubjectID =  IntegerField('logSubjectID',
        []+COMMON_INTEGER_VALIDATORS)
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    staffID = IntegerField('staffID',
        []+COMMON_INTEGER_VALIDATORS)
    phaseStatusID = IntegerField('phaseStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    note = StringField('note',
        []+COMMON_STRING_VALIDATORS)
    date = DateField('date',
        []+COMMON_DATE_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors =  True

        logSubject = query.get_log_subject(self.logSubjectID.data)
        if logSubject is None:
            self.logSubjectID.errors.append("ID not found")
            hasErrors = True

        staff = query.get_staff(self.staffID.data)
        if staff is None:
            self.staffID.errors.append("ID not found")
            hasErrors = True

        phaseStatus = query.get_phase_status(self.phaseStatusID.data)
        if phaseStatus is None:
            self.phaseStatusID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class LogSubjectLUTForm(BaseForm):
    logSubject = StringField('logSubject',
        []+COMMON_STRING_VALIDATORS)

class PatientForm(BaseForm):
    patID = StringField('patID',
        []+COMMON_STRING_VALIDATORS)
    recordID = IntegerField('recordID',
        []+COMMON_INTEGER_VALIDATORS)
    ucrDistID = IntegerField('ucrDistID',
        []+COMMON_INTEGER_VALIDATORS)
    UPDBID = IntegerField('UPDBID',
        []+COMMON_INTEGER_VALIDATORS)
    firstName = StringField('firstName',
        []+COMMON_STRING_VALIDATORS)
    lastName = StringField('lastName',
        []+COMMON_STRING_VALIDATORS)
    middleName = StringField('middleName',
        []+COMMON_STRING_VALIDATORS)
    maidenName = StringField('maidenName',
        []+COMMON_STRING_VALIDATORS)
    aliasFirstName = StringField('aliasFirstName',
        []+COMMON_STRING_VALIDATORS)
    aliasLastName = StringField('aliasLastName',
        []+COMMON_STRING_VALIDATORS)
    aliasMiddleName = StringField('aliasMiddleName',
        []+COMMON_STRING_VALIDATORS)
    dob = DateField('dob',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    SSN = IntegerField('SSN',
        []+COMMON_INTEGER_VALIDATORS)
    sex = StringField('sex',
        []+COMMON_STRING_VALIDATORS)
    race = StringField('race',
        []+COMMON_STRING_VALIDATORS)
    ethnicity = StringField('ethnicity',
        []+COMMON_STRING_VALIDATORS)
    vitalStatus = StringField('vitalStatus',
        []+COMMON_STRING_VALIDATORS)

class PatientAddressForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
        []+COMMON_INTEGER_VALIDATORS)
    patientID = IntegerField('patientID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    street = StringField('street',
        []+COMMON_STRING_VALIDATORS)
    street2 = StringField('street2',
        []+COMMON_STRING_VALIDATORS)
    city = StringField('city',
        []+COMMON_STRING_VALIDATORS)
    state = StringField('state',
        []+COMMON_STRING_VALIDATORS)
    zip = StringField('zip',
        []+COMMON_STRING_VALIDATORS)
    addressStatus = IntegerField('addressStatus',
        []+COMMON_INTEGER_VALIDATORS)
    addressStatusDate = DateField('addressStatusDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    addressStatusSource = StringField('addressStatusSource',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
        if contactSource is None:
            self.contactInfoSourceID.errors.append("ID not found")
            hasErrors = True

        patient = query.get_patient(self.patientID.data)
        if patient is None:
            self.patientID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
        if contactStatus is None:
            self.contactInfoStatusID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class PatientEmailForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
        []+COMMON_INTEGER_VALIDATORS)
    patientID = IntegerField('patientID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    email = StringField('email',
        []+COMMON_STRING_VALIDATORS)
    emailStatus = IntegerField('emailStatus',
        []+COMMON_INTEGER_VALIDATORS)
    emailSource = IntegerField('emailSource',
        []+COMMON_INTEGER_VALIDATORS)
    emailStatusDate = DateField('emailStatusDate',
        []+COMMON_DATE_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
        if contactSource is None:
            self.contactInfoSourceID.errors.append("ID not found")
            hasErrors = True

        patient = query.get_patient(self.patientID.data)
        if patient is None:
            self.patientID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
        if contactStatus is None:
            self.contactInfoStatusID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class PatientPhoneForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
        []+COMMON_INTEGER_VALIDATORS)
    patientID = IntegerField('patientID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    phoneNumber = StringField('phoneNumber',
        []+COMMON_STRING_VALIDATORS)
    phoneSource = StringField('phoneSource',
        []+COMMON_STRING_VALIDATORS)
    phoneStatus = StringField('phoneStatus',
        []+COMMON_STRING_VALIDATORS)
    phoneStatusDate = DateField('phoneStatusDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
        if contactSource is None:
            self.contactInfoSourceID.errors.append("ID not found")
            hasErrors = True

        patient = query.get_patient(self.patientID.data)
        if patient is None:
            self.patientID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
        if contactStatus is None:
            self.contactInfoStatusID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class PatientProjectStatusForm(BaseForm):
    patientProjectStatusTypeID = IntegerField('patientProjectStatusTypeID',
        []+COMMON_INTEGER_VALIDATORS)
    projectPatientID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        patientProjectStatusLUT = query.get_patient_project_status_type(self.patientProjectStatusTypeID.data)
        if patientProjectStatusLUT is None:
            self.patientProjectStatusTypeID.errors.append("ID not found")
            hasErrors = True

        projectPatient = query.get_project_patient(self.projectPatientID.data)
        if projectPatient is None:
            self.projectPatientID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class PatientProjectStatusLUTForm(BaseForm):
    statusDescription = StringField('statusDescription',
        []+COMMON_STRING_VALIDATORS)

class PhaseStatusForm(BaseForm):
    phaseStatus = StringField('phaseStatus',
        []+COMMON_STRING_VALIDATORS)
    phaseDescription = StringField('phaseDescription',
        []+COMMON_STRING_VALIDATORS)

class PhysicianForm(BaseForm):
    firstName = StringField('fname',
        []+COMMON_STRING_VALIDATORS)
    lastName = StringField('lname',
        []+COMMON_STRING_VALIDATORS)
    middleName = StringField('middle_name',
        []+COMMON_STRING_VALIDATORS)
    credentials = StringField('credentials',
        []+COMMON_STRING_VALIDATORS)
    specialty = StringField('specialty',
        []+COMMON_STRING_VALIDATORS)
    aliasFirstName = StringField('alias_fname',
        []+COMMON_STRING_VALIDATORS)
    aliasLastName = StringField('alias_lname',
        []+COMMON_STRING_VALIDATORS)
    aliasMiddleName = StringField('alias_middle_name',
        []+COMMON_STRING_VALIDATORS)
    physicianStatus = IntegerField('physician_status',
        []+COMMON_INTEGER_VALIDATORS)
    physicianStatusDate = DateField('physician_status_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    email = StringField('email',
        []+COMMON_STRING_VALIDATORS)

class PhysicianFacilityForm(BaseForm):
    facilityID = IntegerField('facilityID',
        []+COMMON_INTEGER_VALIDATORS)
    physicianID = IntegerField('physicianID',
        []+COMMON_INTEGER_VALIDATORS)
    physFacilityStatus = IntegerField('physFacilityStatus',
        []+COMMON_INTEGER_VALIDATORS)
    physFacilityStatusDate = DateField('physFacilityStatusDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        facility = query.get_facility(self.facilityID.data)
        if facility is None:
            self.facilityID.errors.append("ID not found")
            hasErrors = True

        physician = query.get_physician(self.physicianID.data)
        if physician is None:
            self.physicianID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class PhysicianAddressForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
        []+COMMON_INTEGER_VALIDATORS)
    physicianID = IntegerField('physicianID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    street = StringField('street',
        []+COMMON_STRING_VALIDATORS)
    street2 = StringField('street2',
        []+COMMON_STRING_VALIDATORS)
    city = StringField('city',
        []+COMMON_STRING_VALIDATORS)
    state = StringField('state',
        []+COMMON_STRING_VALIDATORS)
    zip = StringField('zip',
        []+COMMON_STRING_VALIDATORS)
    addressStatus = IntegerField('addressStatus',
        []+COMMON_INTEGER_VALIDATORS)
    addressStatusDate = DateField('addressStatusDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    addressStatusSource = StringField('addressStatusSource',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
        if contactSource is None:
            self.contactInfoSourceID.errors.append("ID not found")
            hasErrors = True

        physician = query.get_physician(self.physicianID.data)
        if physician is None:
            self.physicianID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
        if contactStatus is None:
            self.contactInfoStatusID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class PhysicianPhoneForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
        []+COMMON_INTEGER_VALIDATORS)
    physicianID = IntegerField('physicianID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    phoneNumber = StringField('phoneNumber',
        []+COMMON_STRING_VALIDATORS)
    phoneType = StringField('phoneType',
        []+COMMON_STRING_VALIDATORS)
    phoneSource = StringField('phoneSource',
        []+COMMON_STRING_VALIDATORS)
    phoneStatus = StringField('phoneStatus',
        []+COMMON_STRING_VALIDATORS)
    phoneStatusDate = DateField('phoneStatusDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
        if contactSource is None:
            self.contactInfoSourceID.errors.append("ID not found")
            hasErrors = True

        physician = query.get_physician(self.physicianID.data)
        if physician is None:
            self.physicianID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
        if contactStatus is None:
            self.contactInfoStatusID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class PhysicianToCTCForm(BaseForm):
    physicianID = IntegerField('physicianID',
        []+COMMON_INTEGER_VALIDATORS)
    ctcID = IntegerField('ctcID',
        []+COMMON_INTEGER_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        physician = query.get_physician(self.physicianID.data)
        if physician is None:
            self.physicianID.errors.append("ID not found")
            hasErrors = True

        ctc = query.get_ctc(self.ctcID.data)
        if physician is None:
            self.ctcID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class PreApplicationForm(BaseForm):
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    piFirstName = StringField('piFirstName',
        []+COMMON_STRING_VALIDATORS)
    piLastName = StringField('piLastName',
        []+COMMON_STRING_VALIDATORS)
    piPhone = StringField('piPhone',
        []+COMMON_STRING_VALIDATORS)
    piEmail = StringField('piEmail',
        []+COMMON_STRING_VALIDATORS)
    contactFirstName = StringField('contactFirstName',
        []+COMMON_STRING_VALIDATORS)
    contactLastName = StringField('contactLastName',
        []+COMMON_STRING_VALIDATORS)
    contactPhone = StringField('contactPhone',
        []+COMMON_STRING_VALIDATORS)
    contactEmail = StringField('contactEmail',
        []+COMMON_STRING_VALIDATORS)
    institution = StringField('institution',
        []+COMMON_STRING_VALIDATORS)
    institution2 = StringField('institution2',
        []+COMMON_STRING_VALIDATORS)
    uid = StringField('uid',
        []+COMMON_STRING_VALIDATORS)
    udoh = IntegerField('udoh',
        []+COMMON_INTEGER_VALIDATORS)
    projectTitle = StringField('projectTitle',
        []+COMMON_STRING_VALIDATORS)
    purpose = StringField('purpose',
        []+COMMON_STRING_VALIDATORS)
    irb0 = BooleanField('irb0',
        []+COMMON_BOOL_VALIDATORS)
    irb1 = BooleanField('irb1',
        []+COMMON_BOOL_VALIDATORS)
    irb2 = BooleanField('irb2',
        []+COMMON_BOOL_VALIDATORS)
    irb3 = BooleanField('irb3',
        []+COMMON_BOOL_VALIDATORS)
    irb4 = BooleanField('irb4',
        []+COMMON_BOOL_VALIDATORS)
    otherIrb = StringField('otherIrb',
        []+COMMON_STRING_VALIDATORS)
    updb = BooleanField('updb',
        []+COMMON_BOOL_VALIDATORS)
    ptContact = BooleanField('ptContact',
        []+COMMON_BOOL_VALIDATORS)
    startDate = DateField('startDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    link = BooleanField('link',
        []+COMMON_BOOL_VALIDATORS)
    deliveryDate = DateField('deliveryDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    description = StringField('description',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project type FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors =  True
        return not hasErrors

class ProjectForm(BaseForm):
    projectTypeID = IntegerField('projectTypeID',
        [] + COMMON_INTEGER_VALIDATORS)
    irbHolderID = IntegerField('irbHolderID',
        []+COMMON_INTEGER_VALIDATORS)
    projectName = StringField('projectName',
        []+COMMON_STRING_VALIDATORS)
    shortTitle = StringField('shortTitle',
        []+COMMON_STRING_VALIDATORS)
    projectSummary = StringField('projectSummary',
        []+COMMON_STRING_VALIDATORS)
    sop = StringField('sop',
        []+COMMON_STRING_VALIDATORS)
    ucrProposal = StringField('ucrProposal',
        []+COMMON_STRING_VALIDATORS)
    budgetDoc = StringField('budgetDoc',
        []+COMMON_STRING_VALIDATORS)
    ucrFee = StringField('ucrFee',
        []+COMMON_STRING_VALIDATORS)
    ucrNoFee = StringField('ucrNoFee',
        []+COMMON_STRING_VALIDATORS)
    budgetEndDate = DateField('budgetEndDate',
        []+COMMON_DATE_VALIDATORS,
        format = "%Y-%m-%d")
    previousShortTitle = StringField('previousShortTitle',
        []+COMMON_STRING_VALIDATORS)
    dateAdded = DateField('dateAdded',
        []+COMMON_DATE_VALIDATORS,
        format=DATE_FORMAT)
    finalRecruitmentReport = StringField('finalRecruitmentReport',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project type FK exists
        projType = query.get_project_type(self.projectTypeID.data)
        if projType is None:
            self.projectTypeID.errors.append("ID not found")
            hasErrors =  True

        # check the irbHolderLUT FK
        irbHolder = query.get_irb_holder(self.irbHolderID.data)
        if irbHolder is None:
            self.irbHolderID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class ProjectPatientForm(BaseForm):
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    staffID = IntegerField('staffID',
        []+COMMON_INTEGER_VALIDATORS)
    ctcID = IntegerField('ctcID',
        []+COMMON_INTEGER_VALIDATORS)
    currentAge = IntegerField('currentAge',
        []+COMMON_INTEGER_VALIDATORS)
    batch = IntegerField('batch',
        []+COMMON_INTEGER_VALIDATORS)
    siteGrp = IntegerField('siteGrp',
        []+COMMON_INTEGER_VALIDATORS)
    finalCode = IntegerField('finalCode',
        []+COMMON_INTEGER_VALIDATORS)
    finalCodeDate = DateField('finalCodeDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    enrollmentDate = DateField('enrollmentDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    dateCoordSigned = DateField('dateCoordSigned',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    importDate = DateField('importDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    finalCodeStaff = IntegerField('finalCodeStaff',
        []+COMMON_INTEGER_VALIDATORS)
    enrollmentStaff = IntegerField('enrollmentStaff',
        []+COMMON_INTEGER_VALIDATORS)
    dateCoordSignedStaff = DateField('dateCoordSignedStaff',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    abstractStatus = IntegerField('abstractStatus',
        []+COMMON_INTEGER_VALIDATORS)
    abstractStatusDate = DateField('abstractStatusDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    abstractStatusStaff = IntegerField('abstractStatusStaff',
        []+COMMON_INTEGER_VALIDATORS)
    sentToAbstractorDate = DateField('sentToAbstractorDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    sentToAbstractorStaff = IntegerField('sentToAbstractorStaff',
        []+COMMON_INTEGER_VALIDATORS)
    abstractedDate = DateField('abstractedDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    abstractorInitials = StringField('abstractorInitials',
        []+COMMON_STRING_VALIDATORS)
    researcherDate = DateField('researcherDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    researcherStaff = IntegerField('researcherStaff',
        []+COMMON_INTEGER_VALIDATORS)
    consentLink = StringField('consentLink',
        []+COMMON_STRING_VALIDATORS)
    tracingStatus = IntegerField('tracingStatus',
        []+COMMON_INTEGER_VALIDATORS)
    medRecordReleaseSigned = BooleanField('medRecordReleaseSigned',
        []+COMMON_BOOL_VALIDATORS)
    medRecordReleaseLink = StringField('medRecordReleaseLink',
        []+COMMON_STRING_VALIDATORS)
    medRecordReleaseStaff = IntegerField('medRecordReleaseStaff',
        []+COMMON_INTEGER_VALIDATORS)
    medRecordReleaseDate = DateField('medRecordReleaseDate',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    surveyToResearcher = DateField('surveyToResearcher',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    surveyToResearcherStaff = IntegerField('surveyToResearcherStaff',
        []+COMMON_INTEGER_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors = True

        staff = query.get_staff(self.staffID.data)
        if staff is None:
            self.staffID.errors.append("ID not found")
            hasErrors = True

        ctc = query.get_ctc(self.ctcID.data)
        if ctc is None:
            self.ctcID.errors.append("ID not found")
            hasErrors = True

        return not hasErrors

class ProjectStaffForm(BaseForm):
    staffRoleID = IntegerField('staffRoleID',
        []+COMMON_INTEGER_VALIDATORS)
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    staffID = IntegerField('staffID',
        []+COMMON_INTEGER_VALIDATORS)
    role = IntegerField('role',
        []+COMMON_INTEGER_VALIDATORS)
    datePledge = DateField('datePledge',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    dateRevoked = DateField('dateRevoked',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    contact = StringField('contact',
        []+COMMON_STRING_VALIDATORS)
    inactive = StringField('inactive',
        []+COMMON_STRING_VALIDATORS)
    humanSubjectTrainingExp = DateField('humanSubjectTrainingExp',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    humanSubjectTrainingTypeID = IntegerField('humanSubjectTrainingTypeID',
        []+COMMON_INTEGER_VALIDATORS)
    studyRole = IntegerField('studyRole',
        []+COMMON_INTEGER_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project type FK exists
        project = query.get_project_type(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors =  True

        staff = query.get_staff(self.staffID.data)
        if staff is None:
            self.staffID.errors.append("ID not found")
            hasErrors = True

        staffRole = query.get_staff_role(self.staffRoleID.data)
        if staffRole is None:
            self.staffRoleID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class ProjectStatusForm(BaseForm):
    projectStatusTypeID = IntegerField('projectStatusTypeID',
        []+COMMON_INTEGER_VALIDATORS)
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    staffID = IntegerField('staffID',
        []+COMMON_INTEGER_VALIDATORS)
    statusDate = DateField('statusDate',
        []+COMMON_DATE_VALIDATORS,
        format=DATE_FORMAT)
    statusNotes = StringField('statusNotes',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project type FK exists
        project = query.get_project_type(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors =  True

        projectStatus = query.get_project_status_lut(self.projectStatusTypeID.data)
        if projectStatus is None:
            self.projectStatusTypeID.errors.append("ID not found")
            hasErrors = True

        staff = query.get_staff(self.staffID.data)
        if staff is None:
            self.staffID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class ProjectStatusLUTForm(BaseForm):
    projectStatus = StringField('projectStatus',
        []+COMMON_STRING_VALIDATORS)
    projectStatusDefinition = StringField('projectStatusDefinition',
        []+COMMON_STRING_VALIDATORS)

class ProjectTypeForm(BaseForm):
    projectType = StringField('projectType',
        []+COMMON_STRING_VALIDATORS)
    projectTypeDefinition = StringField('projectTypeDefinition',
        []+COMMON_STRING_VALIDATORS)

class RCStatusListForm(BaseForm):
    rcStatus = StringField('rc_status',
        []+COMMON_STRING_VALIDATORS)
    rcStatusDefinition = StringField('rc_status_definition',
        []+COMMON_STRING_VALIDATORS)

class ReviewCommitteeForm(BaseForm):
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    rcStatusID = IntegerField('rcStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    rcListID = IntegerField('rcListID',
        []+COMMON_INTEGER_VALIDATORS)
    reviewCommitteeNumber = StringField('reviewCommitteeNumber',
        []+COMMON_STRING_VALIDATORS)
    dateInitialReview = DateField('dateInitialReview',
        []+COMMON_DATE_VALIDATORS,
        format=DATE_FORMAT)
    dateExpires = DateField('dateExpires',
        []+COMMON_DATE_VALIDATORS,
        format=DATE_FORMAT)
    rcNote = StringField('rcNote',
        []+COMMON_STRING_VALIDATORS)
    rcProtocol = StringField('rcProtocol',
        []+COMMON_STRING_VALIDATORS)
    rcApproval = StringField('rcApproval',
        []+COMMON_STRING_VALIDATORS)


    def validate(self):
        f = Form.validate(self)
        hasErrors = False # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project  FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors =  True

        # check the rcStatus FK
        rcStatus = query.get_rc_status(self.rcStatusID.data)
        if rcStatus is None:
            self.rcStatusID.errors.append("ID not found")
            hasErrors = True

        # check the reviewCommitteeList FK
        rc = query.get_rc_status(self.rcListID.data)
        if rc is None:
            self.rcListID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class ReviewCommitteeListForm(BaseForm):
    reviewCommittee = StringField('reviewCommittee',
        []+COMMON_STRING_VALIDATORS)
    rcDescription = StringField('rcDescription',
        []+COMMON_STRING_VALIDATORS)

class StaffForm(BaseForm):
    firstName = StringField('firstName',
        []+COMMON_STRING_VALIDATORS)
    lastName = StringField('lastName',
        []+COMMON_STRING_VALIDATORS)
    middleName = StringField('middleName',
        []+COMMON_STRING_VALIDATORS)
    email = StringField('email',
        []+COMMON_STRING_VALIDATORS)
    phoneNumber = StringField('phoneNumber',
        []+COMMON_STRING_VALIDATORS)
    phoneComment = StringField('phoneComment',
        []+COMMON_STRING_VALIDATORS)
    institution = StringField('institution',
        []+COMMON_STRING_VALIDATORS)
    department = StringField('department',
        []+COMMON_STRING_VALIDATORS)
    position = StringField('position',
        []+COMMON_STRING_VALIDATORS)
    credentials = StringField('credentials',
        []+COMMON_STRING_VALIDATORS)
    street = StringField('street',
        []+COMMON_STRING_VALIDATORS)
    city = StringField('city',
        []+COMMON_STRING_VALIDATORS)
    state = StringField('state',
        []+COMMON_STRING_VALIDATORS)
    humanSubjectTrainingExp = DateField('humanSubjectTrainingExp',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    ucrRole = IntegerField('ucrRole',
        []+COMMON_INTEGER_VALIDATORS)

class StaffRoleLUTForm(BaseForm):
    staffRole = StringField('staffRole',
        []+COMMON_STRING_VALIDATORS)
    staffRoleDescription = StringField('staffRoleDescription',
        []+COMMON_STRING_VALIDATORS)

class StaffTrainingForm(BaseForm):
    staffID = IntegerField('staffID',
        []+COMMON_INTEGER_VALIDATORS)
    humanSubjectTrainingID = IntegerField('humanSubjectTrainingID',
        []+COMMON_INTEGER_VALIDATORS)
    dateTaken = DateField('dateTaken',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    dateExpires = DateField('dateExpires',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project  FK exists
        staff = query.get_staff(self.staffID.data)
        if staff is None:
            self.staffID.errors.append("ID not found")
            hasErrors =  True

        # check the rcStatus FK
        hst = query.get_human_subject_training(self.humanSubjectTrainingID.data)
        if hst is None:
            self.humanSubjectTrainingID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class TracingForm(BaseForm):
    tracingSourceID = IntegerField('tracingSourceID',
        []+COMMON_INTEGER_VALIDATORS)
    projectPatientID = IntegerField('projectPatientID',
        []+COMMON_INTEGER_VALIDATORS)
    date = DateField('date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    staff = IntegerField('staff',
        []+COMMON_INTEGER_VALIDATORS)
    notes = StringField('notes',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project type FK exists
        projectPatient = query.get_project_patient(self.projectPatientID.data)
        if projectPatient is None:
            self.projectPatientID.errors.append("ID not found")
            hasErrors =  True

        # check the irbHolderLUT FK
        tracingSource = query.get_tracing_source(self.tracingSourceID.data)
        if tracingSource is None:
            self.tracingSourceID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class TracingSourceLUTForm(BaseForm):
    description = StringField('description',
        []+COMMON_STRING_VALIDATORS)

class UCRReportForm(BaseForm):
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    reportType = IntegerField('reportType',
        []+COMMON_INTEGER_VALIDATORS)
    reportSubmitted = DateField('reportSubmitted',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    reportDue = DateField('reportDue',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    reportDoc = StringField('reportDoc',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False
        if not f:
            hasErrors = True

        # Check to make sure the project FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors =  True
        return not hasErrors
