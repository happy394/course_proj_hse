import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # where the SCRIPT is located
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
OUTPUT_FILE = os.path.join(PARENT_DIR, 'parsed', 'news.json')
GROUPED_FILE = os.path.join(PARENT_DIR, 'parsed', 'grouped_news.json')
GECKODRIVER_PATH = os.path.join(os.path.expanduser('~'), 'Downloads', 'geckodriver')


def load_existing_news(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data, list(data.keys())[0]  # Get latest timestamp
    except FileNotFoundError:
        print("Файл не найден, создается новый.")
        return {}, None
    except Exception as e:
        print(f"Ошибка при загрузке существующих новостей: {e}")
        return {}, None


def has_reached_latest_timestamp(html, latest_timestamp):
    """Quickly checks if the latest timestamp is present in the current page."""
    soup = BeautifulSoup(html, 'html.parser')
    global_divs = soup.find_all('div', class_="flip-card-wrap")

    if global_divs:
        last_div = global_divs[-1]  # Get the last (oldest) news item
        article_element = last_div.find('article', attrs={"data-datetime": True})

        if article_element:
            last_div_timestamp = article_element.get("data-datetime")
            return last_div_timestamp <= latest_timestamp   # Stop scrolling if duplicate timestamp is found

    return False


def extract_news_from_html(html, latest_timestamp):
    """Extracts news articles from HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    global_divs = soup.find_all('div', class_="flip-card-wrap")
    news_list = {}
    news_count = 0

    for div in global_divs:
        article_element = div.find('article', attrs={"data-datetime": True})
        if article_element is None:
            continue

        timestamp = article_element.get("data-datetime")
        if timestamp == latest_timestamp:
            break  # Stop processing further if we reach the latest saved news

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
        news_count += 1
    return news_list, news_count


def get_page_source(url, latest_timestamp):
    """Scrolls the page while checking for new news. Stops early if duplicate timestamp is found."""
    try:
        options = Options()
        options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
        driver = webdriver.Firefox(service=Service(GECKODRIVER_PATH), options=options)

        driver.get(url)
        time.sleep(3)

        for i in range(1500):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.3)
            html_content = driver.page_source

            # Check if latest timestamp is found (without extracting full news)
            if has_reached_latest_timestamp(html_content, latest_timestamp):
                break
        page_source = driver.page_source
        driver.quit()
        return page_source  # Final page source after scrolling

    except Exception as e:
        print(f"Ошибка при получении HTML-кода: {e}")
        return None


def extract_mentions_with_news(data):
    """Extracts mentions from news data into a structured dictionary."""
    mentions_dict = {}

    for timestamp, news in data.items():
        for mention in news["mentioned"]:
            if mention not in mentions_dict:
                mentions_dict[mention] = []
            mentions_dict[mention].append({
                "timestamp": timestamp,
                "source": news["source"],
                "text": news["text"]
            })

    return mentions_dict


def write_to_json(news_data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(news_data, file, ensure_ascii=False, indent=4)
        print(f"Данные успешно записаны в файл {filename}")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")


def update_news_file(existing_news, new_news, news_filename, mentions_filename):
    if new_news:
        updated_news = {**new_news, **existing_news}  # Merge keeping the newest at the top
        write_to_json(updated_news, news_filename)

        # Extract mentions from the updated news and save it
        mentions_data = extract_mentions_with_news(updated_news)
        write_to_json(mentions_data, mentions_filename)


def news_parse():
    url = 'https://hoopshype.com/rumors/'
    existing_news, latest_timestamp = load_existing_news(OUTPUT_FILE)
    html_content = get_page_source(url, latest_timestamp)

    if html_content:
        news_data, news_count = extract_news_from_html(html_content, latest_timestamp)  # Unpack correctly

        if news_data:  # Ensure we have new news before updating
            update_news_file(existing_news, news_data, OUTPUT_FILE, GROUPED_FILE)
            print(f"Всего добавлено новостей: {news_count}")  # Print count of new articles
        else:
            print("Нет новых новостей для обновления.")
    else:
        print("Не удалось получить HTML-код страницы.")


if __name__ == '__main__':
    news_parse()
