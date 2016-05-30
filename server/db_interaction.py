import sqlite3, smtplib

def sign_in(mail, password):
  """
  Log in to the system
  """
  
  conn = sqlite3.connect("database.db")
  conn.text_factory = sqlite3.OptimezedUnicode
  cursor = conn.cursor()
  
  sql = "SELECT nome, cognome FROM USERS WHERE mail=? AND password=?"
  
  try:
    cursor.execute(sql, (mail, password))
    user = cursor.fetchone()
  except Exception, e:
    err = str(e)
    conn.close()
    abort(404)
    
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
  
  try:
    cursor.execute(sql, (mail, ))
    password = cursor.fetchone()
  except Exception, e:
    err = str(e)
    conn.close()
    abort(404)
    
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
  
  
