import requests
import json
from bs4 import BeautifulSoup

MAIN_URL = 'https://www.basketball-reference.com'
YEARS = ['2024-25', '2025-26', '2026-27', '2027-28', '2028-29', '2029-30']
OUTPUT_FILE = 'parsed/'+'player_salary_parsed.json'

def request(url: str):
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content.decode('utf-8'), "html.parser")
    except requests.RequestException as e:
        print(f"Error while requesting {url}: {e}")
        return None

    return soup

def convert_to_int(value):
    """
    Attempt to convert a value to an integer.
    Return 0 if conversion fails.
    """
    try:
        return int(value.replace(',', ''))  # Remove commas for integer conversion
    except (ValueError, AttributeError):
        return 0

def parser(soup: BeautifulSoup):
    data = dict()
    table = soup.find('table', class_='sortable stats_table')
    soup = table.find('tbody')
    rows = soup.find_all('tr')
    for row in rows:
        if (row.attrs): continue
        player = row.find('td', class_='left').find('a')
        player_name = player.text
        player_url = MAIN_URL + player['href']
        data.update({player_name: {'url_payroll': player_url}})
        data[player_name].update({i: 0 for i in YEARS})
        data[player_name].update({'guaranteed': 0})

        salary_yes = row.find_all('td', class_='right')
        salary_no = row.find_all('td', class_='right iz')
        salaries = salary_yes + salary_no
        for i in range(len(YEARS)):
            try:
                amount = salaries[i]['csk']
                data[player_name][YEARS[i]] = convert_to_int(amount)
            except KeyError as e:
                pass

        try:
            amount = salaries[len(YEARS)]['csk']
            data[player_name]['guaranteed'] = convert_to_int(amount)
        except (KeyError, IndexError):
            pass

    return data

def player_salary_parse():
    url: str = 'https://www.basketball-reference.com/contracts/players.html'
    soup: BeautifulSoup = request(url)

    if soup:
        result = parser(soup)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    player_salary_parse()
