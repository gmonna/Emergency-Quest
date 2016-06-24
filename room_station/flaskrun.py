#!/usr/bin/env python

"""
Created on June 18, 2016
@author: gmonna
"""

import optparse

def flaskrun(app, default_host="127.0.0.1",
                  default_port="5000"):
    """
    Takes a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """

    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname of the Flask app " + \
                           "[default %s]" % default_host,
                      default=default_host)
    parser.add_option("-P", "--port",
                      help="Port for the Flask app " + \
                           "[default %s]" % default_port,
                      default=default_port)

    # Two options useful for debugging purposes, but
    # a bit dangerous so not exposed in the help message.
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-p", "--profile",
                      action="store_true", dest="profile",
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-u", "--userid",
                      action="store", dest="userid",
                      help="User id for FitBit bracelet")
    parser.add_option("-f", "--first",
                      action="store_true", dest="first",
                      help="Type this command if it's first time configuration, then the user has to register to the system before room station could be loaded")

    options, _ = parser.parse_args()

    # If the user selects the profiling option, then we need
    # to do a little extra setup
    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware

        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
                       restrictions=[30])
        options.debug = True

    # This server must start with a userid
    if options.userid:
        app.config['USERID'] = options.userid

    # Check if it's first time starting room station
    if options.first:
        app.config['FIRST'] = True

        app.run(
            debug=options.debug,
            host=options.host,
            port=int(options.port)
        )

    # if there isn't options.userid app can't start
