import requests
import json
import psycopg2
from Employer import Employers

count = 0

class Vacancies:

    def __init__(self):
        pass

    def get_data_vacancies(self):
        """ Создаем метод для получения страницы со списком вакансий."""
        employer_id = []
        company = Employers
        for item in company.load_employer_data(self, 'employers.json'):
            employer_id.append(item[0])

        params = {'employer_id': employer_id}

        req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
        data = req.json()

        vacancies_file = 'vacancies.json'
        with open(vacancies_file, 'w') as f:
              json.dump(data, f, ensure_ascii=False)
        return data


    def create_vacancies_table(self) -> None :
        """Создаем таблицу vacancies"""
        conn = psycopg2.connect(
            host="localhost",
            dbname="hh_db",
            user="postgres",
            password="12345")
        cur = conn.cursor()
        cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INT,
                    vacancy_name VARCHAR NOT NULL,
                    salary INT,
                    url_vacancy TEXT,

                    CONSTRAINT fk_vacancies_employers FOREIGN KEY(employer_id) REFERENCES employers(employer_id) ON DELETE CASCADE
                )
            """)
        conn.commit()
        cur.close()
        conn.close()

    def load_vacancy_data(self, json_file: str) -> list[dict]:
        """Извлекает данные о вакансиях из JSON-файла и возвращает список словарей с соответствующей информацией."""
        all_data = []
        with open (json_file, 'r', encoding='windows-1251') as f:
            data_json = json.load(f)['items']
            for row in data_json:
                row_list_data = list(row.values( ))
                list_dict = row_list_data[7]
                if type(list_dict) != dict:
                    continue
                else:
                    salary = str(list_dict['from']).split(" ")


                final_list_data = row_list_data[0:1] + row_list_data[20]['id'].split(" ") + row_list_data[2:3] + salary + row_list_data[17:18]

                all_data.append(final_list_data)

            return all_data

    def insert_vacancies_data(self) -> None :
        """Добавляет данные 'vacancies.json' в таблицу vacancies."""
        conn = psycopg2.connect (
            host="localhost",
            dbname="hh_db",
            user="postgres",
            password="12345")
        cur = conn.cursor()
        cur.executemany(
            "INSERT INTO vacancies(vacancy_id, employer_id, vacancy_name, salary, url_vacancy) VALUES(%s,%s,%s,%s,%s)",
            self.load_vacancy_data('vacancies.json'))
        conn.commit()
        cur.close()
        conn.close()



vacancy = Vacancies()