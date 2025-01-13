import requests
import json
from bs4 import BeautifulSoup


MAIN_URL = 'https://www.basketball-reference.com'
OUTPUT_FILE = 'course_proj_hse/parsed/'+'season_summary_parsed.json'
HEADS_PER_GAME = [None, None, 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
HEADS_ADVANCED_OVER = ['Offense Four Factors', 'Defense Four Factors']
HEADS_ADVANCED = ['rank', None, 'Age', 'W', 'L', 'PW', 'PL', 'MOV', 'SOS', 'SRS', 'ORtg', 'DRtg', 'NRtg', 'Pace', 'FTr', '3PAr', 'TS%', '\xa0', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', '\xa0', 'eFG%', 'TOV%', 'DRB%', 'FT/FGA', '\xa0', 'Arena', 'Attend.', 'Attend./G']

def request(url: str):
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error while requesting {url}: {e}")
        return None

    return soup


def conference_table_parse(rows: list, direction: str):
    for row in rows:
        if 'thead' in row['class']:
            division: str = row.text
        else:
            header = row.find('th').find('a')
            name = header.text
            url = MAIN_URL+header['href']
            
            columns = row.find_all('td')
            buff = list()
            for column in columns:
                buff.append(column.text)

            data['all_standings'][direction].update({name: {'url': url, 'wins': buff[0], 'losses': buff[1], 
                                                        'win/loss': buff[2], 'gb': buff[3], 'ps/g': buff[4], 
                                                        'pa/g': buff[5], 'srs': buff[6], 'division': division}})


def per_game_table_parse(rows: list):
    for row in rows:
        for i, column in enumerate(row):
            if i < 2:
                if i == 0:
                    buff_rank = column.text
                elif i == 1:
                    team_name = column.text
                    buff = {team_name: {'url': None, 'rank': buff_rank, 'stats': {i: None for i in HEADS_PER_GAME[2:]}}}
                    buff[team_name]['url'] = MAIN_URL+column.find('a')['href'] if column.find('a') else None
            else:
                buff[team_name]['stats'][HEADS_PER_GAME[i]] = column.text

        data['per_game'].update(buff)


def advanced_table_parse(rows: list):
    for row in rows:
        for i, column in enumerate(row):
            if i < 2:
                if i == 0:
                    rank = column.text
                elif i == 1:
                    team_name = column.text
                    url = MAIN_URL+column.find('a')['href'] if column.find('a')['href'] else None
                    buff = {team_name: {'url': url, 'rank': rank, 'stats': {'Age': None, 'W': None, 'L': None, 'PW': None, 'PL': None, 'MOV': None, 'SOS': None, 'SRS': None, 'ORtg': None, 'DRtg': None, 'NRtg': None, 'Pace': None, 'FTr': None, '3PAr': None, 'TS%': None, 'eFG%': None, 'TOV%': None, 'ORB%': None, 'FT/FGA': None, 'eFG%': None, 'TOV%': None, 'DRB%': None, 'FT/FGA': None, 'Arena': None, 'Attend.': None, 'Attend./G': None}}}
            else:
                if column.attrs['data-stat'] == 'DUMMY':
                    continue
                else:
                    buff[team_name]['stats'][HEADS_ADVANCED[i]] = column.text

        data['advansed'].update(buff)


def parser(soup: BeautifulSoup):
    global data
    data = dict()
    data.update({
                'all_standings': {'eastern_standings': dict(), 'western_standings': dict()},
                'per_game': dict(),
                'advansed': dict(),
                })

    # all_standings
    conference_standings = soup.find_all('div', class_='section_wrapper')[2] # division standings
    conference_east, conference_west = conference_standings.find_all('tbody')
    rows = conference_east.find_all('tr')
    conference_table_parse(rows, 'eastern_standings')
    rows = conference_west.find_all('tr')
    conference_table_parse(rows, 'western_standings')

    # per_game
    per_game = soup.find('div', attrs={'id': 'all_per_game_team-opponent'})
    per_game_table = per_game.find('tbody')
    rows = per_game_table.find_all('tr')
    per_game_table_parse(rows)

    # advanced
    advanced = soup.find('div', attrs={'id': 'all_advanced_team'})
    advanced_table = advanced.find('tbody')
    rows = advanced_table.find_all('tr')
    advanced_table_parse(rows)

    return data


def season_summary():
    year: str = '2025' # ability to change seasons by only changing this variable
    url: str = f'https://www.basketball-reference.com/leagues/NBA_{year}.html'
    soup: BeautifulSoup = request(url)

    if soup:
        result = parser(soup)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)



if __name__ == '__main__':
    season_summary()
