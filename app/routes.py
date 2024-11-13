from flask import render_template, request, redirect, url_for, session, send_file, flash
from flask_login import login_user, current_user
from docxtpl import DocxTemplate
from config import Config
from app.models import User
from app.forms import LoginForm
from app import app, forms, utils, db
import sqlalchemy as sa
import jinja2
import uuid
import datetime

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/generatecv/<email>')
def generatecv(email):
    context = Config.mycol.find_one({"email": email})
    if context is not None:
        doc = DocxTemplate("./documents/cvTemplate.docx")
        jinja_env = jinja2.Environment()
        doc.render(context, jinja_env)
        doc.save("generated_doc.docx")
        return send_file('../generated_doc.docx', as_attachment=True)
    return ('not found')

@app.route('/')
def index():
    mydoc = Config.mycol.find(Config.myquery)
    return render_template('my-team.html', mydoc=mydoc)

@app.route('/profile/<email>')
def profile(email):
    mydoc = Config.mycol.find_one({"email": email})
    session['email'] = email
    return render_template('profile.html', mydoc=mydoc)

@app.route('/profile-add', methods=['GET', 'POST'])
def profile_add():
    form = forms.ProfileForm()
    if form.validate_on_submit():
        try:
            mydoc = Config.mycol.find_one({"email": form.email.data})
            if mydoc is not None:
                flash('This email is already used')
                return redirect(url_for('index'))
            else:
                uuid_obj = uuid.uuid4()
                mydoc = {
                    "email": form.email.data,
                    "num_employee": form.num_employee.data,
                    "oracle_id": form.oracle_id.data,
                    "role": form.role.data,
                    "rh_classification": form.rh_classification.data,
                    "phone_num": form.phone_num.data,
                    "employee_firstname": form.employee_firstname.data,
                    "employee_lastname": form.employee_lastname.data,
                    "manager": form.manager.data,
                    "introduction": [],
                    "other_skills": [],
                    "studies": [],
                    "mandates": [],
                    "tools": [],
                    "technologies": [],
                    "certifications": [],
                    "languages": [],
                    "publications": []
                }
                Config.mycol.insert_one(mydoc)
                flash('Profile created')
                return redirect(url_for('profile', email=form.email.data))
        except Exception as e:
            flash('An error occurred: ' + str(e))
    return render_template('profile-add.html', form = form)