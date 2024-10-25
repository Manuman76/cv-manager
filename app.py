import datetime
import json
import pymongo
import uuid
import jinja2
from flask import Flask, render_template, request, session, jsonify, flash, redirect, url_for, send_file
from bson import json_util
from pymongo.read_preferences import read_pref_mode_from_name
from forms import IntroForm, MandateForm, OtherSkillsForm, StudiesForm, ProfileForm
from docxtpl import DocxTemplate

def get_dict_from_string_array(a: str, type: str) -> list[dict]:
    arr = []
    lst = a.split(', ')
    for b in lst:
        d = {}
        d[type] = b
        arr.append(d)
    return arr

def create_app():
    app = Flask(__name__)
    app.secret_key = 'mysecretkey'

    myclient = pymongo.MongoClient("mongodb://192.168.1.128:27017/")
    mydb = myclient["cv-manager"]

    mycol = mydb["entries"]

    myquery = { "manager": "manuel.legault@alithya.com" }

    @app.route('/generatecv/<email>')
    def generatecv(email):
        context = mycol.find_one({"email": email})
        if context is not None:
            doc = DocxTemplate("./documents/cvTemplate.docx")
            jinja_env = jinja2.Environment()
            doc.render(context, jinja_env)
            doc.save("generated_doc.docx")
            return send_file('generated_doc.docx', as_attachment=True)
        return ('not found')

    @app.route('/')
    def index():
        mydoc = mycol.find(myquery)
        return render_template('my-team.html', mydoc=mydoc)

    @app.route('/profile/<email>')
    def profile(email):
        mydoc = mycol.find_one({"email": email})
        session['email'] = email
        return render_template('profile.html', mydoc=mydoc)

    @app.route('/profile-add', methods=['GET', 'POST'])
    def profile_add():
        form = ProfileForm()
        if form.validate_on_submit():
            try:
                mydoc = mycol.find_one({"email": form.email.data})
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
                    mycol.insert_one(mydoc)
                    flash('Profile created')
                    return redirect(url_for('profile', email=form.email.data))
            except Exception as e:
                flash('An error occurred: ' + str(e))
        return render_template('profile-add.html', form = form)

    @app.route('/profile-addIntro/<email>', methods=['GET', 'POST'])
    def profile_addIntro(email):
        form = IntroForm()
        if form.validate_on_submit():
            try:
                mydoc = mycol.find_one({"email": email})
                if mydoc is not None:
                    uuid_obj = uuid.uuid4()
                    mydoc['introduction'].append({ "id_introduction": str(uuid_obj), "intro_ctx": form.intro_ctx.data, "intro_txt": form.intro_txt.data })
                    mycol.replace_one({ "email": email }, mydoc, upsert=True)
                    flash('Introduction added')
                    return redirect(url_for('profile', email=email))
            except Exception as e:
                flash('An error occurred: ' + str(e))
        return render_template('profile-intro-add.html', form = form)

    @app.route('/profile-editIntro/<int:id_intro>', methods=['GET', 'POST'])
    def profile_editIntro(id_intro):
        email = session['email']
        mydoc = mycol.find_one({"email": email})
        form = IntroForm()
        if mydoc is not None:
            form = IntroForm(intro_ctx = mydoc['introduction'][id_intro]['intro_ctx'], intro_txt = mydoc['introduction'][id_intro]['intro_txt'])
            if form.validate_on_submit():
                try:
                    mydoc['introduction'][id_intro]['intro_ctx'] = form.intro_ctx.data
                    mydoc['introduction'][id_intro]['intro_txt'] = form.intro_txt.data
                    mycol.replace_one({ "email": email }, mydoc, upsert=True)
                    flash('Introduction edited')
                    return redirect(url_for('profile', email=email))
                except Exception as e:
                    flash('An error occurred: ' + str(e))
        return render_template('profile-intro-edit.html', form = form)

    @app.route('/profile-deleteIntro', methods=['POST'])
    def profile_deleteIntro():
        email = request.form['email']
        mydoc = mycol.find_one({"email": email})
        id_intro = int(request.form['id_intro'])
        if mydoc is not None:
            mydoc['introduction'].remove(mydoc['introduction'][id_intro])
            mycol.replace_one({ "email": email }, mydoc, upsert=True)
            flash('Introduction deleted')
        return redirect(url_for('profile', email=email))

    @app.route('/profile-addTechno/<email>', methods=['GET', 'POST'])
    def profile_addTechno(email):
        form = OtherSkillsForm()
        if form.validate_on_submit():
            try:
                mydoc = mycol.find_one({"email": email})
                if mydoc is not None:
                    uuid_obj = uuid.uuid4()
                    mydoc['other_skills'].append({
                        "id_other_skills": str(uuid_obj),
                        "skill": form.skill.data,
                        "duration": str(form.duration.data) })
                    mycol.replace_one({ "email": email }, mydoc, upsert=True)
                    flash('Technology added')
                    return redirect(url_for('profile', email=email))
            except Exception as e:
                flash('An error occurred: ' + str(e))
        return render_template('profile-techno-add.html', form = form)

    @app.route('/profile-editTechno/<int:id_Techno>', methods=['GET', 'POST'])
    def profile_editTechno(id_Techno):
        email = session['email']
        mydoc = mycol.find_one({"email": email})
        form = OtherSkillsForm()
        if mydoc is not None:
            form = OtherSkillsForm(skill = mydoc['other_skills'][id_Techno]['skill'],
                duration = mydoc['other_skills'][id_Techno]['duration'])
            if form.validate_on_submit():
                try:
                    mydoc['other_skills'][id_Techno]['skill'] = form.skill.data
                    mydoc['other_skills'][id_Techno]['duration'] = str(form.duration.data)
                    mycol.replace_one({ "email": email }, mydoc, upsert=True)
                    flash('Technology edited')
                    return redirect(url_for('profile', email=email))
                except Exception as e:
                    flash('An error occurred: ' + str(e))
        return render_template('profile-techno-edit.html', form = form)

    @app.route('/profile-deleteTechno', methods=['POST'])
    def profile_deleteTechno():
        email = request.form['email']
        mydoc = mycol.find_one({"email": email})
        id_techno = int(request.form['id_techno'])
        if mydoc is not None:
            mydoc['other_skills'].remove(mydoc['other_skills'][id_techno])
            mycol.replace_one({ "email": email }, mydoc, upsert=True)
            flash('Technology deleted')
        return redirect(url_for('profile', email=email))

    @app.route('/profile-addStudy/<email>', methods=['GET', 'POST'])
    def profile_addStudy(email):
        form = StudiesForm()
        if form.validate_on_submit():
            try:
                mydoc = mycol.find_one({"email": email})
                if mydoc is not None:
                    uuid_obj = uuid.uuid4()
                    mydoc['studies'].append({
                        "id_study": str(uuid_obj),
                        "school_name": form.school_name.data,
                        "degree": form.degree.data,
                        "course": form.course.data,
                        "end_date": str(form.end_date.data) })
                    mycol.replace_one({ "email": email }, mydoc, upsert=True)
                    flash('Education added')
                    return redirect(url_for('profile', email=email))
            except Exception as e:
                flash('An error occurred: ' + str(e))
        return render_template('profile-study-add.html', form = form)

    @app.route('/profile-editStudy/<int:id_study>', methods=['GET', 'POST'])
    def profile_editStudy(id_study):
        email = session['email']
        mydoc = mycol.find_one({"email": email})
        form = StudiesForm()
        if mydoc is not None:
            form = StudiesForm(school_name = mydoc['studies'][id_study]['school_name'],
                degree = mydoc['studies'][id_study]['degree'],
                course = mydoc['studies'][id_study]['course'],
                end_date = datetime.datetime.strptime(mydoc['studies'][id_study]['end_date'], '%Y-%m-%d'))
            if form.validate_on_submit():
                try:
                    mydoc['studies'][id_study]['school_name'] = form.school_name.data
                    mydoc['studies'][id_study]['degree'] = form.degree.data
                    mydoc['studies'][id_study]['course'] = form.course.data
                    mydoc['studies'][id_study]['end_date'] = str(form.end_date.data)
                    mycol.replace_one({ "email": email }, mydoc, upsert=True)
                    flash('Introduction edited')
                    return redirect(url_for('profile', email=email))
                except Exception as e:
                    flash('An error occurred: ' + str(e))
        return render_template('profile-study-edit.html', form = form)

    @app.route('/profile-deleteStudy', methods=['POST'])
    def profile_deleteStudy():
      email = request.form['email']
      mydoc = mycol.find_one({"email": email})
      id_study = int(request.form['id_study'])
      if mydoc is not None:
          mydoc['studies'].remove(mydoc['studies'][id_study])
          mycol.replace_one({ "email": email }, mydoc, upsert=True)
          flash('Education deleted')
      return redirect(url_for('profile', email=email))

    @app.route('/profile-addMandate/<email>', methods=['GET', 'POST'])
    def profile_addMandate(email):
        form = MandateForm()
        if form.validate_on_submit():
            try:
                mydoc = mycol.find_one({"email": email})
                if mydoc is not None:
                    uuid_obj = uuid.uuid4()
                    mydoc['mandates'].append({
                        "id_mandate": str(uuid_obj),
                        "project_name": form.project_name.data,
                        "client_name": form.client_name.data,
                        "function": form.function.data,
                        "start_date": str(form.start_date.data),
                        "end_date": str(form.end_date.data),
                        "size": str(form.size.data),
                        "effort": str(form.effort.data),
                        "resume": form.resume.data,
                        "responsibilities": get_dict_from_string_array(form.responsibilities.data, 'responsibility'),
                        "org_context": form.org_context.data,
                        "project_context": form.project_context.data,
                        "technologies": get_dict_from_string_array(form.technologies.data, 'technology'),
                        "tools": get_dict_from_string_array(form.tools.data, 'tool'),
                        "ref_name": form.ref_name.data,
                        "ref_contact": form.ref_contact.data,
                        "methodologies": get_dict_from_string_array(form.methodologies.data, 'methodology')
                    })
                    mycol.replace_one({ "email": email }, mydoc, upsert=True)
                    flash('Experience added')
                    return redirect(url_for('profile', email=email))
            except Exception as e:
                flash('An error occurred: ' + str(e))
        return render_template('profile-mandate-add.html', form = form)

    @app.route('/profile-editMandate/<int:id_mandate>', methods=['GET', 'POST'])
    def profile_editMandate(id_mandate):
        email = session['email']
        mydoc = mycol.find_one({"email": email})
        form = MandateForm()
        if mydoc is not None:
            mandate = mydoc['mandates'][id_mandate]
            responsibilities = [item['responsibility'] for item in mandate['responsibilities']]
            tools = [item['tool'] for item in mandate['tools']]
            methotodologies = [item['methodology'] for item in mandate['methodologies']]
            technologies = [item['technology'] for item in mandate['technologies']]
            form = MandateForm(
                project_name=mandate['project_name'],
                client_name=mandate['client_name'],
                function=mandate['function'],
                start_date=datetime.datetime.strptime(mandate['start_date'], '%Y-%m-%d'),
                end_date=datetime.datetime.strptime(mandate['end_date'], '%Y-%m-%d'),
                size=mandate['size'],
                effort=mandate['effort'],
                resume=mandate['resume'],
                responsibilities=', '.join(responsibilities),
                org_context=mandate['org_context'],
                project_context=mandate['project_context'],
                technologies=', '.join(technologies),
                tools=', '.join(tools),
                ref_name=mandate['ref_name'],
                ref_contact=mandate['ref_contact'],
                methodologies=', '.join(methotodologies)
            )
            if form.validate_on_submit():
                try:
                    print(form.responsibilities.data)
                    mandate['project_name'] = form.project_name.data
                    mandate['client_name'] = form.client_name.data
                    mandate['function'] = form.function.data
                    mandate['start_date'] = str(form.start_date.data)
                    mandate['end_date'] = str(form.end_date.data)
                    mandate['size'] = str(form.size.data)
                    mandate['effort'] = str(form.effort.data)
                    mandate['resume'] = form.resume.data
                    mandate['responsibilities'] = get_dict_from_string_array(form.responsibilities.data, 'responsibility')
                    mandate['org_context'] = form.org_context.data
                    mandate['project_context'] = form.project_context.data
                    mandate['technologies'] = get_dict_from_string_array(form.technologies.data, 'technology')
                    mandate['tools'] = get_dict_from_string_array(form.tools.data, 'tool')
                    mandate['ref_name'] = form.ref_name.data
                    mandate['ref_contact'] = form.ref_contact.data
                    mandate['methodologies'] = get_dict_from_string_array(form.methodologies.data, 'methodology')
                    mycol.replace_one({"email": email}, mydoc, upsert=True)
                    flash('Experience edited')
                    return redirect(url_for('profile', email=email))
                except Exception as e:
                    flash('An error occurred: ' + str(e))
        return render_template('profile-mandate-edit.html', form=form)

    @app.route('/profile-deleteMandate', methods=['POST'])
    def profile_deleteMandate():
        email = request.form['email']
        mydoc = mycol.find_one({"email": email})
        id_mandate = int(request.form['id_mandate'])
        if mydoc is not None:
            mydoc['mandates'].remove(mydoc['mandates'][id_mandate])
            mycol.replace_one({ "email": email }, mydoc, upsert=True)
            flash('Experience deleted')
        return redirect(url_for('profile', email=email))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
