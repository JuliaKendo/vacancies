import requests
from predict_salary import get_predict_rub_salary
from predict_salary import get_predict_salary
from itertools import count
from terminaltables import AsciiTable

LANGUAGES = ("JavaScript","Java","Python","Ruby","Swift","1С")
URL_TEMPLATE = "https://api.hh.ru/vacancies"

def fetch_records(prog_language):
    pages = []
    params = {'area':'1',
              'text':'Программист AND {}'.format(prog_language)}
    for page in count():
        params['page'] = page
        responce = requests.get(URL_TEMPLATE, params=params)
        responce.raise_for_status()        
        if responce.ok:
            page_data = responce.json()
            if page >= page_data['pages']-1:
                break
            pages.append(page_data)
        else:
            break
    return pages

def fetch_hh():

    fetch_hh = []

    for prog_language in LANGUAGES:
        info_vacancies = {'vacancies_found':0,'vacancies_processed':0,'sum_salary':0}

        pages = fetch_records(prog_language)
        for page_vacancies in pages:
            info_vacancies['vacancies_found'] += page_vacancies['found']
            for vacancy in page_vacancies['items']:
                if vacancy['salary'] is None:
                    continue
                predict_rub_salary_hh = get_predict_rub_salary(vacancy['salary']['from'],
                                                                  vacancy['salary']['to'],
                                                                  vacancy['salary']['currency'])
                predict_salary = get_predict_salary(predict_rub_salary_hh)
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

        fetch_hh.append(total_by_language)

    return fetch_hh

def show_job_statistics_hh(vacancies):
    table_title = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    vacancies.insert(0, table_title)
    table_instance = AsciiTable(vacancies, 'HeadHanter Moscow')
    table_instance.justify_columns[3] = 'right'
    return table_instance.table