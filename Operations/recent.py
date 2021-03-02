from Arcapi import SyncApi
import numpy as np
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
    elif(sec < 3600):
        return str(int(sec/60)) + 'm'
    elif(sec < 86400):
        return str(int(sec/3600)) + 'h'
    else:
        return str(int(sec/86400)) + 'd'

def recent(usercode):
    api_ = SyncApi(user_code=usercode)
    arraybuffer = api_.scores(start=8, end=12)

    song_info = arraybuffer[0]
    personal_info = arraybuffer[1]
    recent_data = personal_info['recent_score'][0]
    try:
        song_name = song_info[recent_data['song_id']]['en']
    except KeyError:
        song_name = recent_data['song_id']

    if personal_info['is_char_uncapped']:
        ava_url = ava + str(personal_info['character']) + 'u_icon.png'
    else:
        ava_url = ava + str(personal_info['character']) + '_icon.png'

    rating = list(str(personal_info['rating']))
    rating.insert(np.size(rating) - 2, '.')
    rating_str = "".join(rating)

    response_embed = discord.Embed(title=song_name+ '[' + str(difficulty[recent_data['difficulty']]) + ']',
                                  type='rich' ,
                    description='**' + str(recent_data['score']) + '**(' + clear_type[recent_data['clear_type']] + ')\n**▸Pure: **' + \
                    str(recent_data['perfect_count']) + '(+' + str(recent_data['shiny_perfect_count']) + ') **▸Far: **' + \
                    str(recent_data['near_count']) + ' **▸Lost: **' + str(recent_data['miss_count']) + '\n**▸Potential: **' + \
                    str(recent_data['constant']) + '->**' + str(recent_data['rating'])[0:6] +'**',
                                  color= discord.Color.magenta())

    response_embed.set_thumbnail(url =cover + recent_data['song_id'] + '.jpg')
    response_embed.set_author(name= personal_info['name'] + ' [' +  rating_str + ']', icon_url=ava_url)
    response_embed.set_footer(text= 'Played ' + checktime(recent_data['time_played']) + ' ago')

    return response_embed