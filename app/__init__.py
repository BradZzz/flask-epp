from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = False

from app import views