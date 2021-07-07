import numpy as np
import discord
import time
import requests
import json

difficulty = ['PST', 'PRS', 'FTR', 'BYD']
clear_type = ['Failed', 'Normal Clear', 'Full Recall', 'Pure Memory', 'Easy Clear', 'Hard Clear']
cover = 'http://119.23.30.103:8080/ArcAssets/cover/'
ava = 'http://119.23.30.103:8080/ArcAssets/icon/'


def query_songname(songid):
    with open("ArcSongList.json", 'r', encoding='utf-8') as load_f:
        dict = json.load(load_f)
    for i in dict['songs']:
        if i['id'] == songid:
            return i['title_localized']['en']


def checktime(timestamp):
    sec = int(time.time() - timestamp / 1000)
    if (sec < 60):
        return str(sec) + 's'
    if (sec < 3600):
        return str(int(sec / 60)) + 'm'
    if (sec < 86400):
        return str(int(sec / 3600)) + 'h'
    return str(int(sec / 86400)) + 'd'


def recent(usercode):
    # contact botarcapi for address and UA
    headers = {"User-Agent": "InsertYourAgentHere"}
    response_userinfo_json = requests.post("see BotArcApi wiki" + usercode + "&recent=1",
                                           headers=headers)

    response_userinfo = response_userinfo_json.json()
    if response_userinfo['status'] != 0:
        return response_userinfo['status'], response_userinfo['message']

    recent_data = response_userinfo['content']['recent_score'][0]

    song_name = query_songname(recent_data['song_id'])

    if response_userinfo['content']['is_char_uncapped']:
        ava_url = ava + str(response_userinfo['content']['character']) + 'u_icon.png'
    else:
        ava_url = ava + str(response_userinfo['content']['character']) + '_icon.png'

    rating = list(str(response_userinfo['content']['rating']))
    rating.insert(np.size(rating) - 2, '.')
    rating_str = "".join(rating)

    response_embed = discord.Embed(title=song_name + '[' + str(difficulty[recent_data['difficulty']]) + ']',
                                   type='rich',
                                   description='**' + str(recent_data['score']) + '**(' + clear_type[
                                       recent_data['clear_type']] + ')\n**▸Pure: **' + \
                                               str(recent_data['perfect_count']) + '(+' + str(
                                       recent_data['shiny_perfect_count']) + ') **▸Far: **' + \
                                               str(recent_data['near_count']) + ' **▸Lost: **' + str(
                                       recent_data['miss_count']) + '\n**▸Potential: **' + \
                                               str(recent_data['rating'])[0:6],
                                   color=discord.Color.magenta())

    response_embed.set_thumbnail(url=cover + recent_data['song_id'] + '.jpg')
    response_embed.set_author(name=response_userinfo['content']['name'] + ' [' + rating_str + ']', icon_url=ava_url)
    response_embed.set_footer(text='Played ' + checktime(recent_data['time_played']) + ' ago')

    return 0, response_embed
