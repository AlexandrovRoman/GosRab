import requests


class ServerError(Exception):
    pass


def get_vacancies(job='', min_salary=0):
    response = requests.get('https://pfproject.herokuapp.com/api/vacancy/')
    if not response:
        raise ServerError()

    vacancies = response.json()['vacancy']
    acceptable_vacancies = []
    for vacancy in vacancies:
        if job.lower() in vacancy['title'] and vacancy['salary'] > min_salary:
            acceptable_vacancies.append(vacancy)
    return acceptable_vacancies
