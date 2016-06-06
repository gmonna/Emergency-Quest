#!/usr/bin/python

"""
Created on May 30, 2016
@author: gmonna
"""

from flask import Flask, jsonify, abort, request, Response
import db_app_interaction

app = Flask(__name__)

#----------- REST APIs FOR APP ----------#
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

@app.route('/rest_api/v1.0/already_signin', methods=['GET'])
def al_log_in():
  if(session['mail']):
    return Response(status=200)
  
@app.route('/rest_api/v1.0/logout', methods=['GET'])
def log_out():
  del session['mail']
  del session['name']
  del session['surname']
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
  
  return jsonify({'settings':prepare_for_json(set_list)})
  
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
def load_history():
  mail = session['mail']
  
  history = []
  notif = db_app_interaction.get_history(mail)
  for item in notif:
    his = prepare_for_json(item)
    history.append(his)
  
  db_app_interaction.history_all_read(mail)
  return jsonify({'history':history})
  
@app.route('/rest_api/v1.0/get_calendar', methods=['GET'])
def load_calendar():
  mail = session['mail']
  
  calendar = []
  cal = db_app_interaction.get_calendar(mail)
  for item in cal:
    cl = prepare_for_json(item)
    calendar.append(cl)
  
  return jsonify({'calendar':calendar})

@app.route('/rest_api/v1.0/calendar/insert', methods=['POST'])
def insert_appointment():
  req = request.json
  
  if (req is not None) and ('title' and 'description' and 'data' and 'ora' and 'message' and 'priority' and 'repeat') in req:
    
    mail = session['mail']
    titolo = req['title']
    data = req['data']
    ora = req['ora']
    message = req['message']
    description = req['description']
    priority = req['priority']
    repeat = req['repeat']
    
    db_app_interaction.set_appointment(mail, description, titolo, data, ora, message, priority, repeat)
    return Response(status=200)
  
  abort(403)

@app.route('/rest_api/v1.0/calendar/<int:code>', methods=['GET'])
def view_appointment(int(code)):
  mail = session['mail']
  
  appo = db_app_interaction.select_appointment(mail, int(code))
  appointment = prepare_for_json(appo)
  return jsonify({'appointment':appointment})
  
@app.route('/rest_api/v1.0/calendar/<int:code>', methods=['DELETE'])
def delete_appointment(int(code)):
  mail = session['mail']
  
  db_app_interaction.delete_appointment(mail, int(code))
  return Response(status=200)
  
@app.route('/rest_api/v1.0/calendar/<int:code>', methods=['PUT'])
def update_appointment(int(code)):
  mail = session['mail']
  update_req = request.json
  
  if update_req is not None and ('code' and 'title' and 'description' and 'data' and 'ora' and 'message' and 'priority' and 'repeat') in update_req:
    code = update_req['code']
    titolo = update_req['title']
    data = update_req['data']
    ora = update_req['ora']
    message = update_req['message']
    description = update_req['description']
    priority = update_req['priority']
    repeat = update_req['repeat']
    
    db_app_interaction.update_appo(mail, int(code), titolo, description, data, ora, message, priority, repeat)
    return Response(status=200)
  
  abort(403)
  
@app.route('/rest_api/v1.0/get_position', methods=['GET']) #--TODO--#
def get_position():
  return None

def prepare_for_json(item):
  tot = dict()

  if (len(item)==4):
    tot['read'] = item[0]
    tot['data'] = item[1]
    tot['ora'] = item[2]
    tot['message'] = item[3]
  if (len(item)==5):
    tot['done'] = item[0]
    tot['titolo'] = item[1]
    tot['data'] = item[2]
    tot['ora'] = item[3]
    tot['code'] = item[4]
  if (len(item)==6):
    tot['perimeter'] = item[0]
    tot['colour'] = item[1]
    tot['song'] = item[2]
    tot['doct'] = item[3]
    tot['message'] = item[4]
    tot['auto_clean'] = item[5]
  if (len(item)==7):
    tot['title'] = item[0]
    tot['description'] = item[1]
    tot['data'] = item[2]
    tot['ora'] = item[3]
    tot['message'] = item[4]
    tot['priority'] = item[5]
    tot['repeat'] = item[6]
  
  return tot
#------ APIs END ------#