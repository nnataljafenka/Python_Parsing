from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time
from pprint import pprint

# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)

# Функция для записи в бд
def new_item(list_item, db, param):
    count = 0
    for i in list_item:
        p_value = i[param]
        if db.count_documents({param : p_value}) == 0:
            count +=1
            db.insert_one(i)
    print(f"Вставлено {count} записей!")

def find_mail():
    driver = webdriver.Chrome()
    driver.get('https://mail.ru/')

    elem = driver.find_element_by_name('login')
    elem.send_keys('study.ai_172@mail.ru')
    elem.send_keys(Keys.ENTER)

    #почему-то через раз работает WebDriverWait
    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))

    elem.send_keys('NextPassword172')
    time.sleep(3)
    elem.send_keys(Keys.ENTER)

    mail_list = []
    while True:
        # mail = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, ".//a[contains(@class,'js-letter-list-item')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'llc')))
        actions = ActionChains(driver)

        try:
            # mails = driver.find_elements_by_xpath(".//a[contains(@class,'js-letter-list-item')]")
            mails = driver.find_elements_by_class_name("llc")

            for mail in mails:
                mail_item = {}
                mail_item['link'] = mail.get_attribute('href')
                mail_item['id'] = mail.get_attribute('data-uidl-id')
                mail_item['email_send'] = mail.find_element_by_class_name('ll-crpt').get_attribute('title')
                mail_item['theme'] = mail.find_element_by_class_name('ll-sj__normal').text
                mail_item['datetime'] = mail.find_element_by_class_name('llc__item_date').get_attribute('title')
                mail_list.append(mail_item)
        except Exception as e:
            print('Что-то пошло не так!', e)
            break;

        if driver.find_elements_by_class_name("list-letter-spinner"):
            break
        else:
            actions.move_to_element(mails[-1])
            actions.perform()
    driver.close()
    return mail_list

mails = find_mail()
# pprint(mail_list)
pprint(f' Собрано {len(mails)} писем, включая дубликаты')

client = MongoClient('127.0.0.1', 27017)
db = client['Mails']
db_Mails = db.Mails

new_item(mails,db_Mails,'link')

pprint(f'В бд {db_Mails.count_documents({})} записей!')

# for mail in db_Mails.find({}):
#      pprint(mail);

