import requests
from itertools import count
from terminaltables import AsciiTable

LIST_LANGUAGES = ("JavaScript","Java","Python","Ruby","Swift","1С")
URL_TEMPLATE = "https://api.hh.ru/vacancies"
TABLE_DATA = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]

def get_predict_salary(salary_from, salary_to):
    result = None
    if salary_from > 0 and salary_to > 0:
        result = (salary_from + salary_to) / 2
    elif salary_from > 0 and salary_to == 0:
        result = salary_from * 1.2
    elif salary_from == 0 and salary_to > 0:
        result = salary_to * 0.8
    else:
        result = 0
    return result    


def get_predict_rub_salary_hh(vacancy):

    result = 0
    if vacancy['from'] is None:
        salary_from = 0 
    else:
        salary_from = vacancy['from']
    if vacancy['to'] is None:
        salary_to = 0 
    else:
        salary_to = vacancy['to']
    if vacancy['currency'] is None:
        return result
    elif vacancy['currency'] != 'RUR':
        return result
    result = get_predict_salary(salary_from, salary_to)
    return result     
    
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

def get_vacancy_info(found_vacancies):
    vacancy_info = {}
    list_salary = []
    vacancy_info['vacancies_found'] = found_vacancies['found']
    for vacancy in found_vacancies['items']:
        if vacancy['salary']:
            salary_of_vacancy = get_predict_rub_salary_hh(vacancy['salary'])
            if salary_of_vacancy > 0:
                list_salary.append(salary_of_vacancy)

    vacancy_info['vacancies_processed'] = len(list_salary)
    vacancy_info['sum_salary'] = sum(list_salary)

    return vacancy_info

def add_vacancy_info(info_vacancies, block_vacancy_info):
    info_vacancies['vacancies_found'] += block_vacancy_info['vacancies_found']
    info_vacancies['vacancies_processed'] += block_vacancy_info['vacancies_processed']
    info_vacancies['sum_salary'] += block_vacancy_info['sum_salary']

def get_vacancies_by_lang(prog_language):
    info_vacancies_by_lang = {'vacancies_found':0,'vacancies_processed':0,'sum_salary':0}
    vacancy_records = fetch_records(prog_language)
    for vacancy_record in vacancy_records:
        block_vacancy_info = get_vacancy_info(vacancy_record)
        add_vacancy_info(info_vacancies_by_lang, block_vacancy_info)
    return info_vacancies_by_lang

def fetch_hh():
    vacancies = {}
    
    for prog_language in LIST_LANGUAGES:

        info_vacancies = {'vacancies_found':0,'vacancies_processed':0,'average_salary':0}        
        info_vacancies_by_lang = get_vacancies_by_lang(prog_language)
        info_vacancies['vacancies_found'] = "{}".format(info_vacancies_by_lang['vacancies_found'])
        info_vacancies['vacancies_processed'] = "{}".format(info_vacancies_by_lang['vacancies_processed'])
        try:
            average_salary = info_vacancies_by_lang['sum_salary'] / info_vacancies_by_lang['vacancies_processed']
        except ZeroDivisionError:
            average_salary = 0    
        info_vacancies['average_salary'] = "{}".format(int(average_salary))
        vacancies[prog_language] = info_vacancies

    return vacancies

def get_vacancies_hh():
    vacancies_hh = fetch_hh()
    for prog_language in vacancies_hh:
        vacancies_info = vacancies_hh[prog_language]
        string_of_table = [prog_language, 
                           vacancies_info['vacancies_found'], 
                           vacancies_info['vacancies_processed'], 
                           vacancies_info['average_salary']]
        TABLE_DATA.append(string_of_table)

    table_instance = AsciiTable(TABLE_DATA, 'HeadHanter Moscow')
    table_instance.justify_columns[3] = 'right'
    return table_instance.table