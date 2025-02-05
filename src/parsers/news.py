import requests
from bs4 import BeautifulSoup

url = 'https://hoopshype.com/rumors/'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    global_divs = soup.find_all('div', class_="flip-card-wrap")

    for div in global_divs:

        target_divs = div.find('div', attrs={'data-gkey': True, 'data-rkey': True})
        if target_divs:
            content = target_divs.get_text(strip='')

        links = div.find_all('a', rel='tag')
        if links:
            mentioned = [(link.get_text(strip=True)) for link in links]

        print(content)
        print(mentioned)
        print("_" * 50)