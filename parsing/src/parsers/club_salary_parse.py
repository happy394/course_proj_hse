import requests
import json
import os
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # where the SCRIPT is located
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
OUTPUT_FILE = os.path.join(PARENT_DIR, 'parsed', 'club_salary_parsed.json')

MAIN_URL = 'https://www.basketball-reference.com'
YEARS = ['2024-25', '2025-26', '2026-27', '2027-28', '2028-29', '2029-30']

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
    table = soup.find('table', class_='suppress_glossary sortable stats_table')
    soup = table.find('tbody')
    rows = soup.find_all('tr', attrs={})    # finds all tr without attributes
    for row in rows:
        team = row.find('td', class_='left').find('a')
        team_name = team.text
        team_url = MAIN_URL+team['href']
        data.update({team_name: {'url_payroll': team_url}})
        data[team_name].update({i: None for i in YEARS})

        salary_yes = row.find_all('td', class_='right')
        salary_no = row.find_all('td', class_='right iz')
        salaries = salary_yes + salary_no
        for i in range(len(YEARS)):
            try:
                amount = salaries[i]['csk']
                data[team_name][YEARS[i]] = amount
            except KeyError as e:
                pass

    return data

def club_salary_parse():
    url: str = 'https://www.basketball-reference.com/contracts/'
    soup: BeautifulSoup = request(url)

    if soup:
        result = parser(soup)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    club_salary_parse()
