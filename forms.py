from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class IntroForm(FlaskForm):
    intro_ctx = StringField('Introduction title', validators=[DataRequired()])
    intro_txt = StringField('Introduction text', validators=[DataRequired()])

class LanguageForm(FlaskForm):
    language = StringField('Language', validators=[DataRequired()])
    is_default = BooleanField('Default')
    is_written = BooleanField('Written')
    is_spoken = BooleanField('Spoken')

class StudiesForm(FlaskForm):
    school_name = StringField('School name', validators=[DataRequired()])
    end_date = StringField('End date', validators=[DataRequired()])
    course = StringField('Course', validators=[DataRequired()])
    degree = StringField('Degree', validators=[DataRequired()])

class CertificationForm(FlaskForm):
    certifying_org = StringField('Certifying organization', validators=[DataRequired()])
    certification = StringField('Certification', validators=[DataRequired()])
    valid_till = StringField('Valid till', validators=[DataRequired()])

class MandateForm(FlaskForm):
    project_name = StringField('Project name', validators=[DataRequired()])
    client_name = StringField('Client name', validators=[DataRequired()])
    size = StringField('Size', validators=[DataRequired()])
    effort = StringField('Effort', validators=[DataRequired()])
    start_date = StringField('Start date', validators=[DataRequired()])
    end_date = StringField('End date', validators=[DataRequired()])
    function = StringField('Function', validators=[DataRequired()])
    resume = StringField('Resume', validators=[DataRequired()])
    technologies = StringField('Technologies', validators=[DataRequired()])
    tools = StringField('Tools', validators=[DataRequired()])
    responsibilities = StringField('Responsibilities', validators=[DataRequired()])
    ref_name = StringField('Reference name', validators=[DataRequired()])
    ref_contact = StringField('Reference contact', validators=[DataRequired()])
    methodologies = StringField('Methodologies', validators=[DataRequired()])
    org_context = StringField('Organization context', validators=[DataRequired()])
    project_context = StringField('Project context', validators=[DataRequired()])
