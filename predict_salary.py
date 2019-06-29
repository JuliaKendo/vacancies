def get_predict_rub_salary(vacancy_from, vacancy_to, vacancy_currency):

    salary_from = 0
    salary_to = 0

    if vacancy_from is not None:
        salary_from = vacancy_from

    if vacancy_to is not None:
        salary_to = vacancy_to

    if vacancy_currency is None:
        return [0, 0]
    elif vacancy_currency == 'RUR':
        return [salary_from, salary_to]
    elif vacancy_currency == 'rub':
        return [salary_from, salary_to]   
    
    return [0, 0]

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
