from flask import render_template, request, redirect, url_for, session, send_file, flash
from docxtpl import DocxTemplate
from app import app, forms, utils
from config import Config
import jinja2
import uuid
import datetime

@app.route('/profile-addMandate/<email>', methods=['GET', 'POST'])
def profile_addMandate(email):
    form = forms.MandateForm()
    if form.validate_on_submit():
        try:
            mydoc = Config.mycol.find_one({"email": email})
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
                    "responsibilities": utils.get_dict_from_string_array(form.responsibilities.data, 'responsibility'),
                    "org_context": form.org_context.data,
                    "project_context": form.project_context.data,
                    "technologies": utils.get_dict_from_string_array(form.technologies.data, 'technology'),
                    "tools": utils.get_dict_from_string_array(form.tools.data, 'tool'),
                    "ref_name": form.ref_name.data,
                    "ref_contact": form.ref_contact.data,
                    "methodologies": utils.get_dict_from_string_array(form.methodologies.data, 'methodology')
                })
                Config.mycol.replace_one({ "email": email }, mydoc, upsert=True)
                flash('Experience added')
                return redirect(url_for('profile', email=email))
        except Exception as e:
            flash('An error occurred: ' + str(e))
    return render_template('profile-mandate-add.html', form = form)

@app.route('/profile-editMandate/<int:id_mandate>', methods=['GET', 'POST'])
def profile_editMandate(id_mandate):
    email = session['email']
    mydoc = Config.mycol.find_one({"email": email})
    form = forms.MandateForm()
    if mydoc is not None:
        mandate = mydoc['mandates'][id_mandate]
        responsibilities = [item['responsibility'] for item in mandate['responsibilities']]
        tools = [item['tool'] for item in mandate['tools']]
        methotodologies = [item['methodology'] for item in mandate['methodologies']]
        technologies = [item['technology'] for item in mandate['technologies']]
        form = forms.MandateForm(
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
                mandate['responsibilities'] = utils.get_dict_from_string_array(form.responsibilities.data, 'responsibility')
                mandate['org_context'] = form.org_context.data
                mandate['project_context'] = form.project_context.data
                mandate['technologies'] = utils.get_dict_from_string_array(form.technologies.data, 'technology')
                mandate['tools'] = utils.get_dict_from_string_array(form.tools.data, 'tool')
                mandate['ref_name'] = form.ref_name.data
                mandate['ref_contact'] = form.ref_contact.data
                mandate['methodologies'] = utils.get_dict_from_string_array(form.methodologies.data, 'methodology')
                Config.mycol.replace_one({"email": email}, mydoc, upsert=True)
                flash('Experience edited')
                return redirect(url_for('profile', email=email))
            except Exception as e:
                flash('An error occurred: ' + str(e))
    return render_template('profile-mandate-edit.html', form=form)

@app.route('/profile-deleteMandate', methods=['POST'])
def profile_deleteMandate():
    email = request.form['email']
    mydoc = Config.mycol.find_one({"email": email})
    id_mandate = int(request.form['id_mandate'])
    if mydoc is not None:
        mydoc['mandates'].remove(mydoc['mandates'][id_mandate])
        Config.mycol.replace_one({ "email": email }, mydoc, upsert=True)
        flash('Experience deleted')
    return redirect(url_for('profile', email=email))
