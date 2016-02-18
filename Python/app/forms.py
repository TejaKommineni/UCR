from wtforms import Form, BooleanField, StringField, validators

class ContactInfoSourceForm(Form):
    contact_info_source = StringField('contact_info_source',[
        validators.InputRequired(),
        validators.Length(min=1)])
        
class ContactInfoStatusForm(Form):
    contact_info_status = StringField('contact_info_status',[
        validators.InputRequired(),
        validators.Length(min=1)])
        
class ContactTypeLUTForm(Form):
    contact_definition = StringField('contact_definition',[
        validators.InputRequired(),
        validators.Length(min=1)])
        
class LogSubjectLUTForm(Form):
    log_subject = StringField('log_subject', [
        validators.InputRequired(),
        validators.Length(min=1)])
        
class PatientProjectStatusLUTForm(Form):
    status_description = StringField('status_description',[
        validators.InputRequired(),
        validators.Length(min=1)])
        
class TracingSourceLUTForm(Form):
    description = StringField('description', [
        validators.InputRequired(),
        validators.Length(min=1)])
 