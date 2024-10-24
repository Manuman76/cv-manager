from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class IntroForm(FlaskForm):
    intro_ctx = StringField('Introduction title', validators=[DataRequired()])
    intro_txt = StringField('Introduction text', validators=[DataRequired()])
    submit = SubmitField('Submit')

class OtherSkillsForm(FlaskForm):
    skill = StringField('Skill', validators=[DataRequired()])
    duration = IntegerField('Duration', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LanguageForm(FlaskForm):
    language = StringField('Language', validators=[DataRequired()])
    is_default = BooleanField('Default')
    is_written = BooleanField('Written')
    is_spoken = BooleanField('Spoken')
    submit = SubmitField('Submit')

class StudiesForm(FlaskForm):
    school_name = StringField('School name', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    course = StringField('Course', validators=[DataRequired()])
    degree = StringField('Degree', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CertificationForm(FlaskForm):
    certifying_org = StringField('Certifying organization', validators=[DataRequired()])
    certification = StringField('Certification', validators=[DataRequired()])
    valid_till = StringField('Valid till', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MandateForm(FlaskForm):
    project_name = StringField('Project name', validators=[DataRequired()])
    client_name = StringField('Client name', validators=[DataRequired()])
    size = StringField('Size', validators=[DataRequired()])
    effort = StringField('Effort', validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    function = StringField('Function', validators=[DataRequired()])
    resume = StringField('Resume', validators=[DataRequired()])
    technologies = StringField('Technologies', validators=[DataRequired()])
    tools = StringField('Tools', validators=[DataRequired()])
    responsibilities = StringField('Responsibilities', validators=[DataRequired()])
    ref_name = StringField('Reference name', validators=[DataRequired()])
    ref_contact = StringField('Reference contact', validators=[DataRequired()])
    methodologies = StringField('Methodologies', validators=[DataRequired()])
    org_context = TextAreaField('Organization context', validators=[DataRequired()])
    project_context = TextAreaField('Project context', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProfileForm(FlaskForm):
    num_employee = StringField('Number of employees', validators=[DataRequired()])
    oracle_id = StringField('Oracle ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    manager = StringField('Manager', validators=[DataRequired()])
    employee_firstname = StringField('Firstname', validators=[DataRequired()])
    employee_lastname = StringField('Lastname', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    rh_classification = StringField('RH classification', validators=[DataRequired()])
    phone_num = StringField('Phone number', validators=[DataRequired()])
    submit = SubmitField('Submit')
