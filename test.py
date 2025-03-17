import json
import requests
from bs4 import BeautifulSoup


# Функция для парсинга страницы университета
def parse_university_page(url):
    try:
        # Загружаем страницу
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешного запроса

        # Парсим HTML с BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Ищем все таблицы с классом 'napde'
        napde_tables = soup.find_all('table', class_='napde')
        napde_data = []
        for napde_table in napde_tables:
            rows = napde_table.find_all('tr')
            for row in rows[1:]:  # Пропускаем первую строку с заголовками
                columns = row.find_all('td')
                if len(columns) >= 4:  # Убедимся, что есть как минимум 4 колонки
                    # Извлекаем данные, игнорируя первую ячейку
                    description = columns[1].text.strip()
                    unit = columns[2].text.strip()
                    value = columns[3].text.strip()

                    # Разделяем данные на описание, значение и единицу измерения
                    napde_data.append({
                        'Описание': description,
                        'Значение': value,
                        'Единица измерения': unit
                    })

        # Ищем все таблицы с id 'analis_dop'
        analis_dop_tables = soup.find_all('table', id='analis_dop')
        analis_dop_data = []
        for analis_dop_table in analis_dop_tables:
            rows = analis_dop_table.find_all('tr')
            for row in rows[1:]:  # Пропускаем первую строку с заголовками
                columns = row.find_all('td')
                if len(columns) >= 4:  # Убедимся, что есть как минимум 4 колонки
                    # Извлекаем данные, игнорируя первую ячейку
                    description = columns[1].text.strip()
                    unit = columns[2].text.strip()
                    value = columns[3].text.strip()

                    # Разделяем данные на описание, значение и единицу измерения
                    analis_dop_data.append({
                        'Описание': description,
                        'Значение': value,
                        'Единица измерения': unit
                    })

        # Собираем все данные
        return {
            'napde_data': napde_data,
            'analis_dop_data': analis_dop_data
        }

    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы {url}: {e}")
        return None


# Пример URL для одного университета (выбери из файла)
url = 'https://monitoring.miccedu.ru/iam/2023/_vpo/inst.php?id=110170'  # Заменить на нужный URL

# Парсим страницу университета
university_data = parse_university_page(url)

# Если данные были успешно получены, выводим их
if university_data:
    print(json.dumps(university_data, ensure_ascii=False, indent=4))
else:
    print("Ошибка при парсинге данных.")
