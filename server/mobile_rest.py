#!/usr/bin/python

"""
Created on May 30, 2016
@author: gmonna
"""

from flask import Flask, jsonify, abort, request, Response
import db_interaction

app = Flask(__name__)

#----------- REST SERVER ----------#
@app.route('/rest_api/v1.0/signup' methods=['POST'])
def new_user:
  insert_request = request.json
  
  if (insert_request is not None) and ('name' and 'surname' and 'mail' and 'password' and 'bcod') in insert_request:
    bcod = insert_request['bcod']
    bc = db_interaction.get_code(bcod)
    if bc is None:
      abort(404)
      
    mail = insert_request['mail']
    password = insert_request['password']
    name = insert_request['name']
    surname = insert_request['surname']
    
    db_interaction.sign_up(bcod, mail, password, name, surname)
    return Response(status=200)
  
  abort(403)
