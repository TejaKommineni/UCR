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
            self.projectID.hasErrors.append("ID not found")
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
            self.projectID.hasErrors.append("ID not found")
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

class LogSubjectLUTForm(Form):
    log_subject = StringField('log_subject',
        []+COMMON_STRING_VALIDATORS)

class PatientProjectStatusLUTForm(Form):
    status_description = StringField('status_description',
        []+COMMON_STRING_VALIDATORS)

class PhaseStatusForm(Form):
    phase_status = StringField('phase_status',
        []+COMMON_STRING_VALIDATORS)
    phase_description = StringField('phase_description',
        []+COMMON_STRING_VALIDATORS)

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
            self.projectType_projectTypeID.hasErrors.append("ID not found")
            hasErrors =  True

        # check the irbHolderLUT FK
        irbHolder = query.get_irb_holder(self.IRBHolderLUT_irbHolderID.data)
        if irbHolder is None:
            self.IRBHolderLUT_irbHolderID.hasErrors.append("ID not found")
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
            self.project_projectID.hasErrors.append("ID not found")
            hasErrors =  True

        # check the rcStatus FK
        rcStatus = query.get_rc_status(self.RCStatusList_rc_StatusID.data)
        if rcStatus is None:
            self.RCStatusList_rc_StatusID.hasErrors.append("ID not found")
            hasErrors = True

        # check the reviewCommitteeList FK
        rc = query.get_rc_status(self.reviewCommitteeList_rcListID.data)
        if rc is None:
            self.reviewCommitteeList_rcListID.hasErrors.append("ID not found")
            hasErrors = True
        return not hasErrors

class ReviewCommitteeListForm(Form):
    review_committee = StringField('review_committee',
        []+COMMON_STRING_VALIDATORS)
    rc_description = StringField('rc_description',
        []+COMMON_STRING_VALIDATORS)

class StaffRoleLUTForm(Form):
    staffRole = StringField('staffRole',
        []+COMMON_STRING_VALIDATORS)
    staffRoleDescription = StringField('staffRoleDescription',
        []+COMMON_STRING_VALIDATORS)

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
            self.projectID.hasErrors.append("ID not found")
            hasErrors =  True
        return not hasErrors
