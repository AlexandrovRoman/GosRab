import requests
from vk_bot.vk_config import EMAIL, PASSWORD


class CustomError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ServerError(CustomError):
    def __init__(self):
        super().__init__('Не удалось получить ответ от сервера, повторите попытку позже.')


class AuthorizationError(CustomError):
    def __init__(self):
        super().__init__('Адрес почты или пароль введены некорректно')


class CriterionError(CustomError):
    def __init__(self):
        super().__init__('Название должности или желаемая зарплата введены некорректно')


class FormatError(CustomError):
    def __init__(self, format, filter):
        super().__init__(f'Некорректный параметр для формата или фильтрации: {format}, {filter}')


class UserApiSession:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()
        response = self.session.get(f"https://pfproject.herokuapp.com/api/login/{self.email}/{self.password}").json()
        if response.get('error', False):
            raise AuthorizationError()
        else:
            print(response)
            print('Authorization completed')

    # возможные значения параметра format - 'json', 'list'
    # возможные значения параметра filter - 'sal', 'alph'(работает только при format == 'list'
    def get_vacancies(self, name='', min_salary=0, format='json', filter='sal'):
        print(name, min_salary, format, filter)
        min_salary = int(min_salary)
        response = self.session.get('https://pfproject.herokuapp.com/api/vacancy')
        if not response:
            raise ServerError()
        else:
            json_resp = response.json()
        if json_resp.get('error', 0):
            raise AuthorizationError()

        vacancies = json_resp['vacancy']
        acceptable_vacancies = []
        for vacancy in vacancies:
            if name.lower() in vacancy['title'].lower() and vacancy['salary'] > min_salary:
                acceptable_vacancies.append(vacancy)

        if format is not None:
            if format == 'json':
                return vacancies
            elif format == 'list':
                if filter == 'sal':
                    acceptable_vacancies = sorted(acceptable_vacancies, key=lambda x: x['salary'], reverse=True)
                elif filter == 'alph':
                    acceptable_vacancies = sorted(acceptable_vacancies, key=lambda x: x['title'])
                return acceptable_vacancies
            else:
                raise FormatError(format, filter)


if __name__ == '__main__':
    api = UserApiSession(EMAIL, PASSWORD)
    print('\n'.join(api.get_vacancies(min_salary=15000, name='', format='list', filter='sal')))
