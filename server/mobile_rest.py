#!/usr/bin/python

"""
Created on May 30, 2016
@author: gmonna
"""

from flask import Flask, jsonify, abort, request, Response
import db_app_interaction

app = Flask(__name__)

#----------- REST SERVER ----------#
@app.route('/rest_api/v1.0/signup', methods=['POST'])
def new_user():
  insert_request = request.json
  
  if (insert_request is not None) and ('name' and 'surname' and 'mail' and 'password' and 'bcod') in insert_request:
    bcod = insert_request['bcod']
    bc = db_app_interaction.get_code(bcod)
    if bc is None:
      abort(404)
      
    mail = insert_request['mail']
    password = insert_request['password']
    name = insert_request['name']
    surname = insert_request['surname']
    
    db_app_interaction.sign_up(bcod, mail, password, name, surname)
    return Response(status=200)
  
  abort(403)
  
@app.route('/rest_api/v1.0/signin', methods=['GET'])
def log_in():
  mail = request.args.get('mail')
  bcod = db_app_interaction.code_bymail(mail)
  if bcode is None:
    abort(404)
    
  password = request.args.get('password')
  user = db_app_interaction.sign_in(mail, password)
  session['mail'] = mail
  session['name'] = user['name']
  session['surname'] = user['surname']
  
@app.route('/rest_api/v1.0/get_settings', methods=['GET'])
def load_settings():
  mail = session['mail']
  
  set_list = db_app_interaction.get_settings(mail)
  settings = prepare_for_json_set(set_list)
  
  return jsonify({settings})
  
def prepare_for_json_set(item):
  settings = dict()
  settings['perimeter'] = item[0]
  settings['colour'] = item[1]
  settings['song'] = item[2]
  settings['doct'] = item[3]
  settings['message'] = item[4]
  settings['auto_clean'] = item[5]
  
  return settings
