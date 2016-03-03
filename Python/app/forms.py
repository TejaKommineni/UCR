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

class ArcReviewForm(Form):
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

class BudgetForm(Form):
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

class ContactForm(Form):
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

class ContactInfoSourceForm(Form):
    contactInfoSource = StringField('contactInfoSource',
        []+COMMON_STRING_VALIDATORS)

class ContactInfoStatusForm(Form):
    contactInfoStatus = StringField('contactInfoStatus',
        []+COMMON_STRING_VALIDATORS)

class ContactTypeLUTForm(Form):
    contactDefinition = StringField('contactDefinition',
        []+COMMON_STRING_VALIDATORS)

class CTCFacilityForm(Form):
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

class CTCForm(Form):
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

class FacilityForm(Form):
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

class FacilityAddressForm(Form):
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

class FacilityPhoneForm(Form):
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

class FundingForm(Form):
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

class FundingSourceLUTForm(Form):
    fundingSource = StringField('fundingSource',
        []+COMMON_STRING_VALIDATORS)

class GrantStatusLUTForm(Form):
    grantStatus = StringField('grantStatus',
        []+COMMON_STRING_VALIDATORS)

class HumanSubjectTrainingLUTForm(Form):
    trainingType = StringField('trainingType',
        []+COMMON_STRING_VALIDATORS)

class IRBHolderLUTForm(Form):
    holder = StringField('holder',
        []+COMMON_STRING_VALIDATORS)
    holderDefinition = StringField('holderDefinition',
        []+COMMON_STRING_VALIDATORS)

class InformantForm(Form):
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

class InformantAddressForm(Form):
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

class InformantPhoneForm(Form):
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

class LogForm(Form):
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

class LogSubjectLUTForm(Form):
    logSubject = StringField('logSubject',
        []+COMMON_STRING_VALIDATORS)

class PatientForm(Form):
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

class PatientAddressForm(Form):
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

class PatientEmailForm(Form):
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

class PatientPhoneForm(Form):
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

class PatientProjectStatusForm(Form):
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

class PatientProjectStatusLUTForm(Form):
    statusDescription = StringField('statusDescription',
        []+COMMON_STRING_VALIDATORS)

class PhaseStatusForm(Form):
    phaseStatus = StringField('phaseStatus',
        []+COMMON_STRING_VALIDATORS)
    phaseDescription = StringField('phaseDescription',
        []+COMMON_STRING_VALIDATORS)

class PhysicianForm(Form):
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

class PhysicianFacilityForm(Form):
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

class PhysicianAddressForm(Form):
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

class PhysicianPhoneForm(Form):
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

class PhysicianToCTCForm(Form):
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

class PreApplicationForm(Form):
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

class ProjectForm(Form):
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

class ProjectPatientForm(Form):
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

class ProjectStaffForm(Form):
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

class ProjectStatusForm(Form):
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

class ProjectStatusLUTForm(Form):
    projectStatus = StringField('projectStatus',
        []+COMMON_STRING_VALIDATORS)
    projectStatusDefinition = StringField('projectStatusDefinition',
        []+COMMON_STRING_VALIDATORS)

class ProjectTypeForm(Form):
    projectType = StringField('projectType',
        []+COMMON_STRING_VALIDATORS)
    projectTypeDefinition = StringField('projectTypeDefinition',
        []+COMMON_STRING_VALIDATORS)

class RCStatusListForm(Form):
    rcStatus = StringField('rc_status',
        []+COMMON_STRING_VALIDATORS)
    rcStatusDefinition = StringField('rc_status_definition',
        []+COMMON_STRING_VALIDATORS)

class ReviewCommitteeForm(Form):
    project_projectID = IntegerField('project_projectID',
        []+COMMON_INTEGER_VALIDATORS)
    RCStatusList_rc_StatusID = IntegerField('RCStatusList_rc_StatusID',
        []+COMMON_INTEGER_VALIDATORS)
    reviewCommitteeList_rcListID = IntegerField('reviewCommitteeList_rcListID',
        []+COMMON_INTEGER_VALIDATORS)
    review_committee_number = StringField('review_committee_number',
        []+COMMON_STRING_VALIDATORS)
    date_initial_review = DateField('date_initial_review',
        []+COMMON_DATE_VALIDATORS,
        format=DATE_FORMAT)
    date_expires = DateField('date_expires',
        []+COMMON_DATE_VALIDATORS,
        format=DATE_FORMAT)
    rc_note = StringField('rc_note',
        []+COMMON_STRING_VALIDATORS)
    rc_protocol = StringField('rc_protocol',
        []+COMMON_STRING_VALIDATORS)
    rc_approval = StringField('rc_approval',
        []+COMMON_STRING_VALIDATORS)


    def validate(self):
        f = Form.validate(self)
        hasErrors = False # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project  FK exists
        project = query.get_project(self.project_projectID.data)
        if project is None:
            self.project_projectID.errors.append("ID not found")
            hasErrors =  True

        # check the rcStatus FK
        rcStatus = query.get_rc_status(self.RCStatusList_rc_StatusID.data)
        if rcStatus is None:
            self.RCStatusList_rc_StatusID.errors.append("ID not found")
            hasErrors = True

        # check the reviewCommitteeList FK
        rc = query.get_rc_status(self.reviewCommitteeList_rcListID.data)
        if rc is None:
            self.reviewCommitteeList_rcListID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class ReviewCommitteeListForm(Form):
    review_committee = StringField('review_committee',
        []+COMMON_STRING_VALIDATORS)
    rc_description = StringField('rc_description',
        []+COMMON_STRING_VALIDATORS)

class StaffForm(Form):
    fname = StringField('fname',
        []+COMMON_STRING_VALIDATORS)
    lname = StringField('lname',
        []+COMMON_STRING_VALIDATORS)
    middle_name = StringField('middle_name',
        []+COMMON_STRING_VALIDATORS)
    email = StringField('email',
        []+COMMON_STRING_VALIDATORS)
    phone = StringField('phone',
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
    human_sub_training_exp = DateField('human_sub_training',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    UCR_role = IntegerField('UCR_role',
        []+COMMON_INTEGER_VALIDATORS)

class StaffRoleLUTForm(Form):
    staffRole = StringField('staffRole',
        []+COMMON_STRING_VALIDATORS)
    staffRoleDescription = StringField('staffRoleDescription',
        []+COMMON_STRING_VALIDATORS)

class StaffTrainingForm(Form):
    staffID = IntegerField('staffID',
        []+COMMON_INTEGER_VALIDATORS)
    humanSubjectTrainingLUTID = IntegerField('humanSubjectTrainingLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    date_taken = DateField('date_taken',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    exp_date = DateField('exp_date',
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
        hst = query.get_human_subject_training(self.humanSubjectTrainingLUTID.data)
        if hst is None:
            self.humanSubjectTrainingLUTID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class TracingForm(Form):
    tracingSourceLUTID = IntegerField('tracingSourceLUTID',
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
        tracingSource = query.get_tracing_source(self.tracingSourceLUTID.data)
        if tracingSource is None:
            self.tracingSourceLUTID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class TracingSourceLUTForm(Form):
    description = StringField('description',
        []+COMMON_STRING_VALIDATORS)

class UCRReportForm(Form):
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    report_type = IntegerField('report_type',
        []+COMMON_INTEGER_VALIDATORS)
    report_submitted = DateField('report_submitted',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    report_due = DateField('report_due',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    report_doc = StringField('report_doc',
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
