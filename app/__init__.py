from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import utils, routes, routes_intro, routes_techno, routes_study, routes_mandate
