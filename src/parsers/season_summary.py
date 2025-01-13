import requests
import json
from bs4 import BeautifulSoup


MAIN_URL = 'https://www.basketball-reference.com'
YEARS = ['2024-25', '2025-26', '2026-27', '2027-28', '2028-29', '2029-30']
OUTPUT_FILE = 'course_proj_hse/parsed/'+'season_summary_parsed.json'

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

        if row['class'] == 'thead':
            print('here')
            division: str = row['class']
        else:
            header = row.find('th').find('a')
            name = header.text
            url = MAIN_URL+header['href']
            
            columns = row.find_all('td')
            buff = list()
            for column in columns:
                buff.append(column.text)

            data['all_standings'][direction].append({'name': name, 'url': url, 'wins': buff[0], 'losses': buff[1], 
                                                        'win/loss': buff[2], 'gb': buff[3], 'ps/g': buff[4], 
                                                        'pa/g': buff[5], 'srs': buff[6], 'division': division})

def parser(soup: BeautifulSoup):
    global data
    data = dict()
    conference_standings = soup.find('div', attrs={'id': 'all_standings'}).find_all('div', class_='section_wrapper')

    conference1, conference2 = conference_standings.find_all('tbody')
    data.update({
                'all_standings': {'eastern_standings': list(), 'western_standings': list()},
                'per_game': {list},
                })

    # all_standings
    rows = conference1.find_all('tr')
    conference_table_parse(rows, 'eastern_standings')
    rows = conference2.find_all('tr')
    conference_table_parse(rows, 'western_standings')

    # per_game


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
