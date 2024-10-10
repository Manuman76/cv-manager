import json
import pymongo
from flask import Flask, render_template, request, session
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

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    
    