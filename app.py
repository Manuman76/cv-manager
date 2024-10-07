from flask import Flask, render_template, request
import pymongo

def create_app():
    app = Flask(__name__)

    myclient = pymongo.MongoClient("mongodb://192.168.1.128:32768/")
    mydb = myclient["cv-manager"]
    mycol = mydb["employees"]

    myquery = { "manager": "manuel.legault@alithya.com" }

    @app.route('/')
    def index():
        mydoc = mycol.find(myquery)
        return render_template('my-team.html', mydoc=mydoc)

    @app.route('/profile')
    def profile():
        return render_template('profile.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)