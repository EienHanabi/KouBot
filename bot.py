# bot.py
import os
import discord
import numpy as np
from dotenv import load_dotenv

from Operations.b30 import b30
from Operations.kou import kou
from Operations.recent import recent
from Operations.target import target

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

players = np.loadtxt('list.txt', dtype=str, comments='&')

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
                       '**!target** -- Randomly select a target chart which might improve your potential\n' \
                       '**!kou** -- Kou!'
            await message.channel.send(content=message.author.mention + '\n' + response)

        elif contentdata[0] == '!kou':
            response = kou()
            await message.channel.send(content=response)

        elif contentdata[0] == '!bind' and len(contentdata) >= 2:
            if(len(contentdata[1]) != 9) or (contentdata[1].isdigit() == False):
                response = 'Wrong format'
                await message.channel.send(content=message.author.mention + '\n' + response)
                return
            else:
                for i in players:
                    if i[1] == contentdata[1] or i[0] == str(message.author.id):
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
                    response = target(i[1])
                    await message.channel.send(content=message.author.mention + '\n' + response)
                    return
            response = 'Please bind your ID first, use !bind <UID>'
            await message.channel.send(content=message.author.mention + '\n' + response)

        elif contentdata[0] == '!recent':
            for i in players:
                if i[0] == str(message.author.id):
                    response_embed = recent(i[1])
                    await message.channel.send(content=message.author.mention, embed=response_embed)
                    return
            response = 'Please bind your ID first, use !bind <UID>'
            await message.channel.send(response)

        elif contentdata[0] == '!b30':
            for i in players:
                if i[0] == str(message.author.id):
                    image = b30(i[1])
                    image.save('output.jpg', quality=95, subsampling=0)
                    await message.channel.send(content=message.author.mention, file=discord.File('output.jpg'))
                    return
            response = 'Please bind your ID first, use !bind <UID>'
            await message.channel.send(response)

client.run(TOKEN)