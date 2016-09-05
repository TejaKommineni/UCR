from wtforms import Form, BooleanField, StringField, IntegerField, DateField, FloatField, BooleanField, validators
import query

COMMON_STRING_VALIDATORS = [
    validators.optional(),
    validators.Length(min=1)]

COMMON_INTEGER_VALIDATORS = [
    validators.optional(),
    validators.number_range(min=0)]

COMMON_DATE_VALIDATORS = [
    validators.optional()
]

COMMON_FLOAT_VALIDATORS = [
    validators.optional()
]

COMMON_BOOL_VALIDATORS = [
    validators.optional()
]

DATE_FORMAT = "%Y-%m-%d"


class BaseForm(Form):
    versionID = IntegerField('versionID',
                             [] + COMMON_INTEGER_VALIDATORS)

    def validate(self):
        return Form.validate(self)

class AbstractStatusForm(BaseForm):
    abstractStatus = StringField('abstractStatus',
                                 [] + COMMON_STRING_VALIDATORS)


class ArcReviewForm(BaseForm):
    projectID = IntegerField('projectID',
                             [validators.InputRequired()])
    reviewType = IntegerField('reviewType',
                              [] + COMMON_INTEGER_VALIDATORS)
    dateSentToReviewer = DateField('dateSentToReviewer',
                                   [] + COMMON_DATE_VALIDATORS,
                                   format=DATE_FORMAT)
    reviewer1 = IntegerField('reviewer1',
                             [] + COMMON_INTEGER_VALIDATORS)
    reviewer1Rec = IntegerField('reviewer1Rec',
                                [] + COMMON_INTEGER_VALIDATORS)
    reviewer1SigDate = DateField('reviewer1SigDate',
                                 [] + COMMON_DATE_VALIDATORS)
    reviewer1Comments = StringField('reviewer1Comments',
                                    [] + COMMON_STRING_VALIDATORS)
    reviewer2 = IntegerField('reviewer2',
                             [] + COMMON_INTEGER_VALIDATORS)
    reviewer2Rec = IntegerField('reviewer2Rec',
                                [] + COMMON_INTEGER_VALIDATORS)
    reviewer2SigDate = DateField('reviewer2SigDate',
                                 [] + COMMON_DATE_VALIDATORS)
    reviewer2Comments = StringField('reviewer2Comments',
                                    [] + COMMON_STRING_VALIDATORS)
    research = StringField('research',
                           [] + COMMON_STRING_VALIDATORS)
    contact = BooleanField('contact',
                           [] + COMMON_BOOL_VALIDATORS)
    linkage = BooleanField('linkage',
                           [] + COMMON_BOOL_VALIDATORS)
    engaged = BooleanField('engaged',
                           [] + COMMON_BOOL_VALIDATORS)
    nonPublicData = BooleanField('nonPublicData',
                                 [] + COMMON_BOOL_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors


class BudgetForm(BaseForm):
    projectID = IntegerField('projectID',
                             [validators.InputRequired()])
    numPeriods = IntegerField('numPeriods',
                              [] + COMMON_INTEGER_VALIDATORS)
    periodStart = DateField('periodStart',
                            [] + COMMON_DATE_VALIDATORS,
                            format=DATE_FORMAT)
    periodEnd = DateField('periodEnd',
                          [] + COMMON_DATE_VALIDATORS,
                          format=DATE_FORMAT)
    periodTotal = FloatField('periodTotal',
                             [] + COMMON_FLOAT_VALIDATORS)
    periodComment = StringField('periodComment',
                                [] + COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors


class ContactForm(BaseForm):
    contactTypeLUTID = IntegerField('contactTypeLUTID',
                                    [validators.InputRequired()])
    participantID = IntegerField('participantID',
                                    [validators.InputRequired()])
    staffID = IntegerField('staffID',
                           [validators.InputRequired()])
    informantID = IntegerField('informantID',
                               [] + COMMON_INTEGER_VALIDATORS)

    informantPhoneID = IntegerField('informantPhoneID',
                               [] + COMMON_INTEGER_VALIDATORS)

    facilityID = IntegerField('facilityID',
                              [] + COMMON_INTEGER_VALIDATORS)

    facilityPhoneID = IntegerField('facilityPhoneID',
                              [] + COMMON_INTEGER_VALIDATORS)

    physicianID = IntegerField('physicianID',
                               [] + COMMON_INTEGER_VALIDATORS)

    physicianPhoneID = IntegerField('physicianPhoneID',
                               [] + COMMON_INTEGER_VALIDATORS)

    patientPhoneID = IntegerField('patientPhoneID',
                                    [] + COMMON_INTEGER_VALIDATORS)

    description = StringField('description',
                              [] + COMMON_STRING_VALIDATORS)
    contactDate = DateField('contactDate',
                            [validators.InputRequired()],
                            format=DATE_FORMAT)
    initials = StringField('initials',
                           [] + COMMON_STRING_VALIDATORS)
    notes = StringField('notes',
                        [] + COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project FK exists
        projectPatient = query.get_project_patient(self.participantID.data)
        if projectPatient is None:
            self.participantID.errors.append("ID not found")
            hasErrors = True

        contactType = query.get_contact_type(self.contactTypeLUTID.data)
        if contactType is None:
            self.contactTypeLUTID.errors.append("ID not found")
            hasErrors = True

        staff = query.get_staff(self.staffID.data)
        if staff is None:
            self.staffID.errors.append("ID not found")
            hasErrors = True

        if self.informantID.data:
            informant = query.get_informant(self.informantID.data)
            if informant is None:
                self.informantID.errors.append("ID not found")
                hasErrors = True

        if self.informantPhoneID.data:
            if self.informantID.data is None:
                self.informantID.errors.append("InformantID required if specifying InformantPhoneID")
                hasErrors = True
            else:
                informantPhone = query.get_informant_phone(self.informantPhoneID.data)
                if informantPhone is None:
                    self.informantPhoneID.errors.append("ID not found")
                    hasErrors = True
                else:
                    informant = query.get_informant(self.informantID.data)
                    if self.informantPhoneID.data not in [x.informantPhoneID for x in informant.informantPhones]:
                        self.informantPhoneID.errors.append("InformantPhoneID is not linked to specified Informant")
                        hasErrors = True

        if self.facilityID.data:
            facility = query.get_project_patient(self.facilityID.data)
            if facility is None:
                self.facilityID.errors.append("ID not found")
                hasErrors = True

        if self.facilityPhoneID.data:
            if self.facilityID.data is None:
                self.facilityID.errors.append("FacilityID required if specifying FacilityPhoneID")
                hasErrors = True
            else:
                faciltyPhone = query.get_facility_phone(self.facilityPhoneID.data)
                if faciltyPhone is None:
                    self.facilityPhoneID.errors.append("ID not found")
                    hasErrors = True
                else:
                    facility = query.get_facility(self.facilityID.data)
                    if self.facilityPhoneID.data not in [x.facilityPhoneID for x in facility.facilityPhones]:
                        self.facilityID.errors.append("FacilityPhoneID is not linked to specified Facility")
                        hasErrors = True

        if self.physicianID.data:
            physician = query.get_physician(self.physicianID.data)
            if physician is None:
                self.physicianID.errors.append("ID not found")
                hasErrors = True

        if self.physicianPhoneID.data:
            if self.physicianID.data is None:
                self.physicianID.errors.append("PhysicianID required if specifying PhysicianPhoneID")
                hasErrors = True
            else:
                physicianPhone = query.get_physician_phone(self.physicianPhoneID.data)
                if physicianPhone is None:
                    self.physicianPhoneID.errors.append("ID not found")
                    hasErrors = True
                else:
                    physician = query.get_physician(self.physicianID.data)
                    if self.physicianPhoneID.data not in [x.physicianPhoneID for x in physician.physicianPhones]:
                        self.physicianPhoneID.errors.append("PhysicianPhoneID is not linked to specified Physician")
                        hasErrors = True

        if self.patientPhoneID.data:
            patientPhone = query.get_patient_phone(self.patientPhoneID.data)
            if patientPhone is None:
                self.patientPhoneID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class ContactInfoSourceForm(BaseForm):
    contactInfoSource = StringField('contactInfoSource',
                                    [] + COMMON_STRING_VALIDATORS)


class ContactInfoStatusForm(BaseForm):
    contactInfoStatus = StringField('contactInfoStatus',
                                    [] + COMMON_STRING_VALIDATORS)


class ContactTypeLUTForm(BaseForm):
    contactDefinition = StringField('contactDefinition',
                                    [] + COMMON_STRING_VALIDATORS)


class CTCFacilityForm(BaseForm):
    ctcID = IntegerField('ctcID',
                         [validators.InputRequired()])
    facilityID = IntegerField('facilityID',
                              [validators.InputRequired()])
    coc = IntegerField('coc', []+COMMON_INTEGER_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False  # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project FK exists
        ctc = query.get_ctc(self.ctcID.data)
        if ctc is None:
            self.ctcID.errors.append("ID not found")
            hasErrors = True

        facility = query.get_facility(self.facilityID.data)
        if facility is None:
            self.facilityID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors


class CTCForm(BaseForm):
    participantID = IntegerField('participantID',
                             [validators.InputRequired()])
    dxDateDay = DateField('dxDateDay',
                       [validators.number_range(max=31)] + COMMON_INTEGER_VALIDATORS)
    dxDateMonth = DateField('dxDateMonth',
                       [validators.number_range(max=12)] + COMMON_INTEGER_VALIDATORS)
    dxDateYear = DateField('dxDateYear',
                       [] + COMMON_INTEGER_VALIDATORS)
    site = StringField('site',
                        [] + COMMON_STRING_VALIDATORS)
    histology = StringField('histology',
                            [] + COMMON_STRING_VALIDATORS)
    behavior = StringField('behavior',
                           [] + COMMON_STRING_VALIDATORS)
    ctcSequence = StringField('ctcSequence',
                              [] + COMMON_STRING_VALIDATORS)
    stage = StringField('stage',
                        [] + COMMON_STRING_VALIDATORS)
    dxAge = IntegerField('dxAge',
                         [] + COMMON_INTEGER_VALIDATORS)
    dxStreet1 = StringField('dxStreet1',
                            [] + COMMON_STRING_VALIDATORS)
    dxStreet2 = StringField('dxStreet2',
                            [] + COMMON_STRING_VALIDATORS)
    dxCity = StringField('dxCity',
                         [] + COMMON_STRING_VALIDATORS)
    dxStateID = IntegerField('dxStateID',
                             [] + COMMON_STRING_VALIDATORS)
    dxZip = IntegerField('dxZip',
                         [] + COMMON_INTEGER_VALIDATORS)
    dxCounty = StringField('dxCounty',
                           [] + COMMON_STRING_VALIDATORS)
    dnc = StringField('dnc',
                      [] + COMMON_STRING_VALIDATORS)
    dncReason = StringField('dncReason',
                            [] + COMMON_STRING_VALIDATORS)
    recordID = StringField('recordID',
                            [] + COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project FK exists
        patient = query.get_patient(self.participantID.data)
        if patient is None:
            self.participantID.errors.append("ID not found")
            hasErrors = True

        if self.dxStateID.data:
            state = query.get_state(self.dxStateID.data)
            if state is None:
                self.dxStateID.errors.append("ID not found")
                hasErrors = True

        return not hasErrors


class FacilityForm(BaseForm):
    facilityName = StringField('facilityName',
                               [] + COMMON_STRING_VALIDATORS)
    contactFirstName = StringField('contactFirstName',
                                   [] + COMMON_STRING_VALIDATORS)
    contactLastName = StringField('contactLastName',
                                  [] + COMMON_STRING_VALIDATORS)
    facilityStatus = IntegerField('facilityStatus',
                                  [] + COMMON_INTEGER_VALIDATORS)
    facilityStatusDate = DateField('facilityStatusDate',
                                   [] + COMMON_DATE_VALIDATORS,
                                   format=DATE_FORMAT)
    contact2FirstName = StringField('contact2FirstName',
                                    [] + COMMON_STRING_VALIDATORS)
    contact2LastName = StringField('contact2LastName',
                                   [] + COMMON_STRING_VALIDATORS)


class FacilityAddressForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    facilityID = IntegerField('facilityID',
                              [validators.InputRequired()])
    contactInfoStatusID = IntegerField('contactInfoStatusID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    street = StringField('street',
                         [] + COMMON_STRING_VALIDATORS)
    street2 = StringField('street2',
                          [] + COMMON_STRING_VALIDATORS)
    city = StringField('city',
                       [] + COMMON_STRING_VALIDATORS)
    stateID = IntegerField('stateID',
                           [] + COMMON_INTEGER_VALIDATORS)
    zip = StringField('zip',
                      [] + COMMON_STRING_VALIDATORS)
    addressStatusDate = DateField('addressStatusDate',
                                  [] + COMMON_DATE_VALIDATORS,
                                  format=DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        facility = query.get_facility(self.facilityID.data)
        if facility is None:
            self.facilityID.errors.append("ID not found")
            hasErrors = True

        if self.contactInfoSourceID.data:
            contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
            if contactSource is None:
                self.contactInfoSourceID.errors.append("ID not found")
                hasErrors = True

        if self.stateID.data:
            state = query.get_state(self.stateID.data)
            if state is None:
                self.stateID.errors.append("ID not found")
                hasErrors = True

        if self.contactInfoStatusID.data:
            contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
            if contactStatus is None:
                self.contactInfoStatusID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class FacilityPhoneForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    facilityID = IntegerField('facilityID',
                              [validators.InputRequired()])
    contactInfoStatusID = IntegerField('contactInfoStatusID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    phoneNumber = StringField('phoneNumber',
                              [] + COMMON_STRING_VALIDATORS)
    clinicName = StringField('clinicName',
                             [] + COMMON_STRING_VALIDATORS)
    phoneTypeID = StringField('phoneTypeID',
                              [] + COMMON_STRING_VALIDATORS)
    phoneStatusDate = DateField('phoneStatusDate',
                                [] + COMMON_DATE_VALIDATORS,
                                format=DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        facility = query.get_facility(self.facilityID.data)
        if facility is None:
            self.facilityID.errors.append("ID not found")
            hasErrors = True

        if self.phoneTypeID.data:
            phoneType = query.get_phone_type(self.phoneTypeID.data)
            if phoneType is None:
                self.phoneTypeID.errors.append("ID not found")
                hasErrors = True

        if self.contactInfoSourceID.data:
            contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
            if contactSource is None:
                self.contactInfoSourceID.errors.append("ID not found")
                hasErrors = True

        if self.contactInfoStatusID.data:
            contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
            if contactStatus is None:
                self.contactInfoStatusID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class FinalCodeForm(BaseForm):
    finalCode = StringField('finalCode',
                            [] + COMMON_STRING_VALIDATORS)


class FundingForm(BaseForm):
    grantStatusID = IntegerField('grantStatusID',
                                 [] + COMMON_INTEGER_VALIDATORS)
    projectID = IntegerField('projectID',
                             [validators.InputRequired()])
    fundingSourceID = IntegerField('fundingSourceID',
                                   [] + COMMON_INTEGER_VALIDATORS)
    primaryFundingSource = StringField('primaryFundingSource',
                                       [] + COMMON_STRING_VALIDATORS)
    secondaryFundingSource = StringField('secondaryFundingSource',
                                         [] + COMMON_STRING_VALIDATORS)
    fundingNumber = StringField('fundingNumber',
                                [] + COMMON_STRING_VALIDATORS)
    grantTitle = StringField('grantTitle',
                             [] + COMMON_STRING_VALIDATORS)
    dateStatus = DateField('dateStatus',
                           [] + COMMON_DATE_VALIDATORS,
                           format=DATE_FORMAT)
    grantPi = IntegerField('grantPi',
                           [] + COMMON_INTEGER_VALIDATORS)
    primaryChartfield = StringField('primaryChartfield',
                                    [] + COMMON_STRING_VALIDATORS)
    secondaryChartfield = StringField('secondaryChartfield',
                                      [] + COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors = True

        if self.grantStatusID.data:
            grantStatus = query.get_grant_status(self.grantStatusID.data)
            if grantStatus is None:
                self.grantStatusID.errors.append("ID not found")
                hasErrors = True

        if self.fundingSourceID.data:
            fundingSource = query.get_funding_source(self.fundingSourceID.data)
            if fundingSource is None:
                self.fundingSourceID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class FundingSourceLUTForm(BaseForm):
    fundingSource = StringField('fundingSource',
                                [] + COMMON_STRING_VALIDATORS)


class GrantStatusLUTForm(BaseForm):
    grantStatus = StringField('grantStatus',
                              [] + COMMON_STRING_VALIDATORS)


class HumanSubjectTrainingLUTForm(BaseForm):
    trainingType = StringField('trainingType',
                               [] + COMMON_STRING_VALIDATORS)


class IRBHolderLUTForm(BaseForm):
    holder = StringField('holder',
                         [] + COMMON_STRING_VALIDATORS)
    holderDefinition = StringField('holderDefinition',
                                   [] + COMMON_STRING_VALIDATORS)


class IncentiveForm(BaseForm):
    participantID = IntegerField('participantID',
                                    [validators.InputRequired()])
    incentiveDescription = StringField('incentiveDescription',
                                       [] + COMMON_STRING_VALIDATORS)
    barcode = StringField('barcode',
                              [] + COMMON_STRING_VALIDATORS)
    dateGiven = DateField('dateGiven',[]+COMMON_DATE_VALIDATORS,
                          format=DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        participant = query.get_project_patient(self.participantID.data)
        if participant is None:
            self.participantID.errors.append("ID not found")
            hasErrors = True

        # make sure barcode is in the table
        if self.barcode.data:
            bc = query.get_gift_card_by_barcode(self.barcode.data)
            if bc is None:
                self.barcode.errors.append("Barcode not found in gift card table.")
                hasErrors = True
        return not hasErrors


class InformantForm(BaseForm):
    participantID = IntegerField('participantID',
                             [validators.InputRequired()])
    firstName = StringField('firstName',
                            [] + COMMON_STRING_VALIDATORS)
    lastName = StringField('lastName',
                           [] + COMMON_STRING_VALIDATORS)
    middleName = StringField('middleName',
                             [] + COMMON_STRING_VALIDATORS)
    informantPrimary = StringField('informantPrimary',
                                   [] + COMMON_STRING_VALIDATORS)
    informantRelationship = StringField('informantRelationship',
                                        [] + COMMON_STRING_VALIDATORS)
    notes = StringField('notes',
                        [] + COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)
        patient = query.get_patient(self.participantID.data)
        if patient is None:
            self.participantID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors


class InformantAddressForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    informantID = IntegerField('informantID',
                               [validators.InputRequired()])
    contactInfoStatusID = IntegerField('contactInfoStatusID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    street = StringField('street',
                         [] + COMMON_STRING_VALIDATORS)
    street2 = StringField('street2',
                          [] + COMMON_STRING_VALIDATORS)
    city = StringField('city',
                       [] + COMMON_STRING_VALIDATORS)
    stateID = IntegerField('stateID',
                           [] + COMMON_INTEGER_VALIDATORS)
    zip = StringField('zip',
                      [] + COMMON_STRING_VALIDATORS)
    addressStatusDate = DateField('addressStatusDate',
                                  [] + COMMON_DATE_VALIDATORS,
                                  format=DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        informant = query.get_informant(self.informantID.data)
        if informant is None:
            self.informantID.errors.append("ID not found")
            hasErrors = True

        if self.contactInfoSourceID.data:
            contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
            if contactSource is None:
                self.contactInfoSourceID.errors.append("ID not found")
                hasErrors = True

        if self.stateID.data:
            state = query.get_contact_info_source(self.stateID.data)
            if state is None:
                self.stateID.errors.append("ID not found")
                hasErrors = True

        if self.contactInfoStatusID.data:
            contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
            if contactStatus is None:
                self.contactInfoStatusID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class InformantPhoneForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    informantID = IntegerField('informantID',
                               [] + COMMON_INTEGER_VALIDATORS)
    contactInfoStatusID = IntegerField('contactInfoStatusID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    phoneTypeID = IntegerField('phoneTypeID',
                               [] + COMMON_INTEGER_VALIDATORS)
    phoneNumber = StringField('phoneNumber',
                              [] + COMMON_STRING_VALIDATORS)
    phoneStatusDate = DateField('phoneStatusDate',
                                [] + COMMON_DATE_VALIDATORS,
                                format=DATE_FORMAT)

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

        phoneType = query.get_phone_type(self.phoneTypeID.data)
        if phoneType is None:
            self.phoneTypeID.errors.append("ID not found")
            hasErrors = True

        contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
        if contactStatus is None:
            self.contactInfoStatusID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors


class LogForm(BaseForm):
    logSubjectID = IntegerField('logSubjectID',
                                [] + COMMON_INTEGER_VALIDATORS)
    projectID = IntegerField('projectID',
                             [validators.InputRequired()])
    staffID = IntegerField('staffID',
                           [validators.InputRequired()])
    phaseStatusID = IntegerField('phaseStatusID',
                                 [] + COMMON_INTEGER_VALIDATORS)
    note = StringField('note',
                       [] + COMMON_STRING_VALIDATORS)
    date = DateField('date',
                     [] + COMMON_DATE_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors = True

        staff = query.get_staff(self.staffID.data)
        if staff is None:
            self.staffID.errors.append("ID not found")
            hasErrors = True

        if self.logSubjectID.data:
            logSubject = query.get_log_subject(self.logSubjectID.data)
            if logSubject is None:
                self.logSubjectID.errors.append("ID not found")
                hasErrors = True

        if self.phaseStatusID.data:
            phaseStatus = query.get_phase_status(self.phaseStatusID.data)
            if phaseStatus is None:
                self.phaseStatusID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class LogSubjectLUTForm(BaseForm):
    logSubject = StringField('logSubject',
                             [] + COMMON_STRING_VALIDATORS)


class PatientForm(BaseForm):
    patID = StringField('patID',
                        [] + COMMON_STRING_VALIDATORS)
    ucrDistID = IntegerField('ucrDistID',
                             [] + COMMON_INTEGER_VALIDATORS)
    UPDBID = IntegerField('UPDBID',
                          [] + COMMON_INTEGER_VALIDATORS)
    firstName = StringField('firstName',
                            [] + COMMON_STRING_VALIDATORS)
    lastName = StringField('lastName',
                           [] + COMMON_STRING_VALIDATORS)
    middleName = StringField('middleName',
                             [] + COMMON_STRING_VALIDATORS)
    maidenName = StringField('maidenName',
                             [] + COMMON_STRING_VALIDATORS)
    aliasFirstName = StringField('aliasFirstName',
                                 [] + COMMON_STRING_VALIDATORS)
    aliasLastName = StringField('aliasLastName',
                                [] + COMMON_STRING_VALIDATORS)
    aliasMiddleName = StringField('aliasMiddleName',
                                  [] + COMMON_STRING_VALIDATORS)
    dobDay = IntegerField('dobDay',
                    [validators.number_range(max=31)] + COMMON_INTEGER_VALIDATORS)
    dobMonth = IntegerField('dobDay',
                    [validators.number_range(max=12)] + COMMON_INTEGER_VALIDATORS)
    dobYear = IntegerField('dobYear',
                    [] + COMMON_INTEGER_VALIDATORS)
    SSN = IntegerField('SSN',
                       [] + COMMON_INTEGER_VALIDATORS)
    sexID = StringField('sexID',
                        [] + COMMON_INTEGER_VALIDATORS)
    raceID = StringField('raceID',
                         [] + COMMON_INTEGER_VALIDATORS)
    ethnicityID = StringField('ethnicityID',
                              [] + COMMON_INTEGER_VALIDATORS)
    vitalStatusID = StringField('vitalStatusID',
                                [] + COMMON_INTEGER_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        if self.sexID.data:
            sex = query.get_sex(self.sexID.data)
            if sex is None:
                self.sexID.errors.append("ID not found")
                hasErrors = True

        if self.raceID.data:
            race = query.get_race(self.raceID.data)
            if race is None:
                self.raceID.errors.append("ID not found")
                hasErrors = True

        if self.ethnicityID.data:
            ethnicity = query.get_ethnicity(self.ethnicityID.data)
            if ethnicity is None:
                self.ethnicityID.errors.append("ID not found")
                hasErrors = True

        if self.vitalStatusID.data:
            vitalStatus = query.get_vital_status(self.vitalStatusID.data)
            if vitalStatus is None:
                self.vitalStatusID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class PatientAddressForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    participantID = IntegerField('participantID',
                             [validators.InputRequired()])
    contactInfoStatusID = IntegerField('contactInfoStatusID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    street = StringField('street',
                         [] + COMMON_STRING_VALIDATORS)
    street2 = StringField('street2',
                          [] + COMMON_STRING_VALIDATORS)
    city = StringField('city',
                       [] + COMMON_STRING_VALIDATORS)
    stateID = IntegerField('stateID',
                           [] + COMMON_INTEGER_VALIDATORS)
    zip = StringField('zip',
                      [] + COMMON_STRING_VALIDATORS)
    addressStatusDate = DateField('addressStatusDate',
                                  [] + COMMON_DATE_VALIDATORS,
                                  format=DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        patient = query.get_patient(self.participantID.data)
        if patient is None:
            self.participantID.errors.append("ID not found")
            hasErrors = True

        if self.contactInfoSourceID.data:
            contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
            if contactSource is None:
                self.contactInfoSourceID.errors.append("ID not found")
                hasErrors = True

        if self.stateID.data:
            state = query.get_state(self.stateID.data)
            if state is None:
                self.stateID.errors.append("ID not found")
                hasErrors = True

        if self.contactInfoStatusID.data:
            contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
            if contactStatus is None:
                self.contactInfoStatusID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class PatientEmailForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    participantID = IntegerField('participantID',
                             [validators.InputRequired()])
    contactInfoStatusID = IntegerField('contactInfoStatusID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    email = StringField('email',
                        [] + COMMON_STRING_VALIDATORS)
    emailStatusDate = DateField('emailStatusDate',
                                [] + COMMON_DATE_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        patient = query.get_patient(self.participantID.data)
        if patient is None:
            self.participantID.errors.append("ID not found")
            hasErrors = True

        if self.contactInfoSourceID.data:
            contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
            if contactSource is None:
                self.contactInfoSourceID.errors.append("ID not found")
                hasErrors = True

        if self.contactInfoStatusID.data:
            contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
            if contactStatus is None:
                self.contactInfoStatusID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class PatientPhoneForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    participantID = IntegerField('participantID',
                             [validators.InputRequired()])
    contactInfoStatusID = IntegerField('contactInfoStatusID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    phoneTypeID = IntegerField('phoneTypeID',
                               [] + COMMON_INTEGER_VALIDATORS)
    phoneNumber = StringField('phoneNumber',
                              [] + COMMON_STRING_VALIDATORS)
    phoneStatusDate = DateField('phoneStatusDate',
                                [] + COMMON_DATE_VALIDATORS,
                                format=DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        patient = query.get_patient(self.participantID.data)
        if patient is None:
            self.participantID.errors.append("ID not found")
            hasErrors = True

        if self.phoneTypeID.data:
            phoneType = query.get_phone_type(self.phoneTypeID.data)
            if phoneType is None:
                self.phoneTypeID.errors.append("ID not found")
                hasErrors = True

        if self.contactInfoSourceID.data:
            contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
            if contactSource is None:
                self.contactInfoSourceID.errors.append("ID not found")
                hasErrors = True

        if self.contactInfoStatusID.data:
            contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
            if contactStatus is None:
                self.contactInfoStatusID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class PatientProjectStatusForm(BaseForm):
    patientProjectStatusTypeID = IntegerField('patientProjectStatusTypeID',
                                              [] + COMMON_INTEGER_VALIDATORS)
    participantID = IntegerField('participantID',
                                    [validators.InputRequired()])

    def validate(self):
        hasErrors = not Form.validate(self)

        projectPatient = query.get_project_patient(self.participantID.data)
        if projectPatient is None:
            self.participantID.errors.append("ID not found")
            hasErrors = True

        if self.patientProjectStatusTypeID.data:
            patientProjectStatusLUT = query.get_patient_project_status_type(self.patientProjectStatusTypeID.data)
            if patientProjectStatusLUT is None:
                self.patientProjectStatusTypeID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class PatientProjectStatusLUTForm(BaseForm):
    statusDescription = StringField('statusDescription',
                                    [] + COMMON_STRING_VALIDATORS)


class PhaseStatusForm(BaseForm):
    phaseStatus = StringField('phaseStatus',
                              [] + COMMON_STRING_VALIDATORS)
    phaseDescription = StringField('phaseDescription',
                                   [] + COMMON_STRING_VALIDATORS)


class PhoneTypeForm(BaseForm):
    phoneType = StringField('phoneType',
                            [] + COMMON_STRING_VALIDATORS)


class PhysicianForm(BaseForm):
    firstName = StringField('firstName',
                            [] + COMMON_STRING_VALIDATORS)
    lastName = StringField('lastName',
                           [] + COMMON_STRING_VALIDATORS)
    middleName = StringField('middleName',
                             [] + COMMON_STRING_VALIDATORS)
    credentials = StringField('credentials',
                              [] + COMMON_STRING_VALIDATORS)
    specialty = StringField('specialty',
                            [] + COMMON_STRING_VALIDATORS)
    aliasFirstName = StringField('aliasFirstName',
                                 [] + COMMON_STRING_VALIDATORS)
    aliasLastName = StringField('aliasLastName',
                                [] + COMMON_STRING_VALIDATORS)
    aliasMiddleName = StringField('aliasMiddleName',
                                  [] + COMMON_STRING_VALIDATORS)
    physicianStatusID = IntegerField('physicianStatusID',
                                     [] + COMMON_INTEGER_VALIDATORS)
    physicianStatusDate = DateField('physicianStatusDate',
                                    [] + COMMON_DATE_VALIDATORS,
                                    format=DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        if self.physicianStatusID.data:
            physicianStatus = query.get_physician_status(self.physicianStatusID.data)
            if physicianStatus is None:
                self.physicianStatusID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class PhysicianFacilityForm(BaseForm):
    facilityID = IntegerField('facilityID',
                              [validators.InputRequired()])
    physicianID = IntegerField('physicianID',
                               [validators.InputRequired()])
    physFacilityStatusID = IntegerField('physFacilityStatus',
                                        [] + COMMON_INTEGER_VALIDATORS)
    physFacilityStatusDate = DateField('physFacilityStatusDate',
                                       [] + COMMON_DATE_VALIDATORS,
                                       format=DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        physician = query.get_physician(self.physicianID.data)
        if physician is None:
            self.physicianID.errors.append("ID not found")
            hasErrors = True

        facility = query.get_facility(self.facilityID.data)
        if facility is None:
            self.facilityID.errors.append("ID not found")
            hasErrors = True

        if self.physFacilityStatusID.data:
            status = query.get_physician_facility_status(self.physFacilityStatusID.data)
            if status is None:
                self.physFacilityStatusID.errors.append("ID not found")
                hasErrors = True

        return not hasErrors


class PhysicianAddressForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    physicianID = IntegerField('physicianID',
                               [validators.InputRequired()])
    contactInfoStatusID = IntegerField('contactInfoStatusID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    street = StringField('street',
                         [] + COMMON_STRING_VALIDATORS)
    street2 = StringField('street2',
                          [] + COMMON_STRING_VALIDATORS)
    city = StringField('city',
                       [] + COMMON_STRING_VALIDATORS)
    stateID = IntegerField('stateID',
                           [] + COMMON_INTEGER_VALIDATORS)
    zip = StringField('zip',
                      [] + COMMON_STRING_VALIDATORS)
    addressStatusDate = DateField('addressStatusDate',
                                  [] + COMMON_DATE_VALIDATORS,
                                  format=DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        if self.contactInfoSourceID.data:
            contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
            if contactSource is None:
                self.contactInfoSourceID.errors.append("ID not found")
                hasErrors = True

        if self.stateID.data:
            state = query.get_state(self.stateID.data)
            if state is None:
                self.stateID.errors.append("ID not found")
                hasErrors = True

        physician = query.get_physician(self.physicianID.data)
        if physician is None:
            self.physicianID.errors.append("ID not found")
            hasErrors = True

        if self.contactInfoStatusID.data:
            contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
            if contactStatus is None:
                self.contactInfoStatusID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class PhysicianEmailForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    physicianID = IntegerField('physicianID',
                               [validators.InputRequired()])
    contactInfoStatusID = IntegerField('contactInfoStatusID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    email = StringField('email',
                        [] + COMMON_STRING_VALIDATORS)
    emailStatusDate = DateField('emailStatusDate',
                                [] + COMMON_DATE_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        if self.contactInfoSourceID.data:
            contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
            if contactSource is None:
                self.contactInfoSourceID.errors.append("ID not found")
                hasErrors = True

        physician = query.get_patient(self.physicianID.data)
        if physician is None:
            self.physicianID.errors.append("ID not found")
            hasErrors = True

        if self.contactInfoStatusID.data:
            contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
            if contactStatus is None:
                self.contactInfoStatusID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class PhysicianPhoneForm(BaseForm):
    contactInfoSourceID = IntegerField('contactInfoSourceID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    physicianID = IntegerField('physicianID',
                               [validators.InputRequired()])
    contactInfoStatusID = IntegerField('contactInfoStatusID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    phoneNumber = StringField('phoneNumber',
                              [] + COMMON_STRING_VALIDATORS)
    phoneTypeID = IntegerField('phoneTypeID',
                               [] + COMMON_INTEGER_VALIDATORS)
    phoneStatusDate = DateField('phoneStatusDate',
                                [] + COMMON_DATE_VALIDATORS,
                                format=DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        if self.phoneTypeID.data:
            phoneType = query.get_phone_type(self.phoneTypeID.data)
            if phoneType is None:
                self.phoneTypeID.errors.append("ID not found")
                hasErrors = True

        if self.contactInfoSourceID.data:
            contactSource = query.get_contact_info_source(self.contactInfoSourceID.data)
            if contactSource is None:
                self.contactInfoSourceID.errors.append("ID not found")
                hasErrors = True

        physician = query.get_physician(self.physicianID.data)
        if physician is None:
            self.physicianID.errors.append("ID not found")
            hasErrors = True

        if self.contactInfoStatusID.data:
            contactStatus = query.get_contact_info_status(self.contactInfoStatusID.data)
            if contactStatus is None:
                self.contactInfoStatusID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class PhysicianStatusForm(BaseForm):
    physicianStatus = StringField('physicianID',
                                  [] + COMMON_STRING_VALIDATORS)


class PhysicianToCTCForm(BaseForm):
    physicianID = IntegerField('physicianID',
                               [validators.InputRequired()])
    ctcID = IntegerField('ctcID',
                         [validators.InputRequired()])

    def validate(self):
        hasErrors = not Form.validate(self)

        physician = query.get_physician(self.physicianID.data)
        if physician is None:
            self.physicianID.errors.append("ID not found")
            hasErrors = True

        ctc = query.get_ctc(self.ctcID.data)
        if ctc is None:
            self.ctcID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors


class PreApplicationForm(BaseForm):
    projectID = IntegerField('projectID',
                             [validators.InputRequired()])
    piFirstName = StringField('piFirstName',
                              [] + COMMON_STRING_VALIDATORS)
    piLastName = StringField('piLastName',
                             [] + COMMON_STRING_VALIDATORS)
    piPhone = StringField('piPhone',
                          [] + COMMON_STRING_VALIDATORS)
    piEmail = StringField('piEmail',
                          [] + COMMON_STRING_VALIDATORS)
    contactFirstName = StringField('contactFirstName',
                                   [] + COMMON_STRING_VALIDATORS)
    contactLastName = StringField('contactLastName',
                                  [] + COMMON_STRING_VALIDATORS)
    contactPhone = StringField('contactPhone',
                               [] + COMMON_STRING_VALIDATORS)
    contactEmail = StringField('contactEmail',
                               [] + COMMON_STRING_VALIDATORS)
    institution = StringField('institution',
                              [] + COMMON_STRING_VALIDATORS)
    institution2 = StringField('institution2',
                               [] + COMMON_STRING_VALIDATORS)
    uid = StringField('uid',
                      [] + COMMON_STRING_VALIDATORS)
    udoh = IntegerField('udoh',
                        [] + COMMON_INTEGER_VALIDATORS)
    projectTitle = StringField('projectTitle',
                               [] + COMMON_STRING_VALIDATORS)
    purpose = StringField('purpose',
                          [] + COMMON_STRING_VALIDATORS)
    irb0 = BooleanField('irb0',
                        [] + COMMON_BOOL_VALIDATORS)
    irb1 = BooleanField('irb1',
                        [] + COMMON_BOOL_VALIDATORS)
    irb2 = BooleanField('irb2',
                        [] + COMMON_BOOL_VALIDATORS)
    irb3 = BooleanField('irb3',
                        [] + COMMON_BOOL_VALIDATORS)
    irb4 = BooleanField('irb4',
                        [] + COMMON_BOOL_VALIDATORS)
    otherIrb = StringField('otherIrb',
                           [] + COMMON_STRING_VALIDATORS)
    updb = BooleanField('updb',
                        [] + COMMON_BOOL_VALIDATORS)
    ptContact = BooleanField('ptContact',
                             [] + COMMON_BOOL_VALIDATORS)
    startDate = DateField('startDate',
                          [] + COMMON_DATE_VALIDATORS,
                          format=DATE_FORMAT)
    link = BooleanField('link',
                        [] + COMMON_BOOL_VALIDATORS)
    deliveryDate = DateField('deliveryDate',
                             [] + COMMON_DATE_VALIDATORS,
                             format=DATE_FORMAT)
    description = StringField('description',
                              [] + COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project type FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors


class ProjectForm(BaseForm):
    projectTypeID = IntegerField('projectTypeID',
                                 [] + COMMON_INTEGER_VALIDATORS)
    irbHolderID = IntegerField('irbHolderID',
                               [] + COMMON_INTEGER_VALIDATORS)
    projectTitle = StringField('projectTitle',
                               [] + COMMON_STRING_VALIDATORS)
    shortTitle = StringField('shortTitle',
                             [] + COMMON_STRING_VALIDATORS)
    projectSummary = StringField('projectSummary',
                                 [] + COMMON_STRING_VALIDATORS)
    sop = StringField('sop',
                      [] + COMMON_STRING_VALIDATORS)
    ucrProposal = StringField('ucrProposal',
                              [] + COMMON_STRING_VALIDATORS)
    budgetDoc = StringField('budgetDoc',
                            [] + COMMON_STRING_VALIDATORS)
    ucrFee = StringField('ucrFee',
                         [] + COMMON_STRING_VALIDATORS)
    ucrNoFee = StringField('ucrNoFee',
                           [] + COMMON_STRING_VALIDATORS)
    previousShortTitle = StringField('previousShortTitle',
                                     [] + COMMON_STRING_VALIDATORS)
    dateAdded = DateField('dateAdded',
                          [] + COMMON_DATE_VALIDATORS,
                          format=DATE_FORMAT)
    finalRecruitmentReport = StringField('finalRecruitmentReport',
                                         [] + COMMON_STRING_VALIDATORS)
    ongoingContact = BooleanField('ongoingContact',
                                  [] + COMMON_BOOL_VALIDATORS)
    activityStartDate = DateField('activityStartDate',
                                  [] + COMMON_DATE_VALIDATORS,
                                  format=DATE_FORMAT)
    activityEndDate = DateField('activityEndDate',
                                [] + COMMON_DATE_VALIDATORS,
                                format=DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project type FK exists
        if self.projectTypeID.data:
            projType = query.get_project_type(self.projectTypeID.data)
            if projType is None:
                self.projectTypeID.errors.append("ID not found")
                hasErrors = True

        # check the irbHolderLUT FK
        if self.irbHolderID.data:
            irbHolder = query.get_irb_holder(self.irbHolderID.data)
            if irbHolder is None:
                self.irbHolderID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class ProjectPatientForm(BaseForm):
    projectID = IntegerField('projectID',
                             [validators.InputRequired()])
    staffID = IntegerField('staffID',
                           [] + COMMON_INTEGER_VALIDATORS)
    ctcID = IntegerField('ctcID',
                         [validators.InputRequired()])
    currentAge = IntegerField('currentAge',
                              [] + COMMON_INTEGER_VALIDATORS)
    batch = IntegerField('batch',
                         [] + COMMON_INTEGER_VALIDATORS)
    siteGrp = IntegerField('siteGrp',
                           [] + COMMON_INTEGER_VALIDATORS)
    finalCodeID = IntegerField('finalCodeID',
                               [validators.InputRequired()])
    finalCodeDate = DateField('finalCodeDate',
                              [] + COMMON_DATE_VALIDATORS,
                              format=DATE_FORMAT)
    enrollmentDate = DateField('enrollmentDate',
                               [] + COMMON_DATE_VALIDATORS,
                               format=DATE_FORMAT)
    dateCoordSigned = DateField('dateCoordSigned',
                                [] + COMMON_DATE_VALIDATORS,
                                format=DATE_FORMAT)
    importDate = DateField('importDate',
                           [validators.InputRequired()],
                           format=DATE_FORMAT)
    finalCodeStaffID = IntegerField('finalCodeStaffID',
                                    [] + COMMON_INTEGER_VALIDATORS)
    enrollmentStaffID = IntegerField('enrollmentStaffID',
                                     [] + COMMON_INTEGER_VALIDATORS)
    dateCoordSignedStaffID = IntegerField('dateCoordSignedStaffID',
                                          [] + COMMON_INTEGER_VALIDATORS)
    abstractStatusID = IntegerField('abstractStatusID',
                                    [] + COMMON_INTEGER_VALIDATORS)
    abstractStatusDate = DateField('abstractStatusDate',
                                   [] + COMMON_DATE_VALIDATORS,
                                   format=DATE_FORMAT)
    abstractStatusStaffID = IntegerField('abstractStatusStaffID',
                                         [] + COMMON_INTEGER_VALIDATORS)
    sentToAbstractorDate = DateField('sentToAbstractorDate',
                                     [] + COMMON_DATE_VALIDATORS,
                                     format=DATE_FORMAT)
    sentToAbstractorStaffID = IntegerField('sentToAbstractorStaffID',
                                           [] + COMMON_INTEGER_VALIDATORS)
    abstractedDate = DateField('abstractedDate',
                               [] + COMMON_DATE_VALIDATORS,
                               format=DATE_FORMAT)
    abstractorStaffID = IntegerField('abstractorStaffID',
                                     [] + COMMON_INTEGER_VALIDATORS)
    researcherDate = DateField('researcherDate',
                               [] + COMMON_DATE_VALIDATORS,
                               format=DATE_FORMAT)
    researcherStaffID = IntegerField('researcherStaffID',
                                     [] + COMMON_INTEGER_VALIDATORS)
    consentLink = StringField('consentLink',
                              [] + COMMON_STRING_VALIDATORS)
    medRecordReleaseSigned = BooleanField('medRecordReleaseSigned',
                                          [] + COMMON_BOOL_VALIDATORS)
    medRecordReleaseLink = StringField('medRecordReleaseLink',
                                       [] + COMMON_STRING_VALIDATORS)
    medRecordReleaseStaffID = IntegerField('medRecordReleaseStaffID',
                                           [] + COMMON_INTEGER_VALIDATORS)
    medRecordReleaseDate = DateField('medRecordReleaseDate',
                                     [] + COMMON_DATE_VALIDATORS,
                                     format=DATE_FORMAT)
    surveyToResearcher = DateField('surveyToResearcher',
                                   [] + COMMON_DATE_VALIDATORS,
                                   format=DATE_FORMAT)
    surveyToResearcherStaffID = IntegerField('surveyToResearcherStaffID',
                                             [] + COMMON_INTEGER_VALIDATORS)
    qualityControl = BooleanField('qualityControl',
                                            []+COMMON_BOOL_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        finalCode = query.get_final_code(self.finalCodeID.data)
        if finalCode is None:
            self.finalCodeID.errors.append("ID not found")
            hasErrors = True

        if self.finalCodeStaffID.data:
            finalCodeStaff = query.get_staff(self.finalCodeStaffID.data)
            if finalCodeStaff is None:
                self.finalCodeStaffID.errors.append("ID not found")
                hasErrors = True

        if self.enrollmentStaffID.data:
            enrollmentStaff = query.get_staff(self.enrollmentStaffID.data)
            if enrollmentStaff is None:
                self.enrollmentStaffID.errors.append("ID not found")
                hasErrors = True

        if self.dateCoordSignedStaffID.data:
            dateCoordSignedStaff = query.get_staff(self.dateCoordSignedStaffID.data)
            if dateCoordSignedStaff is None:
                self.dateCoordSignedStaffID.errors.append("ID not found")
                hasErrors = True

        if self.abstractStatusID.data:
            abstractStatus = query.get_staff(self.abstractStatusID.data)
            if abstractStatus is None:
                self.abstractStatusID.errors.append("ID not found")
                hasErrors = True

        if self.abstractStatusStaffID.data:
            abstractStatusStaff = query.get_staff(self.abstractStatusStaffID.data)
            if abstractStatusStaff is None:
                self.abstractStatusStaffID.errors.append("ID not found")
                hasErrors = True

        if self.sentToAbstractorStaffID.data:
            sentToAbstractorStaff = query.get_staff(self.sentToAbstractorStaffID.data)
            if sentToAbstractorStaff is None:
                self.sentToAbstractorStaffID.errors.append("ID not found")
                hasErrors = True

        if self.abstractorStaffID.data:
            abstractorStaff = query.get_staff(self.abstractorStaffID.data)
            if abstractorStaff is None:
                self.abstractorStaffID.errors.append("ID not found")
                hasErrors = True

        if self.researcherStaffID.data:
            researcherStaff = query.get_staff(self.researcherStaffID.data)
            if researcherStaff is None:
                self.researcherStaffID.errors.append("ID not found")
                hasErrors = True

        if self.medRecordReleaseStaffID.data:
            medRecordReleaseStaff = query.get_staff(self.medRecordReleaseStaffID.data)
            if medRecordReleaseStaff is None:
                self.medRecordReleaseStaffID.errors.append("ID not found")
                hasErrors = True

        if self.surveyToResearcherStaffID.data:
            surveyToResearcherStaff = query.get_staff(self.surveyToResearcherStaffID.data)
            if surveyToResearcherStaff is None:
                self.surveyToResearcherStaffID.errors.append("ID not found")
                hasErrors = True

        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors = True

        if self.staffID.data:
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
                               [] + COMMON_INTEGER_VALIDATORS)
    projectID = IntegerField('projectID',
                             [validators.InputRequired()])
    staffID = IntegerField('staffID',
                           [validators.InputRequired()])
    datePledge = DateField('datePledge',
                           [] + COMMON_DATE_VALIDATORS,
                           format=DATE_FORMAT)
    dateRevoked = DateField('dateRevoked',
                            [] + COMMON_DATE_VALIDATORS,
                            format=DATE_FORMAT)
    contactID = IntegerField('contactID',
                             [] + COMMON_INTEGER_VALIDATORS)
    inactiveID = IntegerField('inactiveID',
                              [] + COMMON_INTEGER_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project type FK exists
        project = query.get_project_type(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors = True

        staff = query.get_staff(self.staffID.data)
        if staff is None:
            self.staffID.errors.append("ID not found")
            hasErrors = True

        if self.contactID.data:
            contact = query.get_contact_enum(self.contactID.data)
            if contact is None:
                self.contactID.errors.append("ID not found")
                hasErrors = True

        if self.inactiveID.data:
            inactive = query.get_inactive_enum(self.inactiveID.data)
            if inactive is None:
                self.inactiveID.errors.append("ID not found")
                hasErrors = True

        if self.staffRoleID.data:
            staffRole = query.get_staff_role(self.staffRoleID.data)
            if staffRole is None:
                self.staffRoleID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class ProjectStatusForm(BaseForm):
    projectStatusTypeID = IntegerField('projectStatusTypeID',
                                       [] + COMMON_INTEGER_VALIDATORS)
    projectID = IntegerField('projectID',
                             [validators.InputRequired()])
    staffID = IntegerField('staffID',
                           [validators.InputRequired()])
    statusDate = DateField('statusDate',
                           [] + COMMON_DATE_VALIDATORS,
                           format=DATE_FORMAT)
    statusNotes = StringField('statusNotes',
                              [] + COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project type FK exists
        project = query.get_project_type(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors = True

        if self.projectStatusTypeID.data:
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
                                [] + COMMON_STRING_VALIDATORS)
    projectStatusDefinition = StringField('projectStatusDefinition',
                                          [] + COMMON_STRING_VALIDATORS)


class ProjectTypeForm(BaseForm):
    projectType = StringField('projectType',
                              [] + COMMON_STRING_VALIDATORS)
    projectTypeDefinition = StringField('projectTypeDefinition',
                                        [] + COMMON_STRING_VALIDATORS)


class ReviewCommitteeStatusLUTForm(BaseForm):
    reviewCommitteeStatus = StringField('reviewCommitteeStatus',
                                        [] + COMMON_STRING_VALIDATORS)
    reviewCommitteeStatusDefinition = StringField('reviewCommitteeStatusDefinition',
                                                  [] + COMMON_STRING_VALIDATORS)


class ReviewCommitteeForm(BaseForm):
    projectID = IntegerField('projectID',
                             [validators.InputRequired()])
    reviewCommitteeStatusID = IntegerField('reviewCommitteeStatusID',
                                           [] + COMMON_INTEGER_VALIDATORS)
    reviewCommitteeLUTID = IntegerField('reviewCommitteeLUTID',
                                        [] + COMMON_INTEGER_VALIDATORS)
    reviewCommitteeNumber = StringField('reviewCommitteeNumber',
                                        [] + COMMON_STRING_VALIDATORS)
    dateInitialReview = DateField('dateInitialReview',
                                  [] + COMMON_DATE_VALIDATORS,
                                  format=DATE_FORMAT)
    dateExpires = DateField('dateExpires',
                            [] + COMMON_DATE_VALIDATORS,
                            format=DATE_FORMAT)
    rcNote = StringField('rcNote',
                         [] + COMMON_STRING_VALIDATORS)
    rcProtocol = StringField('rcProtocol',
                             [] + COMMON_STRING_VALIDATORS)
    rcApproval = StringField('rcApproval',
                             [] + COMMON_STRING_VALIDATORS)

    def validate(self):
        f = Form.validate(self)
        hasErrors = False  # are hasErrors detected?
        if not f:
            hasErrors = True

        # Check to make sure the project  FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors = True

        # check the rcStatus FK
        if self.reviewCommitteeStatusID.data:
            rcStatus = query.get_review_committee_status(self.reviewCommitteeStatusID.data)
            if rcStatus is None:
                self.reviewCommitteeStatusID.errors.append("ID not found")
                hasErrors = True

        # check the reviewCommitteeList FK
        if self.reviewCommitteeLUTID.data:
            rc = query.get_review_committee_lut(self.reviewCommitteeLUTID.data)
            if rc is None:
                self.reviewCommitteeLUTID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class ReviewCommitteeLUTForm(BaseForm):
    reviewCommittee = StringField('reviewCommittee',
                                  [] + COMMON_STRING_VALIDATORS)
    reviewCommitteeDescription = StringField('reviewCommitteeDescription',
                                             [] + COMMON_STRING_VALIDATORS)


class StaffForm(BaseForm):
    firstName = StringField('firstName',
                            [] + COMMON_STRING_VALIDATORS)
    lastName = StringField('lastName',
                           [] + COMMON_STRING_VALIDATORS)
    middleName = StringField('middleName',
                             [] + COMMON_STRING_VALIDATORS)
    email = StringField('email',
                        [] + COMMON_STRING_VALIDATORS)
    phoneNumber = StringField('phoneNumber',
                              [] + COMMON_STRING_VALIDATORS)
    phoneComment = StringField('phoneComment',
                               [] + COMMON_STRING_VALIDATORS)
    institution = StringField('institution',
                              [] + COMMON_STRING_VALIDATORS)
    department = StringField('department',
                             [] + COMMON_STRING_VALIDATORS)
    position = StringField('position',
                           [] + COMMON_STRING_VALIDATORS)
    credentials = StringField('credentials',
                              [] + COMMON_STRING_VALIDATORS)
    street = StringField('street',
                         [] + COMMON_STRING_VALIDATORS)
    city = StringField('city',
                       [] + COMMON_STRING_VALIDATORS)
    stateID = IntegerField('stateID',
                           [] + COMMON_INTEGER_VALIDATORS)
    ucrRoleID = IntegerField('ucrRoleID',
                             [] + COMMON_INTEGER_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        if self.ucrRoleID.data:
            ucrRole = query.get_ucr_role(self.ucrRoleID.data)
            if ucrRole is None:
                self.ucrRoleID.errors.append("ID not found")
                hasErrors = True

        if self.stateID.data:
            state = query.get_state(self.stateID.data)
            if state is None:
                self.stateID.errors.append("ID not found")
                hasErrors = True

        return not hasErrors


class StaffRoleLUTForm(BaseForm):
    staffRole = StringField('staffRole',
                            [] + COMMON_STRING_VALIDATORS)
    staffRoleDescription = StringField('staffRoleDescription',
                                       [] + COMMON_STRING_VALIDATORS)


class StaffTrainingForm(BaseForm):
    staffID = IntegerField('staffID',
                           [validators.InputRequired()])
    humanSubjectTrainingID = IntegerField('humanSubjectTrainingID',
                                          [] + COMMON_INTEGER_VALIDATORS)
    dateTaken = DateField('dateTaken',
                          [] + COMMON_DATE_VALIDATORS,
                          format=DATE_FORMAT)
    dateExpires = DateField('dateExpires',
                            [] + COMMON_DATE_VALIDATORS,
                            format=DATE_FORMAT)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project  FK exists
        staff = query.get_staff(self.staffID.data)
        if staff is None:
            self.staffID.errors.append("ID not found")
            hasErrors = True

        # check the rcStatus FK
        if self.humanSubjectTrainingID.data:
            hst = query.get_human_subject_training(self.humanSubjectTrainingID.data)
            if hst is None:
                self.humanSubjectTrainingID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class TracingForm(BaseForm):
    tracingSourceID = IntegerField('tracingSourceID',
                                   [] + COMMON_INTEGER_VALIDATORS)
    participantID = IntegerField('participantID',
                                    [validators.InputRequired()])
    date = DateField('date',
                     [] + COMMON_DATE_VALIDATORS,
                     format=DATE_FORMAT)
    staffID = IntegerField('staffID',
                           [validators.InputRequired()])
    notes = StringField('notes',
                        [] + COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project type FK exists
        projectPatient = query.get_project_patient(self.participantID.data)
        if projectPatient is None:
            self.participantID.errors.append("ID not found")
            hasErrors = True

        # check the irbHolderLUT FK
        if self.tracingSourceID.data:
            tracingSource = query.get_tracing_source(self.tracingSourceID.data)
            if tracingSource is None:
                self.tracingSourceID.errors.append("ID not found")
                hasErrors = True

        staff = query.get_staff(self.staffID.data)
        if staff is None:
            self.staffID.errors.append("ID not found")
            hasErrors = True
        return not hasErrors


class TracingSourceLUTForm(BaseForm):
    description = StringField('description',
                              [] + COMMON_STRING_VALIDATORS)


class UCRReportForm(BaseForm):
    projectID = IntegerField('projectID',
                             [validators.InputRequired()])
    reportTypeID = IntegerField('reportTypeID',
                             [] + COMMON_INTEGER_VALIDATORS)
    reportSubmitted = DateField('reportSubmitted',
                                [] + COMMON_DATE_VALIDATORS,
                                format=DATE_FORMAT)
    reportDue = DateField('reportDue',
                          [] + COMMON_DATE_VALIDATORS,
                          format=DATE_FORMAT)
    reportDoc = StringField('reportDoc',
                            [] + COMMON_STRING_VALIDATORS)

    def validate(self):
        hasErrors = not Form.validate(self)

        # Check to make sure the project FK exists
        project = query.get_project(self.projectID.data)
        if project is None:
            self.projectID.errors.append("ID not found")
            hasErrors = True

        if self.reportTypeID.data:
            ucrReportType = query.get_report_type(self.reportTypeID.data)
            if ucrReportType is None:
                self.reportTypeID.errors.append("ID not found")
                hasErrors = True
        return not hasErrors


class UCRRoleForm(BaseForm):
    ucrRole = StringField('ucrRole',
                          [] + COMMON_STRING_VALIDATORS)
