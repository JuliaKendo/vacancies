import requests
import os
from predict_salary import get_predict_rub_salary
from predict_salary import get_predict_salary
from dotenv import load_dotenv
from itertools import count
from terminaltables import AsciiTable

LANGUAGES = ("JavaScript","Java","Python","Ruby","Swift","1С")
URL_TEMPLATE = "https://api.superjob.ru/2.0/vacancies"
TOWN_ID = 4
CATALOG_ID = 48

def fetch_records(prog_language):
    pages = [] 
    load_dotenv()   
    app_key = os.getenv('app_key')
    params = {'app_key':app_key,
          'town':TOWN_ID,
          'catalogues':CATALOG_ID,
          'keyword':'{}'.format(prog_language)}
    for page in count():
        params['page'] = page
        responce = requests.get(URL_TEMPLATE, params=params)
        responce.raise_for_status()
        if responce.ok:
            page_data = responce.json()
            if page_data['total'] == 0:
                break
            pages.append(page_data)
        else:
            break
    return pages

def fetch_sj():

    fetch_sj = []

    for prog_language in LANGUAGES:
        info_vacancies = {'vacancies_found':0,'vacancies_processed':0,'sum_salary':0}

        pages = fetch_records(prog_language)
        for page_vacancies in pages:
            info_vacancies['vacancies_found'] += page_vacancies['total']
            for vacancy in page_vacancies['objects']:
                if vacancy is None:
                    continue
                predict_rub_salary_sj = get_predict_rub_salary(vacancy['payment_from'],
                                                               vacancy['payment_to'],
                                                               vacancy['currency'])
                predict_salary = get_predict_salary(predict_rub_salary_sj)
                if predict_salary > 0:
                    info_vacancies['vacancies_processed'] += 1
                    info_vacancies['sum_salary'] += predict_salary

        try:
            average_salary = int(info_vacancies['sum_salary'] / info_vacancies['vacancies_processed'])
        except ZeroDivisionError:
            average_salary = 0

        total_by_language = [prog_language, 
                             info_vacancies['vacancies_found'], 
                             info_vacancies['vacancies_processed'], 
                             average_salary] 

        fetch_sj.append(total_by_language)  

    return fetch_sj
    
def show_job_statistics_sj(vacancies):
    table_title = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    vacancies.insert(0, table_title)
    table_instance = AsciiTable(vacancies, 'Superjob Moscow')
    table_instance.justify_columns[3] = 'right'
    return table_instance.table