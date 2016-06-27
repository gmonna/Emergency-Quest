#!/usr/bin/env python

"""
Created on May 30, 2016
@author: gmonna

Main server running on public IP address to be accessible from all mobile apps and all room stations
"""

from flask import Flask, jsonify, abort, session, Response, make_response, request, current_app
from datetime import timedelta
from functools import update_wrapper
from gcm import *
from apns import APNs, Payload
from apscheduler.schedulers.background import BackgroundScheduler
import db_app_interaction, time, smtplib

app = Flask(__name__)
gcm = GCM("AIzaSyBLfB5vNmQ2LbiEtxNNKwiid4GaB66Onkg")
apns = APNs(use_sandbox=True, cert_file='cers/aps_prod_cert.pem', key_file='cers/aps_prod_key.pem', enhanced=True)

app.secret_key = 'F12Zr47jyXRX@H!jmM]Lwf?KT'

#---cron job to do auto_cleaning every day---#

@app.before_first_request
def initialize():
    sched = BackgroundScheduler()

    @sched.scheduled_job('cron', day_of_week='mon')
    def auto_clean():
        try:
            db_app_interaction.delete_history_doneappo()
        except Exception, e:
            print "Impossible to do auto_clean cron job"

    sched.start()

#---grant access control from everywhere---#

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

#--- function to prepare objects to be sent with json coding ---#

def prepare_for_json(item):
    tot = dict()

    if len(item)==2:
      tot['calendar'] = item[0]
      tot['history'] = item[1]
    if len(item)==3:
        tot['code'] = item[0]
        tot['message'] = item[1]
        tot['ora'] = item[2]
    if len(item)==4:
      tot['read'] = item[0]
      tot['data'] = item[1]
      tot['ora'] = item[2]
      tot['message'] = item[3]
    if len(item)==5:
      tot['code'] = item[0]
      tot['title'] = item[1]
      tot['done'] = item[2]
      tot['data'] = item[3]
      tot['ora'] = item[4]
    if len(item)==6:
      tot['title'] = item[0]
      tot['description'] = item[1]
      tot['data'] = item[2]
      tot['ora'] = item[3]
      tot['message'] = item[4]
      tot['priority'] = item[5]
    if len(item)==8:
      tot['perimeter'] = item[0]
      tot['colour'] = item[1]
      tot['song'] = item[2]
      tot['doct'] = item[3]
      tot['message'] = item[4]
      tot['auto_clean'] = item[5]
      tot['doc_access'] = item[6]
      tot['address'] = item[7]

    return tot

#--- send notification email ---#

def send_email(email, message):
    sender = 'info@emergencyquest.com'
    receivers = [email]

    content = """From: From EmergencyQuest Team <info@emergencyquest.com>
    Subject: New notification

    You have a new unread notification in your patient history! This is the message: '""" + message + """'
    Hope it is not an extreme condition.

    Best regards"""

    try:
        smtpObj = smtplib.SMTP('smtp.googlemail.com')
        smtpObj.sendemail(sender, receivers, content)
        print "Successfully sent email"
    except:
        print "Error: unable to send email"

#----------- REST APIs FOR MOBILE APP ----------#

@app.route('/rest_api/v1.0/signup', methods=['POST'])
@crossdomain(origin='*')
def new_user():
    insert_request = request.json

    if (insert_request is not None) and ('name' and 'surname' and 'email' and 'password' and 'bcod') in insert_request:
      bcod = insert_request.get('bcod')
      bc = db_app_interaction.get_code(bcod)
      if bc is None:
        abort(404)

      email = insert_request.get('email')
      em = db_app_interaction.check_presence(email, bcod)
      if em is not None:
        abort(405) #--already existing user--#
      password = insert_request.get('password')
      name = insert_request.get('name')
      surname = insert_request.get('surname')

      try:
        db_app_interaction.sign_up(bcod, email, password, name, surname)
        return Response(status=200)
      except Exception, e:
        return Response(status=500)

    abort(403)

@app.route('/rest_api/v1.0/signin', methods=['POST'])
@crossdomain(origin='*')
def log_in():
    email = request.json.get('email')
    bcod = db_app_interaction.check_email(email)
    if bcod is None:
      abort(404)

    password = request.json.get('password')
    patient = request.json.get('patient')
    session['patient'] = patient

    try:
        user = db_app_interaction.sign_in(email, password)
        if user is None:
            abort(403)
        session['email'] = email
        session['first'] = 'n'
        deviceid = request.json.get('deviceid')
        anorapp = request.json.get('anorapp')
        try:
            db_app_interaction.insert_token(email, deviceid, anorapp)
        except Exception, e:
            print e
        return Response(status=200)
    except Exception, e:
        return Response(status=500)

@app.route('/rest_api/v1.0/already_signin', methods=['GET'])
@crossdomain(origin='*')
def al_log_in():
    if 'email' in session:
        return Response(status=200)
    else:
        return Response(status=404)

@app.route('/rest_api/v1.0/logout', methods=['GET'])
@crossdomain(origin='*')
def log_out():
    del session['email']
    del session['first']
    del session['patient']
    return Response(status=200)

@app.route('/rest_api/v1.0/lost_password', methods=['POST'])
@crossdomain(origin='*')
def retrieve_pass():
    email = request.json.get('email')
    bcod = db_app_interaction.check_email(email)
    if bcod is None:
      abort(404)

    db_app_interaction.lost_password(email)
    return Response(status=200)

@app.route('/rest_api/v1.0/get_settings', methods=['GET'])
@crossdomain(origin='*')
def load_settings():
    email = session['email']

    set_list = db_app_interaction.get_settings(email)
    if not set_list:
        session['first'] = 'y'
        return Response(status=404)

    return jsonify({'settings':prepare_for_json(set_list)})

@app.route('/rest_api/v1.0/set_settings', methods=['POST'])
@crossdomain(origin='*')
def settings():
    setting_req = request.json

    if (setting_req is not None) and ('perimeter' and 'message' and 'doct' and 'colour' and 'song' and 'auto_clean' and 'doc_access' and 'address') in setting_req:

      email = session['email']
      perimeter = setting_req.get('perimeter')
      colour = setting_req.get('colour')
      song = setting_req.get('song')
      doct = setting_req.get('doct')
      message = setting_req.get('message')
      auto_clean = setting_req.get('auto_clean')
      doc_access = setting_req.get('doc_access')
      address = setting_req.get('address')
      first = session['first']

      try:
        db_app_interaction.set_settings(email, perimeter, colour, song, doct, message, auto_clean, doc_access, address, first)
        session['first'] = 'n'
        return Response(status=200)
      except Exception, e:
        return Response(status=500)

    print setting_req
    abort(403)

@app.route('/rest_api/v1.0/get_numbers', methods=['GET'])
@crossdomain(origin='*')
def load_numbers():
    email = session['email']

    numbers = db_app_interaction.get_numbers(email)
    if not numbers:
        return Response(status=404)

    return jsonify({'numbers':prepare_for_json(numbers), 'patient':session['patient']})

@app.route('/rest_api/v1.0/get_history', methods=['GET'])
@crossdomain(origin='*')
def load_history():
    email = session['email']

    history = []
    notif = db_app_interaction.get_history(email)
    if not notif:
        return Response(status=404)
    for item in notif:
      his = prepare_for_json(item)
      history.append(his)

    db_app_interaction.history_all_read(email)
    return jsonify({'history':history})

@app.route('/rest_api/v1.0/get_calendar', methods=['GET'])
@crossdomain(origin='*')
def load_calendar():
    email = session['email']

    calendar = []
    cal = db_app_interaction.get_calendar(email)
    if not cal:
        return Response(status=404)

    for item in cal:
      cl = prepare_for_json(item)
      calendar.append(cl)

    return jsonify({'calendar':calendar})

@app.route('/rest_api/v1.0/store_if_code', methods=['POST'])
@crossdomain(origin='*')
def store_code():
    store_request = request.json

    if (store_request is not None) and ('code') in store_request:
      session['code'] = store_request.get('code')
      return Response(status=200)

    abort(403)

@app.route('/rest_api/v1.0/get_if_code', methods=['GET'])
@crossdomain(origin='*')
def get_if_code():
    if 'code' in session:
        code = session['code']
        del session['code']
        return jsonify({'code': code})

    return Response(status=404)

@app.route('/rest_api/v1.0/calendar/insert', methods=['POST'])
@crossdomain(origin='*')
def insert_appointment():
    req = request.json

    if (req is not None) and ('title' and 'description' and 'data' and 'ora' and 'message' and 'priority') in req:

      email = session['email']
      titolo = req.get('title')
      data = req.get('data')
      ora = req.get('ora')
      message = req.get('message')
      description = req.get('description')
      priority = req.get('priority')

      try:
        db_app_interaction.set_appointment(email, description, titolo, data, ora, message, priority)
        return Response(status=200)
      except Exception, e:
          return Response(status=500)

    abort(403)

@app.route('/rest_api/v1.0/calendar/<string:code>', methods=['GET'])
@crossdomain(origin='*')
def view_appointment(code):
    email = session['email']

    appo = db_app_interaction.select_appointment(email, code)
    appointment = prepare_for_json(appo)
    return jsonify({'appointment':appointment})

@app.route('/rest_api/v1.0/calendar/<string:code>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_appointment(code):
    email = session['email']

    try:
        db_app_interaction.delete_appointment(email, code)
        return Response(status=200)
    except Exception, e:
        return Response(status=500)

@app.route('/rest_api/v1.0/calendar/<string:code>', methods=['PUT'])
@crossdomain(origin='*')
def update_appointment(code):
    email = session['email']
    update_req = request.json

    if update_req is not None and ('title' and 'description' and 'data' and 'ora' and 'message' and 'priority') in update_req:
      titolo = update_req.get('title')
      data = update_req.get('data')
      ora = update_req.get('ora')
      message = update_req.get('message')
      description = update_req.get('description')
      priority = update_req.get('priority')

      try:
        db_app_interaction.update_appo(email, code, titolo, description, data, ora, message, priority)
        return Response(status=200)
      except Exception, e:
        return Response(status=500)

    abort(403)

@app.route('/rest_api/v1.0/get_position', methods=['GET'])
@crossdomain(origin='*')
def get_position():
    position = db_app_interaction.get_position(session['email'])
    if not position:
        abort(404)

    return jsonify({'position':{'latitude':position['latitude'], 'longitude':position['longitude']}})

@app.route('/rest_api/v1.0/set_position/', methods=['POST'])
@crossdomain(origin='*')
def set_position():
    pos_request = request.json

    if (pos_request is not None) and ('latitude' and 'longitude') in pos_request and 'patient' in session and session['patient']=='y':
        try:
            db_app_interaction.set_position(session['email'], pos_request['latitude'], pos_request['longitude'])
            return Response(status=200)
        except Exception, e:
            return Response(status=500)

#------ APIs FOR MOBILE APP END ------#

#------ APIs FOR ROOM STATIONS ------#

@app.route('/rest_api/v1.0/save_bcode/<string:bcod>', methods=['POST'])
def save_bcode(bcod):
    try:
        db_app_interaction.save_bcode(bcod, time.strftime("%Y-%m-%d"))
        return Response(status=200)
    except Exception, e:
        return Response(status=500)

@app.route('/rest_api/v1.0/get_user_settings/<string:bcode>', methods=['GET'])
@crossdomain(origin='*')
def load_user_settings(bcode):
    email = db_app_interaction.get_email(bcode)
    email = email[0]

    set_list = db_app_interaction.get_settings(email)
    if not set_list:
        return Response(status=404)

    return jsonify({'settings':prepare_for_json(set_list)})

@app.route('/rest_api/v1.0/new_notification/<string:bcod>&<string:message>', methods=['POST'])
def send_push(bcod, message):
    email = db_app_interaction.get_email(bcod)
    email = email[0]
    db_app_interaction.insert_notification(email, time.strftime("%Y-%m-%d"), time.strftime("%H:%M"), message)
    send_email(email, message)
    if db_app_interaction.grant_docaccess:
        send_email(db_app_interaction.get_docemail(bcod), message)
    devices = db_app_interaction.get_devices_token(email)
    for device in devices:
        if device[1]=='ios':
            payload = Payload(alert=message, sound="default", badge=1)
            apns.gateway_server.send_notification(device[0], payload)
        else:
            data = {'message': message}
            reg_id = device[0]
            gcm.plaintext_request(registration_id=reg_id, data=data)

@app.route('/rest_api/v1.0/get_day_calendar/<string:date>&<string:bcod>', methods=['GET'])
@crossdomain(origin='*')
def load_day_calendar(bcod, date):

    daily = []
    email = db_app_interaction.get_email(bcod)
    email = email[0]
    day = db_app_interaction.get_day_calendar(email, date)
    if not day:
        return Response(status=404)

    for item in day:
      d = prepare_for_json(item)
      daily.append(d)

    return jsonify({'daily_cal':daily})

@app.route('/rest_api/v1.0/set_appointment_done/<string:code>&<string:bcod>', methods=['PUT'])
@crossdomain(origin='*')
def set_appointment_done(code, bcod):
    update_req = request.json
    email = db_app_interaction.get_email(bcod)
    email = email[0]

    if update_req is not None:

      try:
        db_app_interaction.set_appointment_done(email, code)
        return Response(status=200)
      except Exception, e:
        return Response(status=500)

    abort(403)

@app.route('/rest_api/v1.0/get_last_position/<string:bcod>', methods=['GET'])
@crossdomain(origin='*')
def get_last_position(bcod):
    email = db_app_interaction.get_email(bcod)
    email = email[0]
    position = db_app_interaction.get_position(email)
    if not position:
        abort(404)

    return jsonify({'position': {'latitude': position['latitude'], 'longitude': position['longitude']}})

#------ APIs FOR ROOM STATIONS END ------#

if __name__ == '__main__':
    app.run(host='192.168.1.102', port=8080)
