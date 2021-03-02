from Arcapi import SyncApi
import random


def target(usercode):
    api_ = SyncApi(user_code=usercode)
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
    return response