from app import app
from flask import request, Response
from conn_nic import ConnNic
import json
# from flask_restful import Resource, Api, reqparse

# api = Api(app)
#
# def after_this_request(f):
#   if not hasattr(g, 'after_request_callbacks'):
#     g.after_request_callbacks = []
#   g.after_request_callbacks.append(f)
#   return f
#
# @app.after_request
# def call_after_request_callbacks(response):
#   for callback in getattr(g, 'after_request_callbacks', ()):
#     callback(response)
#   return response
#
# class HelloWorld(Resource):
#   def get(self):
#     return {'hello': 'world'}
#
# class Backorder(Resource):
#   def post(self):
#     return handleEPPActions(request.form, 'backorder')
#
# class Create(Resource):
#   def post(self):
#     return handleEPPActions(request.form, 'create')
#
# api.add_resource(HelloWorld, '/', '/index')
# api.add_resource(Backorder, '/backorder')
# api.add_resource(Create, '/create')
#
#
#


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
  print form
  if request.headers['Content-Type'] == 'application/json':
    form = json.dumps(request.json)
  print form
  if not ('domain' in form):
    return "No domain in form"
  nic = ConnNic(form["domain"], action)
  return Response(nic.perform(), mimetype='text/plain')