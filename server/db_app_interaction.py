#!/usr/bin/python

"""
Created on May 30, 3016
@author: gmonna
"""

import sqlite3, smtplib

def get_code(bcod):
  """
  Check if bcod inserted by user is present
  """
  
  conn = sqlite3.connect("database.db")
  conn.text_factory = sqlite3.OptimizedUnicode
  cursor = conn.cursor()
  
  sql = "SELECT bcod FROM CODE WHERE bcod=?"
  cursor.execute(sql, (bcod, ))
  bcod = cursor.fetchone()
  
  conn.close()
  return bcod

def code_byemail(mail):
  """
  Check if mail is connected to any bcode
  """
  conn = sqlite3.connect("database.db")
  conn.text_factory = sqlite3.OptimizedUnicode
  cursor = conn.cursor()
  
  sql = "SELECT bcod FROM USERS WHERE mail=?"
  cursor.execute(sql, (mail, ))
  bcod = cursor.fetchone()
  
  conn.close()
  return bcod

def sign_in(mail, password):
  """
  Log in to the system
  """
  
  conn = sqlite3.connect("database.db")
  conn.text_factory = sqlite3.OptimezedUnicode
  cursor = conn.cursor()
  
  sql = "SELECT nome, cognome FROM USERS WHERE mail=? AND password=?"
  
  cursor.execute(sql, (mail, password))
  user = cursor.fetchone()
    
  conn.close()
  return user
  
def sign_up(bcod, mail, password, name, surname):
  """
  Sign up to the system
  """
  
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  sql = "INSERT INTO USERS(bcod, mail, password, name, surname) VALUES (?, ?, ?, ?, ?)"
  
  try:
    cursor.execute(sql, (bcod, mail, password, name, surname))
    conn.commit()
  except Exception, e:
    print str(e)
    conn.rollback()
    
  conn.close()
  
def lost_password(mail):
  """
  Send password to user
  """
  
  conn = sqlite3.connect("database.db")
  conn.text_factory = sqlite3.OptimezedUnicode
  cursor = conn.cursor()
  
  sql = "SELECT password FROM USERS WHERE mail=?"
  
  cursor.execute(sql, (mail, ))
  password = cursor.fetchone()
  
  sender = 'info@emergencyquest.com'
  receivers = [mail]

  message = """From: From EmergencyQuest Team <info@emergencyquest.com>
  Subject: Lost password

  We received your password request. Here it is your old password: """ + password + """
  We recommend to change it very soon.

  Best regards"""

  try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message)         
    print "Successfully sent email"
  except SMTPException:
    print "Error: unable to send email"
   
  conn.close()
  
def get_settings(mail)
  """
  Get current settings for the user
  """
  
  conn = sqlite3.connect("database.db")
  conn.text_factory = sqlite3.OptimezedUnicode
  cursor = conn.cursor()
  
  sql = "SELECT perimeter, colour, song, doct, message, auto_clean FROM PREFERENCES WHERE mail=?"

  cursor.execute(sql, (mail, ))
  settings = cursor.fetchone()
  
  conn.close()
  return settings

def set_settings(mail, perimeter, colour, song, doct, message, auto_clean, first):
  """
  Set preferences distinguishing between new user and already registered user
  """
  
  if (first=="y"):
    sql = "INSERT INTO PREFERENCES(perimeter, colour, song, doct, message, auto_clean, mail) VALUES (?, ?, ?, ?, ?, ?, ?)"
  else:
    sql = "UPDATE PREFERENCES SET perimeter=?, colour=?, song=?, doct=?, message=?, auto_clean=? WHERE mail=?"
    
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  
  try:
    cursor.execute(sql, (perimeter, colour, song, doct, message, auto_clean, mail))
    conn.commit()
  except Exception, e:
    print str(e)
    conn.rollback()
    
  conn.close()
  
def get_history(mail):
  """
  Get patient's history of notifications
  """
  history = []
  
  conn = sqlite3.connect("database.db")
  conn.text_factory = sqlite3.OptimezedUnicode
  cursor = conn.cursor()
  
  sql = "SELECT read, data, ora, message FROM HISTORY WHERE mail=?"

  cursor.execute(sql, (mail, ))
  history = cursor.fetchall()

  return history

def history_all_read(mail):
  """
  Set all notifications as read after opening history page
  """
  history = []
  
  conn = sqlite3.connect("database.db")
  conn.text_factory = sqlite3.OptimezedUnicode
  cursor = conn.cursor()
  
  sql = "UPDATE HISTORY SET read=y WHERE mail=?"

  cursor.execute(sql, (mail, ))
  history = cursor.fetchall()

  return history
  
def delete_history_doneappo(mail):
  """
  Delete patient's history and done appointments from database every *x* time
  """

  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  
  sql = "DELETE FROM HISTORY WHERE mail=?"
  sql2 = "DELETE FROM CALENDAR WHERE mail=? AND done=y"
  
  try:
    cursor.execute(sql, (mail, ))
    cursor.execute(sql2, (mail, ))
    conn.commit()
  except Exception, e:
    err = str(e)
    conn.rollback()
    
  conn.close()

def get_calendar(mail):
  """
  Get patient's appointments
  """
  calendar = []
  
  conn = sqlite3.connect("database.db")
  conn.text_factory = sqlite3.OptimezedUnicode
  cursor = conn.cursor()
  
  sql = "SELECT code, title, done, data, ora FROM CALENDAR WHERE mail=?"

  cursor.execute(sql, (mail, ))
  calendar = cursor.fetchall()

  conn.close()
  return calendar
  
def select_appointment(mail, code):
  """
  Get patient's specific appointment
  """
  calendar = []
  
  conn = sqlite3.connect("database.db")
  conn.text_factory = sqlite3.OptimezedUnicode
  cursor = conn.cursor()
  
  sql = "SELECT title, description, data, ora, message, priority, repeat FROM CALENDAR WHERE mail=? AND code=?"

  cursor.execute(sql, (mail, code ))
  calendar = cursor.fetchone()

  conn.close()
  return calendar

def set_appointment(mail, description, title, data, ora, message, priority, repeat):
  """
  Add an appointment to the calendar
  """
  
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  done = "n"
  sql = "INSERT INTO CALENDAR(mail, description, title, done, data, ora, message, priority, repeat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
  
  try:
    cursor.execute(sql, (mail, decription, title, done, data, ora, message, priority, repeat))
    conn.commit()
  except Exception, e:
    print str(e)
    conn.rollback()
    
  conn.close()

def delete_appointment(mail, code):
  """
  Add an appointment to the calendar
  """
  
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  sql = "DELETE FROM CALENDAR WHERE mail=? AND code=?"
  
  try:
    cursor.execute(sql, (mail, code))
    conn.commit()
  except Exception, e:
    print str(e)
    conn.rollback()
    
  conn.close()
  
def update_appo(mail, code, title, description, data, ora, message, priority, repeat):
  """
  Update an appointment into the calendar
  """
  
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  sql = "UPDATE CALENDAR SET title=? AND description=? AND data=? AND ora=? AND message=? AND priority=? AND repeat=? WHERE mail=? AND code=?"
  
  try:
    cursor.execute(sql, (title, description, data, ora, message, priority, repeat, mail, code))
    conn.commit()
  except Exception, e:
    print str(e)
    conn.rollback()
    
  conn.close()
