import requests
import json
from bs4 import BeautifulSoup


MAIN_URL = 'https://www.basketball-reference.com'
OUTPUT_FILE = 'course_proj_hse/parsed/'+'player_advanced.json'
HEADS = ['rank', '', 'Age', 'Team', 'Pos', 'G', 'GS', 'MP', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP', 'Awards']

def request(url: str):
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error while requesting {url}: {e}")
        return None

    return soup


def parser(soup: BeautifulSoup):
    data = list()
    table = soup.find('table', class_=['stats_table', 'sortable', 'soc'])
    soup = table.find('tbody')
    rows = soup.find_all('tr')
    for row in rows:
        buff = {'player': None, 'url': None, 'rank': None, 'stats': {'Age': None, 'Team': None, 'Pos': None, 'G': None, 'GS': None, 'MP': None, 'PER': None, 'TS%': None, '3PAr': None, 'FTr': None, 'ORB%': None, 'DRB%': None, 'TRB%': None, 'AST%': None, 'STL%': None, 'BLK%': None, 'TOV%': None, 'USG%': None, 'OWS': None, 'DWS': None, 'WS': None, 'WS/48': None, 'OBPM': None, 'DBPM': None, 'BPM': None, 'VORP': None, 'Awards': None}}
        row.find_all('td')
        for i, column in enumerate(row):
            if i % 2 == 0:
                continue
            else:
                if i > 3:
                    buff['stats'][HEADS[i//2]] = column.text
                elif i == 1:
                    buff['rank'] = column.text
                elif i == 3:
                    buff['player'] = column.text
                    buff['url'] = MAIN_URL+column.find('a')['href'] if column.find('a') else None

        data.append(buff)

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
