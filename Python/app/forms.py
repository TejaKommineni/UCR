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
    review_type = IntegerField('review_type',
        []+COMMON_INTEGER_VALIDATORS)
    date_sent_to_reviewer = DateField('date_sent_to_reviewer',
        []+COMMON_DATE_VALIDATORS,
        format=DATE_FORMAT)
    reviewer1 = IntegerField('reviewer1',
        []+COMMON_INTEGER_VALIDATORS)
    reviewer1_rec = IntegerField('reviewer1_rec',
        []+COMMON_INTEGER_VALIDATORS)
    reviewer1_sig_date = DateField('reviewer1_sig_date',
        []+COMMON_DATE_VALIDATORS)
    reviewer1_comments = StringField('reviewer1_comments',
        []+COMMON_STRING_VALIDATORS)
    reviewer2 = IntegerField('reviewer2',
        []+COMMON_INTEGER_VALIDATORS)
    reviewer2_rec = IntegerField('reviewer2_rec',
        []+COMMON_INTEGER_VALIDATORS)
    reviewer2_sig_date = DateField('reviewer2_sig_date',
        []+COMMON_DATE_VALIDATORS)
    reviewer2_comments = StringField('reviewer2_comments',
        []+COMMON_STRING_VALIDATORS)
    research = StringField('research',
        []+COMMON_STRING_VALIDATORS)
    contact = BooleanField('contact',
        []+COMMON_BOOL_VALIDATORS)
    lnkage = BooleanField('lnkage',
        []+COMMON_BOOL_VALIDATORS)
    engaged = BooleanField('engaged',
        []+COMMON_BOOL_VALIDATORS)
    non_public_data = BooleanField('non_public_data',
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
    contact_date = DateField('contact_date',
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
    contact_info_source = StringField('contact_info_source',
        []+COMMON_STRING_VALIDATORS)

class ContactInfoStatusForm(Form):
    contact_info_status = StringField('contact_info_status',
        []+COMMON_STRING_VALIDATORS)

class ContactTypeLUTForm(Form):
    contact_definition = StringField('contact_definition',
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
    dx_date = DateField('dx_date',
        []+COMMON_DATE_VALIDATORS,
        format= DATE_FORMAT)
    site = IntegerField('site',
        []+COMMON_INTEGER_VALIDATORS)
    histology = StringField('histology',
        []+COMMON_STRING_VALIDATORS)
    behavior = StringField('behavior',
        []+COMMON_STRING_VALIDATORS)
    ctc_sequence = StringField('ctc_sequence',
        []+COMMON_STRING_VALIDATORS)
    stage = StringField('stage',
        []+COMMON_STRING_VALIDATORS)
    dx_age = IntegerField('dx_age',
        []+COMMON_INTEGER_VALIDATORS)
    dx_street1 = StringField('dx_street1',
        []+COMMON_STRING_VALIDATORS)
    dx_street2 = StringField('dx_street2',
        []+COMMON_STRING_VALIDATORS)
    dx_city = StringField('dx_city',
        []+COMMON_STRING_VALIDATORS)
    dx_state = StringField('dx_state',
        []+COMMON_STRING_VALIDATORS)
    dx_zip = IntegerField('dx_zip',
        []+COMMON_INTEGER_VALIDATORS)
    dx_county = StringField('dx_county',
        []+COMMON_STRING_VALIDATORS)
    dnc = StringField('dnc',
        []+COMMON_STRING_VALIDATORS)
    dnc_reason = StringField('dnc_reason',
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
    facility_name = StringField('facility_name',
        []+COMMON_STRING_VALIDATORS)
    contact_fname = StringField('contact_fname',
        []+COMMON_STRING_VALIDATORS)
    contact_lname = StringField('contact_lname',
        []+COMMON_STRING_VALIDATORS)
    facility_status = IntegerField('facility_status',
        []+COMMON_INTEGER_VALIDATORS)
    facility_status_date = DateField('facility_status_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    contact2_fname = StringField('contact2_fname',
        []+COMMON_STRING_VALIDATORS)
    contact2_lname = StringField('contact2_lname',
        []+COMMON_STRING_VALIDATORS)

class FacilityAddressForm(Form):
    contactInfoSourceLUTID = IntegerField('contactInfoSourceLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    facilityID = IntegerField('facilityID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusLUTID = IntegerField('contactInfoStatusLUTID',
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
    facility_address_status = IntegerField('address_status',
        []+COMMON_INTEGER_VALIDATORS)
    facility_address_status_date = DateField('address_status_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    facility_address_status_source = StringField('address_status_source',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceLUTID.data)
        if contactSource is None:
            self.contactInfoSourceLUTID.errors.append("ID not found")
            hasErrors = True

        facility = query.get_facility(self.facilityID.data)
        if facility is None:
            self.facilityID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusLUTID.data)
        if contactStatus is None:
            self.contactInfoStatusLUTID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class FacilityPhoneForm(Form):
    contactInfoSourceLUTID = IntegerField('contactInfoSourceLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    facilityID = IntegerField('facilityID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    facility_phone = StringField('phone',
        []+COMMON_STRING_VALIDATORS)
    clinic_name = StringField('clinic_name',
        []+COMMON_STRING_VALIDATORS)
    facility_phone_type = StringField('facility_phone_type',
        []+COMMON_STRING_VALIDATORS)
    facility_phone_source = StringField('phone_source',
        []+COMMON_STRING_VALIDATORS)
    facility_phone_status = StringField('phone_status',
        []+COMMON_STRING_VALIDATORS)
    facility_phone_status_date = DateField('phone_status_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceLUTID.data)
        if contactSource is None:
            self.contactInfoSourceLUTID.errors.append("ID not found")
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
    grantStatusLUTID = IntegerField('grantStatusLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    fundingSourceLUTID = IntegerField('fundingSourceLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    primary_funding_source = StringField('primary_funding_source',
        []+COMMON_STRING_VALIDATORS)
    secondary_funding_source = StringField('secondary_funding_source',
        []+COMMON_STRING_VALIDATORS)
    funding_number = StringField('grant_title',
        []+COMMON_STRING_VALIDATORS)
    grantStatusID = IntegerField('grantStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    date_status = DateField('date_status',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    grant_pi = IntegerField('grant_pi',
        []+COMMON_INTEGER_VALIDATORS)
    primary_chartfield = StringField('primary_chartfield',
        []+COMMON_STRING_VALIDATORS)
    secondary_chartfield = StringField('secondary_chartfield',
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

        grantStatus = query.get_grant_status(self.grantStatusLUTID.data)
        if grantStatus is None:
            self.grantStatusLUTID.errors.append("ID not found")
            hasErrors = True

        fundingSource = query.get_funding_source(self.fundingSourceLUTID.data)
        if fundingSource is None:
            self.fundingSourceLUTID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class FundingSourceLUTForm(Form):
    fundingSource = StringField('fundingSource',
        []+COMMON_STRING_VALIDATORS)

class GrantStatusLUTForm(Form):
    grant_status = StringField('grant_status',
        []+COMMON_STRING_VALIDATORS)

class HumanSubjectTrainingLUTForm(Form):
    training_type = StringField('training_type',
        []+COMMON_STRING_VALIDATORS)

class IRBHolderLUTForm(Form):
    irb_holder = StringField('irb_holder',
        []+COMMON_STRING_VALIDATORS)
    irb_holder_definition = StringField('irb_holder_definition',
        []+COMMON_STRING_VALIDATORS)

class InformantForm(Form):
    patAutoID = IntegerField('patAutoID',
        []+COMMON_INTEGER_VALIDATORS)
    fname = StringField('fname',
        []+COMMON_STRING_VALIDATORS)
    lname = StringField('lname',
        []+COMMON_STRING_VALIDATORS)
    middle_name = StringField('middle_name',
        []+COMMON_STRING_VALIDATORS)
    informant_primary = StringField('fname',
        []+COMMON_STRING_VALIDATORS)
    informant_relationship = StringField('fname',
        []+COMMON_STRING_VALIDATORS)
    notes = StringField('fname',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)
        patient = query.get_patient(self.patAutoID.data)
        if patient is None:
            self.patAutoID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class InformantAddressForm(Form):
    contactInfoSourceLUTID = IntegerField('contactInfoSourceLUTID',
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
    address_status = IntegerField('address_status',
        []+COMMON_INTEGER_VALIDATORS)
    address_status_date = DateField('address_status_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    address_status_source = StringField('address_status_source',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceLUTID.data)
        if contactSource is None:
            self.contactInfoSourceLUTID.errors.append("ID not found")
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
    contactInfoSourceLUTID = IntegerField('contactInfoSourceLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    informantID = IntegerField('informantID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    phone = StringField('phone',
        []+COMMON_STRING_VALIDATORS)
    phone_source = StringField('phone_source',
        []+COMMON_STRING_VALIDATORS)
    phone_status = StringField('phone_status',
        []+COMMON_STRING_VALIDATORS)
    phone_status_date = DateField('phone_status_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceLUTID.data)
        if contactSource is None:
            self.contactInfoSourceLUTID.errors.append("ID not found")
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
    logSubjectLUTID =  IntegerField('logSubjectLUTID',
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

        logSubject = query.get_log_subject(self.logSubjectLUTID.data)
        if logSubject is None:
            self.logSubjectLUTID.errors.append("ID not found")
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
    log_subject = StringField('log_subject',
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
    fname = StringField('fname',
        []+COMMON_STRING_VALIDATORS)
    lname = StringField('lname',
        []+COMMON_STRING_VALIDATORS)
    middle_name = StringField('middle_name',
        []+COMMON_STRING_VALIDATORS)
    maiden_name = StringField('maiden_name',
        []+COMMON_STRING_VALIDATORS)
    alias_fname = StringField('alias_fname',
        []+COMMON_STRING_VALIDATORS)
    alias_lname = StringField('alias_lname',
        []+COMMON_STRING_VALIDATORS)
    alias_middle_name = StringField('alias_middle_name',
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
    vital_status = StringField('vital_status',
        []+COMMON_STRING_VALIDATORS)

class PatientAddressForm(Form):
    contactInfoSourceLUTID = IntegerField('contactInfoSourceLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    patientID = IntegerField('patientID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusLUTID = IntegerField('contactInfoStatusLUTID',
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
    address_status = IntegerField('address_status',
        []+COMMON_INTEGER_VALIDATORS)
    address_status_date = DateField('address_status_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    address_status_source = StringField('address_status_source',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceLUTID.data)
        if contactSource is None:
            self.contactInfoSourceLUTID.errors.append("ID not found")
            hasErrors = True

        patient = query.get_patient(self.patientID.data)
        if patient is None:
            self.patientID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusLUTID.data)
        if contactStatus is None:
            self.contactInfoStatusLUTID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class PatientEmailForm(Form):
    contactInfoSourceLUTID = IntegerField('contactInfoSourceLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    patientID = IntegerField('patientID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    email = StringField('email',
        []+COMMON_STRING_VALIDATORS)
    email_status = IntegerField('email_status',
        []+COMMON_INTEGER_VALIDATORS)
    email_source = IntegerField('email_source',
        []+COMMON_INTEGER_VALIDATORS)
    email_status_date = DateField('email_status_date',
        []+COMMON_DATE_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceLUTID.data)
        if contactSource is None:
            self.contactInfoSourceLUTID.errors.append("ID not found")
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
    contactInfoSourceLUTID = IntegerField('contactInfoSourceLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    patientID = IntegerField('patientID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    phone = StringField('phone',
        []+COMMON_STRING_VALIDATORS)
    phone_source = StringField('phone_source',
        []+COMMON_STRING_VALIDATORS)
    phone_status = StringField('phone_status',
        []+COMMON_STRING_VALIDATORS)
    phone_status_date = DateField('phone_status_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceLUTID.data)
        if contactSource is None:
            self.contactInfoSourceLUTID.errors.append("ID not found")
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
    patientProjectStatusLUTID = IntegerField('patientProjectStatusLUT',
        []+COMMON_INTEGER_VALIDATORS)
    projectPatientID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        patientProjectStatusLUT = query.get_patient_project_status_type(self.patientProjectStatusLUTID.data)
        if patientProjectStatusLUT is None:
            self.patientProjectStatusLUTID.errors.append("ID not found")
            hasErrors = True

        projectPatient = query.get_project_patient(self.projectPatientID.data)
        if projectPatient is None:
            self.projectPatientID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class PatientProjectStatusLUTForm(Form):
    status_description = StringField('status_description',
        []+COMMON_STRING_VALIDATORS)

class PhaseStatusForm(Form):
    phase_status = StringField('phase_status',
        []+COMMON_STRING_VALIDATORS)
    phase_description = StringField('phase_description',
        []+COMMON_STRING_VALIDATORS)

class PhysicianForm(Form):
    fname = StringField('fname',
        []+COMMON_STRING_VALIDATORS)
    lname = StringField('lname',
        []+COMMON_STRING_VALIDATORS)
    middle_name = StringField('middle_name',
        []+COMMON_STRING_VALIDATORS)
    credentials = StringField('credentials',
        []+COMMON_STRING_VALIDATORS)
    specialty = StringField('specialty',
        []+COMMON_STRING_VALIDATORS)
    alias_fname = StringField('alias_fname',
        []+COMMON_STRING_VALIDATORS)
    alias_lname = StringField('alias_lname',
        []+COMMON_STRING_VALIDATORS)
    alias_middle_name = StringField('alias_middle_name',
        []+COMMON_STRING_VALIDATORS)
    physician_status = IntegerField('physician_status',
        []+COMMON_INTEGER_VALIDATORS)
    physician_status_date = DateField('physician_status_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    email = StringField('email',
        []+COMMON_STRING_VALIDATORS)

class PhysicianFacilityForm(Form):
    facilityID = IntegerField('facilityID',
        []+COMMON_INTEGER_VALIDATORS)
    physicianID = IntegerField('physicianID',
        []+COMMON_INTEGER_VALIDATORS)
    phys_facility_status = IntegerField('phys_facility_status',
        []+COMMON_INTEGER_VALIDATORS)
    phys_facility_status_date = DateField('phys_facility_status_date',
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
    contactInfoSourceLUTID = IntegerField('contactInfoSourceLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    physicianID = IntegerField('physicianID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusLUTID = IntegerField('contactInfoStatusLUTID',
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
    address_status = IntegerField('address_status',
        []+COMMON_INTEGER_VALIDATORS)
    address_status_date = DateField('address_status_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    address_status_source = StringField('address_status_source',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceLUTID.data)
        if contactSource is None:
            self.contactInfoSourceLUTID.errors.append("ID not found")
            hasErrors = True

        physician = query.get_physician(self.physicianID.data)
        if physician is None:
            self.physicianID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusLUTID.data)
        if contactStatus is None:
            self.contactInfoStatusLUTID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class PhysicianPhoneForm(Form):
    contactInfoSourceLUTID = IntegerField('contactInfoSourceLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    physicianID = IntegerField('physicianID',
        []+COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
        []+COMMON_INTEGER_VALIDATORS)
    phone = StringField('phone',
        []+COMMON_STRING_VALIDATORS)
    phone_source = StringField('phone_source',
        []+COMMON_STRING_VALIDATORS)
    phone_status = StringField('phone_status',
        []+COMMON_STRING_VALIDATORS)
    phone_status_date = DateField('phone_status_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        contactSource = query.get_contact_info_source(self.contactInfoSourceLUTID.data)
        if contactSource is None:
            self.contactInfoSourceLUTID.errors.append("ID not found")
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
    pi_fname = StringField('pi_fname',
        []+COMMON_STRING_VALIDATORS)
    pi_phone = StringField('pi_phone',
        []+COMMON_STRING_VALIDATORS)
    pi_email = StringField('pi_email',
        []+COMMON_STRING_VALIDATORS)
    contact_fname = StringField('contact_fname',
        []+COMMON_STRING_VALIDATORS)
    contact_lname = StringField('contact_lname',
        []+COMMON_STRING_VALIDATORS)
    contact_phone = StringField('contact_phone',
        []+COMMON_STRING_VALIDATORS)
    contact_email = StringField('contact_email',
        []+COMMON_STRING_VALIDATORS)
    institution = StringField('institution',
        []+COMMON_STRING_VALIDATORS)
    institution2 = StringField('institution2',
        []+COMMON_STRING_VALIDATORS)
    uid = StringField('uid',
        []+COMMON_STRING_VALIDATORS)
    udoh = IntegerField('udoh',
        []+COMMON_INTEGER_VALIDATORS)
    project_title = StringField('project_title',
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
    other_irb = StringField('other_irb',
        []+COMMON_STRING_VALIDATORS)
    updb = BooleanField('updb',
        []+COMMON_BOOL_VALIDATORS)
    pt_contact = BooleanField('pt_contact',
        []+COMMON_BOOL_VALIDATORS)
    start_date = DateField('start_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    link = BooleanField('link',
        []+COMMON_BOOL_VALIDATORS)
    delivery_date = DateField('delivery_date',
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
    projectType_projectTypeID = IntegerField('projectType_projectTypeID',
        [] + COMMON_INTEGER_VALIDATORS)
    IRBHolderLUT_irbHolderID = IntegerField('IRBHolderLUT_irbHolderID',
        []+COMMON_INTEGER_VALIDATORS)
    project_name = StringField('project_name',
        []+COMMON_STRING_VALIDATORS)
    short_title = StringField('short_title',
        []+COMMON_STRING_VALIDATORS)
    project_summary = StringField('project_summary',
        []+COMMON_STRING_VALIDATORS)
    sop = StringField('sop',
        []+COMMON_STRING_VALIDATORS)
    UCR_proposal = StringField('UCR_proposal',
        []+COMMON_STRING_VALIDATORS)
    budget_doc = StringField('budget_doc',
        []+COMMON_STRING_VALIDATORS)
    UCR_fee = StringField('UCR_fee',
        []+COMMON_STRING_VALIDATORS)
    UCR_no_fee = StringField('UCR_no_fee',
        []+COMMON_STRING_VALIDATORS)
    budget_end_date = DateField('budget_end_date',
        []+COMMON_DATE_VALIDATORS,
        format = "%Y-%m-%d")
    previous_short_title = StringField('previous_short_title',
        []+COMMON_STRING_VALIDATORS)
    date_added = DateField('date_added',
        []+COMMON_DATE_VALIDATORS,
        format=DATE_FORMAT)
    final_recruitment_report = StringField('final_recruitment_report',
        []+COMMON_STRING_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project type FK exists
        projType = query.get_project_type(self.projectType_projectTypeID.data)
        if projType is None:
            self.projectType_projectTypeID.errors.append("ID not found")
            hasErrors =  True

        # check the irbHolderLUT FK
        irbHolder = query.get_irb_holder(self.IRBHolderLUT_irbHolderID.data)
        if irbHolder is None:
            self.IRBHolderLUT_irbHolderID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class ProjectPatientForm(Form):
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    staffID = IntegerField('staffID',
        []+COMMON_INTEGER_VALIDATORS)
    ctcID = IntegerField('ctcID',
        []+COMMON_INTEGER_VALIDATORS)
    current_age = IntegerField('current_age',
        []+COMMON_INTEGER_VALIDATORS)
    batch = IntegerField('batch',
        []+COMMON_INTEGER_VALIDATORS)
    sitegrp = IntegerField('sitegrp',
        []+COMMON_INTEGER_VALIDATORS)
    final_code = IntegerField('final_code',
        []+COMMON_INTEGER_VALIDATORS)
    final_code_date = DateField('final_code_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    enrollment_date = DateField('enrollment_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    date_coord_signed = DateField('date_coord_signed',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    import_date = DateField('import_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    final_code_staff = IntegerField('final_code_staff',
        []+COMMON_INTEGER_VALIDATORS)
    enrollment_staff = IntegerField('enrollment_staff',
        []+COMMON_INTEGER_VALIDATORS)
    date_coord_signed_staff = DateField('date_coord_signed_staff',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    abstract_status = IntegerField('abstract_status',
        []+COMMON_INTEGER_VALIDATORS)
    abstract_status_date = DateField('abstract_status_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    abstract_status_staff = IntegerField('abstract_status_staff',
        []+COMMON_INTEGER_VALIDATORS)
    sent_to_abstractor = DateField('sent_to_abstractor',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    sent_to_abstractor_staff = IntegerField('sent_to_abstractor_staff',
        []+COMMON_INTEGER_VALIDATORS)
    abstracted_date = DateField('abstracted_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    abstractor_initials = StringField('abstractor_initials',
        []+COMMON_STRING_VALIDATORS)
    researcher_date = DateField('researcher_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    researcher_staff = IntegerField('researcher_staff',
        []+COMMON_INTEGER_VALIDATORS)
    consent_link = StringField('consent_link',
        []+COMMON_STRING_VALIDATORS)
    tracing_status = IntegerField('tracing_status',
        []+COMMON_INTEGER_VALIDATORS)
    med_record_release_signed = BooleanField('med_record_release_signed',
        []+COMMON_BOOL_VALIDATORS)
    med_record_release_link = StringField('med_record_release_link',
        []+COMMON_STRING_VALIDATORS)
    med_record_release_staff = IntegerField('med_record_release_staff',
        []+COMMON_INTEGER_VALIDATORS)
    med_record_release_date = DateField('med_record_release_date',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    survey_to_researcher = DateField('survey_to_researcher',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    survey_to_researcher_staff = IntegerField('survey_to_researcher_staff',
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
    staffRoleLUTID = IntegerField('staffRoleLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    staffID = IntegerField('staffID',
        []+COMMON_INTEGER_VALIDATORS)
    role = IntegerField('role',
        []+COMMON_INTEGER_VALIDATORS)
    date_pledge = DateField('date_pledge',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    date_revoked = DateField('date_revoked',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    contact = StringField('contact',
        []+COMMON_STRING_VALIDATORS)
    inactive = StringField('inactive',
        []+COMMON_STRING_VALIDATORS)
    human_sub_training_exp = DateField('human_sub_training_exp',
        []+COMMON_DATE_VALIDATORS,
        format = DATE_FORMAT)
    human_sub_type_id = IntegerField('human_sub_type_id',
        []+COMMON_INTEGER_VALIDATORS)
    study_role = IntegerField('study_role',
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

        staffRole = query.get_staff_role(self.staffRoleLUTID.data)
        if staffRole is None:
            self.staffRoleLUTID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class ProjectStatusForm(Form):
    projectStatusLUTID = IntegerField('projectStatusLUTID',
        []+COMMON_INTEGER_VALIDATORS)
    projectID = IntegerField('projectID',
        []+COMMON_INTEGER_VALIDATORS)
    staffID = IntegerField('staffID',
        []+COMMON_INTEGER_VALIDATORS)
    status_date = DateField('status_date',
        []+COMMON_DATE_VALIDATORS,
        format=DATE_FORMAT)
    status_notes = StringField('status_notes',
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

        projectStatus = query.get_project_status_lut(self.projectStatusLUTID.data)
        if projectStatus is None:
            self.projectStatusLUTID.errors.append("ID not found")
            hasErrors = True

        staff = query.get_staff(self.staffID.data)
        if staff is None:
            self.staffID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors

class ProjectStatusLUTForm(Form):
    project_status = StringField('project_status',
        []+COMMON_STRING_VALIDATORS)
    status_definition = StringField('status_definition',
        []+COMMON_STRING_VALIDATORS)

class ProjectTypeForm(Form):
    project_type = StringField('project_type',
        []+COMMON_STRING_VALIDATORS)
    project_type_definition = StringField('project_type_definition',
        []+COMMON_STRING_VALIDATORS)

class RCStatusListForm(Form):
    rc_status = StringField('rc_status',
        []+COMMON_STRING_VALIDATORS)
    rc_status_definition = StringField('rc_status_definition',
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
