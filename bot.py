# bot.py
import os
from Arcapi import SyncApi
import random
import time
import discord
import numpy as np
from dotenv import load_dotenv
from PIL import Image, ImageFilter, ImageDraw, ImageFont

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

difficulty = ['PST', 'PRS', 'FTR', 'BYD']
clear_type = ['Failed', 'Normal Clear', 'Full Recall', 'Pure Memory', 'Easy Clear', 'Hard Clear']
clear_type_short = ['F', 'NC', 'FR', 'PM', 'EC', 'HC']
cover = 'http://119.23.30.103:8080/ArcAssets/cover/'
ava = 'http://119.23.30.103:8080/ArcAssets/icon/'

players = np.loadtxt('list.txt', dtype=str, comments='&')

pics = ['https://pbs.twimg.com/media/EGmTOK9UEAA9SuK?format=jpg&name=orig',
        'https://pbs.twimg.com/media/EFYsR4RUwAAWLcR?format=jpg&name=orig',
        'https://pbs.twimg.com/media/EsExsIoVkAQYd_r?format=jpg&name=orig',
        'https://pbs.twimg.com/media/EcyhiPuU4AAbBC4?format=jpg&name=orig',
        'https://pbs.twimg.com/media/EICUBAEU8AEnHCd?format=jpg&name=orig',
        'https://pbs.twimg.com/media/Ec8O8iKUEAAXbgi?format=jpg&name=orig',
        'https://pbs.twimg.com/media/ElrJbQNVcAUD4kZ?format=jpg&name=orig',
        'https://pbs.twimg.com/media/EmiKEdgUYAINRuL?format=jpg&name=orig',
        'https://pbs.twimg.com/media/EGrE1fJUEAYHIcO?format=jpg&name=orig',
        'https://pbs.twimg.com/media/Ed_a7wTU0AEc7Cv?format=jpg&name=orig',
        'https://pbs.twimg.com/media/EKEBCGKUcAAF4iR?format=jpg&name=orig',
        'https://pbs.twimg.com/media/EI1CKGmUYAAVUCV?format=jpg&name=orig',]

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


def margin_text(draw, x, y, text, font, shadowcolor):
    # thin border
    draw.text((x - 1, y), text, font=font, fill=shadowcolor)
    draw.text((x + 1, y), text, font=font, fill=shadowcolor)
    draw.text((x, y - 1), text, font=font, fill=shadowcolor)
    draw.text((x, y + 1), text, font=font, fill=shadowcolor)

    # thicker border
    draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
    draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
    draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)
    draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)

    draw.text((x, y), text, fill='#FFFFFF', font=font)


def add_stat(im, x, y, i, song_info, best_30):
    song_name_cut = song_info[best_30[i]['song_id']]['en']
    if len(song_name_cut) > 10:
        song_name_cut = song_name_cut[0:11] + '..'
    text = '#' + str(i + 1) + ' ' + song_name_cut + '[' + str(
        difficulty[best_30[i]['difficulty']]) + \
           ']\n\n\n PTT:' + str(best_30[i]['rating'])[0:5] + '    F:' + str(
        best_30[i]['near_count']) + ' L:' + str(best_30[i]['miss_count'])
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("Exo-Medium.ttf", 24)
    shadowcolor = 'black'
    margin_text(draw, x, y, text, font, shadowcolor)

    temp_image = Image.open('ArcAssets/cover/' + best_30[i]['song_id'] + '.jpg')
    temp_image = temp_image.resize((120, 120))
    im.paste(temp_image, (x - 128, y))

    text = str(best_30[i]['score']) + ' (' + clear_type_short[best_30[i]['clear_type']] + ')'
    font = ImageFont.truetype("Exo-Medium.ttf", 32)
    x += 15
    y += 37
    margin_text(draw, x, y, text, font, shadowcolor)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    global players

    if message.author.id == client.user.id:
        return

    if len(message.content) > 0:
        contentdata = message.content.split()
        if contentdata[0] == '!help':
            response = '**!bind <UID>** --- Binding discord ID with your Arcaea UID\n' \
                       '**!recent** -- Show your recent play\n' \
                       '**!b30** -- Show your best 30 plays in a picture\n' \
                       '**!b30e** -- Show your best 30 plays in discord embed\n' \
                       '**!target** -- Randomly select a target chart which might improve your potential\n' \
                       '**!kou** -- Kou!'
            await message.channel.send(content=message.author.mention + '\n' + response)

        elif contentdata[0] == '!kou':
            response = random.choice(pics)
            await message.channel.send(content=response)

        elif contentdata[0] == '!bind' and len(contentdata) >= 2:
            if(len(contentdata[1]) != 9) or (contentdata[1].isdigit() == False):
                response = 'Wrong format'
                await message.channel.send(content=message.author.mention + '\n' + response)
                return
            else:
                for i in players:
                    if(i[1] == contentdata[1] or i[0] == str(message.author.id)):
                        response = 'This ID is already linked to an account'
                        await message.channel.send(content=message.author.mention + '\n' + response)
                        return
                players = np.append(players, [[message.author.id, contentdata[1]]], axis=0)
                print([message.author.id, contentdata[1]])
                np.savetxt('list.txt', players, fmt='%s %s', newline='\n')
                response = 'Binding Complete!'
                await message.channel.send(content=message.author.mention + '\n' + response)

        elif contentdata[0] == '!target':
            for i in players:
                if i[0] == str(message.author.id):
                    api_ = SyncApi(user_code=i[1])
                    arraybuffer = api_.scores(start=8, end=12)

                    song_info = arraybuffer[0]
                    personal_info = arraybuffer[1]
                    best_info = []
                    for i in range(len(arraybuffer)):
                        if (i > 1):
                            best_info.append(arraybuffer[i])
                    best_info.sort(key=lambda info: info['rating'], reverse=True)
                    target = []
                    for i in range(len(best_info)):
                        if i >= 30 and best_info[i]['constant']> personal_info['rating']/100 - 2:
                            target.append(best_info[i])
                    if len(target) > 5:
                        choice = random.choice(target)
                        response = song_info[choice['song_id']]['en']
                    else:
                        best_info.sort(key=lambda info: info['score'])
                        choice = random.choice(best_info[0:5] + target)
                        response = song_info[choice['song_id']]['en']
                    await message.channel.send(content=message.author.mention + '\n' + response)
                    return
            response = 'Please bind your ID first, use !bind <UID>'
            await message.channel.send(content=message.author.mention + '\n' + response)

        elif contentdata[0] == '!recent':
            for i in players:
                if i[0] == str(message.author.id):
                    api_ = SyncApi(user_code=i[1])
                    arraybuffer = api_.scores(start=8, end=12)

                    song_info = arraybuffer[0]
                    personal_info = arraybuffer[1]
                    recent_data = personal_info['recent_score'][0]

                    if (personal_info['is_char_uncapped'] == True):
                        avaurl = ava + str(personal_info['character']) + 'u_icon.png'
                    else:
                        avaurl = ava + str(personal_info['character']) + '_icon.png'

                    rating = list(str(personal_info['rating']))
                    rating.insert(np.size(rating) - 2, '.')
                    ratingstr = "".join(rating)

                    responseembed = discord.Embed(title=song_info[recent_data['song_id']]['en']+ '[' + str(difficulty[recent_data['difficulty']]) + ']',
                                                  type='rich' ,
                                    description='**' + str(recent_data['score']) + '**(' + clear_type[recent_data['clear_type']] + ')\n**▸Pure: **' + \
                                    str(recent_data['perfect_count']) + '(+' + str(recent_data['shiny_perfect_count']) + ') **▸Far: **' + \
                                    str(recent_data['near_count']) + ' **▸Lost: **' + str(recent_data['miss_count']) + '\n**▸Potential: **' + \
                                    str(recent_data['constant']) + '->**' + str(recent_data['rating'])[0:6] +'**',
                                                  color= discord.Color.magenta())

                    responseembed.set_thumbnail(url =cover + recent_data['song_id'] + '.jpg')
                    responseembed.set_author(name= personal_info['name'] + ' [' +  ratingstr + ']', icon_url=avaurl)
                    responseembed.set_footer(text= 'Played ' + checktime(recent_data['time_played']) + ' ago')

                    await message.channel.send(content=message.author.mention ,embed= responseembed)
                    return
            response = 'Please bind your ID first, use !bind <UID>'
            await message.channel.send(response)

        elif contentdata[0] == '!b30e':
            for i in players:
                if i[0] == str(message.author.id):
                    api_ = SyncApi(user_code=i[1])
                    arraybuffer = api_.scores(start=8, end=12)

                    song_info = arraybuffer[0]
                    personal_info = arraybuffer[1]
                    best_info = []
                    for i in range(len(arraybuffer)):
                        if (i > 1):
                            best_info.append(arraybuffer[i])
                    best_info.sort(key=lambda info: info['rating'], reverse=True)
                    best_30 = best_info[0:30]
                    b30 = 0
                    for i in best_30:
                        b30 += i['rating']
                    b30 = b30 / 30
                    r10 = personal_info['rating'] * 0.01 * 4 - b30 * 3

                    if (personal_info['is_char_uncapped'] == True):
                        avaurl = ava + str(personal_info['character']) + 'u_icon.png'
                    else:
                        avaurl = ava + str(personal_info['character']) + '_icon.png'

                    rating = list(str(personal_info['rating']))
                    rating.insert(np.size(rating) - 2, '.')
                    ratingstr = "".join(rating)

                    responseembed = discord.Embed(title= 'Best 30',type='rich',color=discord.Color.magenta())
                    responseembed.set_author(name=personal_info['name'] + ' [' + ratingstr + ']', icon_url=avaurl)

                    for i in range(len(best_30)):
                        if i == 15:
                            await message.channel.send(content=message.author.mention ,embed= responseembed)
                            responseembed.clear_fields()
                            responseembed.remove_author()
                        responseembed.add_field(name='#'+ str(i+1) + ' ' + song_info[best_30[i]['song_id']]['en'] + '[' +
                                                     str(difficulty[best_30[i]['difficulty']]) + ']',
                                value='**' + str(best_30[i]['score']) + '** (' + clear_type[best_30[i]['clear_type']] + ')\n**▸Pure: **' + \
                                str(best_30[i]['perfect_count']) + '(+' + str(best_30[i]['shiny_perfect_count']) + ')\n**▸Far: **' + \
                                str(best_30[i]['near_count']) + ' **▸Lost: **' + str(best_30[i]['miss_count']) + '\n**▸Potential: **' + \
                                str(best_30[i]['constant']) + '->**' + str(best_30[i]['rating'])[0:6] + '**',
                                                inline=True)

                    responseembed.set_footer(text='Best 30:' + str(b30)[0:6] + "\nRecent 10: " + str(r10)[0:6])
                    await message.channel.send(embed= responseembed)
                    return
            response = 'Please bind your ID first, use !bind <UID>'
            await message.channel.send(response)

        elif contentdata[0] == '!b30':
            for i in players:
                if i[0] == str(message.author.id):
                    api_ = SyncApi(user_code=i[1])
                    arraybuffer = api_.scores(start=8, end=12)
                    personal_info = arraybuffer[1]
                    song_info = arraybuffer[0]
                    best_info = []
                    for i in range(len(arraybuffer)):
                        if i > 1:
                            best_info.append(arraybuffer[i])
                    best_info.sort(key=lambda info: info['rating'], reverse=True)
                    best_30 = best_info[0:30]
                    b30 = 0
                    for i in best_30:
                        b30 += i['rating']
                    b30 = b30 / 30
                    r10 = arraybuffer[1]['rating'] * 0.01 * 4 - b30 * 3

                    image = Image.open('background-darken.jpg')

                    for i in range(5):
                        image = image.filter(ImageFilter.GaussianBlur)
                    for n in range(10):
                        for m in range(3):
                            add_stat(image, 165 + 400 * m, 60 + 142 * n, n * 3 + m, song_info, best_30)

                    user_x = 825
                    user_y = 1500

                    temp_image = Image.open('ArcAssets/images/icon_shadow.png')
                    temp_image = temp_image.resize((100, 100))
                    image.paste(temp_image, (user_x, user_y), mask=temp_image)

                    print()

                    if personal_info['rating'] / 100 < 3.5:
                        rating_div = 0
                    elif personal_info['rating'] / 100 < 7:
                        rating_div = 1
                    elif personal_info['rating'] / 100 < 10:
                        rating_div = 2
                    elif personal_info['rating'] / 100 < 11:
                        rating_div = 3
                    elif personal_info['rating'] / 100 < 12:
                        rating_div = 4
                    elif personal_info['rating'] / 100 < 12.5:
                        rating_div = 5
                    else:
                        rating_div = 6
                    temp_image = Image.open('ArcAssets/images/rating_' + str(rating_div) + '.png')
                    temp_image = temp_image.resize((100, 100))
                    image.paste(temp_image, (user_x, user_y), mask=temp_image)

                    user_x += 14
                    user_y += 28

                    draw = ImageDraw.Draw(image)
                    text = str("%.2f" % (personal_info['rating'] / 100))
                    font = ImageFont.truetype("Exo-Medium.ttf", 33)
                    shadowcolor = 'black'
                    margin_text(draw, user_x, user_y, text, font, shadowcolor)

                    user_x += 100
                    user_y -= 13
                    text = personal_info['name']
                    font = ImageFont.truetype("Exo-Medium.ttf", 50)
                    margin_text(draw, user_x, user_y, text, font, shadowcolor)

                    user_y += 65
                    text = 'Best 30: ' + str(b30)[0:6] + '\nRecent 10: ' + str(r10)[0:6] + '\n\nGenerated by Kou Bot'
                    font = ImageFont.truetype("Exo-Medium.ttf", 25)
                    margin_text(draw, user_x, user_y, text, font, shadowcolor)

                    image.save('output.jpg', quality=95, subsampling=0)
                    await message.channel.send(content=message.author.mention, file=discord.File('output.jpg'))
                    return
            response = 'Please bind your ID first, use !bind <UID>'
            await message.channel.send(response)

client.run(TOKEN)