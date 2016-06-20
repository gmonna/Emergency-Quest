from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from alyt_api import AlytHub
import time, db_room_interaction, requests, os, vlc, fitbit_api

app = Flask(__name__)
bcod = "" #--it is the user-id for fitbit bracelet--#
perimeter = 0
colour = None
song = None
message = None
ms_motion = None
Alyt = AlytHub("http://192.168.1.103")

#---create motion message to play---#
def motion():
    ms = 'You went too far, keep calm and step back, your family will be home soon.'
    wget_line = 'wget -q -U Mozilla -O motion.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&tl=en&q=' + ms + '&client=tw-ob"'
    os.system(wget_line)
    ms = os.getcwd() + '/motion.mp3'
    ms_motion = vlc.MediaPlayer(ms)

#---new notification function to call when something dangerous happen---#
def new_notification(message):
    url = "http://127.0.0.1:5000/rest_api/v1.0/new_notification/"+bcod+"&"+message
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    requests.post(url, headers=headers)

#---function to get settings---#
def settings():
    url = "http://127.0.0.1:5000/rest_api/v1.0/get_settings/" + bcod
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    settings = requests.get(url, headers=headers)
    if(os.path.isfile(os.getcwd()+'/message.mp3')):
        os.remove(os.getcwd() + '/message.mp3')
    perimeter = settings['settings']['perimeter']
    colour = settings['settings']['colour']
    song = settings['settings']['song']
    if song == 'relax':
        song = os.getcwd() + '/songs/relax.mp3'
    elif song == 'remind':
        song = os.getcwd() + '/songs/remind.mp3'
    else:
        song = os.getcwd() + '/songs/concentrate.mp3'
    song = vlc.MediaPlayer(song)
    mg = settings['settings']['message']
    wget_line = 'wget -q -U Mozilla -O message.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&tl=en&q='+mg+'&client=tw-ob"'
    os.system(wget_line)
    mess = os.getcwd() + '/message.mp3'
    message = vlc.MediaPlayer(mess)

#---cron job to ask sensors---#

@app.before_first_request
def initialize():
    sched = BackgroundScheduler()
    settings()
    motion()

    @sched.scheduled_job('interval', seconds=10)
    def get_motion():
        if (Alyt.get_motion_state("Motion Detector 1") == 1 or Alyt.get_motion_state("Motion Detector 2") == 1):
            ms_motion.play()
            time.sleep(5)
            new_notification("The system detected a strange behavior of patient, he went too close to a dangerous situation and motion sensors turned on.")

    @sched.scheduled_job('interval', minutes=1)
    def check_appointment():
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
                url = "http://127.0.0.1:5000/rest_api/v1.0/set_appointment_done/"+appo[0]+"&"+bcod
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                requests.post(url, headers=headers)

    @sched.scheduled_job('interval', minutes=5)
    def control_agitation():
        h_rate = fitbit_api.get_agitation(bcod)
        if h_rate is not None:
            message.play()
            Alyt.turn_on_off_HueBulb("HueBulb 1", "on")
            if (colour=="blue"):
                r = 15
                g = 0
                b = 222
            elif (colour=="red"):
                r = 226
                g = 60
                b = 0
            else:
                r = 226
                g = 211
                b = 0
            Alyt.set_Huecolor_rgb("HueBulb 1", r, g, b)
            song.play()
            Alyt.turn_on_off_HueBulb("HueBulb 1", "off")
        new_notification(
            "System was unable to get patient's heart rate, maybe he took off the bracelet.")

    @sched.scheduled_job('interval', minutes=5)
    def get_position():
        position = fitbit_api.get_position(bcod)
        if position is not None:
            url = "http://127.0.0.1:5000/rest_api/v1.0/set_position/" + bcod + "&" + position['latitude'] + "&" + \
                  position['longitude']
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, headers=headers)
        new_notification(
            "System was unable to get patient's position, maybe he took off the bracelet.")

    @sched.scheduled_job('interval', hour=1)
    def refresh_settings():
        settings()

    @sched.scheduled_job('cron', hour=0)
    def get_today_calendar():
        db_room_interaction.delete_calendar()
        url = "http://127.0.0.1:5000/rest_api/v1.0/get_day_calendar/"+time.strftime("%Y-%m-%d")+"&"+bcod
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        calendar = requests.get(url, headers=headers)
        db_room_interaction.import_calendar(calendar['daily_cal'])

    sched.start()

if __name__ == '__main__':
    app.run(debug=True)
