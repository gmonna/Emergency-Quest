#!/usr/bin/python

"""
Created on May 30, 2016
@author: gmonna
"""

import sqlite3, smtplib, os, base64, hashlib
DATABASE = os.getcwd()+'/db/database.db'

def get_device_tokens(email):
    """
    Get token of user's devices to send him a push notification
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT deviceid, anorapp FROM DEVICE WHERE email=?"
    cursor.execute(sql, (email,))
    devices = cursor.fetchall()

    conn.close()
    return devices

def insert_token(email, deviceid, anorapp):
    """
    Insert user's device token to send him push notifications
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    req = "SELECT deviceid FROM DEVICE WHERE email=?"
    cursor.execute(req, (email, ))
    devices = cursor.fetchall()
    if(deviceid not in devices):
        sql = "INSERT INTO DEVICE(email, deviceid, anorapp) VALUES(?, ?, ?)"
        try:
            cursor.execute(sql, (email, deviceid, anorapp))
            conn.commit()
        except Exception, e:
            print str(e)
            conn.rollback()

    conn.close()

def get_code(bcod):
    """
    Check if bcod inserted by user is present
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT bcod FROM CODE WHERE bcod=?"
    cursor.execute(sql, (bcod, ))
    bcod = cursor.fetchone()

    conn.close()
    return bcod

def check_presence(email, bcod):
    """
    Check if email or bcod are present into the database
    """
    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT bcod FROM USERS WHERE email=? OR bcod=?"
    cursor.execute(sql, (email, bcod))
    bcod = cursor.fetchone()

    conn.close()
    return bcod

def check_email(email):
    """
    Check if email is present for log in
    """
    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT bcod FROM USERS WHERE email=?"
    cursor.execute(sql, (email, ))
    bcod = cursor.fetchone()

    conn.close()
    return bcod

def get_email(bcod):
    """
    Get email connected to B_CODE
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT email FROM USERS WHERE bcod=?"
    cursor.execute(sql, (bcod, ))
    email = cursor.fetchone()

    conn.close()
    return email

def get_docemail(bcod):
    """
    Get docemail connected to B_CODE
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT doct FROM USERS, PREFERENCES WHERE USERS.EMAIL = PREFERENCES.EMAIL AND bcod=?"
    cursor.execute(sql, (bcod, ))
    email = cursor.fetchone()

    conn.close()
    return email

def sign_in(email, password):
    """
    Log in to the system
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT name, surname FROM USERS WHERE email=? AND password=?"

    cursor.execute(sql, (email, password))
    user = cursor.fetchone()

    conn.close()
    return user

def sign_up(bcod, email, password, name, surname):
    """
    Sign up to the system
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = "INSERT INTO USERS(bcod, email, password, name, surname) VALUES (?, ?, ?, ?, ?)"

    try:
        cursor.execute(sql, (bcod, email, password, name, surname))
        conn.commit()
    except Exception, e:
        print str(e)
        conn.rollback()

    conn.close()

def lost_password(email):
    """
    Send password to user
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT password FROM USERS WHERE email=?"

    cursor.execute(sql, (email, ))
    password = cursor.fetchone()

    sender = 'info@emergencyquest.com'
    receivers = [email]

    message = """From: From EmergencyQuest Team <info@emergencyquest.com>
    Subject: Lost password

    We received your password request. Here it is your old password: """ + password + """
    We recommend to change it very soon.

    Best regards"""

    try:
        smtpObj = smtplib.SMTP('smtp.googlemail.com')
        smtpObj.sendemail(sender, receivers, message)
        print "Successfully sent email"
    except:
        print "Error: unable to send email"

    conn.close()

def get_settings(email):
    """
    Get current settings for the user
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT perimeter, colour, song, doct, message, auto_clean, doc_access FROM PREFERENCES WHERE email=?"

    cursor.execute(sql, (email, ))
    settings = cursor.fetchone()

    conn.close()
    return settings

def grant_docaccess(email):
    """
    Get doctor access setting for the user
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT doc_access FROM PREFERENCES WHERE email=?"

    cursor.execute(sql, (email,))
    docaccess = cursor.fetchone()

    conn.close()

    if docaccess[0]=='y':
        return True
    else:
        return False

def set_settings(email, perimeter, colour, song, doct, message, auto_clean, doc_access, address, first):
    """
    Set preferences distinguishing between new user and already registered user
    """

    if (first=='y'):
        sql = "INSERT INTO PREFERENCES(perimeter, colour, song, doct, message, auto_clean, doc_access, address, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    else:
        sql = "UPDATE PREFERENCES SET perimeter=?, colour=?, song=?, doct=?, message=?, auto_clean=?, doc_access=?, address=? WHERE email=?"

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute(sql, (perimeter, colour, song, doct, message, auto_clean, doc_access, address, email))
        conn.commit()
    except Exception, e:
        print str(e)
        conn.rollback()

    conn.close()

def get_history(email):
    """
    Get patient's history of notifications
    """
    history = []

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT read, data, ora, message FROM HISTORY WHERE email=? ORDER BY read ASC, data DESC, ora DESC"

    cursor.execute(sql, (email, ))
    history = cursor.fetchall()

    return history

def insert_notification(email, data, ora, message):
    """
    Add a notification to history
    """
    code = base64.urlsafe_b64encode(hashlib.md5(email + data + ora + message).digest())

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    read = "n"
    sql = "INSERT INTO HISTORY(email, code, read, data, ora, message) VALUES (?, ?, ?, ?, ?, ?)"

    try:
        cursor.execute(sql, (email, code, read, data, ora, message))
        conn.commit()
    except Exception, e:
        print str(e)
        conn.rollback()

    conn.close()

def history_all_read(email):
    """
    Set all notifications as read after opening history page
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    sql = "UPDATE HISTORY SET read='y' WHERE email=?"

    try:
      cursor.execute(sql, (email, ))
      conn.commit()
    except Exception, e:
      print str(e)
      conn.rollback()

    conn.close()

def delete_history_doneappo():
    """
    Delete patient's history and done appointments from database every *x* time
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    sql = "DELETE FROM HISTORY WHERE read='y' AND email IN (SELECT email FROM PREFERENCES WHERE auto_clean='y')"
    sql2 = "DELETE FROM CALENDAR WHERE done='y' AND email IN (SELECT email FROM PREFERENCES WHERE auto_clean='y')"

    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        conn.commit()
    except Exception, e:
        conn.rollback()

    conn.close()

def get_calendar(email):
    """
    Get patient's appointments
    """
    calendar = []

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT code, title, done, data, ora FROM CALENDAR WHERE email=? ORDER BY data ASC, ora ASC, done ASC"

    cursor.execute(sql, (email, ))
    calendar = cursor.fetchall()

    conn.close()
    return calendar

def get_day_calendar(email, date):
    """
    Get patient's appointments of the day
    """
    calendar = []

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT code, message, ora FROM CALENDAR WHERE email=? AND data=? ORDER BY ora ASC"

    cursor.execute(sql, (email, date))
    calendar = cursor.fetchall()

    conn.close()
    return calendar

def set_appointment_done(email, code):
    """
    Set this appointment to done=y
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "UPDATE CALENDAR SET done='y' WHERE email=? AND code=?"

    try:
        cursor.execute(sql, (email, code))
        conn.commit()
    except Exception, e:
        print str(e)
        conn.rollback()

    conn.close()

def get_numbers(email):
    """
    Get patient's appointments
    """
    numbers = []

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql1 = "SELECT COUNT(*) FROM CALENDAR WHERE email=? AND done='n'"
    cursor.execute(sql1, (email, ))
    numb1 = cursor.fetchone()
    numbers.append(numb1)

    sql2 = "SELECT COUNT(*) FROM HISTORY WHERE email=? AND read='n'"
    cursor.execute(sql2, (email,))
    numb2 = cursor.fetchone()
    numbers.append(numb2)

    conn.close()
    if numb1 is None or numb2 is None:
        return -1

    return numbers

def select_appointment(email, code):
    """
    Get patient's specific appointment
    """
    calendar = []

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT title, description, data, ora, message, priority FROM CALENDAR WHERE email=? AND code=?"

    cursor.execute(sql, (email, code ))
    calendar = cursor.fetchone()

    conn.close()
    return calendar

def set_appointment(email, description, title, data, ora, message, priority):
    """
    Add an appointment to the calendar
    """

    code = base64.urlsafe_b64encode(hashlib.md5(email+title+description).digest())

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    done = "n"
    sql = "INSERT INTO CALENDAR(email, description, code, title, done, data, ora, message, priority) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

    try:
        cursor.execute(sql, (email, description, code, title, done, data, ora, message, priority))
        conn.commit()
    except Exception, e:
        print str(e)
        conn.rollback()

    conn.close()

def delete_appointment(email, code):
    """
    Add an appointment to the calendar
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = "DELETE FROM CALENDAR WHERE email=? AND code=?"

    try:
        cursor.execute(sql, (email, code))
        conn.commit()
    except Exception, e:
        print str(e)
        conn.rollback()

    conn.close()

def update_appo(email, code, title, description, data, ora, message, priority):
    """
    Update an appointment into the calendar
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = "UPDATE CALENDAR SET title=?, description=?, data=?, ora=?, message=?, priority=? WHERE email=? AND code=?"

    try:
        cursor.execute(sql, (title, description, data, ora, message, priority, email, code))
        conn.commit()
    except Exception, e:
        print str(e)
        conn.rollback()

    conn.close()

def set_position(email, lat, long):
    """
    Add new position to database
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = "INSERT INTO POSITION(email, latitude, longitude) VALUES (?, ?, ?)"

    try:
        cursor.execute(sql, (email, lat, long))
        conn.commit()
    except Exception, e:
        print str(e)
        conn.rollback()

    conn.close()

def get_position(email):
    """
    Get patient's last position registered
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT latitude, longitude FROM POSITION WHERE email=?"

    cursor.execute(sql, (email, ))
    position = cursor.fetchone()

    pos = dict()
    pos['latitude'] = position[0]
    pos['longitude'] = position[1]

    conn.close()
    return pos