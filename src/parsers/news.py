from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from pymongo import MongoClient
import time


def extract_news_from_html(html):
    """
    Извлекает текст новостей и ссылки на источники из HTML-кода, предоставленного Hoopshype.

    Args:
        html (str): HTML-код страницы.

    Returns:
        list: Список словарей, каждый из которых содержит текст новости и ссылку на источник.
              Возвращает пустой список в случае ошибки.
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')

        # Находим все элементы с текстом новостей (div с атрибутами data-gkey и data-rkey)
        global_divs = soup.find_all('div', class_="flip-card-wrap")

        news_list = []

        for div in global_divs:

            target_divs = div.find('div', attrs={'data-gkey': True, 'data-rkey': True})
            if target_divs:
                content = target_divs.get_text(strip='')

            links = div.find_all('a', rel='tag')
            if links:
                mentioned = [(link.get_text(strip=True)) for link in links]

            source_element = div.find_next('a', class_='meta-source')
            if source_element:
                source_link = source_element['href']
            else:
                source_link = None

            news_list.append({'text': content, 'mentioned': mentioned, 'source': source_link})

        return news_list

    except Exception as e:
        print(f"Ошибка при извлечении информации из HTML: {e}")
        return []


def get_page_source(url):
    """
    Получает HTML-код страницы, используя Selenium и Firefox.

    Args:
        url (str): URL страницы.

    Returns:
        str: HTML-код страницы или None в случае ошибки.
    """
    try:
        # Настройка Firefox Options
        firefox_options = Options()
        # firefox_options.add_argument("--headless") # Headless режим (опционально)

        # Укажите ПРАВИЛЬНЫЙ путь к Firefox (ОБЯЗАТЕЛЬНО!)
        firefox_binary_path = "/Applications/Firefox.app/Contents/MacOS/firefox"  # Пример для macOS
        firefox_options.binary_location = firefox_binary_path

        # Путь к geckodriver (замените на ваш реальный путь)
        gecko_path = '/Users/artem2284708/Downloads/geckodriver'

        # Создание сервиса для geckodriver
        service = Service(executable_path=gecko_path)

        # Инициализация драйвера Firefox
        driver = webdriver.Firefox(service=service, options=firefox_options)

        # Загрузка страницы
        driver.get(url)

        # Ожидание загрузки
        time.sleep(3)

        # Скроллим страницу вниз несколько раз
        for _ in range(10):  # 5 прокруток (можете настроить это количество)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.1)  # Ждем немного, чтобы новые элементы успели загрузиться

        # Получение HTML-кода страницы после прокрутки
        page_source = driver.page_source

        return page_source

    except Exception as e:
        print(f"Ошибка при получении HTML-кода: {e}")
        return None
    finally:
        try:
            driver.quit()
        except:
            pass


def write_to_file(news_data, filename='news_data.txt'):
    """
    Записывает данные о новостях в файл.

    Args:
        news_data (list): Список словарей с данными о новостях.
        filename (str): Имя файла для записи (по умолчанию 'news_data.txt').
    """
    try:
        client = MongoClient("mongodb://localhost:27017/")  # Change if using a remote database
        db = client["nba_scouting"]  # Database name
        collection = db["news"]  # Collection name
        collection.insert_many(news_data)  # Insert news into MongoDB collection
        for doc in collection.find():
            print(doc)  # Print news data (for demonstration purposes)
    except Exception as e:
        print(f"Ошибка при записи: {e}")


# Пример использования
if __name__ == '__main__':
    url = 'https://hoopshype.com/rumors/'
    html_content = get_page_source(url)

    if html_content:
        # Извлекаем все новости из HTML
        news_data = extract_news_from_html(html_content)

        if news_data:
            # Записываем новости в файл
            write_to_file(news_data)
        else:
            print("Не удалось извлечь новости.")
    else:
        print("Не удалось получить HTML-код страницы.")
