import json
import pymongo
import uuid
from flask import Flask, render_template, request, session, jsonify, flash, redirect, url_for
from bson import json_util
from forms import IntroForm

def create_app():
    app = Flask(__name__)
    app.secret_key = 'mysecretkey'

    myclient = pymongo.MongoClient("mongodb://192.168.1.128:27017/")
    mydb = myclient["cv-manager"]
    mycol = mydb["entries"]

    myquery = { "manager": "manuel.legault@alithya.com" }

    @app.route('/')
    def index():
        mydoc = mycol.find(myquery)
        return render_template('my-team.html', mydoc=mydoc)

    @app.route('/profile/<email>')
    def profile(email):
        mydoc = mycol.find_one({"email": email})
        session['mydoc'] = json.loads(json_util.dumps(mydoc))
        session['email'] = email
        return render_template('profile.html', session=session)

    @app.route('/profile-addIntro/<email>', methods=['GET', 'POST'])
    def profile_addIntro(email):
        form = IntroForm()
        if form.validate_on_submit():
            try:
                mydoc = mycol.find_one({"email": email})
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
        mydoc['introduction'].remove(mydoc['introduction'][id_intro])
        mycol.replace_one({ "email": email }, mydoc, upsert=True)
        flash('Introduction deleted')
        return redirect(url_for('profile', email=email))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    
    