import requests
import json
import time
from bs4 import BeautifulSoup

def parse_image(url, name, name_short):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content.decode('utf-8'), "html.parser")
    except:
        print(f'[*] Couldn`t acces website. {name}', response)
        return

    images = soup.find_all('img')
    for image in images:
        if image['alt']:
            res = image if name_short in image['alt'] else None
            if res: break

    if not res:
        print(f'[*] Couldn`t parse image for {name}.')
        return
    
    name_ = name.lower()
    name_ = name_.replace(' ', '_')
    if "'" in name_: name_ = name_.replace("'", "`")

    try:
        image = requests.get(res['src']).content
        with open(f'parsing/parsed/images/{name_}.jpg', 'wb') as file:
            file.write(image)
        print(f'[*] Parsed for {name}')
    except:
        print(f'[*] Couldn`t fetch/save image. {name}', res)

    
if __name__ == '__main__':
    with open('parsing/parsed/player_advanced.json', 'r') as file:
        players = json.load(file)
    
    list_names = list(players)
    counter = 429
    
    for i, name in enumerate(list_names[counter:]):
        print(i, end=' ')
        url = players[name]['url']
        time.sleep(3)
        name_ = name.split("'")[0]
        parse_image(url, name, name_)
