from flask import render_template, request, redirect, url_for, session, send_file, flash
from docxtpl import DocxTemplate
from app import app, forms, utils
from config import Config
import jinja2
import uuid
import datetime

@app.route('/profile-addTechno/<email>', methods=['GET', 'POST'])
def profile_addTechno(email):
    form = forms.OtherSkillsForm()
    if form.validate_on_submit():
        try:
            mydoc = Config.mycol.find_one({"email": email})
            if mydoc is not None:
                uuid_obj = uuid.uuid4()
                mydoc['other_skills'].append({
                    "id_other_skills": str(uuid_obj),
                    "skill": form.skill.data,
                    "duration": str(form.duration.data) })
                Config.mycol.replace_one({ "email": email }, mydoc, upsert=True)
                flash('Technology added')
                return redirect(url_for('profile', email=email))
        except Exception as e:
            flash('An error occurred: ' + str(e))
    return render_template('profile-techno-add.html', form = form)

@app.route('/profile-editTechno/<int:id_Techno>', methods=['GET', 'POST'])
def profile_editTechno(id_Techno):
    email = session['email']
    mydoc = Config.mycol.find_one({"email": email})
    form = forms.OtherSkillsForm()
    if mydoc is not None:
        form = forms.OtherSkillsForm(skill = mydoc['other_skills'][id_Techno]['skill'],
            duration = mydoc['other_skills'][id_Techno]['duration'])
        if form.validate_on_submit():
            try:
                mydoc['other_skills'][id_Techno]['skill'] = form.skill.data
                mydoc['other_skills'][id_Techno]['duration'] = str(form.duration.data)
                Config.mycol.replace_one({ "email": email }, mydoc, upsert=True)
                flash('Technology edited')
                return redirect(url_for('profile', email=email))
            except Exception as e:
                flash('An error occurred: ' + str(e))
    return render_template('profile-techno-edit.html', form = form)

@app.route('/profile-deleteTechno', methods=['POST'])
def profile_deleteTechno():
    email = request.form['email']
    mydoc = Config.mycol.find_one({"email": email})
    id_techno = int(request.form['id_techno'])
    if mydoc is not None:
        mydoc['other_skills'].remove(mydoc['other_skills'][id_techno])
        Config.mycol.replace_one({ "email": email }, mydoc, upsert=True)
        flash('Technology deleted')
    return redirect(url_for('profile', email=email))
