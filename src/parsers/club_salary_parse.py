import requests
import json
from bs4 import BeautifulSoup

MAIN_URL = 'https://www.basketball-reference.com'
YEARS = ['2024-25', '2025-26', '2026-27', '2027-28', '2028-29', '2029-30']
OUTPUT_FILE = 'parsed/'+'club_salary_parsed.json'

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
    Attempt to convert a string value to an integer.
    Return 0 if the value is None or conversion fails.
    """
    try:
        return int(value.replace(',', '')) if value else 0  # Remove commas and convert to int
    except (ValueError, AttributeError):
        return 0

def parser(soup: BeautifulSoup):
    data = dict()
    table = soup.find('table', class_='suppress_glossary sortable stats_table')
    soup = table.find('tbody')
    rows = soup.find_all('tr', attrs={})  # finds all tr without attributes
    for row in rows:
        team = row.find('td', class_='left').find('a')
        team_name = team.text
        team_url = MAIN_URL + team['href']
        data.update({team_name: {'url_payroll': team_url}})
        data[team_name].update({i: 0 for i in YEARS})  # Initialize years with 0

        salary_yes = row.find_all('td', class_='right')
        salary_no = row.find_all('td', class_='right iz')
        salaries = salary_yes + salary_no
        for i in range(len(YEARS)):
            try:
                amount = salaries[i]['csk']
                data[team_name][YEARS[i]] = convert_to_int(amount)  # Convert salary to integer
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
