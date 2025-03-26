import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time


def load_existing_news(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data, list(data.keys())[0]
    except FileNotFoundError:
        print("Файл не найден, создается новый.")
        return {}, None
    except Exception as e:
        print(f"Ошибка при загрузке существующих новостей: {e}")
        return {}, None


def extract_news_from_html(html, latest_timestamp):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        global_divs = soup.find_all('div', class_="flip-card-wrap")
        news_list = {}

        for div in global_divs:
            article_element = div.find('article', attrs={"data-datetime": True})
            if article_element is None:
                continue

            timestamp = article_element.get("data-datetime")
            if timestamp == latest_timestamp:
                break

            target_div = div.find('div', attrs={'data-gkey': True, 'data-rkey': True})
            if target_div is None:
                continue

            content = target_div.get_text(strip=True)
            postterms = div.find('span', class_='post-terms')
            mentioned = [link.get_text(strip=True) for link in postterms.find_all('a', rel='tag')] if postterms else []

            source_element = div.find_next('a', class_='meta-source')
            source_link = source_element['href'] if source_element else None

            news_list[timestamp] = {
                'text': content,
                'mentioned': mentioned,
                'source': source_link
            }

        return news_list
    except Exception as e:
        print(f"Ошибка при извлечении информации из HTML: {e}")
        return {}


def get_page_source(url):
    try:
        options = Options()
        options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
        driver = webdriver.Firefox(service=Service('/Users/artem2284708/Downloads/geckodriver'), options=options)

        driver.get(url)
        time.sleep(3)

        for _ in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.3)

        page_source = driver.page_source
        driver.quit()
        return page_source
    except Exception as e:
        print(f"Ошибка при получении HTML-кода: {e}")
        return None


def write_to_json(news_data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(news_data, file, ensure_ascii=False, indent=4)
        print(f"Данные успешно записаны в файл {filename}")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")


def update_news_file(existing_news, new_news, filename):
    if new_news:
        updated_news = {**new_news, **existing_news}  # Merge keeping the newest at the top
        write_to_json(updated_news, filename)
    else:
        print("No new news to update.")


if __name__ == '__main__':
    url = 'https://hoopshype.com/rumors/'
    existing_news, latest_timestamp = load_existing_news(
        '/Users/artem2284708/course_proj_hse/parsing/parsed/news_data.json')

    html_content = get_page_source(url)
    if html_content:
        news_data = extract_news_from_html(html_content, latest_timestamp)
        if news_data:
            update_news_file(existing_news, news_data,
                             '/Users/artem2284708/course_proj_hse/parsing/parsed/news_data.json')
        else:
            print("Нет новых новостей для обновления.")
    else:
        print("Не удалось получить HTML-код страницы.")
