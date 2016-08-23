# noinspection PyPep8
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.request
import discord
import lxml.html
import wget
import requests
from PIL import Image

print('Starting up...')
start_time = time.time()
time = time.time()
current_time = datetime.datetime.now().time()
current_time.isoformat()

if not os.path.isfile('config.json'):
    sys.exit('Fatal Error: config.json is not present.\nIf you didn\'t already, rename config.example.json to config.json and try again.')
else:
    print('config.json present, continuing...')
if not os.path.isfile('commands.json'):
    sys.exit('Fatal Error: commands.json is not present.\nIf you didn\'t already, rename config.example.json to config.json and try again.')
else:
    print('commands.json present, continuing...')

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = config_file.read()
    config = json.loads(config)
    print('Loaded configuration.')
with open('commands.json', 'r', encoding='utf-8') as commands_file:
    commands = commands_file.read()
    commands = json.loads(commands)
    print('Loaded commands.')

token = (config['Token'])
if token == '':
    sys.exit('Token not provided, please open config.json and place your token.')
pfx = (config['Prefix'])
ownr = (config['OwnerID'])
client = discord.Client()
riot_api_key = '759fa53e-7837-4109-bf6a-05b8dc63d702'
mashape_key = 'nvLNoBix6DmshG97ORG4iB51mHa5p1UezKwjsnigQ85K5RXieT'
owm_key = 'b49efc119530833da61588e4d87668c1'

# Commands
cmd_help = (commands['cmd_help'])
cmd_overwatch = (commands['cmd_overwatch'])
cmd_league = (commands['cmd_league'])
cmd_bns = (commands['cmd_bns'])
cmd_ud = (commands['cmd_ud'])
cmd_weather = (commands['cmd_weather'])
cmd_hearthstone = (commands['cmd_hearthstone'])

# I love spaghetti!

@client.event
async def on_ready():
    GameName = '>>help'
    game = discord.Game(name=GameName)
    await client.change_status(game)
    print('\nLogin Details:')
    print('---------------------')
    print('Logged in as:')
    print(client.user.name)
    print('Bot User ID:')
    print(client.user.id)
    print('---------------------\n')
    print('---------------------------------------')
    print('Running discord.py version ' + discord.__version__)
    print('---------------------------------------\n')
    print('STATUS: Finished Loading!')
    print('-------------------------\n')
    print('-----------------------------------------')
    print('Authors: AXAz0r, Awakening')
    print('Bot Version: Beta 0.1')
    print('Build Date: 20. August 2016.')
    print('-----------------------------------------\n')

@client.event
async def on_message(message):
    # Static Strings
    initiator_data = ('by: ' + str(message.author) + '\nUserID: ' + str(message.author.id) + '\nServer: ' + str(message.server.name) + '\nServerID: ' + str(message.server.id) + '\n-----------------------------------------')
    client.change_status(game=None)
    if message.content.startswith(pfx + cmd_help):
        cmd_name = 'Help'
        await client.send_typing(message.channel)
        await client.send_message(message.channel, '\nHelp: `' + pfx + cmd_help + '`' +
                                  '\nOverwatch: `' + pfx + cmd_overwatch + '`' +
                                  '\nLeague of Legends: `' + pfx + cmd_league + '`' +
                                  '\nBlade and Soul: `' + pfx + cmd_bns + '`'
                                  '\nUrban Dictionary: `' + pfx + cmd_ud + '`' +
                                  '\nWeather: `' + pfx + cmd_weather + '`' +
                                  '\nHearthstone: `' + pfx + cmd_hearthstone + '`')
        print('CMD [' + cmd_name + '] > ' + initiator_data)
# Overwatch API
    elif message.content.startswith(pfx + cmd_overwatch + ' '):
        cmd_name = 'Overwatch'
        await client.send_typing(message.channel)
        ow_input = (str(message.content[len(cmd_overwatch) + 1 + len(pfx):])).replace('#', '-')
        ow_region_x, ignore, ow_name = ow_input.partition(' ')
        ow_region = ow_region_x.replace('NA', 'US')
        try:
            profile = ('http://127.0.0.1:9000/pc/' + ow_region.lower() + '/' + ow_name + '/profile').replace(' ', '')
            profile_json_source = urllib.request.urlopen(profile).read().decode('utf-8')
            profile_json = json.loads(profile_json_source)
            good = True
        except:
            await client.send_message(message.channel, 'Error 503: Service ubnavailable.')
            good = False
        if good == True:
            try:
                avatar_link = profile_json['data']['avatar']
                border_link = profile_json['data']['levelFrame']
                if os.path.isfile('avatar.png'):
                    os.remove('avatar.png')
                if os.path.isfile('border.png'):
                    os.remove('border.png')
                if os.path.isfile('profile.png'):
                    os.remove('profile.png')
                wget.download(avatar_link)
                avatar_link_base = 'https://blzgdapipro-a.akamaihd.net/game/unlocks/'
                avatar_name = str(profile_json['data']['avatar'])
                os.rename(avatar_name[len(avatar_link_base):], 'avatar.png')
                wget.download(border_link)
                border_link_base = 'https://blzgdapipro-a.akamaihd.net/game/playerlevelrewards/'
                border_name = str(profile_json['data']['levelFrame'])
                os.rename(border_name[len(border_link_base):], 'border.png')
                base = Image.open('base.png')
                overlay = Image.open('overlay.png')
                foreground = Image.open('border.png')
                foreground_res = foreground.resize((128, 128), Image.ANTIALIAS)
                background = Image.open('avatar.png')
                background_res = background.resize((72, 72), Image.ANTIALIAS)
                base.paste(background_res, (28, 28))
                base.paste(overlay, (0, 0), overlay)
                base.paste(foreground_res, (0, 0), foreground_res)
                base.save('profile.png')
                if message.author.id == '152239976338161664':
                    rank_error = 'Goddamn it Bubu!'
                else:
                    rank_error = 'Season not active.'
                overwatch_profile = ('**Name:** ' + profile_json['data']['username'] +
                                    '\n**Level:** ' + str(profile_json['data']['level']) +
                                    '\n**Quick Games:**' +
                                    '\n    **- Played:** ' + str(profile_json['data']['games']['quick']['played']) +
                                    '\n    **- Won:** ' + str(profile_json['data']['games']['quick']['wins']) +
                                    '\n    **- Lost:** ' + str(profile_json['data']['games']['quick']['lost']) +
                                    '\n**Competitive Games:**' +
                                    '\n    **- Played:** ' + str(profile_json['data']['games']['competitive']['played']) +
                                    '\n    **- Won:** ' + str(profile_json['data']['games']['competitive']['wins']) +
                                    '\n    **- Lost:** ' + str(profile_json['data']['games']['competitive']['lost']) +
                                    '\n    **- Rank:** ' + rank_error +
                                    '\n**Playtime:**' +
                                    '\n    **- Quick:** ' +str(profile_json['data']['playtime']['quick']) +
                                    '\n    **- Competitive:** ' + str(profile_json['data']['playtime']['competitive'])
                                     )
                print('CMD [' + cmd_name + '] > ' + initiator_data)
                await client.send_file(message.channel, 'profile.png')
                await client.send_message(message.channel, overwatch_profile)
                if os.path.isfile('avatar.png'):
                    os.remove('avatar.png')
                if os.path.isfile('border.png'):
                    os.remove('border.png')
                if os.path.isfile('profile.png'):
                    os.remove('profile.png')
            except KeyError:
                try:
                    print('CMD [' + cmd_name + '] > ' + initiator_data)
                    print(profile_json['error'])
                    await client.send_message(message.channel, profile_json['error'])
                except:
                    print('CMD [' + cmd_name + '] > ' + initiator_data)
                    await client.send_message(message.channel, 'Something went wrong.\nThe servers are most likely overloaded, please try again.')
        else:
            print('CMD [' + cmd_name + '] > ' + initiator_data)
    # League of Legends API
    elif message.content.startswith(pfx + cmd_league + ' '):
        await client.send_typing(message.channel)
        cmd_name = 'League of Legends'
        if os.path.isfile('lolsig.png'):
            os.remove('lolsig.png')
        lol_input = (str(message.content[len(cmd_league) + 1 + len(pfx):]))
        region_x, ignore, summoner_name_x = lol_input.partition(' ')
        summoner_name = summoner_name_x.lower()
        region = region_x.lower()
        lol_sig_url = ('http://lolsigs.com/' + summoner_name + '_' + region + '_266_0.png')
        wget.download(lol_sig_url)
        os.rename(summoner_name + '_' + region + '_266_0.png', 'lolsig.png')
        try:
            await client.send_file(message.channel, 'lolsig.png')
            if os.path.isfile('lolsig.png'):
                os.remove('lolsig.png')
            print('CMD [' + cmd_name + '] > ' + initiator_data)
        except KeyError:
            print('CMD [' + cmd_name + '] > ' + initiator_data)
            await client.send_message(message.channel, 'Something went wrong.\nThe servers are most likely overloaded, please try again.')
    elif message.content.startswith('-read<@92747043885314048>'):
        if message.author.id == ownr:
            await client.send_message(message.channel, 'Alex stop wasting time and get back to working on my APIs...')
        elif message.author.id == '92747043885314048':
            await client.send_message(message.channel, 'Ace, I heard Alex bought this giant black dildo, wanna go test it out?')
        else:
            await client.send_message(message.channel, 'No! ಠ_ಠ')
# Blade and Soul API
    elif message.content.startswith(pfx + cmd_bns + ' '):
        cmd_name = 'Blade and Soul'
        bns_input = (str(message.content[len(cmd_bns) + 1 + len(pfx):]))
        region_x, ignore, char_name_x = bns_input.partition(' ')
        char_name = char_name_x.lower()
        region = region_x.lower()
        profile_url = ('http://' + region + '-bns.ncsoft.com/ingame/bs/character/profile?c=' + char_name)
        try:
            message_text = ('Character Name: `' + character_name + '` | Class: `' + character_class + '` | `' + character_clan + '`\n\n' +
                            'Offensive Stats:\n```\n' +
                            'Attack Power: `' + attack_power + '`' +
                            'Evolved Attck Rate: `' + evolved_attack_rate + '`' +
                            'Piercing: `' + piercing + '`' +
                            'Accuracy: `' + accuracy + '`' +
                            'Concentration: `' + concentration + '`' +
                            'Critical Hit: `' + critical_hit + '`' +
                            'Critical Damage: `' + critical_damage + '`' +
                            'Mastery: `' + mastery + '`' +
                            'Additional Damage: `' + additional_damage + '`' +
                            'Threat: `' + threat + '`' +
                            'Flame Damage: `' + flame_damage + '`' +
                            'Frost Damage: `' + frost_damage + '`\n```\n' +
                            'Defensive Stats:\n```\n' +
                            'HP: `' + hp + '`' +
                            'Defense: `' + defense + '`' +
                            'Evolved Defense: `' + evolved_defense + '`' +
                            'Evasion: `' + evasion + '`' +
                            'Block: `' + block + '`' +
                            'Critical Defense: `' + critical_hit + '`' +
                            'Willpower: `' + willpower + '`' +
                            'Damage Reduction: `' + damage_reduction + '`' +
                            'Health Regen: `' + health_regen + '`' +
                            'Recovery: `' + recovery + '`' +
                            'Debuff Defemse: `' + debuff_defense + '`\n```')
            await client.send_message(message.channel, message_text)
        except:
            client.send_message(message.channel, 'Something went wrong...')
            print('CMD [' + cmd_name + '] > ' + initiator_data)
#Urban Dictionary API
    elif message.content.startswith(pfx + cmd_ud + ' '):
        await client.send_typing(message.channel)
        cmd_name = 'Urban Dictionary'
        ud_input = (str(message.content[len(cmd_ud) + 1 + len(pfx):]))
        url = "https://mashape-community-urban-dictionary.p.mashape.com/define?term=" + ud_input
        headers = {'X-Mashape-Key': mashape_key, 'Accept': 'text/plain'}
        #r = requests.get(url, headers=headers)
        #r_dec = r.read.decode('utf-8')
        response = requests.get(url, headers=headers).json()
        result_type = str((response['result_type']))
        if result_type == 'exact':
            try:
                definition = str((response['list'][0]['definition']))
                permalink = str((response['list'][0]['permalink']))
                #thumbs_up = str((response['list'][0]['thumbs_up']))
                #thumbs_down = str((response['list'][0]['thumbs_down']))
                example = str((response['list'][0]['example']))
                await client.send_message(message.channel, 'Word: `' + ud_input + '`\n'
                                          'Definition:\n```' + definition + '```\n' +
                                          'Example:\n```' + example + '```\n' +
                                          'Source: ```' + permalink + '```')
                print('CMD [' + cmd_name + '] > ' + initiator_data)
            except IndexError:
                await client.send_message(message.channel, 'Something went wrong... The API dun goofed...')
                print('CMD [' + cmd_name + '] > ' + initiator_data)
        elif result_type == 'no_results':
            try:
                await client.send_message(message.channel, 'No results :cry:')
                print('CMD [' + cmd_name + '] > ' + initiator_data)
            except:
                await client.send_message(message.channel, 'Something went wrong, and we don\'t know what!')
                print('CMD [' + cmd_name + '] > ' + initiator_data)
    elif message.content.startswith(pfx + cmd_weather + ' '):
        await client.send_typing(message.channel)
        cmd_name = 'Weather'
        owm_input = (str(message.content[len(cmd_weather) + 1 + len(pfx):]))
        city, ignore, country = owm_input.partition(' ')
        owm_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country + '&appid=' + owm_key
        owm_data = urllib.request.urlopen(owm_url).read().decode('utf-8')
        owm_json = json.loads(owm_data)
        kelvin = 273.16
        try:
            coord_lon = str(owm_json['coord']['lon'])
            coord_lat = str(owm_json['coord']['lat'])
            sys_country = str(owm_json['sys']['country'])
            sys_city = str(owm_json['name'])
            weather = str(owm_json['weather'][0]['main'])
            temp = (str(round(owm_json['main']['temp'] - kelvin)) + '°C')
            temp_f = (str(round((((owm_json['main']['temp'] - kelvin) * 9) / 5) + 32)) + '°F')
            humidity = (str(owm_json['main']['humidity']) + '%')
            pressure = (str(owm_json['main']['pressure']) + ' mb')
            temp_min_c = (str(round(owm_json['main']['temp_min'] - kelvin)) + '°C')
            temp_max_c = (str(round(owm_json['main']['temp_max'] - kelvin)) + '°C')
            temp_min_f = (str(round((((owm_json['main']['temp_min'] - kelvin) * 9) / 5) + 32)) + '°F')
            temp_max_f = (str(round((((owm_json['main']['temp_max'] - kelvin) * 9) / 5) + 32)) + '°F')
            if weather == 'Thunderstorm':
                icon = ':thunder_cloud_rain:'
            elif weather == 'Drizzle':
                icon = ':cloud:'
            elif weather == 'Rain':
                icon = ':cloud_rain:'
            elif weather == 'Snow':
                icon = ':cloud_snow:'
            elif weather == 'Clear':
                icon = ':sunny:'
            elif weather == 'Clouds':
                icon = ':white_sun_cloud:'
            elif weather == 'Extreme':
                icon = ':cloud_tornado:'
            else:
                icon = ':earth_americas:'
            weather_message = ('Weather in `' + sys_city + ', ' + sys_country + '` ' +
                               'Lat: `' + coord_lat + '` | Lon: `' + coord_lon + '`\n\n' +
                               'Current State: `' + weather + '` ' + icon + '\n\n' +
                               'Details:\n```Current: ' + temp + ' (' + temp_f + ')\n' +
                               'High: ' + temp_max_c + ' (' + temp_max_f + ')\n' +
                               'Low: ' + temp_min_c + ' (' + temp_min_f + ')\n' +
                               'Humidity: ' + humidity + '\nPressure: ' + pressure + '\n```')
            await client.send_message(message.channel, weather_message)
            print('CMD [' + cmd_name + '] > ' + initiator_data)
        except AttributeError:
            await client.send_message(message.channel, 'Something went wrong, and we don\'t know what!')
            print('CMD [' + cmd_name + '] > ' + initiator_data)
        try:
            owm_error_code = str(owm_json['cod'])
            if owm_error_code == '404':
                await client.send_message(message.channel, 'Error: Requested location not found!')
                print('CMD [' + cmd_name + '] > ' + initiator_data)
        except AttributeError:
            await client.send_message(message.channel, 'Something went wrong, and we don\'t know what!')
            print('CMD [' + cmd_name + '] > ' + initiator_data)
    elif message.content.startswith(pfx + cmd_hearthstone + ' '):
        await client.send_typing(message.channel)
        cmd_name = 'Hearthstone'
        hs_input = (str(message.content[len(cmd_hearthstone) + 1 + len(pfx):]))
        url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/" + hs_input
        headers = {'X-Mashape-Key': mashape_key, 'Accept': 'text/plain'}
        response = requests.get(url, headers=headers).json()
        try:
            name = str(response[0]['name'])
            cardset = str(response[0]['cardSet'])
            rarity = str(response[0]['rarity'])
            type = str(response[0]['type'])
            try:
                cost = str(response[0]['cost'])
            except:
                cost = '0'
            try:
                faction = str(response[0]['faction'])
            except:
                faction = 'None'
            try:
                description = str(response[0]['flavor'])
            except:
                description = 'None'
            if type == 'Minion':
                attack = str(response[0]['attack'])
                health = str(response[0]['health'])
                message_text = ('Name: `' + name + '`\n' +
                                '\nType: `' + type + '`' +
                                '\nFaction: `' + faction + '`' +
                                '\nRarity: `' + rarity + '`' +
                                '\nCard Set: `' + cardset + '`' +
                                '\nCost: `' + cost + '`' +
                                '\nAttack: `' + attack + '`' +
                                '\nHealth: `' + health + '`\n' +
                                '\nDescription:```\n' + description + '```')
            elif type == 'Spell':
                try:
                    text = str(response[0]['text'])
                except:
                    text = 'None'
                message_text = ('Name: `' + name + '`\n' +
                                '\nType: `' + type + '`' +
                                '\nFaction: `' + faction + '`' +
                                '\nRarity: `' + rarity + '`' +
                                '\nCard Set: `' + cardset + '`' +
                                '\nCost: `' + cost + '`' +
                                '\nText: \n```' + text + '\n```' +
                                '\nDescription:```\n' + description + '```')
            elif type == 'Weapon':
                attack = str(response[0]['attack'])
                durability = str(response[0]['durability'])
                try:
                    text = str(response[0]['text'])
                except:
                    text = 'None'
                message_text = ('Name: `' + name + '`\n' +
                                '\nType: `' + type + '`' +
                                '\nFaction: `' + faction + '`' +
                                '\nRarity: `' + rarity + '`' +
                                '\nCard Set: `' + cardset + '`' +
                                '\nCost: `' + cost + '`' +
                                '\nAttack: `' + attack + '`' +
                                '\nDurability: `' + durability + '`' +
                                '\nText: `' + text + '`' +
                                '\nDescription:```\n' + description + '```')
            else:
                message_text = 'Data incomplete or special, uncollectable card...'
            await client.send_message(message.channel, message_text)
            print('CMD [' + cmd_name + '] > ' + initiator_data)
        except TypeError:
            try:
                error = str(response['error'])
                err_message = str(response['message'])
                await client.send_message(message.channel, 'Error: ' + error + '. ' + err_message)
            except:
                await client.send_message(message.channel, 'Something went wrong...')
            print('CMD [' + cmd_name + '] > ' + initiator_data)
    elif message.content.startswith('(╯°□°）╯︵ ┻━┻'):
        await client.send_message(message.channel, '┬─┬﻿ ノ( ゜-゜ノ)')
client.run(token)