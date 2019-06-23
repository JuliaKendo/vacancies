import requests
from itertools import count
from terminaltables import AsciiTable

LIST_LANGUAGES = ("JavaScript","Java","Python","Ruby","Swift","1С")
URL_TEMPLATE = "https://api.hh.ru/vacancies"
TABLE_DATA = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]

def fetch_records(prog_language):
    pages_list = []
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
            pages_list.append(page_data)
        else:
            break
    return pages_list

def get_predict_rub_salary_hh(vacancy):

    salary_from = 0
    salary_to = 0
    if vacancy is None:
        return [0, 0]
    if vacancy['from'] is not None:
        salary_from = vacancy['from']
    if vacancy['to'] is not None:
        salary_to = vacancy['to']
    if vacancy['currency'] is None:
        return [0, 0]
    elif vacancy['currency'] != 'RUR':
        return [0, 0]
    return [salary_from, salary_to]

def get_predict_salary(predict_salary):
    result = None
    salary_from = predict_salary[0] 
    salary_to = predict_salary[1]
    if salary_from > 0 and salary_to > 0:
        result = (salary_from + salary_to) / 2
    elif salary_from > 0 and salary_to == 0:
        result = salary_from * 1.2
    elif salary_from == 0 and salary_to > 0:
        result = salary_to * 0.8
    else:
        result = 0
    return result    

def fetch_hh():

    for prog_language in LIST_LANGUAGES:
        info_vacancies = {'vacancies_found':0,'vacancies_processed':0,'sum_salary':0}

        pages_list = fetch_records(prog_language)
        for page_vacancies in pages_list:
            info_vacancies['vacancies_found'] += page_vacancies['found']
            for vacancy in page_vacancies['items']:
                predict_rub_salary_hh = get_predict_rub_salary_hh(vacancy['salary'])
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

        TABLE_DATA.append(total_by_language)  

    table_instance = AsciiTable(TABLE_DATA, 'HeadHanter Moscow')
    table_instance.justify_columns[3] = 'right'
    return table_instance.table