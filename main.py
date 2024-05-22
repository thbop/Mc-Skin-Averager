import requests as req
from PIL import Image
from os import listdir
from mojang import API
from time import sleep


def download_skin(username):
    if username+'.png' in listdir('skins'):
        return 0
    api = API()
    
    uuid = api.get_uuid(username)
    if not uuid:
        print(f"{username} is not a taken username.")
    else:
        print(f'Found {username}\'s UUID and SKIN!')
        profile = api.get_profile(uuid)
    
        res = req.get(profile.skin_url)
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
    while True:
        print(f'Fetching {u}\'s skin.')
        try:
            download_skin(u)
            im = Image.open(f'skins/{u}.png')
            if im.size == (64, 64):
                imgs.append(Image.open(f'skins/{u}.png'))
            print('Success!')
            break
        except:
            sleep(.5)
    
    
im = average_img(imgs)
im.save('average.png')
