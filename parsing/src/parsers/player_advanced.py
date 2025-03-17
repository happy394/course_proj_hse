import requests
import json
from bs4 import BeautifulSoup


MAIN_URL = 'https://www.basketball-reference.com'
OUTPUT_FILE = 'parsing/parsed/'+'player_advanced.json'
HEADS = ['rank', '', 'Age', 'Team', 'Pos', 'G', 'GS', 'MP', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP', 'Awards']

def request(url: str):
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content.decode('utf-8'), "html.parser")
    except requests.RequestException as e:
        print(f"Error while requesting {url}: {e}")
        return None

    return soup


def parser(soup: BeautifulSoup):
    data = dict()
    table = soup.find('table', class_=['stats_table', 'sortable', 'soc'])
    soup = table.find('tbody')
    rows = soup.find_all('tr')
    for row in rows:
        row.find_all('td')
        for i, column in enumerate(row):
            if i % 2 == 0:
                continue
            else:
                if i > 3:
                    buff[player_name][HEADS[i//2]] = column.text
                elif i == 1:
                    rank = column.text
                elif i == 3:
                    player_name = column.text
                    player_name_lower = player_name.lower()
                    player_name_lower = player_name_lower.replace(' ', '_')
                    player_name_lower = player_name_lower.replace("'", '`')
                    buff = {player_name: {'url': None, 'rank': rank, 'name_lower': player_name_lower, }}
                    buff[player_name].update({i: None for i in HEADS[2:]})
                    buff[player_name]['url'] = MAIN_URL+column.find('a')['href'] if column.find('a') else None

        data.update(buff)

    return data


def player_advanced():
    url: str = 'https://www.basketball-reference.com/leagues/NBA_2025_advanced.html'
    soup: BeautifulSoup = request(url)

    if soup:
        result = parser(soup)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    player_advanced()
