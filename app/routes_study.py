from flask import render_template, request, redirect, url_for, session, send_file, flash
from docxtpl import DocxTemplate
from app import app, forms, utils
from config import Config
import jinja2
import uuid
import datetime

@app.route('/profile-addStudy/<email>', methods=['GET', 'POST'])
def profile_addStudy(email):
    form = forms.StudiesForm()
    if form.validate_on_submit():
        try:
            mydoc = Config.mycol.find_one({"email": email})
            if mydoc is not None:
                uuid_obj = uuid.uuid4()
                mydoc['studies'].append({
                    "id_study": str(uuid_obj),
                    "school_name": form.school_name.data,
                    "degree": form.degree.data,
                    "course": form.course.data,
                    "end_date": str(form.end_date.data) })
                Config.mycol.replace_one({ "email": email }, mydoc, upsert=True)
                flash('Education added')
                return redirect(url_for('profile', email=email))
        except Exception as e:
            flash('An error occurred: ' + str(e))
    return render_template('profile-study-add.html', form = form)

@app.route('/profile-editStudy/<int:id_study>', methods=['GET', 'POST'])
def profile_editStudy(id_study):
    email = session['email']
    mydoc = Config.mycol.find_one({"email": email})
    form = forms.StudiesForm()
    if mydoc is not None:
        form = forms.StudiesForm(school_name = mydoc['studies'][id_study]['school_name'],
            degree = mydoc['studies'][id_study]['degree'],
            course = mydoc['studies'][id_study]['course'],
            end_date = datetime.datetime.strptime(mydoc['studies'][id_study]['end_date'], '%Y-%m-%d'))
        if form.validate_on_submit():
            try:
                mydoc['studies'][id_study]['school_name'] = form.school_name.data
                mydoc['studies'][id_study]['degree'] = form.degree.data
                mydoc['studies'][id_study]['course'] = form.course.data
                mydoc['studies'][id_study]['end_date'] = str(form.end_date.data)
                Config.mycol.replace_one({ "email": email }, mydoc, upsert=True)
                flash('Introduction edited')
                return redirect(url_for('profile', email=email))
            except Exception as e:
                flash('An error occurred: ' + str(e))
    return render_template('profile-study-edit.html', form = form)

@app.route('/profile-deleteStudy', methods=['POST'])
def profile_deleteStudy():
    email = request.form['email']
    mydoc = Config.mycol.find_one({"email": email})
    id_study = int(request.form['id_study'])
    if mydoc is not None:
        mydoc['studies'].remove(mydoc['studies'][id_study])
        Config.mycol.replace_one({ "email": email }, mydoc, upsert=True)
        flash('Education deleted')
    return redirect(url_for('profile', email=email))
