import time
import vlc
from alyt_api import AlytHub
from fitbit_api import Fitbit

def main():

    Alyt = AlytHub("http://192.168.1.103")
    Fitbit = Fitbit()

    message_1 = vlc.MediaPlayer('mp3 file to play to remember to do when Motion Detector 1 is active, presents in database')
    message_2 = vlc.MediaPlayer('mp3 file to play to remember to do when Motion Detector 2 is active, presents in database')
    music = vlc.MediaPlayer('mp3 file to relax, presents in database')

    #Alyt.turn_on_off_HueBulb("HueBulb 1", "off")
    #Alyt.set_Huecolor_rgb("HueBulb 1", 255, 0, 0)

    Alyt.turn_on_off_HueBulb("HueBulb 1", "on")
    Alyt.set_Huecolor_rgb("HueBulb 1", 100, 150, 150)

    state_HueBulb = Alyt.get_HueBulb_state("HueBulb 1")
    list_RGB_colors = state_HueBulb['color'].split('-')



    while(1):

        if (Alyt.get_motion_state("Motion Detector 1") == 1):

            message_1.play()

            # WAIT 5 SECONDS TO CLEAR SUCCESSFULL FLAG OF MOTION DETECTOR 1

            for i in range(0, 5):
                time.sleep(1)

        if (Alyt.get_motion_state("Motion Detector 2") == 1):

            message_2.play()

            # WAIT 5 SECONDS TO CLEAR SUCCESSFULL FLAG OF MOTION DETECTOR 2

            for i in range(0, 5):
                time.sleep(1)



        if (Fitbit.get_HR() > 100):

            Alyt.turn_on_off_HueBulb("HueBulb 1", "on")
            Alyt.set_Huecolor_rgb("HueBulb 1", 0, 100, 250)

            # STORE TIME WHEN OCCURED AGITATION IN THE PATIENT IN THE DATABASE

            while (Fitbit.get_HR() > 100):

                music.play()

            music.stop()
            Alyt.set_Huecolor_rgb("HueBulb 1", list_RGB_colors[0], list_RGB_colors[1], list_RGB_colors[2])



    #prova = Alyt.get_list()
    #Alyt.print_json(prova)

if __name__ == '__main__':
    main()