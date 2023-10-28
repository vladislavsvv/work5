from Employer import Employers
from Vacancies import Vacancies
from dbmanager import DBManager
from config import config

params = config()
db_name = 'HH_db'


if __name__ == '__main__':
    company = Employers()

    company.create_database(db_name, params)
    company.create_employer_table()
    company.insert_employers_data()

    vacancy = Vacancies()
    vacancy.create_vacancies_table()
    vacancy.insert_vacancies_data()

    dbmanager = DBManager()
    dbmanager.get_companies_and_vacancies_count()
    dbmanager.get_all_vacancies()
    dbmanager.get_avg_salary()
    dbmanager.get_vacancies_with_higher_salary()
    dbmanager.get_vacancies_with_keyword()