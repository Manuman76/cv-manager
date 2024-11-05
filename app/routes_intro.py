from flask import render_template, request, redirect, url_for, session, send_file, flash
from docxtpl import DocxTemplate
from app import app, forms, utils
from config import Config
import jinja2
import uuid
import datetime

@app.route('/profile-addIntro/<email>', methods=['GET', 'POST'])
def profile_addIntro(email):
    form = forms.IntroForm()
    if form.validate_on_submit():
        try:
            mydoc = Config.mycol.find_one({"email": email})
            if mydoc is not None:
                uuid_obj = uuid.uuid4()
                mydoc['introduction'].append({ "id_introduction": str(uuid_obj), "intro_ctx": form.intro_ctx.data, "intro_txt": form.intro_txt.data })
                Config.mycol.replace_one({ "email": email }, mydoc, upsert=True)
                flash('Introduction added')
                return redirect(url_for('profile', email=email))
        except Exception as e:
            flash('An error occurred: ' + str(e))
    return render_template('profile-intro-add.html', form = form)

@app.route('/profile-editIntro/<int:id_intro>', methods=['GET', 'POST'])
def profile_editIntro(id_intro):
    email = session['email']
    mydoc = Config.mycol.find_one({"email": email})
    form = forms.IntroForm()
    if mydoc is not None:
        form = forms.IntroForm(intro_ctx = mydoc['introduction'][id_intro]['intro_ctx'], intro_txt = mydoc['introduction'][id_intro]['intro_txt'])
        if form.validate_on_submit():
            try:
                mydoc['introduction'][id_intro]['intro_ctx'] = form.intro_ctx.data
                mydoc['introduction'][id_intro]['intro_txt'] = form.intro_txt.data
                Config.mycol.replace_one({ "email": email }, mydoc, upsert=True)
                flash('Introduction edited')
                return redirect(url_for('profile', email=email))
            except Exception as e:
                flash('An error occurred: ' + str(e))
    return render_template('profile-intro-edit.html', form = form)

@app.route('/profile-deleteIntro', methods=['POST'])
def profile_deleteIntro():
    email = request.form['email']
    mydoc = Config.mycol.find_one({"email": email})
    id_intro = int(request.form['id_intro'])
    if mydoc is not None:
        mydoc['introduction'].remove(mydoc['introduction'][id_intro])
        Config.mycol.replace_one({ "email": email }, mydoc, upsert=True)
        flash('Introduction deleted')
    return redirect(url_for('profile', email=email))
