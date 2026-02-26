import requests
import time
import urllib3

import threading
import simpleaudio as sa

import random


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

live_game_data_base_url = "https://127.0.0.1:2999/liveclientdata"

all_game_data_url = "allgamedata"

player_scores_url = "playerscores?riotId="

player_list_url = "playerlist"

active_player_url = "activeplayer"





laughter_sound = sa.WaveObject.from_wave_file("laughter.wav")

roast_tts = sa.WaveObject.from_wave_file("roastTTS.wav")

hyperSpeed_tts = sa.WaveObject.from_wave_file("hyperspeedTTS.wav")









def get_player_list():

    url = f"{live_game_data_base_url}/{player_list_url}"

    response = requests.get(url, verify=False)

    if response.status_code == 200:

        json = response.json()

        return json

def get_current_player_data():
        
    url = f"{live_game_data_base_url}/{active_player_url}"

    response = requests.get(url, verify=False)

    if response.status_code == 200:

        json = response.json()

        return json
        
def get_current_game_data(riot_id):

    url = f"{live_game_data_base_url}/{player_scores_url}{riot_id}"

    response = requests.get(url, verify=False)

    if response.status_code == 200:

        json = response.json()
        
        return json
    
    
def get_kda(current_match_data):

    kda = [
        {"Kills": current_match_data['kills']},
        {"Deaths": current_match_data['deaths']},
        {"Assists": current_match_data['assists']}
    ]
    
    return kda


def get_movespeed():

    url = f"{live_game_data_base_url}/{active_player_url}"

    response = requests.get(url, verify=False)

    if response.status_code == 200:
        json = response.json()
        
        stats = json["championStats"]

        movespeed = stats['moveSpeed']

    return movespeed
    


# print(players_in_game)


#Checks the kda every 0.1 seconds

def roast():

    


    prev_death_count = current_kda[1]["Deaths"]
    while not stop_event.is_set():

        kda = get_kda(get_current_game_data(riotId))
            
        death_count = kda[1]["Deaths"]    
        


        #print(f"PREVIOUS DEATHCOUNT: {prev_death_count}")


        if death_count > prev_death_count:
            prev_death_count = death_count

            laughter_sound.play()
            roast_tts.play()

            time.sleep(2.5)



        time.sleep(0.25)


riotId = get_current_player_data()['riotId']

print(f"Current Player: {riotId}")

current_kda = get_kda(get_current_game_data(riotId))

players_in_game = get_player_list()

stop_event = threading.Event()


speed_songs = [
sa.WaveObject.from_wave_file("Sonic.wav"), # Sonic
sa.WaveObject.from_wave_file("GAS.wav"), # GAS
sa.WaveObject.from_wave_file("90s.wav"), # 90s

]



if 'WarwickR' in get_current_player_data()['abilities']['R']['id']:
    print("Player is playing Warwick! adding Animals to Speed Songs! AWOOO!!")
    speed_songs.append(sa.WaveObject.from_wave_file("Animals.wav")) # Adds Animals to the list
    
else:
    print("PLAYER NOT PLAYING WARWICK :(")
    print(get_current_player_data()['abilities']['R']['id'])
    
def initiateZoom():

        
    while not stop_event.is_set():
            
        movespeed = get_movespeed()
        #print(f"CURRENT MOVESPEED {movespeed}")

        if movespeed > 895:
            randomNum = random.randint(0, len(speed_songs) - 1)
            
            # print(f"MOVESPEED ABOVE THRESHOLD")

            
            chosenSong = speed_songs[randomNum]

            hyperSpeed_tts.play().wait_done()
            
            chosenSong.play().wait_done()
    
            

            


        time.sleep(0.25)


roastThread = threading.Thread(target=roast, daemon=True)

zoomThread = threading.Thread(target=initiateZoom, daemon=True)

roastThread.start()
zoomThread.start()

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:
        print("Stopping..")
        stop_event.set()