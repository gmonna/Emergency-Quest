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
  return Response(status=200)
  
@app.route('/rest_api/v1.0/lost_password', methods=['GET'])
def retrieve_pass():
  mail = request.args.get('mail')
  bcod = db_app_interaction.code_bymail(mail)
  if bcode is None:
    abort(404)
    
  db_app_interaction.lost_password(mail)
  return Response(status=200)
  
@app.route('/rest_api/v1.0/get_settings', methods=['GET'])
def load_settings():
  mail = session['mail']
  
  set_list = db_app_interaction.get_settings(mail)
  
  return jsonify({'settings':prepare_for_json_set(set_list)})
  
@app.route('/rest_api/v1.0/set_settings', methods=['POST'])
def settings():
  setting_req = request.json
  
  if (setting_req is not None) and ('perimeter' and 'colour' and 'song' and 'doct' and 'message' and 'auto_clean' and 'first') in setting_req:
    
    mail = session['mail']
    perimeter = setting_req['perimeter']
    colour = setting_req['colour']
    song = setting_req['song']
    doct = setting_req['doct']
    message = setting_req['message']
    auto_clean = setting_req['auto_clean']
    first = setting_req['first']
    
    db_app_interaction.set_settings(mail, perimeter, colour, song, doct, message, auto_clean, first)
    return Response(status=200)
  
  abort(403)

@app.route('/rest_api/v1.0/get_history', methods=['GET'])
def load_settings():
  mail = session['mail']
  
  history = []
  notif = db_app_interaction.get_history(mail)
  for item in notif:
    his = prepare_for_json_tot(item)
    history.append(his)
  
  return jsonify({'history':history})
  
@app.route('/rest_api/v1.0/get_calendar', methods=['GET'])
def load_calendar():
  mail = session['mail']
  
  calendar = []
  cal = db_app_interaction.get_calendar(mail)
  for item in cal:
    cl = prepare_for_json_tot(item)
    calendar.append(cl)
  
  return jsonify({'calendar':calendar})
  
@app.route('/rest_api/v1.0/calendar/<int:code>', methods=['DELETE'])
def delete_appointment(code):
  mail = session['mail']
  
  db_app_interaction.delete_appointment(mail, int(code))
  return Response(status=200)
  
@app.route('/rest_api/v1.0/calendar/<int:code>', methods=['PUT'])
def delete_appointment(code):
  mail = session['mail']
  update_req = request.json
  #--
  db_app_interaction.update_appointment(mail, int(code), data, ora, message)
  return Response(status=200)
  
def prepare_for_json_set(item):
  settings = dict()
  settings['perimeter'] = item[0]
  settings['colour'] = item[1]
  settings['song'] = item[2]
  settings['doct'] = item[3]
  settings['message'] = item[4]
  settings['auto_clean'] = item[5]
  
  return settings

def prepare_for_json_tot(item)
  tot = dict()
  tot['code'] = item[0]
  tot['data'] = item[1]
  tot['ora'] = item[2]
  tot['message'] = item[3]
  
  return tot
