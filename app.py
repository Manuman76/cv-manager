import json

import bson
import pymongo
import uuid
from flask import Flask, render_template, request, session, jsonify
from bson import json_util

def create_app():
    app = Flask(__name__)
    app.secret_key = 'mysecretkey'

    myclient = pymongo.MongoClient("mongodb://192.168.1.128:32768/")
    mydb = myclient["cv-manager"]
    mycol = mydb["employees"]

    myquery = { "manager": "manuel.legault@alithya.com" }

    @app.route('/')
    def index():
        mydoc = mycol.find(myquery)
        return render_template('my-team.html', mydoc=mydoc)

    @app.route('/profile/<email>')
    def profile(email):
        mydoc = mycol.find_one({"email": email})
        session['mydoc'] = json.loads(json_util.dumps(mydoc))
        return render_template('profile.html', session=session)

    @app.route('/profile-addIntro/<email>', methods=['GET', 'POST'])
    def profile_addIntro(email):
        if request.method == 'GET':
            return render_template('profile-addIntro.html')
        if request.method == 'POST':
            mydoc = mycol.find_one({"email": email})
            intro_ctx = request.form['intro_ctx']
            intro_txt = request.form['intro_txt']
            uuid_obj = uuid.uuid4()
            mydoc['introduction'].append({ " id_introduction": uuid_obj.hex, "intro_ctx": intro_ctx, "intro_txt": intro_txt })
            session['mydoc'] = json.loads(json_util.dumps(mydoc))
            mycol.replace_one({ "email": email }, mydoc, upsert=True)

        return render_template('profile.html', session=session)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    
    