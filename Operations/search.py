from Arcapi import SyncApi
import numpy as np
import random
import discord
import time

difficulty = ['PST', 'PRS', 'FTR', 'BYD']
clear_type = ['Failed', 'Normal Clear', 'Full Recall', 'Pure Memory', 'Easy Clear', 'Hard Clear']
cover = 'http://119.23.30.103:8080/ArcAssets/cover/'
ava = 'http://119.23.30.103:8080/ArcAssets/icon/'

def checktime(timestamp):
    sec = int(time.time() - timestamp/1000)
    if(sec < 60):
        return str(sec) + 's'
    if(sec < 3600):
        return str(int(sec/60)) + 'm'
    if(sec < 86400):
        return str(int(sec/3600)) + 'h'
    return str(int(sec/86400)) + 'd'

def search(usercode, song_name, song_difficulty='FTR'):
    api_ = SyncApi(user_code=usercode)
    arraybuffer = api_.scores(start=8, end=12)
    personal_info = arraybuffer[1]
    song_info = arraybuffer[0]
    best_info = []
    for i in range(len(arraybuffer)):
        if i > 1:
            best_info.append(arraybuffer[i])
    best_info.sort(key=lambda info: info['rating'], reverse=True)
    
    result = []
    for i in best_info:
        if song_info[i['song_id']]['en'].lower().startswith(song_name.lower())\
                and difficulty[i['difficulty']].lower() == song_difficulty.lower():
            result.append(i)

    if len(result) == 0:
        return False

    response = random.choice(result)
    
    try:
        song_name = song_info[response['song_id']]['en']
    except KeyError:
        song_name = response['song_id']

    if personal_info['is_char_uncapped']:
        ava_url = ava + str(personal_info['character']) + 'u_icon.png'
    else:
        ava_url = ava + str(personal_info['character']) + '_icon.png'

    rating = list(str(personal_info['rating']))
    rating.insert(np.size(rating) - 2, '.')
    rating_str = "".join(rating)

    response_embed = discord.Embed(title=song_name+ '[' + str(difficulty[response['difficulty']]) + ']',
                                  type='rich' ,
                    description='**' + str(response['score']) + '**(' + clear_type[response['clear_type']] + ')\n**▸Pure: **' + \
                    str(response['perfect_count']) + '(+' + str(response['shiny_perfect_count']) + ') **▸Far: **' + \
                    str(response['near_count']) + ' **▸Lost: **' + str(response['miss_count']) + '\n**▸Potential: **' + \
                    str(response['constant']) + '->**' + str(response['rating'])[0:6] +'**',
                                  color= discord.Color.magenta())

    response_embed.set_thumbnail(url =cover + response['song_id'] + '.jpg')
    response_embed.set_author(name= personal_info['name'] + ' [' +  rating_str + ']', icon_url=ava_url)
    response_embed.set_footer(text= 'Played ' + checktime(response['time_played']) + ' ago')

    return response_embed
    