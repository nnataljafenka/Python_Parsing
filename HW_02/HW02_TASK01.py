from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
from pprint import pprint

# Функция для преобразования зп в нужный формат
def salary_format(vacancy_salary):
    salary_result = {}
    if vacancy_salary is not None:
        salary_txt = vacancy_salary.replace('\xa0', '').replace('-', ' ')
        salary = salary_txt.split(' ')
        if len(salary) == 3:
            if salary[0] == 'до':
                sal_min, sal_max, currency = None, salary[1], salary[-1];
            elif salary[0] == 'от':
                sal_min, sal_max, currency = salary[1], None, salary[-1];
            else:
                sal_min, sal_max, currency = salary[0], salary[1], salary[-1];
    else:
        sal_min, sal_max,  currency = None, None, None;
    salary_result['sal_min'] = sal_min;
    salary_result['sal_max'] = sal_max;
    salary_result['currency'] =  currency;

    return salary_result;

# Функция вывода текста из узла
def node_text(node):
    try:
        n_text = node.text;
    except AttributeError:
        n_text = None;
    return n_text;

# https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=Sap
main_link = 'https://hh.ru/'
search = input('Введите запрос: ')

params = {'clusters': 'true',
          'area': '1',
          'enable_snippets': 'true',
          'st': 'searchVacancy',
          'text': search,
          # 'page':'33'
          }
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0'}

response = requests.get(main_link + 'search/vacancy', params=params, headers=headers)
soup = bs(response.text, 'html.parser')
vacancies = []

while True:
    if response.ok:
        vacancy_block = soup.findAll('div', {'data-qa': 'vacancy-serp__vacancy'})
        for vacancy in vacancy_block:
            vacancy_data = {}
            vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
            vacancy_company = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
            vacancy_salary_el = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

            vacancy_data['link'] = vacancy_name['href']
            vacancy_data['original link'] = response.url
            vacancy_data['name'] = node_text(vacancy_name);
            vacancy_data['company'] = node_text(vacancy_company);

            salary = salary_format(node_text(vacancy_salary_el));

            vacancy_data['sal_min'] = salary['sal_min'];
            vacancy_data['sal_max'] = salary['sal_max'];
            vacancy_data['currency'] = salary['currency'];

            vacancies.append(vacancy_data)
    else:
        break;

    # pprint(len(vacancies))
    # pprint(vacancies)
    print(pd.DataFrame.from_dict(vacancies))

    next_page = soup.find('a', {'class': 'HH-Pager-Controls-Next'})
    if next_page is None:
        break;
    next_page_link = next_page['href']
    response = requests.get(main_link + next_page_link, headers=headers)
    soup = bs(response.text, 'html.parser')



