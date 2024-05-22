import requests as req
from base64 import b64decode
import json
from PIL import Image
from os import listdir


def download_skin(username):
    if username+'.png' in listdir():
        return 0
    r = req.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')

    res = r.json()
    try:
        print(res['errorMessage'])
    except:
        ID = res['id']
        r = req.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{ID}')
        
        res = r.json()
        try:
            print(res['errorMessage'])
        except:
            texdat = json.loads(b64decode(res['properties'][0]['value']).decode('utf-8'))
            skinurl = texdat['textures']['SKIN']['url']
            
            res = req.get(skinurl)
            with open(f'skins/{username}.png', 'wb') as f:
                f.write(res.content)

def average_color(colors):
    colora = [0, 0, 0, 0]
    
    for i in range(4):
        for c in colors:
            colora[i] += c[i]
        colora[i] = round(colora[i]/len(colors))
    return tuple(colora)

def colors_at(pixes, x, y):
    colors = []
    for pix in pixes:
        colors.append(pix[x, y])
    return colors

def average_img(imgs):
    pixes = []
    for i in imgs:
        pixes.append(i.load())
    
    ima = Image.new('RGBA', (64, 64))
    pixa = ima.load()
    for j in range(64):
        for i in range(64):
            pixa[i, j] = average_color(colors_at(pixes, i, j))
    return ima

with open('usernames.txt') as f:
    usernames = f.read().splitlines()

imgs = []
for u in usernames:
    download_skin(u)
    imgs.append(Image.open(f'skins/{u}.png'))
    
    
im = average_img(imgs)
im.save('average.png')