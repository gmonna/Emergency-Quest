#!/usr/bin/python

"""
Created on May 30, 2016
@author: gmonna
"""

from flask import Flask, jsonify, abort, session, Response, make_response, request, current_app
from datetime import timedelta
from functools import update_wrapper
import db_app_interaction, os

app = Flask(__name__)

app.secret_key = 'F12Zr47jyXRX@H!jmM]Lwf?KT'

#----grant access control-----#
def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

#----------- REST APIs FOR APP ----------#
@app.route('/rest_api/v1.0/signup', methods=['POST'])
@crossdomain(origin='*')
def new_user():
    insert_request = request.json

    if (insert_request is not None) and ('name' and 'surname' and 'mail' and 'password' and 'bcod') in insert_request:
      bcod = insert_request['bcod']
      bc = db_app_interaction.get_code(bcod)
      if bc is None:
        abort(404)

      mail = insert_request['mail']
      em = db_app_interaction.code_byemail(mail)
      if em is not None:
        abort(302) #--already existing user--#
      password = insert_request['password']
      name = insert_request['name']
      surname = insert_request['surname']

      db_app_interaction.sign_up(bcod, mail, password, name, surname)
      return Response(status=200)

    abort(403)

@app.route('/rest_api/v1.0/signin', methods=['GET'])
@crossdomain(origin='*')
def log_in():
    mail = request.args.get('mail')
    bcod = db_app_interaction.code_byemail(mail)
    if bcod is None:
      abort(404)

    password = request.args.get('password')
    user = db_app_interaction.sign_in(mail, password)
    session['mail'] = mail
    session['name'] = user['name']
    session['surname'] = user['surname']

    return Response(status=200)

@app.route('/rest_api/v1.0/already_signin', methods=['GET'])
@crossdomain(origin='*')
def al_log_in():
    if 'mail' in session:
        return Response(status=200)
    else:
        return Response(status=205)

@app.route('/rest_api/v1.0/logout', methods=['GET'])
@crossdomain(origin='*')
def log_out():
    del session['mail']
    del session['name']
    del session['surname']
    return Response(status=200)

@app.route('/rest_api/v1.0/lost_password', methods=['GET'])
@crossdomain(origin='*')
def retrieve_pass():
    mail = request.args.get('mail')
    bcod = db_app_interaction.code_byemail(mail)
    if bcod is None:
      abort(404)

    db_app_interaction.lost_password(mail)
    return Response(status=200)

@app.route('/rest_api/v1.0/get_settings', methods=['GET'])
@crossdomain(origin='*')
def load_settings():
    mail = session['mail']

    set_list = db_app_interaction.get_settings(mail)
    if set_list == -1:
        return Response(status=205)

    return jsonify({'settings':prepare_for_json(set_list)})

@app.route('/rest_api/v1.0/set_settings', methods=['POST'])
@crossdomain(origin='*')
def settings():
    setting_req = request.json

    if (setting_req is not None) and ('perimeter' and 'colour' and 'song' and 'doct' and 'message' and 'auto_clean' and 'first') in setting_req:

      mail = session['mail']
      perimeter = setting_req['perimeter']
      colour = setting_req['colour']
      song = setting_req['song']
      if song == 'relax':
          song = os.getcwd()+'/songs/relax.mp3'
      elif song == 'concentrate':
          song = os.getcwd() + '/songs/concentrate.mp3'
      else:
          song = os.getcwd() + '/songs/remind.mp3'
      doct = setting_req['doct']
      message = setting_req['message']
      auto_clean = setting_req['auto_clean']
      first = setting_req['first']

      db_app_interaction.set_settings(mail, perimeter, colour, song, doct, message, auto_clean, first)
      return Response(status=200)

    abort(403)

@app.route('/rest_api/v1.0/get_numbers', methods=['GET'])
@crossdomain(origin='*')
def load_numbers():
    mail = session['mail']

    numbers = db_app_interaction.get_numbers(mail)
    if numbers == -1:
        return Response(status=205)

    return jsonify({'numbers':prepare_for_json(numbers)})

@app.route('/rest_api/v1.0/get_history', methods=['GET'])
@crossdomain(origin='*')
def load_history():
    mail = session['mail']

    history = []
    notif = db_app_interaction.get_history(mail)
    for item in notif:
      his = prepare_for_json(item)
      history.append(his)

    if history == -1:
        return Response(status=205)

    db_app_interaction.history_all_read(mail)
    return jsonify({'history':history})

@app.route('/rest_api/v1.0/get_calendar', methods=['GET'])
@crossdomain(origin='*')
def load_calendar():
    mail = session['mail']

    calendar = []
    cal = db_app_interaction.get_calendar(mail)
    for item in cal:
      cl = prepare_for_json(item)
      calendar.append(cl)

    if calendar == -1:
      return Response(status=205)

    return jsonify({'calendar':calendar})

@app.route('/rest_api/v1.0/calendar/insert', methods=['POST'])
@crossdomain(origin='*')
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
@crossdomain(origin='*')
def view_appointment(code):
    mail = session['mail']

    appo = db_app_interaction.select_appointment(mail, int(code))
    appointment = prepare_for_json(appo)
    return jsonify({'appointment':appointment})

@app.route('/rest_api/v1.0/calendar/<int:code>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_appointment(code):
    mail = session['mail']

    db_app_interaction.delete_appointment(mail, int(code))
    return Response(status=200)

@app.route('/rest_api/v1.0/calendar/<int:code>', methods=['PUT'])
@crossdomain(origin='*')
def update_appointment(code):
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

@app.route('/rest_api/v1.0/get_position', methods=['GET'])
@crossdomain(origin='*') #--TODO--#
def get_position():
    return jsonify({'position':{'latitude':'45.0853512', 'longitude':'7.6709614'}})

def prepare_for_json(item):
    tot = dict()

    if len(item)==2:
      tot['calendar'] = item[0]
      tot['history'] = item[1]
    if len(item)==4:
      tot['read'] = item[0]
      tot['data'] = item[1]
      tot['ora'] = item[2]
      tot['message'] = item[3]
    if len(item)==5:
      tot['done'] = item[0]
      tot['titolo'] = item[1]
      tot['data'] = item[2]
      tot['ora'] = item[3]
      tot['code'] = item[4]
    if len(item)==6:
      tot['perimeter'] = item[0]
      tot['colour'] = item[1]
      tot['song'] = item[2]
      tot['doct'] = item[3]
      tot['message'] = item[4]
      tot['auto_clean'] = item[5]
    if len(item)==7:
      tot['title'] = item[0]
      tot['description'] = item[1]
      tot['data'] = item[2]
      tot['ora'] = item[3]
      tot['message'] = item[4]
      tot['priority'] = item[5]
      tot['repeat'] = item[6]

    return tot

#------ APIs END ------#

if __name__ == '__main__':
    app.run(debug=True)