from flask import Flask, jsonify, abort, session, Response, make_response, current_app
from apscheduler.schedulers.background import BackgroundScheduler
import time, db_room_interaction, requests

app = Flask(__name__)
bcod = 0 #--in first bracelet connection to the system we store code here--#
perimeter = 0
colour = 0
song = 0
message = None

#---new notification function to call when something dangerous happen---#
def new_notification(message):
    url = "http://127.0.0.1:5000/rest_api/v1.0/new_notification/"+bcod+"&"+message
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    requests.post(url, headers=headers)

#---cron job to ask sensors---#

@app.before_first_request
def initialize():
    sched = BackgroundScheduler()

    @sched.scheduled_job('interval', minutes=10)
    def timed_job():
        print('Use this type of function to call APIs for motion sensors -> get position from smartphone/get bracelet data/get motion data')

    @sched.scheduled_job('interval', hour=1)
    def refresh_settings():
        url = "http://127.0.0.1:5000/rest_api/v1.0/get_settings/"+bcod
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        settings = requests.get(url, headers=headers)
        perimeter = settings['settings']['perimeter']
        colour = settings['settings']['colour']
        song = settings['settings']['song']
        message = settings['settings']['message']

    @sched.scheduled_job('interval', hour=24)
    def get_today_calendar():
        db_room_interaction.delete_calendar()
        url = "http://127.0.0.1:5000/rest_api/v1.0/get_day_calendar/"+time.strftime("%Y-%m-%d")+"&"+bcod
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        calendar = requests.get(url, headers=headers)
        db_room_interaction.import_calendar(calendar['daily_cal'])

    @sched.scheduled_job('cron', day_of_week='mon')
    def auto_clean():
        print "Wake up it's monday"

    sched.start()

if __name__ == '__main__':
    app.run(debug=True)
