#!/bin/env python3

import discord
import requests
import json
from datetime import datetime, timezone
import pytz

client = discord.Client()
# Fill this with your credentials
client.login('LOGIN@DOMAIN.COM', 'PASSWORD')

def get_english_name(name):
    jp_dict = {
    'アンチョビットゲームズ': 'Ancho-V Games',
    'アロワナモール': 'Arowana Mall',
    'Ｂバスパーク': 'Blackbelly Skatepark',
    'ネギトロ炭鉱': 'Bluefin Depot',
    'モンガラキャンプ場': 'Camp Triggerfish',
    'ヒラメが丘団地': 'Flounder Heights',
    'マサバ海峡大橋': 'Hammerhead Bridge',
    'モズク農園': 'Kelp Dome',
    'マヒマヒリゾート＆スパ': 'Mahi-Mahi Resort',
    'タチウオパーキング': 'Moray Towers',
    'キンメダイ美術館': 'Museum d‘Alfonsino',
    'ショッツル鉱山': 'Piranha Pit',
    'ホッケふ頭': 'Port Mackarel',
    'シオノメ油田': 'Saltspray Rigs',
    'デカライン高架下': 'Urchin Underpass',
    'ハコフグ倉庫': 'Walleye Warehouse',
    'ガチエリア': 'Splat Zones',
    'ガチホコ': 'Rainmaker',
    'ガチヤグラ': 'Tower Control'
    }

    return jp_dict[name]

def get_schedule():
    #You can change for fitting your region. Choices are eu, na and jp
    response = requests.get('http://splatapi.ovh/schedule_eu.json')
    data = response.json()
    return data

def display_current_rotation(message):
    data = get_schedule()
    schedule = data['schedule']
    if data['festival'] == True:
        client.send_message(message.channel, "Splatfest ongoing. Please use `!r fes` instead.")
        return "fes"
    else:
        client.send_message(message.channel, '==== Now ====\n'+'**Turf War:** '+get_english_name(schedule[0]["stages"]["regular"][0]["name"])+', '+get_english_name(schedule[0]["stages"]["regular"][1]["name"])+'\n'+'**Ranked ['+get_english_name(schedule[0]["ranked_mode"])+']:** '+get_english_name(schedule[0]["stages"]["ranked"][0]["name"])+', '+get_english_name(schedule[0]["stages"]["ranked"][1]["name"]))

def display_next_rotation(message):
    data = get_schedule()
    schedule = data['schedule']
    if data['festival'] == True:
        client.send_message(message.channel, "Splatfest ongoing. Please use `!r fes` instead.")
        return "fes"
    else:
        begin = schedule[1]["begin"]
        # Change this to fit the timezone you need
        france = pytz.timezone('Europe/Paris')
        t = datetime.strptime(begin.replace('+09:00', '+0900'), "%Y-%m-%dT%H:%M:%S.%f%z")
        tz = france.normalize(t.astimezone(france))
        client.send_message(message.channel, '==== Next Rotation at '+tz.strftime("%Hh")+' ====\n'+'**Turf War:** '+get_english_name(schedule[1]["stages"]["regular"][0]["name"])+', '+get_english_name(schedule[1]["stages"]["regular"][1]["name"])+'\n'+'**Ranked ['+get_english_name(schedule[1]["ranked_mode"])+']:** '+get_english_name(schedule[1]["stages"]["ranked"][0]["name"])+', '+get_english_name(schedule[1]["stages"]["ranked"][1]["name"]))

def display_last_rotation(message):
    data = get_schedule()
    schedule = data['schedule']
    if data['festival'] == True:
        client.send_message(message.channel, "Splatfest ongoing. Please use `!r fes` instead.")
        return "fes"
    else:
        begin = schedule[2]["begin"]
        # Change this to fit the timezone you need
        france = pytz.timezone('Europe/Paris')
        t = datetime.strptime(begin.replace('+09:00', '+0900'), "%Y-%m-%dT%H:%M:%S.%f%z")
        tz = france.normalize(t.astimezone(france))
        client.send_message(message.channel, '==== Last Rotation at '+tz.strftime("%Hh")+' ====\n'+'**Turf War:** '+get_english_name(schedule[2]["stages"]["regular"][0]["name"])+', '+get_english_name(schedule[2]["stages"]["regular"][1]["name"])+'\n'+'**Ranked ['+get_english_name(schedule[2]["ranked_mode"])+']:** '+get_english_name(schedule[2]["stages"]["ranked"][0]["name"])+', '+get_english_name(schedule[2]["stages"]["ranked"][1]["name"]))

def display_all_rotations(message):
    ifFes = display_current_rotation(message)
    if  ifFes == "fes":
        pass
    else:
        display_next_rotation(message)
        display_last_rotation(message)

def display_fes(message):
    data = get_schedule()
    if data['festival'] == False:
        client.send_message(message.channel, "No Splatfest right now. Please us `!r now`, `!r next`, `!r last` or `!r all` instead.")
    else:
        schedule = data['schedule']
        now = datetime.now(timezone.utc)
        end = schedule[0]["end"]
        tend = datetime.strptime(end.replace('+00:00', '+0000'), "%Y-%m-%dT%H:%M:%S.%f%z")
        countdown = str(tend - now)
        hours, minutes, seconds = countdown.split(':', 2)
        client.send_message(message.channel, '==== Splatfest ====\n'+schedule[0]["team_alpha_name"]+' **vs** '+schedule[0]["team_bravo_name"]+'\n'+'**Ends in:** '+hours+'h'+minutes+'min\n'+'**Maps :** '+get_english_name(schedule[0]["stages"][0]["name"])+', '+get_english_name(schedule[0]["stages"][1]["name"])+', '+get_english_name(schedule[0]["stages"][2]["name"])+'\n\nHappy Splatfest! And may the odds be ever in your favor!')

def display_commands(message):
    client.send_message(message.channel, "List of commands for the Splat Rotations bot:\n\n- `!r help` : You're using it\n- `!r now` : Displays the current rotation\n- `!r next` : Displays the next rotation\n- `!r last` : Displays the last rotaton\n- `!r all` : Displays all rotations\n- `!r fes` : Displays current Splatfest infos\n\nくコ:彡 ***Stay Fresh***")

def display_helper(message):
    client.send_message(message.channel, "Use `!r help` to list all the available commands")

@client.event
def on_message(message):
    if message.content.startswith('!r help'):
        display_commands(message)
    elif message.content.startswith('!r now'):
        display_current_rotation(message)
    elif message.content.startswith('!r next'):
        display_next_rotation(message)
    elif message.content.startswith('!r last'):
        display_last_rotation(message)
    elif message.content.startswith('!r all'):
        display_all_rotations(message)
    elif message.content.startswith('!r fes'):
        display_fes(message)
    elif message.content.startswith('!r'):
        display_helper(message)

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()
