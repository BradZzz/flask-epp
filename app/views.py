from app import app
from flask import request
from conn_nic import ConnNic

@app.route('/')
@app.route('/index')
def index():
  return "Hello, World!"

@app.route('/backorder', methods=['POST'])
def backorder():
  return handleEPPActions(request.form, 'backorder')

@app.route('/create', methods=['POST'])
def create():
  return handleEPPActions(request.form, 'create')

def handleEPPActions(form, action):
  if not ('domain' in form):
    return "No domain in form"
  nic = ConnNic(form["domain"], action)
  return "request submitted!"