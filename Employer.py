import json
from typing import Any

import psycopg2
import requests

count = 0

class Employers:

    def __init__(self):
        pass

    def get_data_employers(self):
        """ Создаем метод для получения страницы со списком компаний."""
        params = {'text': 'газ', 'area': 1, 'only_with_vacancies': True}

        req = requests.get('https://api.hh.ru/employers', params)  # Посылаем запрос к API
        data = req.json()

        employers_file = 'employers.json'
        with open(employers_file, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
        return data


    def create_database(self, db_name, params: dict) -> None:
        """Создает новую базу данных."""

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE {db_name}')
        cur.execute(f'CREATE DATABASE {db_name}')

        cur.close()
        conn.close()

    def create_employer_table(self) -> None:
        """Создаем таблицу employers"""
        conn = psycopg2.connect(
            host="localhost",
            dbname="hh_db",
            user="postgres",
            password="12345")
        cur = conn.cursor()
        cur.execute("""
                   CREATE TABLE employers (
                       employer_id SERIAL PRIMARY KEY,
                       company_name VARCHAR NOT NULL,
                       url_vacancies TEXT,
                       open_vacancies VARCHAR
                   )
               """)
        conn.commit()
        cur.close()
        conn.close()

    def load_employer_data(self, json_file: str) -> list[dict]:
        """Извлекает данные о работодателях из JSON-файла и возвращает список словарей с соответствующей информацией."""
        all_data = []
        with open(json_file, 'r', encoding='windows-1251') as f:
            data_json = json.load(f)['items']
            for row in data_json:
                row_list_data = list(row.values())
                final_list_data = row_list_data[0:2] + row_list_data[5:]
                all_data.append(final_list_data)

        return all_data

    def insert_employers_data(self) -> None:
        """Добавляет данные 'employers.json' в таблицу employers."""
        conn = psycopg2.connect(
            host="localhost",
            dbname="hh_db",
            user="postgres",
            password="12345")
        cur = conn.cursor()
        cur.executemany(
            "INSERT INTO employers(employer_id, company_name, url_vacancies, open_vacancies) VALUES(%s,%s,%s,%s)",
            self.load_employer_data('employers.json'))
        conn.commit()
        cur.close()
        conn.close()



company = Employers()
