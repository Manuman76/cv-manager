import os
import pymongo

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'

    myclient = pymongo.MongoClient("mongodb://192.168.1.128:27017/")
    mydb = myclient["cv-manager"]
    mycol = mydb["entries"]
    myquery = { "manager": "manuel.legault@alithya.com" }

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
