import json
from src.vacancy import Vacancy
from src.api_classes import HHApi, SJApi
from src.json_classes import JSONSaver

FILENAME = 'vacancies.json'


def show_vacancy():
    """Возвращает список для показа в консоль"""
    with open(FILENAME, 'r', encoding='utf-8') as file:
        data = json.load(file)

    vacancies = [Vacancy(line["name"], line["firm"], line["salary from"],
                         line["salary to"], line["url"], line["area"]) for line in data]

    for x in vacancies:
        print(x)


def show_top_vacancy():
    """Возвращает список top-5 вакансий"""
    with open(FILENAME, 'r', encoding='utf-8') as file:
        data = json.load(file)
    vacancies = [Vacancy(line["name"], line["firm"], line["salary from"],
                         line["salary to"], line["url"], line["area"]) for line in data]
    top_vacancies = sorted(vacancies, key=lambda x: x.salary_from, reverse=True)[:5]

    if len(top_vacancies) >= 5:
        print('Топ-5 вакансий:\n')
        for x in top_vacancies[:5]:
            print(x)
    else:
        print('Недостаточно вакансий для отображения топ-5\n')


def user_interactions(class_object, salary):
    """Общая для всех платформ часть взаимодействия с пользователем"""
    js = JSONSaver()
    js.save_json(class_object)
    try:
        sorted_vacancies = js.get_vacancy_by_salary(int(salary))
    except ValueError:
        print('Неверный ввод данных о зарплате')
        return
    js.delete_vacancy(sorted_vacancies)
    show_vacancy()
    user_choice = input('\nХотите посмотреть топ-5 вакансий по зарплате?\n'
                        'Введите нужную цифру\n'
                        '1-Да; 2-Нет\n')
    if user_choice == '1':
        show_top_vacancy()


def user_interaction_hh():
    """Часть взаимодействия с пользователем при выборе платформы Head Hunter"""

    search_word = input('Введите ключевое слово для поиска вакансий: ')
    salary = input('Введите минимальную зарплату: ')
    hh = HHApi(search_word)
    user_interactions(hh, salary)


def user_interaction_sj():
    """Часть взаимодействия с пользователем при выборе платформы SuperJob"""

    search_word = input('Введите ключевое слово для поиска вакансий: ')
    salary = input('Введите минимальную зарплату: ')
    sj = SJApi(search_word)
    user_interactions(sj, salary)
