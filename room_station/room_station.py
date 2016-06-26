#!/usr/bin/env python

"""
Created on June 4, 2016
@author: gmonna, fieraverto

Central room station for controlling everything in the house
"""

from flask import Flask, request
from flaskrun import flaskrun
from apscheduler.schedulers.background import BackgroundScheduler
from alyt_api import AlytHub
import time, db_room_interaction, requests, os, vlc, fitbit_api, math, json, logging

app = Flask(__name__)
perimeter = 0
latitude = None
longitude = None
colour = None
song = None
message = None
ms_motion = None
cal = 'noappos'
alyt = AlytHub("192.168.1.103")

#---shutdown server function---#
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

#---first installation of service, save bracelet code for usage---#
def create_code():
    url = "http://192.168.1.102:8080/rest_api/v1.0/save_bcode/"+app.config['USERID']
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    requests.post(url, headers=headers)

#---convert address to its latitude and longitude---#
def coordinates(address):
    url = "https://maps.google.com/maps/api/geocode/json?address="+address+"&sensor=false"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.get(url, headers=headers)
    coor = json.loads(response.text)
    latitude = coor['results'][0]['geometry']['location']['lat']
    longitude = coor['results'][0]['geometry']['location']['lng']

#---get perimeter distance---#
def deg2rad(deg):
    return deg * (math.pi/180)

def getDistanceFromLatLonInM(lat1,lon1,lat2,lon2):
    R = 6371 # Radius of the earth in km
    dlat = deg2rad(lat2-lat1)
    dlon = deg2rad(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + \
    math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * \
    math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c  * 1000 # Distance in m
    return d

#---create motion message to play---#
def motion():
    ms = 'You went too far, keep calm and step back, your family will be home soon.'
    wget_line = 'wget -q -U Mozilla -O motion.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&tl=en&q=' + ms + '&client=tw-ob"'
    os.system(wget_line)
    ms = os.getcwd() + '/motion.mp3'
    ms_motion = vlc.MediaPlayer(ms)

#---new notification function to call when something dangerous happen---#
def new_notification(message):
    url = "http://192.168.1.102:8080/rest_api/v1.0/new_notification/"+app.config['USERID']+"&"+message
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    requests.post(url, headers=headers)

#---function to get settings---#
def settings():
    url = "http://192.168.1.102:8080/rest_api/v1.0/get_user_settings/" + app.config['USERID']
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.get(url, headers=headers)
    sttings = json.loads(response.text)
    if not sttings:
        return
    if(os.path.isfile(os.getcwd()+'/message.mp3')):
        os.remove(os.getcwd() + '/message.mp3')
    perimeter = sttings['settings']['perimeter']
    address = sttings['settings']['address']
    coordinates(address)
    colour = sttings['settings']['colour']
    song = sttings['settings']['song']
    if song == 'relax':
        song = os.getcwd() + '/songs/relax.mp3'
    elif song == 'remind':
        song = os.getcwd() + '/songs/remind.mp3'
    else:
        song = os.getcwd() + '/songs/concentrate.mp3'
    song = vlc.MediaPlayer(song)
    mg = sttings['settings']['message']
    wget_line = 'wget -q -U Mozilla -O message.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&tl=en&q='+mg+'&client=tw-ob"'
    os.system(wget_line)
    mess = os.getcwd() + '/message.mp3'
    message = vlc.MediaPlayer(mess)

#---cron jobs to ask sensors---#

@app.before_first_request
def initialize():
    logging.basicConfig()
    if app.config['FIRST']: #-- create code in main server database only if it's first time
        create_code()
        shutdown_server()
    sched = BackgroundScheduler()
    settings()
    motion()

    @sched.scheduled_job('interval', minutes=1)
    def check_appointment():
        if (cal!='noappos'):
            appointments = db_room_interaction.get_appointments()
            for appo in appointments:
                if appo[2] == time.strftime("%02H:%02M"):
                    wget_line = 'wget -q -U Mozilla -O reminder.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&tl=en&q=' + appo[1] + '&client=tw-ob"'
                    os.system(wget_line)
                    reminder = vlc.MediaPlayer(os.getcwd()+'/reminder.mp3')
                    reminder.play()
                    time.sleep(5)
                    os.remove('reminder.mp3')
                    db_room_interaction.set_done(appo[0])
                    url = "http://192.168.1.102:8080/rest_api/v1.0/set_appointment_done/"+appo[0]+"&"+app.config['USERID']
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    requests.post(url, headers=headers)

    @sched.scheduled_job('interval', seconds=30)
    def check_motion():
        if (alyt.get_motion_state("Motion Sensor 1") == 1 or alyt.get_motion_state("Motion sensor 2") == 1):
            ms_motion.play()
            time.sleep(5)
            new_notification(
                "System detected a dangerous situation by motion sensors, now it's helping the patient avoid it.")

    @sched.scheduled_job('interval', minutes=5)
    def get_position():
        url = "http://192.168.1.102:8080/rest_api/v1.0/get_last_position/" + app.config['USERID']
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.get(url, headers=headers)
        position = json.loads(response.text)
        if not position:
            return
        if (getDistanceFromLatLonInM(position['latitude'], position['longitude'], latitude, longitude)>perimeter):
            new_notification(
                "System detected an exit from the perimeter of the patient, we suggest you to return home.")

    @sched.scheduled_job('interval', minutes=20)
    def get_agitation():
        if (fitbit_api.get_agitation(app.config['USERID']) > 100):
            message.play()
            alyt.turn_on_off_HueBulb("Hue Bulb 1", "on")
            if (colour == 'blue'):
                r = 22
                g = 14
                b = 170
            elif (colour == 'red'):
                r = 173
                g = 0
                b = 9
            else:
                r = 180
                g = 173
                b = 32
            alyt.set_Huecolor_rgb("Hue Bulb 1", r, g, b)
            song.play()
            time.sleep(10)
            alyt.turn_on_off_HueBulb("Hue Bulb 1", "off")
            new_notification(
                "System detected a condition of agitation on the patient during last five minutes, now it's trying to calm him down.")

    @sched.scheduled_job('interval', minutes=60)
    def refresh_settings():
        settings()

    @sched.scheduled_job('cron', day_of_week='mon-sun')
    def get_today_calendar():
        db_room_interaction.delete_calendar()
        url = "http://192.168.1.102:8080/rest_api/v1.0/get_day_calendar/"+time.strftime("%Y-%m-%d")+"&"+app.config['USERID']
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.get(url, headers=headers)
        if(response.text is not None):
            cal = 'todayappos'
            calendar = json.loads(response.text)
            db_room_interaction.import_calendar(calendar['daily_cal'])
        else:
            cal = 'noappos'

    sched.start()

if __name__ == '__main__':
    flaskrun(app)
