import logging
import os
import requests
import fetch_hh
import fetch_sj

def main():

    current_directory = os.path.dirname(__file__)
    logfile = os.path.join(current_directory,'jobs.log')   
    logging.basicConfig(filename=logfile, filemode='w')
    logging.info("Program started")

    try:
        vacancies_hh = fetch_hh.fetch_hh()
        jobs_table_hh = fetch_hh.show_job_statistics_hh(vacancies_hh)
        print(jobs_table_hh)
    except requests.exceptions.HTTPError as error:
        logging.info("Не могу получить данные с сервера HeadHanter:\n{0}".format(error))

    try:
        vacancies_sj = fetch_sj.fetch_sj()
        jobs_table_sj = fetch_sj.show_job_statistics_sj(vacancies_sj)
        print(jobs_table_sj)

    except requests.exceptions.HTTPError as error:
        logging.info("Не могу получить данные с сервера SuperJob:\n{0}".format(error))

    logging.info("Done!")

if __name__ == "__main__":
    main()
    