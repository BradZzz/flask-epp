from app import app
from flask import request, Response
from conn_nic import ConnNic
import json
from time import sleep

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

def testy(domain, action):
  n = 10
  while n > 0:
    yield "data: hi\n\n"
    sleep(0.5)
    n = n - 1

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

@app.route('/test', methods=['POST'])
def test():
  return Response(
    testy(request.form, 'create'),
    mimetype="text/event-stream"
  )

def handleEPPActions(form, action):
  if request.headers['Content-Type'] == 'application/json':
    form = json.loads(json.dumps(request.json))
  if not ('domain' in form):
    return "No domain in form"
  nic = ConnNic(form['domain'], action)
  return Response(nic.perform(), mimetype='text/plain')