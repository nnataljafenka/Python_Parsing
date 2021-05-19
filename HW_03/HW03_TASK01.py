from pymongo import MongoClient
from pprint import pprint
from HW02_TASK01 import get_vacancies

# Функция записывающая результат в бд
def insert_db(arg_db, arg_val):
   arg_db.insert_many(arg_val);

# Функция выводящая зп больше введенной суммы
def get_money():
    global db_vacancies
    value = int(input("Введите минимальную сумму:"))
    for db_vacancies in db_vacancies.find({ '$or': [{'sal_min': {'$gt': value}},{'sal_max': {'$gt': value}}]}):
        pprint(db_vacancies);

# Функция добавляющая только новые вакансии
def new_vacancies():
    new_v = get_vacancies()
    count = 0
    global db_vacancies
    for i in new_v:
        param = i['vacancy_id']
        if db_vacancies.count_documents({'vacancy_id' : param}) == 0:
            count +=1
            db_vacancies.insert_one(i)

    print(f"Вставлено {count} записей!")

##########################################################

client = MongoClient('127.0.0.1', 27017)
db = client['HH_Vacancy']
db_vacancies = db.vacancies

##########################################################

#  Для удаления db_vacancies
# db_vacancies.delete_many({})

# Вставка всех записей в db_vacancies
# insert_db(db_vacancies,get_vacancies());

# get_money();

# for db_vacancies in db_vacancies.find({}):
#     pprint(db_vacancies);

pprint(db_vacancies.count_documents({}))
new_vacancies()
pprint(db_vacancies.count_documents({}))

