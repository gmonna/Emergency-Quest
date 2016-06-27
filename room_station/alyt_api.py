# coding=utf-8
#!/usr/bin/env python

"""
Created on June 4, 2016
@author: fieraverto

Module for controlling Alyt Hub and all sensors
"""
import requests, json


class AlytHub:
    """
    A class representing a Alyt Hub
    """
    def __init__(self, url, passwd = "FlickaGlitch39"):

        # remove trailing slashes
        if url[-1] == '/':
            url = url[:-1]

        # store the base API URL
        self.alyt_url = url + ":8080/alyt"

        # store the Alyt passwd
        self.passwd = passwd

        #search and store Philips Hue ID
        self.ID_HueBulb1 = self.get_ID("HueBulb 1")

        #search and store Motion Detector 1 ID
        self.ID_motion_d1 = self.get_ID("Motion Detector 1")

        #search and store Motion Detector 2 ID
        self.ID_motion_d2 = self.get_ID("Motion Detector 2")


    def create_URL(self, command):

        return self.alyt_url + command

    def print_json(self, obj_json):

        #parsed = json.loads(obj_json)          # usefull to print json objects created by programmer
        print json.dumps(obj_json, indent=4, sort_keys=False)


    def create_session(self):

        url = self.create_URL("/login")
        payload = { 'password' : self.passwd }

        response = requests.post(url, data = payload)
        answer = response.json()

        return answer.get("SESSION_ID", {})


    def get_list(self):

        session_ID = self.create_session()
        cookie = {'SESSION_ID' : session_ID}
        cookie_json = json.dumps(cookie)

        url = self.create_URL("/get_list")

        payload = { 'category' : 'device', 'filter' : 'all'}

        response = requests.get(url, params=payload, headers={ 'Cookie' : cookie_json })
        answer = response.json()

        return answer


    def get_ID(self, device):

        answer = self.get_list()

        list_of_device = answer['TAG_RISP_CMD']['CMD_INFO']

        for num in range(0, len(list_of_device)):
            temp = list_of_device[num]['LIST']

            if (len(temp) != 0):
                for enum in range(0, len(temp)):
                    info_device = temp[enum]['JSONOBJ']
                    name_device = info_device['TAG_DESCRIPTION']

                    if (name_device == device):
                        ID = info_device['TAG_ID']
                        return ID


    def get_motion_state(self, sensor):

        if (sensor == "Motion Detector 1"):
            ID = self.ID_motion_d1

        elif (sensor == "Motion Detector 2"):
            ID = self.ID_motion_d2

        else:
            print "ERROR 404: Sensor not found"
            return -1

        session_ID = self.create_session()
        cookie = {'SESSION_ID' : session_ID}
        cookie_json = json.dumps(cookie)

        url = self.create_URL("/get_prog")

        payload = { 'category' : "zwave", 'id' : ID}

        response = requests.get(url, params=payload, headers={ 'Cookie' : cookie_json })
        answer = response.json()

        state = answer['TAG_RISP_CMD']['CMD_INFO']['TAG_DATA']['TAG_STATE']

        return state


    def get_HueBulb_state(self, sensor):

        if (sensor == "HueBulb 1"):
            ID = self.ID_HueBulb1

        else:
            print "ERROR 404: Sensor not found"
            return -1

        session_ID = self.create_session()
        cookie = {'SESSION_ID' : session_ID}
        cookie_json = json.dumps(cookie)

        url = self.create_URL("/get_prog")

        payload = { 'category' : 'zigbee', 'id' : ID}

        response = requests.get(url, params=payload, headers={ 'Cookie' : cookie_json })
        answer = response.json()

        state = dict()

        state['color'] = answer['TAG_RISP_CMD']['CMD_INFO']['TAG_DATA']['TAG_COLOR']
        state['state'] = answer['TAG_RISP_CMD']['CMD_INFO']['TAG_DATA']['TAG_STATE']

        return state


    def turn_on_off_HueBulb(self, sensor, state):

        if (state.lower() == "on"):
            tag_description = json.loads(json.dumps({'TAG_ENG_DESC' : 'Activated', 'TAG_DEF_DESC' : 'activation', 'TAG_FRA_DESC' : 'Activée', 'TAG_ITA_DESC' : 'Attivata'}))
            action_ID = 4

        elif (state.lower() == "off"):
            tag_description = json.loads(json.dumps({'TAG_ENG_DESC' : 'Deactivated', 'TAG_DEF_DESC' : 'deactivation', 'TAG_FRA_DESC' : 'Désactivé', 'TAG_ITA_DESC' : 'Disattivato'}))
            action_ID = 5

        else:
            print "ERROR 403: Wrong state parameter"
            return -1


        if (sensor == "HueBulb 1"):
            ID = self.ID_HueBulb1

        else:
            print "ERROR 404: Sensor not found"
            return -1

        session_ID = self.create_session()
        cookie = {'SESSION_ID' : session_ID}
        cookie_json = json.dumps(cookie)


        url = self.create_URL("/capability_cmd")


        capability = {'TAG_TYPE' : 'Simple', 'TAG_DESCRIPTION' : tag_description, 'TAG_ACTION_ID' : action_ID, 'TAG_I/O' : 'Output'}
        state_json = json.dumps(capability)

        payload = { 'prot_type' : 2, 'id' : ID, 'capability' : state_json}

        response = requests.post(url, data=payload, headers={ 'Cookie' : cookie_json })


    def set_Huecolor_rgb(self, sensor, red, green, blue):

        if (red<0 or red>255):
            print "ERROR 403: Wrong red parameter"
            return -1

        if (green<0 or green>255):
            print "ERROR 403: Wrong green parameter"
            return -1

        if (blue<0 or blue>255):
            print "ERROR 403: Wrong blue parameter"
            return -1



        if (sensor == "HueBulb 1"):
            ID = self.ID_HueBulb1

        else:
            print "ERROR 404: Sensor not found"
            return -1


        session_ID = self.create_session()
        cookie = {'SESSION_ID' : session_ID}
        cookie_json = json.dumps(cookie)


        url = self.create_URL("/capability_cmd")

        action_ID = 0

        tag_description = json.loads(json.dumps({'TAG_ENG_DESC' : 'Set RGB color', 'TAG_DEF_DESC' : 'Set RGB color', 'TAG_FRA_DESC' : 'Définissez la couleur RGB', 'TAG_ITA_DESC' : 'Impostare il colore RGB'}))
        capability = {'TAG_TYPE' : 'Complex', 'TAG_CHOSEN_VALUES' : [red, green, blue], 'TAG_DESCRIPTION' : tag_description, 'TAG_CAPABILITY_NAME' : 'set_color_rgb', 'TAG_INFO' : 'set the values of red, green and blue. Accepted range: 0­255', 'TAG_ACTION_ID' : action_ID, 'TAG_I/O' : 'Output'}
        color_json = json.dumps(capability)

        payload = { 'prot_type' : 2, 'id' : ID, 'capability' : color_json}

        response = requests.post(url, data=payload, headers={ 'Cookie' : cookie_json })


    # PROTOCOL TYPE: '1' -> ZWAVE
    # PROTOCOL TYPE: '2' -> ZIGBEE
