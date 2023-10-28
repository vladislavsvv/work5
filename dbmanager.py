import psycopg2

class DBManager:

    def __init__(self):
        pass

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect (
            host="localhost",
            dbname="hh_db",
            user="postgres",
            password="12345")
        cur = conn.cursor ( )
        cur.execute ("SELECT company_name, open_vacancies FROM employers")
        myresult = cur.fetchall ( )
        print ("Получаем список всех компаний и количество вакансий у каждой компании.")
        for row in myresult :
            print(row)
        print()
        conn.commit()
        cur.close()
        conn.close()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect (
            host="localhost",
            dbname="hh_db",
            user="postgres",
            password="12345")
        cur = conn.cursor ( )
        cur.execute ("SELECT vacancy_name, employers.company_name, salary, url_vacancy FROM vacancies INNER JOIN employers USING(employer_id)")
        myresult = cur.fetchall ( )
        print("Получаем список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.")
        for row in myresult:
            print(row)
        print()
        conn.commit()
        cur.close()
        conn.close()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(
            host="localhost",
            dbname="hh_db",
            user="postgres",
            password="12345")
        cur = conn.cursor()
        cur.execute("SELECT AVG(salary) FROM vacancies")
        myresult = cur.fetchall()
        print("Получаем среднюю зарплату по вакансиям")
        print(myresult)
        print()
        conn.commit()
        cur.close()
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(
            host="localhost",
            dbname="hh_db",
            user="postgres",
            password="12345")
        cur = conn.cursor()
        cur.execute ("SELECT vacancy_name FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)")
        myresult = cur.fetchall()
        print("Получаем список всех вакансий, у которых зарплата выше средней по всем вакансиям.")
        for row in myresult:
            print(row)
        print()
        conn.commit()
        cur.close()
        conn.close()

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых содержатся переданное слово 'газ'"""
        conn = psycopg2.connect(
            host="localhost",
            dbname="hh_db",
            user="postgres",
            password="12345")
        cur = conn.cursor()
        cur.execute ("SELECT vacancy_name FROM vacancies WHERE vacancy_name LIKE '%газ%'")
        myresult = cur.fetchall()
        print("Получаем список всех вакансий, в названии которых содержатся переданное слово 'газ'.")
        for row in myresult:
            print(row)
        print()
        conn.commit()
        cur.close()
        conn.close()