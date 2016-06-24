#!/usr/bin/python

"""
Created on June 19, 2016
@author: gmonna
"""

import sqlite3, os
DATABASE = os.getcwd()+'/db/db_station.db'

def set_done(code):
    """
    Set this appointment to done=y
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "DELETE FROM CALENDAR WHERE code=?"

    try:
        cursor.execute(sql, (code, ))
        conn.commit()
    except Exception, e:
        print str(e)
        conn.rollback()

    conn.close()

def delete_calendar():
    """
    Clear all calendar
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "DELETE FROM CALENDAR;"

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception, e:
        print str(e)
        conn.rollback()

    conn.close()

def import_calendar(calendar):
    """
    Add daily calendar to database
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    try:
        for item in calendar:
            sql = "INSERT INTO CALENDAR(code, message, ora, priority) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (item['code'], item['message'], item['ora'], item['priority']))
        conn.commit()
    except Exception, e:
        print str(e)
        conn.rollback()

    conn.close()

def get_appointments():
    """
    Get all daily appointments
    """

    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()

    sql = "SELECT code, message, ora FROM CALENDAR;"
    cursor.execute(sql)
    appos = cursor.fetchall()

    conn.close()
    return appos;