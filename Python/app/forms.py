from wtforms import Form, BooleanField, StringField, validators

COMMON_STRING_VALIDATORS = [
        validators.InputRequired(),
        validators.Length(min=1)]

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
 